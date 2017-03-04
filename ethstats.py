#!/usr/bin/python

from optparse import OptionParser
import time
import sys

parser = OptionParser()
parser.add_option("-n", "--period", dest="PERIOD", default=1,
                  help="average period in seconds, default 1 sec")
parser.add_option("-i", "--interface", dest="INTERFACE", default="all",
                  help="interface witch statistics is measured, default all interfaces")

(options, args) = parser.parse_args()

class ethstats:

    def __init__(self):
        self.interface = vars(options)['INTERFACE']
        try:
            self.period = int( vars(options)['PERIOD'])
        except ValueError as e:
            sys.stderr.write("Wrong period n: '%s', n should be integer\n"%vars(options)['PERIOD'])
            sys.exit(1)

        try:
            self.previous, self.pts = self.__read_stats()
        except KeyError as e:
            sys.stderr.write("Interface %s not found\n"%e)
            sys.exit(1)

    def __read_stats(self):
        d= {}
        l= []
        with open('/proc/net/dev') as f:
            next(f)
            next(f)
            for line in f:
                l= line.split()
                d[l[0].rstrip(':')]=list(map(int,l[1:]))

        ts=time.time()
        if self.interface == "all":
            return d, ts
        
        return  {self.interface:d[self.interface]}, ts

    def get(self):
        current, cts = self.__read_stats()
        rez={}
        for interface in current:
            rx=(current[interface][0] - self.previous[interface][0])*8/10**6/(cts-self.pts)
            tx=(current[interface][8] - self.previous[interface][8])*8/10**6/(cts-self.pts)
            rpps=(current[interface][1] - self.previous[interface][1])/10**3/(cts-self.pts)
            tpps=(current[interface][9] - self.previous[interface][9])/10**3/(cts-self.pts)
            rez[interface]=[tx,tpps,rx,rpps]
        
        self.previous, self.pts = current, cts
        return rez

stats=ethstats()
while True: 
    try:
        time.sleep(stats.period)
        rez=stats.get()
        for interface in rez:
            sys.stdout.write("%10s: TX%9.2f Mbps%8.2f kPPS RX%9.2f Mbps%8.2f kPPS\n"%tuple([interface]+rez[interface]))
            sys.stdout.flush()
    except KeyboardInterrupt:
        break
