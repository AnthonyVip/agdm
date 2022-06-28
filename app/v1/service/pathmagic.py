import os
import sys


class context:
    def __enter__(self):
        bp = os.path.dirname(os.path.realpath('.')).split(os.sep)
        modpath = os.sep.join(bp)
        print(modpath)
        sys.path.insert(0, modpath)

    def __exit__(self, *args):
        pass
