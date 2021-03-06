import pkgutil

# Needed for from data_getter.schemas import *

__path__ = pkgutil.extend_path(__path__, __name__)

for imp, module, ispackage in pkgutil.walk_packages(path=__path__, prefix=__name__ + '.'):
    __import__(module)
