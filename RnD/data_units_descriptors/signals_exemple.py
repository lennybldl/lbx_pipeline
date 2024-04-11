class pyqtSignal:
    def __init__(self):
        self.handlers = []

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return BoundSignal(self, instance)

    def connect(self, handler):
        self.handlers.append(handler)

    def emit(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


class BoundSignal:
    def __init__(self, signal, instance):
        self.signal = signal
        self.instance = instance

    def connect(self, handler):
        self.signal.connect(handler)

    def emit(self, *args, **kwargs):
        self.signal.emit(*args, **kwargs)


# Example usage:
class MyClass:
    my_signal = pyqtSignal()


# Create instances
instance1 = MyClass()
instance2 = MyClass()

# Connect signals
instance1.my_signal.connect(lambda: print("Signal emitted from instance 1"))
instance2.my_signal.connect(lambda: print("Signal emitted from instance 2"))

# Emit signals
instance1.my_signal.emit()  # Output: Signal emitted from instance 1
instance2.my_signal.emit()  # Output: Signal emitted from instance 2
