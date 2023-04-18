import os
import sys


def block_stdout():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enable_stdout():
    sys.stdout = sys.__stdout__
