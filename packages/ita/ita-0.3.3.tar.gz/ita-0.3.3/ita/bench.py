from matplotlib import pyplot
import time
import types
import collections

from matplotlib import pyplot
import time
import types
import collections

_list_access_cnt = 0
_recursion_cnt = 0

def argToStr(arg):
    def argToStrMain(arg):
        if isinstance(arg, collections.abc.Sequence) and len(arg) > 3:
            return "[" + argToStrMain(arg[0]) + "," + argToStrMain(arg[1]) + ", ...]"
        else:
            return str(arg)
    if isinstance(arg, tuple):
        return argToStrMain(arg)
    else:
        return "(" + argToStrMain(arg) + ")"

def evalWithTime(fn, f, arg, criteria, c):
    global _list_access_cnt
    global _recursion_cnt
    _list_access_cnt = 0
    _recursion_cnt = 0
    print("evaluating ", fn + argToStr(arg), "... ", end="")
    start = time.perf_counter()
    for i in range(c):
        if isinstance(arg, tuple):
            f(*arg)
        else:
            f(arg)
    et = (time.perf_counter() - start) / c
    print("finished in ", et, " seconds.")
    if criteria == "time":
        return et
    elif criteria == "access":
        return _list_access_cnt / c
    elif criteria == "recursion":
        return _recursion_cnt / c
    else:
        raise TypeError("bench: unsupported criteria")

def count_recursive_call(func):
   def wrapper(*args, **kwargs):
       global _recursion_cnt
       _recursion_cnt += 1
       return func(*args, **kwargs)
   return wrapper

def default_measure(x):
    if isinstance(x, int) or isinstance(x, float):
        return x
    if isinstance(x, tuple):
        return sum([default_measure(y) for y in x])
    if isinstance(x, collections.abc.Sized):
        return len(x)
    raise TypeError("bench: the size of the argument is unknown. Specify the mesure.")

def bench(f, args, criteria="time", measure=default_measure, count=1):
    if not hasattr(f, '__call__'):
        raise TypeError("bench: first argument should be a function")
    if not isinstance(args, collections.abc.Sequence):
        raise TypeError("bench: second argument should be a series of arguments")
    x = [measure(i) for i in args]
    func = count_recursive_call(f)
    globals()[f.__name__] = func
    y = [evalWithTime(f.__name__, f ,i, criteria, count) for i in args]
    globals()[f.__name__] = f
    return (x, y)


def plot(d, xlogscale=False, ylogscale=False):
    if xlogscale:
        pyplot.xscale("log")
    else:
        pyplot.xscale("linear")
    if ylogscale:
        pyplot.yscale("log")
    else:
        pyplot.yscale("linear")
    pyplot.plot(d[0],d[1])
    pyplot.show()

