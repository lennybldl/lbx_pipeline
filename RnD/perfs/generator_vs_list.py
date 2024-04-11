from lbx_python import context


def time_it(func):
    def wrapper(*args, **kwargs):
        with context.TimeIt(message=func.__name__):
            return func(*args, **kwargs)

    return wrapper


count = 10**6


def iterate(iterable):
    for i in iterable:
        pass


items = list(range(1000))


@time_it
def create_generator_comprehension():
    for _ in range(count):
        _generator = (i for i in items)


@time_it
def create_list_comprehension():
    for _ in range(count):
        _list = [i for i in items]


@time_it
def create_list():
    for _ in range(count):
        _list = list()
        for i in items:
            _list.append(i)


_generator = (i for i in items)


@time_it
def iterate_generator():
    for _ in _generator:
        pass


_list = (i for i in items)


@time_it
def iterate_list():
    for _ in _list:
        pass


# test
create_generator_comprehension()
create_list_comprehension()
create_list()
iterate_generator()
iterate_list()

# result for count = 10**6:
# 2024-04-21 15:43:11,829|   DEBUG| Timer | create_generator_comprehension - 0.188527 secs | context (line 83)
# 2024-04-21 15:43:25,466|   DEBUG| Timer | create_list_comprehension - 13.636865 secs | context (line 83)
# 2024-04-21 15:43:56,563|   DEBUG| Timer | create_list - 31.096216 secs | context (line 83)
# 2024-04-21 15:43:56,564|   DEBUG| Timer | iterate_generator - 3e-05 secs | context (line 83)
# 2024-04-21 15:43:56,564|   DEBUG| Timer | iterate_list - 2.9e-05 secs | context (line 83)
