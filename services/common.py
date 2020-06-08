import os
import sys

from functools import wraps

from log_config import logger
from auth import jwt_decode
import json


AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_PUBLIC_KEY = os.getenv('AUTH0_CLIENT_PUBLIC_KEY')


class TokenError(Exception):
    """Raised when token is invalid, malformed or expired"""


def insert_repo(handler):
    @wraps(handler)
    def wrapper(event, context):
        sys.path.append('data_dynamodb')
        sys.path.append('data_common')
        from data_dynamodb.dynamodb_repository import DynamoRepository

        # While developing, dynamodb local is used. So if `DYANMODB_LOCAL_ENDPOINT` is present in env vars
        # dynamodb boto client is patched to use local db
        context.repo = DynamoRepository(
            region_name=os.environ['REGION'],
            table='sp-{STAGE}'.format(STAGE=os.environ['STAGE']),
            user_id=context.user_id,
            email=context.email,
            dynamodb_local_endpoint=os.environ['DYNAMO_ENDPOINT'] if 'DYNAMO_ENDPOINT' in os.environ else None
        )

        return handler(event, context)

    return wrapper


def get_repo(record):
    """This is not a decorator"""
    sys.path.append('data_dynamodb')
    sys.path.append('data_common')
    from data_common.exceptions import UserIdNotInObject
    from data_dynamodb.dynamodb_repository import DynamoRepository
    import json

    try:
        body = record['body']
        user_id = json.loads(body)['user_id']
    except KeyError:
        raise UserIdNotInObject

    # While developing, dynamodb local is used. So if `DYANMODB_LOCAL_ENDPOINT` is present in env vars
    # dynamodb boto client is patched to use local db
    try:
        repo = DynamoRepository(
            region_name=os.environ['REGION'],
            table='sp-{STAGE}'.format(STAGE=os.environ['STAGE']),
            user_id=user_id,
            dynamodb_local_endpoint=os.environ['DYNAMO_ENDPOINT']
        )

    except KeyError:
        repo = DynamoRepository(
            region_name=os.environ['REGION'],
            table='sp-{STAGE}'.format(STAGE=os.environ['STAGE']),
            user_id=user_id,
        )

    return repo


def check_auth(handler):
    @wraps(handler)
    def wrapper(event, context):
        logger.debug('event: {}'.format(event))

        try:
            token_parts = event['headers']['Authorization'].split(' ')
        except KeyError:
            return {
                'statusCode': 401,
                'body': 'The resource you are trying to access is private. '
                        'Please provide an Authorization token'
            }

        auth_token = token_parts[1]

        decoded = jwt_decode(auth_token, AUTH0_CLIENT_PUBLIC_KEY)

        if 'email' in decoded and 'sub' in decoded:
            context.email = decoded['email']
            context.user_id = decoded['sub'][6:]

            # App metadata is inserted into context in insert_repo()
        else:
            return {
                'statusCode': 401,
                'body': 'invalid_token. '
                        'The access token provided is expired, '
                        'revoked, malformed, '
                        'or invalid for other reasons'
            }

        return handler(event, context)

    return wrapper