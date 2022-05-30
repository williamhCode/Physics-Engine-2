import glm
import time

position = (1, 2)
t1 = time.perf_counter()
# temp_pos = (position[0], position[1], 0.0)
temp_pos = (*position, 0.0)
t2 = time.perf_counter()
print(t2 - t1)