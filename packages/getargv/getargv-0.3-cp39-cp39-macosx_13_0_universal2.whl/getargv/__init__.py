# Python code for getargv module
import sys
from getargv.getargv import *
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata
__version__ = metadata.version('getargv')
