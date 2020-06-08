import boto3
from boto3.dynamodb.conditions import Key, Attr
import base64
import binascii

from data_common.exceptions import BadParameters, NoSuchEntity, UnsupportedMediaType
from data_common.repository import ProfileRepository
from data_common.notifications import SnsNotifier
from data_common.utils import clean, generate_affiliate_id
import os


class DynamoProfileRepository(ProfileRepository, SnsNotifier):
    @staticmethod
    def base64_to_png(image_string):
        image_filepath = "/tmp/image.png"

        # starts with 'data:image/png;base64,'
        image_string = image_string.split("data:image/png;base64,")[-1]

        try:
            with open(image_filepath, "wb") as fp:
                image_data = image_string.encode('utf-8')

                # fix incorrect padding issue (binascii.Error: Incorrect padding)
                missing_padding = len(image_data) % 4
                if missing_padding:
                    image_data += b'=' * (4 - missing_padding)

                fp.write(base64.decodebytes(image_data))
        except binascii.Error:
            raise UnsupportedMediaType

        return image_filepath


    def get_or_create_profile(self):
        obj_type = 'user'

        user_obj = self._storage.get(self._user_id)
        if not user_obj:
            for _ in range(1000):
                affiliate_id = generate_affiliate_id()

                query = {
                    'KeyConditionExpression': Key('affiliate_id').eq(affiliate_id) & Key('obj_type').eq(obj_type),
                    'IndexName': 'by_affiliate_id_and_obj_type'
                }

                response = self._storage.get_items(query)

                if response['Count'] <= 0:
                    break

            user_obj = {
                'entity_id': self._user_id,
                'user_id': self._user_id,
                'firstname': '',
                'lastname': '',
                'email': self._email,
                'affiliate_id': affiliate_id,
            }
            user_obj = self._storage.save(obj_type, user_obj)
            self.sns_publish('sp-' + os.environ['STAGE'] + '-' + obj_type, user_obj)  # publish notification

        user_obj = clean(user_obj)

        return user_obj

    def update_profile(self, obj):
        obj_type = 'user'

        # check if the entity_id in obj exists
        try:
            entity_id = obj["entity_id"]
            profile = self._storage.get(entity_id)
            if not profile:
                raise NoSuchEntity
        except KeyError:
            raise BadParameters

        if "picture" in obj:
            picture_string = obj.pop("picture")
            image_filepath = self.base64_to_png(picture_string)

            if 'S3_ENDPOINT' in os.environ:
                s3 = boto3.client('s3', endpoint_url=os.environ['S3_ENDPOINT'])
            else:
                s3 = boto3.client('s3')

            bucket_name = os.environ['S3_UPLOADS_BUCKET_NAME']

            s3_filepath = "profile_pictures/{USER_ID}/profile_pic.png".format(USER_ID=self._user_id)
            s3.upload_file(image_filepath, bucket_name, s3_filepath)

        user_obj = self._storage.save(obj_type, obj)
        self.sns_publish('sp-' + os.environ['STAGE'] + '-' + obj_type, obj)  # publish notification

        user_obj = clean(user_obj)

        name = ""
        if "name" in user_obj:
            name = user_obj["name"]
        else:
            if user_obj.get('firstname', False):
                name += user_obj['firstname']

            if user_obj.get('lastname', False):
                name += " " + user_obj['firstname']

            name = name.lstrip()

        if name:
            # update Auth0 Profile
            auth0_profile = {"name": name}

            resp = self._auth0.update_profile(auth0_profile)
            if resp.status_code != 200:
                error = resp.json()

                msg = 'Unable to update Auth0 profile. Unknown error.'
                if 'message' in error:
                    msg = error['message']

                raise BadParameters(msg)

        # update password if existing in request
        password = ""
        if "password" in user_obj:
            password = user_obj["password"]

            # update Auth0 Profile password
            auth0_profile = {"password": password}

            resp = self._auth0.update_profile(auth0_profile)

            # adding a flag, might help in UI changes like signing out a user upon password update
            if resp.status_code != 200:
                error = resp.json()

                msg = 'Unable to update Auth0 profile. Unknown error.'
                if 'message' in error:
                    msg = error['message']

                raise BadParameters(msg)
            else:
                user_obj.pop('password')
                user_obj['password_updated'] = True

        return user_obj


    def update_user_app_metadata(self, app_metadata):
        obj_type = 'user'

        # get user profile
        user_obj = self._storage.get_by_user_id(self._user_id)

        if not user_obj:
            raise NoSuchEntity

        user_obj = clean(user_obj)

        # update app_metadata
        user_obj["app_metadata"] = app_metadata
        user_obj = self._storage.save(obj_type, user_obj)
        self.sns_publish('sp-' + os.environ['STAGE'] + '-' + obj_type, user_obj)  # publish notification

        return user_obj


    def get_user_app_metadata(self):
        obj_type = 'user'

        # get user profile
        user_obj = self._storage.get_by_user_id(self._user_id)

        if not user_obj:
            raise NoSuchEntity

        user_obj = clean(user_obj)

        app_metadata = user_obj.get("app_metadata", {})
        return app_metadata


    def delete_profile(self):
        obj_type = 'user'

        profile = self._storage.get(self._user_id)

        if profile:
            obj = clean(profile)

            obj["active"] = False
            self._storage.save(obj_type, obj)
            self.sns_publish('sp-' + os.environ['STAGE'] + '-' + obj_type, obj)  # publish notification
        else:
            raise NoSuchEntity