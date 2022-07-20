
from settings import base_path
import os


def getAbsolutePath(table_name):
    return os.path.join(base_path, table_name)

