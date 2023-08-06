from matplotlib import pyplot
import time
import types
import collections
import copy

import ita.global_vars as ig

def argToStr(arg):
    def argToStrMain(arg):
        if isinstance(arg, collections.abc.Sequence) and len(arg) > 3:
            return ("[" + argToStrMain(arg[0]) + "," +
                    argToStrMain(arg[1]) + ", ...]")
        else:
            return str(arg)
    if isinstance(arg, tuple):
        return argToStrMain(arg)
    else:
        return "(" + argToStrMain(arg) + ")"

def default_measure(x):
    if isinstance(x, tuple):
        return sum(default_measure(y) for y in x)
    if hasattr(type(x), "__len__"):
        return len(x)
    if hasattr(type(x), "__abs__"):
        return abs(x)
    raise TypeError("bench: the size of the argument is unknown. Specify the mesure.")

def count_recursive_call(func):
   def wrapper(*args, **kwargs):
       ig._recursion_cnt += 1
       return func(*args, **kwargs)
   return wrapper

def evalWithTime(f, arg, criteria="time", measure=default_measure, count=1):
    if not hasattr(f, '__call__'):
        raise TypeError("evalWithTime: first argument must be a function")
    ig._list_access_cnt = 0
    ig._recursion_cnt = 0
    tempf = copy.deepcopy(f)
    func = count_recursive_call(tempf)
    tempf.__globals__[f.__name__] = func
    print("evaluating ", f.__name__ + argToStr(arg), "... ", end="")
    start = time.perf_counter()
    for i in range(count):
        if isinstance(arg, tuple):
            tempf(*arg)
        else:
            tempf(arg)
    et = (time.perf_counter() - start)
    tempf.__globals__[f.__name__] = f
    print("finished in ", et, " seconds.")
    r = { "time" : et,
          "access" : ig._list_access_cnt,
          "recursion" : ig._recursion_cnt }
    if criteria not in r.keys():
        raise TypeError("evalWithTime: unsupported criteria")
    return (measure(arg), r[criteria] / count)

def bench(f, args, criteria="time", measure=default_measure, count=1):
    if not hasattr(f, '__call__'):
        raise TypeError("bench: first argument must be a function")
    if not isinstance(args, collections.abc.Sequence):
        raise TypeError("bench: second argument must be a series of arguments")
    x, y = [], []
    for arg in args:
        v, w = evalWithTime(f, arg,
                            criteria=criteria, measure=measure, count=count)
        x.append(v)
        y.append(w)
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

