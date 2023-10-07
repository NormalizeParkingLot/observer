from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import socket
import json
from scapy.all import *

# firebase variables
fbCred = credentials.Certificate('./firebaseCredential.json')
app = firebase_admin.initialize_app(fbCred)
nodeRef = firestore.client().collection("module")

# socket variables
sendSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
port = 61617

# observer variables
# macToIp = {}
uidToIp = {}
observerId = 0

def ipFormat(ipList):
    converted = []
    for i in range(0,8): converted.append(ipList[2*i] + ipList[2*i+1])
    return ':'.join(converted[:4]) + "::" + ':'.join(converted[5:])

def registerNode(hexList, baseI): 
    # 인터넷 레이어의 mac주소 != 모듈의 mac주소
    # IEEE802.15.4 쪽의 packet에서 모듈의 mac주소 탐지
    dst_mac = ':'.join(hexList[37:45])
    dst_ip  = ipFormat(hexList[baseI-16 : baseI])

    macToIp[dst_mac] = dst_ip
    # registerNode(dst_mac, observerId)
    print("new node uidToIp")
    print("mac: " + dst_mac + "    / ip: " + macToIp[dst_mac])
    nodeRef.document(dst_mac).set({"connected": False, "observerId": observerId, "isBlocked": True})

def documnetEventListener(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "MODIFIED":
            msg = 0 if change.document.get("isBlocked") else 1
            dst = uidToIp[change.document.id]
            sendToNode(dst, msg)

def updateDocument(mac, isOcupied): nodeRef.document(mac).update({"isOcupied": isOcupied})

def packetLoadToHex(original_s):
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

def handlePacket(rowPacket):
    pk = rowPacket[0]
    src_ip = pk[1].src; src_mac = pk[0].src
    dst_ip = pk[1].dst; dst_mac = pk[0].dst

    if "2001" not in dst_ip: return

    # find new Node
    # wireshark 상으로는 1에서 child로 가는데, scapy에서는 1에서 1로 가는걸로 보임
    # if (src_ip == dst_ip) and (src_mac != dst_mac):
    #     hexList = packetLoadToHex(pk[3].load)
        
    #     # print(hexList)
    #     # print(len(hexList))
    #     # if ("87" in hexList) and (len(hexList) == 114):
    #     #     neighbor_i = hexList.index("87")
    #     #     if (hexList[neighbor_i + 1] == "00"):
    #     #         print("neighbor register")
    #             # registerNode(hexList, neighbor_i)

    #     # 9b == icmpv6.type.RPL_Control, 03 == icmpv6.code.Destination_Advertisement_Object_Acknowlegement
    #     if ("9b" in hexList) and ("03" in hexList):
    #         rpl_i = hexList.index("9b")
    #         code3_i = hexList.index("03")
            
    #         # 01을 체크 하는거는 응답이 계속 오기때문에 처음만 체크
    #         if (rpl_i+1 == code3_i) and (hexList[code3_i + 5] == "01"):
    #             print("rpl register")
    #             registerNode(hexList, rpl_i)
    
    # node state udpate
    if hasattr(pk[3], "load"):
        load = str(pk[3].load)
        hexList = packetLoadToHex(pk[3].load)
        
        if ("check_reception" in load) and (len(load) == 26):
            # print(load)
            # print(hexList)
            unique_id = load[-5:-1]
            if(unique_id not in uidToIp):
                nodeRef.document(unique_id).set({"connected": False, "observerId": observerId, "isBlocked": True})
                uidToIp[unique_id] = src_ip
                print(unique_id + " registered")

            isOcupied = (hexList[0] == '01')
            updateDocument(unique_id, isOcupied)

def sendToNode(dst, msg):
    print("sendToNode")
    sendSocket.connect((dst, port))
    sendSocket.send(msg.to_bytes(1, 'big'))
    # sendSocket.close()


# run
col_query = nodeRef.where(filter=FieldFilter("observerId", "==", observerId))
query_watch = col_query.on_snapshot(documnetEventListener)

# while True:
sniff(iface="wisun", prn = handlePacket, count = 0)
    # quit = input("type q if you want quit this : ")
    # break;  
sendSocket.close()