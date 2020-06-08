import os
import boto3
import time
import json
from botocore.exceptions import ClientError
from string import Template



def create_bucket_if_not_exists(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    # Please note: We are using the legacy s3 endpoint to avoid the following issue:
    # If we set default region to any other than `us-east-1` and try to create a bucket in `us-east-1`
    # irrespective of if we pass the locationconstraint or not, it leads to IllegalLocationConstraintException
    # this seems like an issue with boto3
    try:
        if region is None or region == 'us-east-1':
            s3_client = boto3.client('s3', endpoint_url='https://s3.amazonaws.com')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region, endpoint_url='https://s3.amazonaws.com')
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyExists':
            print("\n" + "*" * 50 + "\n")
            print("S3 bucket-name is not globally unique. Please change bucket-name and try again")
            print("\n" + "*" * 50 + "\n")
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            return True
        if e.response['Error']['Code'] == 'IllegalLocationConstraintException':
            print("\n" + "*" * 50 + "\n")
            print("(IllegalLocationConstraintException): "
                  "This issue could be linked to https://github.com/boto/boto3/issues/125"
                  "s3 client when created in us-east-1 doesnt accept LocationConstraint")
            print("\n" + "*" * 50 + "\n")
        else:
            print(e)
        return False
    return True


def apply_cors_policy_to_bucket(bucket_name, region=None):
    s3 = boto3.resource('s3', region_name=region)
    bucket_cors = s3.BucketCors(bucket_name)
    response = bucket_cors.put(
        CORSConfiguration={
            'CORSRules': [
                {
                    'AllowedHeaders': [
                        '*',
                    ],
                    'AllowedMethods': [
                        'GET',
                        'PUT',
                        'POST',
                        'DELETE',
                        'HEAD',
                    ],
                    'AllowedOrigins': [
                        '*',
                    ],
                    'MaxAgeSeconds': 3000
                },
            ]
        },
    )
    return response


def apply_acl_policy_to_bucket(bucket_name, policy_file='bucket_acl_policy.json', region=None):
    client = boto3.client('s3', region_name=region)
    try:
        # if the bucket is already public, this will lead to an error
        # Get and modify Block public access (bucket settings) of the bucket
        print("Trying to switch off block-all-public access")
        resp = client.get_public_access_block(Bucket=bucket_name)
        public_access_block_config = resp['PublicAccessBlockConfiguration']
        public_access_block_config['BlockPublicPolicy'] = False

        resp = client.put_public_access_block(Bucket=bucket_name,
                                              PublicAccessBlockConfiguration=public_access_block_config)
        # time needed for the permissions change to take effect
        print("Waiting for 10secs for permissions to take effect")
        time.sleep(10)
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            print("Bucket is private only. Adding public-access ACL policy")
            client.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )

    with open(policy_file, 'rt') as fp:
        policy = fp.read()
        policy = Template(policy).safe_substitute(S3_UPLOADS_BUCKET_NAME=bucket_name)

    response = client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=policy
    )

    return response



if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) >= 2:
        stage = args[1]

        os.environ['STAGE'] = stage

        config_filename = 'config.' + stage + '.json'
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_filepath = os.path.join(parent_dir, config_filename)

        with open(config_filepath, 'rt') as fp:
            config = json.load(fp)

        try:
            bucket_name = config['S3_UPLOADS_BUCKET_NAME']
        except KeyError:
            print("Missing env variable 'S3_UPLOADS_BUCKET_NAME' in config.{STAGE}.json".format(STAGE=stage))
            sys.exit(1)

        try:
            region = config['REGION']
        except KeyError:
            region = None
            print("Missing env variable 'S3_UPLOADS_BUCKET_NAME' in config.{STAGE}.json".format(STAGE=stage))

        print("Create bucket if not exists")
        success = create_bucket_if_not_exists(bucket_name, region)

        if not success:
            sys.exit(1)

        print("Waiting till bucket exists")
        client = boto3.client('s3', region_name=region)
        waiter = client.get_waiter('bucket_exists')
        waiter.wait(
            Bucket=bucket_name
        )

        print("Apply CORS policy to bucket")
        apply_cors_policy_to_bucket(bucket_name, region=region)

        
        print("Apply ACL Public access policy to folders in bucket")
        apply_acl_policy_to_bucket(bucket_name, region=region)
        