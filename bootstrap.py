#!/usr/bin/env python2

import unittest
import random
import numpy as np

## Source: Johan Garcia, Message-ID: <548F05E2.6050307@kau.se>
##Funktion
#Bootstrap percentile CI from:
#http://stackoverflow.com/questions/26429322/bootstrap-on-a-groupby-object-in-pandas
# also at http://people.duke.edu/~ccc14/pcfb/analysis.html
def bootstrap(data, num_samples, statistic, alpha):
    """Returns bootstrap estimate of 100.0*(1-alpha) CI for statistic."""
    n = len(data)                                                        
    idx = np.random.randint(0, n, (num_samples, n))
    samples = data[idx]                            
    stat = np.sort(statistic(samples, 1))
    #return (stat[int((alpha/2.0)*num_samples)],
    #        stat[int((1-alpha/2.0)*num_samples)])
    #Fix to return values adapted to bar plot yerr
    return (stat.mean() - stat[int((alpha/2.0)*num_samples)] ,
            stat[int((1-alpha/2.0)*num_samples)] - stat.mean())


##Anrop
#ll = bootstrap(A3xT2[A3xT2['evenstarthour'] == wd]['TpMbps'], 100000, np.mean, 0.05)
#ax.bar(xrange(len(barvals)),barvals,yerr=np.array(ll).T,alpha=0.3)

#### UNIT TESTING


class TestAppCompletion(unittest.TestCase):

    def setUp(self):
        # init

        # Always start with same random seed when testing
        np.random.seed(seed=1)

    def test_bootstrap(self):
        
        #arr=np.array([int(random.gauss(100,10)) for x in range(10)])
        arr=np.concatenate([np.random.normal(3, 1, 10), np.random.normal(6, 2, 20)])
        ll = bootstrap(arr, 10000, np.mean, alpha=0.05)
        print ll

        self.assertTrue(ll==(0.77012024033117221, 0.7876734495953519))
        self.assertFalse(ll==(0.8, 0.7))

    def test_normaldist(self):

        import math
        arr=np.random.normal(50,50,10000)
        print arr
        print "mean = " + str(arr.mean())
        print "std  = " + str(arr.std())
        print "std/sqrt = " + str(arr.std()*1.96/math.sqrt(len(arr)))
        print "bootstrap ci = " + repr(bootstrap(arr, 10000, np.mean, alpha=0.05))
        #print arr


if __name__ == '__main__':
    unittest.main()