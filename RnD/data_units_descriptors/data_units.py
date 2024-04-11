class DataUnit(object):
    def __init__(self, **kwargs):
        self.data = kwargs
        self.instances = dict()

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if instance in self.instances:
            return self.instances[instance]

        param = BoundDataUnit(**self.data)
        self.instances[instance] = param
        return param


class BoundDataUnit(object):
    def __init__(self, value, default):
        self.value = value
        self.default = default

    def __str__(self):
        return str(self.value)

    def set(self, value):
        self.value = value

    def reset(self):
        self.value = self.default


# Example usage:
class Plug(object):
    value = DataUnit("int", value=0, default=0)
    min = DataUnit("int", value=0, default=None)
    max = DataUnit("int", value=1, default=None)


# Create instances
plug1 = Plug()
print("_________")
print("plug 1")
print(plug1.value)
print(plug1.min)
print(plug1.max)

plug2 = Plug()
print("_________")
print("plug 2")
print(plug2.value)
print(plug2.min)
print(plug2.max)

plug1.value.set(3)
plug1.min.set(4)
plug1.max.set(5)
plug2.min.reset()

print("_________")
print("plug 1")
print(plug1.value)
print(plug1.min)
print(plug1.max)
print("_________")
print("plug 1")
print(plug2.value)
print(plug2.min)
print(plug2.max)
