# import numpy as np
# import cv2 as cv
# import time

# img = np.zeros((1200, 700, 3), np.uint8)
# t1 = time.perf_counter()
# for _ in range(5000):
#     cv.rectangle(img, (0, 0), (100, 100), (255, 255, 255), 1)
# t2 = time.perf_counter()
# print(t2 - t1)