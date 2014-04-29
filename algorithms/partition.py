"""
--------------------------------------------------------------------------------
Project: prototyping

Description: an implementation of rapid partitioning and aggregation routines.
             Based on the Udacity Algorithms course.
--------------------------------------------------------------------------------
Copyright:

This is an unpublished work the copyright in which vests in Tekever Ltd.
All rights reserved.

The information contained herein is the property of Tekever Ltd and is supplied
without liability for errors or omissions. No part may be reproduced, disclosed
or used except as authorised by contract or other written permission.

The copyright and the foregoing restriction on reproduction, disclosure and use
extend to all media in which the information may be embodied.
--------------------------------------------------------------------------------
"""


import collections
import random

#-------------------------------------------------------
# Partitioning functions on lists of DISTINCT elements

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
    return ([x for x in L if x < v], [v], [x for x in L if x > v])

def min_k(L, k) :
    """Returns the k smallest elements in L in an arbitrary order, in TH(N) time."""
    if len(L) == k :
        return L
    
    v = L[random.randrange(len(L))]
    (left, mid, right) = partition(L, v)
    iv = len(left)
    ik = k-1
    if iv == ik  : return left + [v]
    if iv > ik  : return min_k(left, k)
    return left + [v] + min_k(right, ik - iv)

def max_k(L, k) :
    """Returns the k largest elements in L in an arbitrary order, in TH(N) time."""
    N = len(L)
    if N == k :
        return L

    v = L[random.randrange(len(L))]
    (left, mid, right) = partition(L, v)
    iv = len(left)
    ik = N - k
    if iv == ik : return right + [v]
    if iv < ik  : return max_k(right, k)
    return right + [v] + max_k(left, k - (N-iv))

#-------------------------------------------------------
# Order stats -- trying to be Theta(N)

def mean(L) :
    # the value of m minimises sum_i( (L[i] - m)^2 )
    return float(sum(L))/len(L)

def median(L) :
    # the value of m minimises sum_i( |L[i] - m| )
    n = len(L)
    upper = min_k(max_k(L, 1 + n//2), 1)
    lower = max_k(min_k(L, 1 + n//2), 1)
    return 0.5*(upper[0] + lower[0])

def mode(L) :
    d = collections.defaultdict(int)
    commonest, count = L[0], 1
    for x in L :
        d[x] += 1
        if d[x] > count :
            count = d[x]
            commonest = x
    return commonest
    

#-------------------------------------------------------
if __name__ == '__main__' :
    #random.seed(12345L)

    def test(data, K, correct_max, correct_min) :
        print ''
        print data
        failures_max = 0
        failures_min = 0
        N = 1000
        for i in xrange(N) :
            try :
                m = set(max_k(data, K))
                #print '+',max_k(data, K)
                if len(m) != K: # or m != correct_max :
                    failures_max += 1
            except ValueError, e :
                print e
                failures_max += 1

            try :
                m = set(min_k(data, K))
                #print '-',min_k(data, K)
                if len(m) != K :# or m != correct_min :
                    failures_min += 1
            except ValueError :
                failures_min += 1

        print 'max-k failure rate is {:.2f}%'.format(100*float(failures_max)/N)
        print 'min-k failure rate is {:.2f}%'.format(100*float(failures_min)/N)

    # no duplicates
    U = 20
    K = U/2
    data = range(1,U+1)
    random.shuffle(data)
    test(data, K, set(range(U-K+1, U+1)), set(range(1,K+1)))

    
