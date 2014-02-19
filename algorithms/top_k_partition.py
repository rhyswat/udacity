#
# Write partition to return a new array with 
# all values less then `v` to the left 
# and all values greater then `v` to the right
#

import random

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

def top_k(L, k) :
    """Returns the k smallest elements in L in an arbitrary order."""
    if len(L) == k :
        return L
    
    v = L[random.randrange(len(L))]
    (left, mid, right) = partition(L, v)
    if len(left) + 1 == k : return left + [v] # quick exit
    if len(left) > k : return top_k(left, k) # top_k is within left somewhere
    return left + [v] + top_k(right, k - len(left) - 1) # top_k is left + v + some of the rest


test = range(1,21)
random.shuffle(test)
print test
print top_k(test, 5)



