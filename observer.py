from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin
import threading
import socket
from scapy.all import *

# firebase variables
fbCred = credentials.Certificate('./firebaseCredential.json')
app = firebase_admin.initialize_app(fbCred)
nodeRef = firestore.client().collection("node")

# socket variables
sendSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
port = 61617

# observer variables
macToIp = {}
observerId = 0


def registerNode(mac, observerId):
    nodeRef.document(mac)
        .set({"connected": False, "observerId": observerId})

def documnetEventListener(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == "MODIFIED":
            # need to update
            msg = "open" if change.document.barrierState else "close"
            dst = macToIp[change.document.id]
            sendToNode(dst, msg)

def handlePacket(rowPacket):
    pk = rowPacket[0]
    # update macToIp(arp table)
    macToIp[pk[0].src] = pk[1].src
    macToIp[pk[0].dst] = pk[1].dst

    # handle acture data
    print(rowPacket.show())

def sendToNode(dst, msg):
    sendSocket.connect((dst, port))
    sendSocket.send(msg.encode())
    sendSocket.close()


# run
col_query = nodeRef.where("observerId", "==", observerId)
query_watch = col_query.on_snapshot(documnetEventListener)

sniff(iface="wisun", prn = handlePacket, count = 0)