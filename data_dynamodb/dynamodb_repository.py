from data_adapter import DynamoStorage
from auth0_adapter import Auth0
import os
import sys, inspect
import importlib

from data_common.repository import Repository

# Import dynamodb repository classes
parent = os.path.dirname(os.path.abspath(__file__))
repository = os.path.join(parent, 'repository')
sys.path.append(repository)

for repo_mod in os.listdir(repository):
    if repo_mod.endswith('.py') and repo_mod is not '__init__.py':
        repo_mod = repo_mod.split('.py')[0]
        mod = importlib.import_module('repository.' + repo_mod)

        # add module attrs to globals()
        if "__all__" in mod.__dict__:
            names = mod.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in mod.__dict__ if not x.startswith("_")]

        for k in names:
            globals()[k] = getattr(mod, k)

dynamo_classes = [cls_tup[1] for cls_tup in inspect.getmembers(sys.modules[__name__], inspect.isclass)
                if cls_tup[0].startswith('Dynamo') and cls_tup[0].endswith('Repository')]


class DynamoRepository(Repository,
                       *dynamo_classes
                       ):
    def __init__(self,
                 region_name,
                 table,
                 user_id=None,
                 email='',
                 dynamodb_local_endpoint=None):
        # dynamodb_local_endpoint if present is used to patch the dynamodb boto client to
        # use a local db instance instead of going to AWS

        Repository.__init__(self, region_name, user_id, email)

        if dynamodb_local_endpoint:
            self._storage = DynamoStorage(table=table, user_id=user_id, endpoint_url=dynamodb_local_endpoint)
        else:
            self._storage = DynamoStorage(table=table, user_id=user_id)

        self._auth0 = Auth0(user_id)