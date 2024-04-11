import timeit
import uuid

count = 10**6

print("uuid1", timeit.timeit(stmt="uuid.uuid1()", number=count, globals=globals()))
print("uuid4", timeit.timeit(stmt="uuid.uuid4()", number=count, globals=globals()))

# result for count = 10**6:
# uuid1 2.4410444
# uuid4 1.1783028
