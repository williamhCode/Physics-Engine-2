import glm
import time

t1 = time.perf_counter()
arr = glm.array.zeros(10, glm.float32)
arr[:2] = glm.array(glm.float32, 1, 2)
# arr[0] = 1
# arr[1] = 2
t2 = time.perf_counter()
print(repr(arr))
print(t2 - t1)