import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./firebaseCredential.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

# Create an Event for notifying main thread.
callback_done = threading.Event()
def on_snapshot(doc_snapshot, changes, read_time):
    print("callback called")
    for doc in doc_snapshot:
        print(f"Received document snapshot: {doc.id}")
    callback_done.set()


doc_watch = doc_ref.on_snapshot(on_snapshot)

while True:
    1 + 1