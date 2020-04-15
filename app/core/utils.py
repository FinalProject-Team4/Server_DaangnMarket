import os


def make_dir(val, num=1):
    if num == 0:
        return val
    ret = os.path.dirname(make_dir(val, num - 1))
    return ret
