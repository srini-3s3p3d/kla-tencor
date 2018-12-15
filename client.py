import zmq
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import csv

# Create the client
ctx = zmq.Context.instance()
client_socket = ctx.socket(zmq.PAIR)

# Connect to the server
client_socket.connect("tcp://127.0.0.1:8008")

client_socket.send_string("SETJOBID 2")
new_socket = client_socket.recv_string()

# Check the GETINFO Job
client_socket.send_string('GETINFO')
meta_data_info = client_socket.recv_string()
data=meta_data_info.split(' ')
print('Metadata information : ' + meta_data_info)

# Process Metadata information
data_socket = ctx.socket(zmq.PAIR)

data_socket.connect("tcp://127.0.0.1:" + new_socket)
client_socket.send_string("STARTJOB")
final=Image.new('L',(int(data[2])*int(data[6]),int(data[3])*int(data[7])))
for i in range(8):
    if i % 2 == 0: 
        for j in range(8): 
            msg = data_socket.recv()
            img=Image.frombuffer("L", (int(data[0]),int(data[1])), msg,'raw','L',0,1)
            final.paste(img,(j*(int(data[0])),i*(int(data[1]))))
    else: 
        for j in range(8 - 1, -1, -1): 
            msg = data_socket.recv()
            img=Image.frombuffer("L", (int(data[0]),int(data[1])), msg,'raw','L',0,1)
            final.paste(img,(j*(int(data[0])),i*(int(data[1]))))


# Process the Message
final.show()
image_data = np.asarray(final)
print(np.matrix(image_data))
""" with open('data.csv','w') as csvfile:
    writer=csv.writer(csvfile,delimiter=' ',quotechar='|',quoting=csv.QUOTE_ALL)
    for w in tt:
        writer.writerow(w)
 """    
rd=[]
dr=[]
dc=[]
cd=[]
row,col=image_data.shape

for i in range(row):
    for j in range(col):
        if(image_data[i][j]>240):
            dr.append(int(i/1024))
            dc.append(int(j/1024))
            rd.append(i)
            cd.append(j)


with open('some2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(dr,dc,rd, cd))
client_socket.send_string("END")