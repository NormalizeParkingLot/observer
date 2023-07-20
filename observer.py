from google.cloud.firestore_v1.base_query import FieldFilter
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import threading
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
stickerToIp = {}, ipToSticker = {}

def registerNode(mac, observerId):
    nodeRef.document(mac).set({"connected": False, "observerId": observerId})

def documnetEventListener(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "MODIFIED":
            msg = 1 if change.document.get("valid") else 0
            dst = stickerToIp[change.document.get("mac")]
            # dst = macToIp[change.document.id]
            sendToNode(dst, msg)

def updateDocument(mac, carState): nodeRef.document(mac).set({"car": carState})

def handlePacket(rowPacket):
    pk = rowPacket[0]

    if "2001" in pk[1].src:
        load = str(pk[3].load)
        if "check_reception" in load:
            carState = '1' in load
            updateDocument(pk[0].src, carState)

def sendToNode(dst, msg):
    sendSocket.connect((dst, port))
    sendSocket.send(msg.to_bytes(1, 'big'))
    # sendSocket.close()

def read_LeasedIp():
    with open("../wisun-visualizer/leasedIP.json", "r") as leasedIP:
        visualizer_map = json.load(leasedIP)["map"]

        for key in visualizer_map:
            converted = []
            ori = list(visualizer_map[key].split('-'))
            for i in range(0,8): converted.append(ori[2*i] + ori[2*i+1])

            stickerToIp[key] = ':'.join(converted[:4]) + "::" + ':'.join(converted[5:])
            ipToSticker[stickerToIp[key]] = key

# run
read_LeasedIp()
col_query = nodeRef.where(filter=FieldFilter("observerId", "==", observerId))
query_watch = col_query.on_snapshot(documnetEventListener)

while True:
    # sniff(iface="wisun", prn = handlePacket, count = 1)
    quit = input("type q if you want quit this : ")
    break;  
sendSocket.close()