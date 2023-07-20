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
nodeRef = firestore.client().collection("test")

# socket variables
sendSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
port = 61617

# observer variables
macToIp = {}
observerId = 0

def registerNode(mac, observerId): nodeRef.document(mac).set({"connected": False, "observerId": observerId})

def documnetEventListener(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "MODIFIED":
            msg = 1 if change.document.get("valid") else 0
            dst = macToIp[change.document.id]
            sendToNode(dst, msg)

def updateDocument(mac, carState): nodeRef.document(mac).set({"car": carState})

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
    if (src_ip == dst_ip) and (src_mac != dst_mac):
        hexList = packetLoadToHex(pk[3].load)

        # 9b == icmpv6.type.RPL_Control, 03 == icmpv6.code.Destination_Advertisement_Object_Acknowlegement
        if ("9b" in hexList) and ("03" in hexList):
            rpl_i = hexList.index("9b")
            code3_i = hexList.index("03")
            
            # 01을 체크 하는거는 응답이 계속 오기때문에 처음만 체크
            if (rpl_i+1 == code3_i) and (hexList[code3_i + 5] == "01"):
                hexIpList = hexList[rpl_i-16 : rpl_i]
                converted = []
                for i in range(0,8): converted.append(hexIpList[2*i] + hexIpList[2*i+1])
                macToIp[dst_mac] = ':'.join(converted[:4]) + "::" + ':'.join(converted[5:])
                registerNode(dst_mac, observerId)
                print("new node registered")
                print("mac: " + dst_mac + "    / ip: " + macToIp[dst_mac])
    
    # node state udpate
    load = str(pk[3].load)
    if "check_reception" in load:
        carState = '1' in load
        updateDocument(pk[0].src, carState)

def sendToNode(dst, msg):
    sendSocket.connect((dst, port))
    sendSocket.send(msg.to_bytes(1, 'big'))
    # sendSocket.close()


# run
col_query = nodeRef.where(filter=FieldFilter("observerId", "==", observerId))
query_watch = col_query.on_snapshot(documnetEventListener)

while True:
    # sniff(iface="wisun", prn = handlePacket, count = 1)
    quit = input("type q if you want quit this : ")
    break;  
sendSocket.close()