from scapy.all import *

unicode = str
protocols = {1: 'ICMP', 6: 'TCP', 17:'UDP'}

def showpacket(packet):
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst
    proto  =packet[0][1].proto

    if proto in protocols:
        #  print('protocol : %s: %s -> %s' %(protocols[proto], src_ip,dst_ip))
        print("packet")
        if proto == 17:
            print('type:[%d], code:[%d]' %(packet[0][2].type, packet[0][2].code))

def main(filter):
    sniff(filter =filter, prn = showpacket, count = 0)
#count가 0이므로 모니터링 모드이다.

if __name__ == '__main__':
    main(filter)

# def showPacket(packet):  
#     a = packet.show()  
#     print (a)  
  
# def sniffing(filter):  
#     sniff(filter = filter, prn = showPacket, count = 1)  
  
# if __name__ == '__main__':  
#     filter = 'ip'  
#     sniffing(filter)  