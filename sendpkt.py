#!/usr/bin/env python2
from scapy.all import RadioTap, sendp
import codecs
# this is used to send the following packet:
inStr = '3341ffff2222000000aa0102000c1433ffff3333'
sendp(RadioTap(codecs.decode(inStr, 'hex')), iface='h1-eth0', inter=100, loop=1)