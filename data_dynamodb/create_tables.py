import importlib
import inspect
import os
import sys

import boto3
from bloop import (
    BaseModel, GlobalSecondaryIndex, Engine
)

# Import table definition classes
parent = os.path.dirname(os.path.abspath(__file__))
tables = os.path.join(parent, 'tables')
sys.path.append(tables)

for table_mod in os.listdir(tables):
    if table_mod.endswith('.py') and table_mod is not '__init__.py':
        table_mod = table_mod.split('.py')[0]
        mod = importlib.import_module(table_mod)

        # add module attrs to globals()
        if "__all__" in mod.__dict__:
            names = mod.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in mod.__dict__ if not x.startswith("_")]

        for k in names:
            globals()[k] = getattr(mod, k)

# find model classes among all imported classes
classes = [cls_tup[1] for cls_tup in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
models = []
sql_models = []
for cls in classes:
    bases = getattr(cls, '__bases__', None)

    if any(base == BaseModel for base in bases):
        models.append(cls)

if __name__ == '__main__':
    import sys
    import json
    import os

    # for development we use dynamodb-local
    sys.path.insert(0, os.path.join(os.path.abspath(os.path.curdir), 'dynamodb_local_patch.py'))
    from dynamodb_local_patch import patch_engine

    args = sys.argv
    if len(args) >= 2:
        stage = args[1]

        config_filename = 'config.' + stage + '.json'
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_filepath = os.path.join(parent_dir, config_filename)

        with open(config_filepath, 'r') as fp:
            config = json.load(fp)

        region = config['REGION']

        try:
            endpoint = args[2]
            client = boto3.client('dynamodb', region_name=region, endpoint_url=endpoint)
            engine = patch_engine(Engine(dynamodb=client))
        except IndexError:
            client = boto3.client('dynamodb', region_name=region)
            engine = Engine(dynamodb=client)

        resp = client.list_tables()
        tables = resp['TableNames']

        for model in models:
            model.Meta.table_name = model.Meta.table_name.format(STAGE=stage)

        print('Running dynamodb tables creation script '
              'in Region: {REGION}'.format(REGION=region))
        print("Dynamodb Tables: ")
        for model in models:
            if model.Meta.table_name not in tables:
                print('Creating table: ', model.Meta.table_name)
                engine.bind(model)