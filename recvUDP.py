#!/usr/bin/env python3
#sniff(filter = 'dst port 5555')

from scapy.all import *
from time import time
pktData = {}

def recvFunction(packet):

    # do processing here. Store
    data = int(packet.getlayer(UDP).payload.load)
    addflowReading(int(packet.sport), data)

def addflowReading(srcPort, data):
    global pktData
    # if entry does not exist, create it
    if srcPort not in pktData.keys():
        pktData[srcPort] = {}
        if 'ts' not in pktData[srcPort].keys():
            pktData[srcPort]['ts'] = []
        if 'data' not in pktData[srcPort]:
            pktData[srcPort]['data'] = []

    pktData[srcPort]['ts'].append(float(time()))
    pktData[srcPort]['data'].append(data)

def dumpToFile(FILENAME):
    f = open(FILENAME, 'w+')
    for srcPort in pktData:
        for num in range(len(pktData[srcPort]['ts'])):
            f.write("%d,%f,%d\n" % (int(srcPort), float(pktData[srcPort]['ts'][int(num)]), int(pktData[srcPort]['data'][int(num)])))

def printTotalPacket():
    for srcPort in pktData:
        
        print("%d received %s packets" % (int(srcPort), len(pktData[srcPort]['ts'])))
        for x in range(len(pktData[srcPort]['data'])):
            if x not in pktData[srcPort]['data']:
                print("    Missing packet %d" % (x))
            
            

    # generate graph of dinges.

    # x axis: time
    # y axis: packets that are dropped
# h1 watch echo "hello" >> /dev/udp/10.0.1.20/1433 &
# h2 python3 ./recvUDP.py

def main():
# start the sniffer
    FILENAME = 'output.txt'
    sniff(filter = 'udp and dst port 1433', prn = recvFunction)
    print("Reached the end for some reason")

    # do processing here
    printTotalPacket()
    dumpToFile(FILENAME)
if __name__ == '__main__':
    main()