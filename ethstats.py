#!/usr/bin/python

from optparse import OptionParser
import pdb

parser = OptionParser()
parser.add_option("-n", "--period", dest="PERIOD", default=1,
                  help="average period in seconds, default 1 sec")
parser.add_option("-i", "--interface", dest="INTERFACE", default="all",
                  help="interface or interfaces witch statistics is measured")

(options, args) = parser.parse_args()

class ethstats:

    def __init__(self):
        self.period = vars(options)['PERIOD']
        self.interfaces = vars(options)['INTERFACE']

    def read_stats(self):
        d= {}
        l= []
        with open('/proc/net/dev') as f:
            next(f)
            next(f)
            for line in f:
                l= line.split()
                d[l[0].rstrip(':')]=l[1:]

        return(d['wlp3s0'])
#            interface = {line.split(":") for line in lines}
#            data=[x.split() for x in rez]
    

stats=ethstats()
print(stats.read_stats())
#    def count_stats():

