#
# Write partition to return a new array with 
# all values less then `v` to the left 
# and all values greater then `v` to the right
#

import random

random.seed(12345L)

def rank(L, v):
    """
    Gets the position of v in L if L were sorted.
    Assumes the elements of L are distinct.
    """
    pos = 0
    for val in L:
        if val < v:
            pos += 1
    return pos

def partition(L, v):
    """Partitions L into (less than v, v, greater than v)."""
    r = rank(L, v)
    return ([x for x in L if x < v], [v], [x for x in L if x > v])

def min_k(L, k, first=False) :
    """Returns the k smallest elements in L in an arbitrary order, in TH(N) time."""
    if len(L) == k :
        return L
    
    v = L[random.randrange(len(L))]
    (left, mid, right) = partition(L, v)
    ix = len(left)
    if ix == k-1  : return left + [v]
    if ix > k-1   : return min_k(left, k)
    return left + [v] + min_k(right, k - ix-1)

def max_k(L, k, first=False, s=1) :
    """Returns the k largest elements in L in an arbitrary order, in TH(N) time."""
    N = len(L)
    if N == k :
        return L

    v = L[random.randrange(len(L))]
    (left, mid, right) = partition(L, v)
    ix = len(left)
    if ix == N-k : return right + [v]
    if ix < N-k  : return max_k(right, k, s=s)
    return right + [v] + max_k(left, k - (1 + len(right)), s=s)


U = 20
K = 5
test = range(1,U+1)
random.shuffle(test)

correct_max = set(xrange(U-K+1, U+1))
correct_min = set(xrange(1, K+1))
failures_max = 0
failures_min = 0
N = 1000
for i in xrange(N) :
    try :
        m = set(max_k(test, K, first=True))
        if m != correct_max :
            failures_max += 1
            print 'FAIL',m
    except ValueError :
        failures_max += 1

    try :
        m = set(min_k(test, K))
        if m != correct_min :
            failures_min += 1
            print 'FAIL',m
    except ValueError :
        failures_min += 1

print 'max-k failure rate is {:.2f}%'.format(100*float(failures_max)/N)
print 'min-k failure rate is {:.2f}%'.format(100*float(failures_min)/N)



