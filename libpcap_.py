import libpcap

from libpcap import sniff

for plen, t, buf in sniff("enp2s0", filters="port 53", count=-1, promisc=1, out_file="pcap.pcap"):
    print("[+]: Payload len=", plen)
    print("[+]: Time", t)
    print("[+]: Payload", buf)

# https://python-libpcap.readthedocs.io/en/latest/introduction.html#usage
# https://libpcap.readthedocs.io/en/latest/#