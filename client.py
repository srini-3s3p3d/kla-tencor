import zmq
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# Create the client
ctx = zmq.Context.instance()
client_socket = ctx.socket(zmq.PAIR)

# Connect to the server
client_socket.connect("tcp://127.0.0.1:8008")

client_socket.send_string("SETJOBID 1")
new_socket = client_socket.recv_string()

def print_img(mat): 
    global M, N 
      
    # Traverse through all rows 
    for i in range(M): 
          
        # If current row is 
        # even, print from 
        # left to right 
        if i % 2 == 0: 
            for j in range(N): 
                print(str(mat[i][j]), 
                          end = " ") 
  
        # If current row is  
        # odd, print from 
        # right to left 
        else: 
            for j in range(N - 1, -1, -1): 
                print(str(mat[i][j]),  
                          end = " ") 

# Check the GETINFO Job
client_socket.send_string('GETINFO')
meta_data_info = client_socket.recv_string()
data=meta_data_info.split(' ')
print('Metadata information : ' + meta_data_info)

# Process Metadata information
data_socket = ctx.socket(zmq.PAIR)

data_socket.connect("tcp://127.0.0.1:" + new_socket)
client_socket.send_string("STARTJOB")

final = np.zeros(shape=(int(data[2]),int(data[3])))
for i in range(0,64):
    print(i)
    msg = data_socket.recv()
    #msg=[msg[i:i+2] for i in range(0, len(msg), 1)]
    q=0
    inter=np.zeros(shape=(int(data[0]),int(data[1])))
    img=Image.frombuffer("L", (512,512), msg,'raw','L',0,1)
    img.show()

# Process the Message

plt.imshow(inter, cmap="gray")
plt.show()
client_socket.send_string("END")