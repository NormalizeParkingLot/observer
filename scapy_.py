from scapy.all import *

def showpacket(packet):
    # https://secretpack.tistory.com/112 
    # src_ip = packet[0][1].src
    # dst_ip = packet[0][1].dst
    # proto  =packet[0][1].proto

    # if proto in protocols:
        #  print('protocol : %s: %s -> %s' %(protocols[proto], src_ip,dst_ip))
    print(packet.show())
        # if proto == 17:
        #     print('type:[%d], code:[%d]' %(packet[0][2].type, packet[0][2].code))

sniff(iface="wisun", prn = showpacket, count = 0)