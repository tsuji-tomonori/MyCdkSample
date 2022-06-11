import numpy as np


def handler(event, context):
    print("hello")
    return np.random.rand()
