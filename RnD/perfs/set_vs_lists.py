import random

from lbx_python import context

count = 10**5

# create the items towork with
items = list(range(count))
# make sure we process the items in a random order
random.shuffle(items)
append = list(items)
random.shuffle(items)
remove = list(items)
# create a list of numbers to test if they are in the items
random_test_numbers = [random.randint(0, count) for _ in range(int(count / 2))]
random_test_numbers += [random.randint(count, 2 * count) for _ in range(int(count / 2))]


# test lists

# with context.TimeIt(message="list append"):
#     data = list()
#     for i in append:
#         data.append(i)

# with context.TimeIt(message="list remove"):
#     for i in remove:
#         data.remove(i)

# with context.TimeIt(message="list is in"):
#     for i in random_test_numbers:
#         if i in items:
#             pass

# test dicts

dico = {i: str(i) for i in items}

with context.TimeIt(message="dict is in"):
    for i in random_test_numbers:
        if i in dico:
            pass

with context.TimeIt(message="dict.keys is in"):
    keys = dico.keys()
    for i in random_test_numbers:
        if i in keys:
            pass

# test sets

with context.TimeIt(message="set add"):
    data = set()
    for i in append:
        data.add(i)

with context.TimeIt(message="set remove"):
    for i in remove:
        data.remove(i)

with context.TimeIt(message="set is in"):
    for i in random_test_numbers:
        if i in data:
            pass

with context.TimeIt(message="set is in (convert list to set)"):
    data = set(items)
    for i in random_test_numbers:
        if i in data:
            pass

with context.TimeIt(message="set(dict.keys) is in"):
    keys = set(dico.keys())
    for i in random_test_numbers:
        if i in keys:
            pass


# result for count = 10**5:
# list append - 0.008098 secs | context (line 83)
# list remove - 35.741496 secs | context (line 83)
# list is in - 86.759617 secs | context (line 83)
# dict is in - 0.00722 secs | context (line 83)
# dict.keys is in - 0.006649 secs | context (line 83)
# set add - 0.010775 secs | context (line 83)
# set remove - 0.00892 secs | context (line 83)
# set is in - 0.007277 secs | context (line 83)
# set is in (convert list to set) - 0.009957 secs | context (line 83)
# set(dict.keys) is in - 0.012565 secs | context (line 83)
