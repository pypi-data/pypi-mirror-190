import copy
import types
import matplotlib.pyplot as plt
import random as rnd
import collections.abc

import copy
import types
import matplotlib.pyplot as plt
import random as rnd
import collections.abc

import ita.global_vars as ig

class AccessCountingList(list):
   def __init__(self, *args):
       super().__init__(*args)
   def __getitem__(self, idx):
       ig._list_access_cnt += 1
       if isinstance(idx, slice):
         return AccessCountingList(super().__getitem__(idx))
       else:
         return super().__getitem__(idx)
   def __setitem__(self, key, value):
       global _list_access_cnt
       ig._list_access_cnt += 1
       return super().__setitem__(key, value)
   def __iter__(self):
       self.iterator = AccessCountIterator(super().__iter__())
       return self.iterator
   def __add__(self, arg):
     return AccessCountingList(super().__add__(arg))

class AccessCountIterator(collections.abc.Iterator):
   def __init__(self, it, *args):
       self._it = it
   def __iter__(self):
       return self
   def __next__(self):
       ig._list_access_cnt += 1
       return self._it.__next__()

def make1d(n, value=0, random=False):
    if not type(n) is int:
        raise TypeError("make1d: first argument should be an integer")
    if random:
        return AccessCountingList(rnd.random() for i in range(0, n))
    else:
        return AccessCountingList(copy.deepcopy(value) for i in range(0, n))

def make2d(n, m, value=0, random=False):
    if not type(n) is int:
        raise TypeError("make2d: first argument should be an integer")
    if not type(m) is int:
        raise TypeError("make2d: second argument should be an integer")
    return AccessCountingList(make1d(m, value=value, random=random)
                              for i in range(0, n))

def make3d(n, m, k, value=0, random=False):
    if not type(n) is int:
        raise TypeError("make3d: first argument should be an integer")
    if not type(m) is int:
        raise TypeError("make3d: second argument should be an integer")
    if not type(k) is int:
        raise TypeError("make3d: third argument should be an integer")
    return AccessCountingList(make2d(m, k, value=value, random=random)
                              for i in range(0, n))

def print2d(data, rowLabels=None, colLabels=None): #not used in the textbook
    if not (isinstance(data, collections.abc.Sequence) and
            isinstance(data[0], collections.abc.Sequence)):
        raise TypeError("print2d: argument should be a 2d-array")
    tbl = plt.table(cellText=[[str(j) for j in i] for i in data],
                    bbox=[0,0,1,1], cellLoc='center', loc='top',
                    rowLabels=rowLabels, colLabels=colLabels)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(16)
    plt.axis('off')
    plt.show()
