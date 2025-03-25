import os
import sys

PROJECT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        os.pardir,
        os.pardir
    )
)

sys.path.extend([ROOT_DIR])

class Interface:
    def __init__(self):
        pass

