# check latest version on deployment table
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import json
from dynamodb_json import json_util

# Returns exit status 1 if issue_id (script_number) already exists or if table not found

if __name__ == '__main__':
    import sys

    args = sys.argv
    if len(args) >= 2:
        stage = args[1]

        os.environ['STAGE'] = stage

        config_filename = 'config.' + stage + '.json'
        parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_filepath = os.path.join(parent_dir, config_filename)

        with open(config_filepath, 'r') as fp:
            config = json.load(fp)

        region = config['REGION']

        resource = boto3.resource('dynamodb', region_name=region)
        table = resource.Table('sp-deployment')

        # check if table and item exists, if yes exit
        try:
            response = table.query(
                KeyConditionExpression=Key('stage').eq(stage),
                Limit=1,
                ScanIndexForward=False
            )
        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ResourceNotFoundException':
                print("current_version: 0")
                sys.exit(0)
            raise ex

        try:
            items = json_util.loads(response['Items'])
            if not items:
                print("current_version: 0")
            else:
                latest = items[0]
                print("current_version: {0}".format(latest['script_number']))
            sys.exit(0)
        except KeyError:
            pass