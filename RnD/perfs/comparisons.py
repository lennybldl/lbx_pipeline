import timeit

count = 10**9

setup = "a = 'value'; b = 'test'"
print("== :", timeit.timeit(stmt="a == b", setup=setup, number=count))
print("!= :", timeit.timeit(stmt="a != b", setup=setup, number=count))


class A(object):
    pass


a = A()
print(
    ".__class__ is :",
    timeit.timeit(stmt="a.__class__ is A", number=count, globals=globals()),
)
print(
    "isinstance :",
    timeit.timeit(stmt="isinstance(a,A)", number=count, globals=globals()),
)
# result for count = 10**9
# == : 17.166535500000002
# != : 17.0043765
# .__class__ is : 30.7785335
# isinstance : 35.1233453
