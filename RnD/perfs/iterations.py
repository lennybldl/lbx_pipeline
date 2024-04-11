import timeit


count = 10**6


def iterate(iterable):
    for _ in iterable:
        pass


print(
    "list : ",
    timeit.timeit(
        stmt="iterate(items)",
        setup="items = list(range(1000))",
        number=count,
        globals=globals(),
    ),
)
print(
    "tuple : ",
    timeit.timeit(
        stmt="iterate(items)",
        setup="items = tuple(range(1000))",
        number=count,
        globals=globals(),
    ),
)
print(
    "set : ",
    timeit.timeit(
        stmt="iterate(items)",
        setup="items = set(range(1000))",
        number=count,
        globals=globals(),
    ),
)

# result for count = 10**6 :
# list :  5.212095000000001
# tuple :  5.6897369
# set :  7.0700165
