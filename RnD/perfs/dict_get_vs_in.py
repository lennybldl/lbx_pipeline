import random

from lbx_python import context

count = 10**7
items = list(range(count))

# create data
data = {i: str(i) for i in items}

# create a list of numbers to test if they are in the items
random_test_numbers = [random.randint(0, count) for _ in range(int(count / 2))]
random_test_numbers += [random.randint(count, 2 * count) for _ in range(int(count / 2))]
# create random numbers all included in data
random_included_numbers = list(items)
random.shuffle(random_included_numbers)

# # test get

# with context.TimeIt(message="in __getitem__"):
#     for i in random_test_numbers:
#         if i in data:
#             a = data[i]

# with context.TimeIt(message="get"):
#     for i in random_test_numbers:
#         a = data.get(i, list())

# # test removing


# data = {i: str(i) for i in items}

# with context.TimeIt(message="del included"):
#     for i in random_included_numbers:
#         del data[i]

# data = {i: str(i) for i in items}

# with context.TimeIt(message="pop included"):
#     for i in random_included_numbers:
#         data.pop(i)

# data = {i: str(i) for i in items}

# with context.TimeIt(message="del random"):
#     for i in random_included_numbers:
#         if i in data:
#             del data[i]

# data = {i: str(i) for i in items}

# with context.TimeIt(message="pop random"):
#     for i in random_included_numbers:
#         data.pop(i)

# test adding

data = dict()
with context.TimeIt(message="__setitem__"):
    for i in items:
        data[i] = str(i)

data = dict()
with context.TimeIt(message="update"):
    for i in items:
        data.update({i: str(i)})

# result for count = 10**7:
# in __getitem__ - 3.06128 secs | context (line 83)
# get - 3.217398 secs | context (line 83)
# del included - 3.550838 secs | context (line 83)
# pop included - 3.611687 secs | context (line 83)
# del random - 3.945815 secs | context (line 83)
# pop random - 3.647245 secs | context (line 83)
# __setitem__ - 1.945777 secs | context (line 83)
# update - 2.865868 secs | context (line 83)
