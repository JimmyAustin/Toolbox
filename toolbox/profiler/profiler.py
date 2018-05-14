import flamegraph
import tempfile
from subprocess import call
from os import path


class Profiler():
    def __init__(self, output='./perf.svg'):
        self.output = output

    def start():
        self.__enter__()

    def stop():
        self.__stop__(None, None, None)

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.profile_thread = flamegraph.start_profile_thread(fd=self.temp_file)
        return self

    def __exit__(self ,type, value, traceback):
        self.profile_thread.stop()
        self.profile_thread.join()
        self.temp_file.close()

        with open(self.output, 'wb') as f:
            args = [get_flamegraph_executable_path(), self.temp_file.name]
            call(args, stdout=f)
            
def get_flamegraph_executable_path():
    return path.join(path.dirname(__file__), 'flamegraph/flamegraph.pl')

def profile_function(func):
    def func_wrapper(*args, **kwargs):
        with Profiler(output="{0}.svg".format(func.__name__)):
           return func(*args, **kwargs)
    return func_wrapper
