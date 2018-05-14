from datetime import datetime

def print_proxy(txt):
    print(txt)

class Timer():
    def __init__(self, name=None, print_func=print_proxy):
        self.name = name
        self.print_func = print_func

    def start():
        self.__enter__()

    def stop():
        self.__exit__(None, None, None)

    def __enter__(self):
        self.start_time = datetime.now()
        return self

    def __exit__(self ,type, value, traceback):
        self.length = (datetime.now() - self.start_time).total_seconds()
        self.print_func("Function ({0}) Finished: {1}s".format(self.name, self.length))

def time_function(print_func=print_proxy):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            with Timer(name=func.__name__, print_func=print_func):
               return func(*args, **kwargs)
        return func_wrapper
    return decorator
