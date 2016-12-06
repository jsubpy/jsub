def load_func(func):
    return None

class CustomFunc():
    def __init__(self, func):
        self._func = func

    def split(self):
        func = load_func(self._func)
        return func()
