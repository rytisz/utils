#!/usr/bin/python

from optparse import OptionParser
import pdb
import time

parser = OptionParser()
parser.add_option("-n", "--period", dest="PERIOD", default=1,
                  help="average period in seconds, default 1 sec")
parser.add_option("-i", "--interface", dest="INTERFACE", default="all",
                  help="interface witch statistics is measured, default all interfaces")

(options, args) = parser.parse_args()

class ethstats:

    def __init__(self):
        self.period = int( vars(options)['PERIOD'])
        self.interface = vars(options)['INTERFACE']
        self.previous= self.__read_stats()

    def __read_stats(self):
        d= {}
        l= []
        with open('/proc/net/dev') as f:
            next(f)
            next(f)
            for line in f:
                l= line.split()
                d[l[0].rstrip(':')]=l[1:]
        if self.interface == "all":
            return d
        
        return  {self.interface:d[self.interface]}

    def get(self):
        current= self.__read_stats()
        rez={}
        for interface in current:
            rx=(int(current[interface][0]) - int(self.previous[interface][0]))*8/10**6/self.period
            tx=(int(current[interface][8]) - int(self.previous[interface][8]))*8/10**6/self.period
            rpps=(int(current[interface][1]) - int(self.previous[interface][1]))/10**3/self.period
            tpps=(int(current[interface][9]) - int(self.previous[interface][9]))/10**3/self.period
            rez[interface]=[tx,tpps,rx,rpps]
        
        self.previous=current
        return rez

stats=ethstats()
while True: 
    time.sleep(stats.period)
    rez=stats.get()
    for interface in rez:
        print("%10s: TX%8.2f Mbps%5.2fKPPS RX%8.2f Mbps%5.2fKPPS "%tuple([interface]+rez[interface]))
