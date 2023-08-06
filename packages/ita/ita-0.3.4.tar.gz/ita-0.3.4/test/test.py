# usage: pip install -e . && python test/test.py

import ita

print("version of ita:", ita.__version__)

def comb(n, m):
  if m == 0 or n == m:
    return 1
  else:
    return comb(n-1, m) + comb(n-1, m-1)

def total(x):
  c = 0
  for i in x:
    c = c + i
  return c

def sum_iter(n):
  if n == 0:
    return 0
  else: 
    return sum_iter(n-1) + n

def simple_sort(x):
  for i in range(len(x)):
    mi = i + x[i:].index(min(x[i:]))
    x[mi], x[i] = x[i], x[mi]

def mergesort(x):
    def merge(x, y):
        r = ita.array.make1d(len(x) + len(y))
        ix,iy = 0,0
        for i in range(0, len(r)):
            if iy >= len(y) or (ix < len(x) and x[ix] <= y[iy]):
                r[i] = x[ix]
                ix += 1
            else:
                r[i] = y[iy]
                iy += 1
        return r
    if len(x) <= 1:
        return x
    else:
        c = len(x) // 2
        return merge(mergesort(x[:c]), mergesort(x[c:]))

# print(ita.bench.bench(comb, [(i*2+1,i) for i in range(10)]))
# print(ita.bench.bench(sum_iter, [i for i in range(20)], criteria="recursion"))
# print(ita.bench.bench(comb, [(i*2+1,i) for i in range(10)], criteria="recursion"))
# print(ita.bench.bench(total, [ita.array.make1d(i*100, random=True) for i in range(20)], criteria="access"))
# print(ita.bench.bench(simple_sort, [ita.array.make1d(i*100, random=True) for i in range(20)], criteria="access"))
# print(ita.bench.bench(mergesort, [ita.array.make1d(i*100, random=True) for i in range(20)], criteria="access"))

import random
data = [(2 * i + random.random()*10, 3 * i + random.random()*10) for i in range(100)]
ita.plot.linear_fit(data)

