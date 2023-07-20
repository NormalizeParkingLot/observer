from scapy.all import *

def loadToHex(original_s):
    s = str(original_s)[2:-1]
    hexList = []

    i = 0
    while i < len(s):
        if s[i: i+2] == "\\x":
            hexList.append( s[i+2: i+4] )
            i += 4
        elif s[i: i+2] == "\\r":
            hexList.append( "0d" )
            i += 2
        else:
            hexList.append( hex(ord(s[i]))[2:] )
            i += 1
    return hexList

def showpacket(packet):
    # https://secretpack.tistory.com/112 
    src_ip = packet[0][1].src
    dst_ip = packet[0][1].dst

    src_mac = packet[0][0].src
    dst_mac = packet[0][0].dst

    # if proto in protocols:
        #  print('protocol : %s: %s -> %s' %(protocols[proto], src_ip,dst_ip))
    if ("2001" in dst_ip) and (src_ip == dst_ip) and (src_mac != dst_mac):
        # load = str(packet[0][3].load)
        # rpl3_i = load.find("\\x9b\\x03")
        # if (rpl3_i > 0) and (load[rpl3_i+24: rpl3_i+28] == "\\x01"):
        hexList = loadToHex(packet[0][3].load)

        if ("9b" in hexList) and ("03" in hexList):
            rpl_i = hexList.index("9b")
            code3_i = hexList.index("03")
            
            if (rpl_i+1 == code3_i) and (hexList[code3_i + 5] == "01"):
                hexIpList = hexList[rpl_i-16 : rpl_i]
                converted = []
                for i in range(0,8): converted.append(hexIpList[2*i] + hexIpList[2*i+1])
                newNodeIp = ':'.join(converted[:4]) + "::" + ':'.join(converted[5:])
                print(newNodeIp)

    #     load = str(packet[0][3].load).replace("check_reception",'')
    #     print("no car" if load[5]=='1' else "car exist")
        # if proto == 17:
        #     print('type:[%d], code:[%d]' %(packet[0][2].type, packet[0][2].code))

sniff(iface="wisun", prn = showpacket, count = 0)