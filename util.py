import random
import cv2
import numpy as np

def get_random_hash():
    return ''.join(random.choice('0123456789ABCDEF') for i in range(16))


def write_image(path, data):
    if type(data) is str:
        data = cv2.imread(data)
    cv2.imwrite(path, np.array(data))