#!/usr/bin/env python3
import socket
from random import randint
import random
import threading
import string
from time import sleep
from time import time
import argparse

class hostconn(object):
    def __init__(self, name=None, address="127.0.0.1", dstPort=1433, rate=1, duration=10, startTime = 0, srcPort = 1443):
        self.name = name
        self.address = address
        self.dstport = dstPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.bind(('', int(srcPort)))
        self.sendThread = threading.Thread(target=self.send_pkts,args=())
        self.rate = float(rate)
        self.stop = False
        self.srcPort = int(srcPort)
        self.startTime = startTime
        self.duration = duration
        self.printInfo()
    
    def printInfo(self):
        print('------------------------------------')
        print('Name %s ' % self.name)
        print('Address %s' % self.address)
        print('Source Port %s' % self.srcPort)
        print('Destination Port %s' % self.dstport)
        print('Packet rate %s' % self.rate)
        print('------------------------------------')


    def shutdown(self):
        self.stop = True
        self.sendThread.join()

    def send_pkts(self):
        sleep(self.startTime)
        print('Host %s started sending packets' % self.name)
        tStart = time()
        i = 0
        while float(time() - tStart) <= float(self.duration):
            if self.stop == True:
                break
            sleep(float(1/float(self.rate)))
            self.sock.sendto(str(i).encode('utf-8'), (self.address, self.dstport))
            i += 1
        
        self.stop = True

        print('Host %s stopped sending packets' % self.name)
            
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--flows', '-f', dest="nrFlows",default=10)
    parser.add_argument('--maxrate', '-mr', dest="maxRate",default=6)

    parser.add_argument('--duration','-d',dest="duration",default=10)
    parser.add_argument('--dstAddr','-dst',dest="dstAddr",default='10.0.1.2')
    parser.add_argument('--random','-r',dest="random",action='store_true',default=False)
    
    return parser.parse_args()

def calcplaybooksumRates(playbook):
    # calculate the ideal graph of the playbook
    graphlist = {}
    for x in playbook:
        for y in range(int(x),int(playbook[x]['duration']) + int(x)):
            if int(y) in graphlist:
                graphlist[int(y)] += int(playbook[x]['hostrate'] * playbook[x]['hostnumber'])
            else: 
                graphlist[int(y)] = int(playbook[x]['hostrate'] * playbook[x]['hostnumber'])

    # open file for writing:
    f= open("./Data/packetGenInput/bench_data.txt","w+")
    for x in graphlist:
        f.write("%s %s\n" % (x, graphlist[x]))
    f.close()

def addPlaybookentry(playbook, t_start, n_hosts, r_host, duration):
    if t_start not in playbook.keys():
        playbook[t_start] = {}
        playbook[t_start]['hostnumber'] = n_hosts
        playbook[t_start]['hostrate'] = r_host
        playbook[t_start]['duration'] = duration
        return playbook

def main(args=None):
    """
    Main entry point for your project.
    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it
            None to use sys.argv.
    """
    try:
        args = get_parser()
        srcPort = 10000
        if args.random == True:
            conn = []
            # Spawn random threads, all starting from t=0:
            for x in range(0,int(args.nrFlows)):
                host = hostconn(name='conn'+str(x),
                        address=args.dstAddr, 
                        rate=random.random()*int(args.maxRate), 
                        dstPort=1433,
                        srcPort = srcPort)
                host.sendThread.start()
                conn.append(host)
                srcPort += 1
            sleep(int(args.duration))

            for x in conn:
                x.stop = True
        else:
            # start a program:
            playbook = {}
            playbook = addPlaybookentry(playbook=playbook, t_start=5, n_hosts=1, r_host=100,duration=1)
            playbook = addPlaybookentry(playbook=playbook, t_start=10, n_hosts=1, r_host=10,duration=60)
            playbook = addPlaybookentry(playbook=playbook, t_start=10, n_hosts=1, r_host=90,duration=50)
            playbook = addPlaybookentry(playbook=playbook, t_start=20, n_hosts=1, r_hosts=10, duration=10)
            playbook = addPlaybookentry(playbook=playbook, t_start=40, n_hosts=1, r_hosts=999999999999999, duration=1)
            
            #calcplaybooksumRates(playbook)
            playThreads = []
            for x in sorted(playbook.keys()):
                #print('At t=%s, start %i hosts with each a rate of %i pkts/sec for %i seconds' % (x,playbook[x]['hostnumber'],playbook[x]['hostrate'], playbook[x]['duration']))
                playbook[x]['conn'] = []
                for y in range(0,int(playbook[x]['hostnumber'])):
                    playThreads.append(
                        hostconn(name='conn'+ str(x) + '.' + str(y),
                        address=args.dstAddr, 
                        rate=playbook[x]['hostrate'], 
                        dstPort=1433,
                        srcPort = srcPort,
                        startTime=float(x),
                        duration=playbook[x]['duration']
                        )
                    )
                    srcPort += 1
            # start all threads
            for x in playThreads:
                x.sendThread.start()

            # wait until all threads are finished:
            for x in playThreads:
                x.sendThread.join()             
            

    except KeyboardInterrupt:
            print("Shutting down.")
            for x in conn:
                x.shutdown()
            quit()

if __name__ == '__main__':
    main()



