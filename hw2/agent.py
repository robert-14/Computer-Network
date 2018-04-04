import socket
import sys
import random

myhost = '127.0.0.1'
myport = 8787

sender_IP = '127.0.0.1'
sender_Port = 8888

receiver_IP = '127.0.0.1'
receiver_Port = 8887
#create socket
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print "Socket Created"
except socket.error:
    print "Failed to create socket"
    sys.exit(1)

#bind to socket
try:
    s.bind((myhost,myport))
except socket.error:
    print "Binding Failed"
    sys.exit(1)
print "Socket Binding Complete!"


lost_r = input("please enter lose rate:")
real_lost_r = random.random()
data_lost = 0.0
data_num = 0.0
#open file




#get and forward
while (1):
    d = []
    d = s.recvfrom(1032)
    if not d: print("don't get data")
     
    if len(d[0]) > 8: #data package
        if( real_lost_r >= lost_r):
            s.sendto(d[0],( receiver_IP,receiver_Port))
            packet = d[0][8:len(d[0])]
            header = d[0][0:8].decode("utf-8")

            if header[0] == 'd':
                data_num  = data_num + 1
                real_lost_r = data_lost/data_num
                seq_num = header[1:8]
                seq_num = int(seq_num)
                print("get    data    #" + str(seq_num) )
                print("fwd    data    #" + str(seq_num) + ",   lost rate = " + str(real_lost_r) )
            else:
                print("error : undefined package")    
                
        else:
            packet = d[0][8:len(d[0])]
            header = d[0][0:8].decode("utf-8")

            if header[0] == 'd':
                data_num  = data_num + 1
                data_lost = data_lost + 1
                real_lost_r = data_lost/data_num
                seq_num = header[1:8]
                seq_num = int(seq_num)
                print("get    data    #" + str(seq_num) )
                print("drop   data    #" + str(seq_num) + ",   " +"lost rate = "+ str(real_lost_r) )
            else:
                print("error : undefined package")  

    else: #ack(a) fin(f) finack(z)
        header = d[0][0:8]
        if header[0] == 'a':
            seq_num = header[1:8]
            seq_num = int(seq_num)
            print("get    ack     #" + str(seq_num) )
            print("fwd    ack     #" + str(seq_num) )
            s.sendto(header,(sender_IP,sender_Port))


        elif header[0] == 'f':
            print("get    fin")
            print("fwd    fin")
            s.sendto("ffffffff",( receiver_IP,receiver_Port))
        elif header[0] == 'z':
            print("get    finack")
            print("fwd    finack")
            s.sendto("zzzzzzzz",( sender_IP,sender_Port))
            s.close()
            sys.exit()

        
        

   