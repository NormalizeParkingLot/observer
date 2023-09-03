# import json

# stickerToIp = {}
# with open("../wisun-visualizer/leasedIP.json", "r") as leasedIP:
#     st_python = json.load(leasedIP)
#     visualizer_map = st_python["map"]

#     for key in visualizer_map:
#         ori = list(visualizer_map[key].split('-'))
#         converted = []
#         for i in range(0,8): converted.append(ori[2*i] + ori[2*i+1])
#         stickerToIp[key] = ':'.join(converted[:4]) + "::" + ':'.join(converted[5:])

# print(stickerToIp)

import codecs

s = b'\x02\x01\x00\x00\x01\x01\xff\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002A\xccf\xfe\xca\x00^0\x04\x00K\x12\x00\x08\xc5"\x04\x00K\x12\x00{3:\x87\x00\x08h\x00\x00\x00\x00\xfe\x80\x00\x00\x00\x00\x00\x00\x02\x12K\x00\x040^\x00\xd8'
# s = b'EX\x02\x01\x00\x00\x01\x01\xff\x01\x01\x01\x01\x01\x01\x01\x01\x02\x02\x02\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00RA\xccf\xfe\xca\x08\xc5"\x04\x00K\x12\x00\x00^0\x04\x00K\x12\x00z\x00: \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01   \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d\x9b\x03\xd9\x98\x00\x80\x01\x00 \x01\r\xb8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01J\x0c'
# s = b'\x01   \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d'
s = str(s)[2:-1]

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

# print(hexList)

l = ['08', 'c5', '22', '04', '00', '4b', '12', '00']
print(':'.join(l))