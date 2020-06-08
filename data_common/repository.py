import abc
import os
import sys, inspect
import importlib

# Import repository abstract classes
parent = os.path.dirname(os.path.abspath(__file__))
repositories = os.path.join(parent, 'repositories')
sys.path.append(repositories)

for repo_mod in os.listdir(repositories):
    if repo_mod.endswith('.py') and repo_mod is not '__init__.py':
        repo_mod = repo_mod.split('.py')[0]
        mod = importlib.import_module('repositories.' + repo_mod)

        # add module attrs to globals()
        if "__all__" in mod.__dict__:
            names = mod.__dict__["__all__"]
        else:
            # otherwise we import all names that don't begin with _
            names = [x for x in mod.__dict__ if not x.startswith("_")]

        for k in names:
            globals()[k] = getattr(mod, k)


abstract_classes = [cls_tup[1] for cls_tup in inspect.getmembers(sys.modules[__name__], inspect.isclass)]


class BaseRepository:
    def __init__(self, region_name, user_id=None, email=''):
        self._region_name = region_name
        self._user_id = user_id
        self._email = email
        self._stage = os.environ["STAGE"]
    # If more attributes are required, modify SQSManager, SnsNotifier class as well to match with this signature


class Repository(*abstract_classes,
                 BaseRepository,
                 metaclass=abc.ABCMeta):
    pass