from scapy.all import *

def showpacket(packet):
    # https://secretpack.tistory.com/112 
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst

    src_mac = packet[0][0].src
    dst_mac = packet[0][0].dst
    # proto  =packet[0][1].proto

    # if proto in protocols:
        #  print('protocol : %s: %s -> %s' %(protocols[proto], src_ip,dst_ip))
    # print(packet.show())
    print(src_ip + ": " + src_mac)
    print(dst_ip + ": " + dst_mac)
        # if proto == 17:
        #     print('type:[%d], code:[%d]' %(packet[0][2].type, packet[0][2].code))

sniff(iface="wisun", prn = showpacket, count = 0)

"""
packet[0]에 들어 있는 데이터(추측)
###[ Ethernet ]###
    dst       = 00:ff:70:9f:5a:a6
    src       = 00:ff:71:9f:5a:a6
    type      = IPv6
###[ IPv6 ]###
    version   = 6
    tc        = 0
    fl        = 0
    plen      = 22
    nh        = UDP
    hlim      = 64
    src       = 2001:db8::65
    dst       = 2001:db8::1
###[ UDP ]###
    sport     = 61617
    dport     = 61617
    len       = 22
    chksum    = 0xa6bc
###[ Raw ]###
    load      = '\x00\x00\x00\x00\\xe4\x0c\x00uinject'
"""