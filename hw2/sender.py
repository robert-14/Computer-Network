import sys 
import socket
import string
import os 
import time
import fcntl
import math


#create socket
try:
    s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM) 
except socket.error:
    print "Fail to create socket"
    sys.exit(1)

print("successfully create")

#set host 
myHost = '127.0.0.1'   
myPort = 8888

dest_IP = '127.0.0.1'
dest_Port = 8787

recv_IP = '127.0.0.1'
recv_Port = 8887

try:
    s.bind((myHost,myPort))
except socket.error:
    print "Binding Failed"
    sys.exit(1)
print "Socket Binding Complete!"

#set non blocking socket
fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

#set filename and open file 
filename = raw_input("enter file name:")
file = open(filename,"rb")

#send file name to server
s.sendto(filename,(recv_IP,recv_Port))

#load file into data segment, header format(8 byte): data type(1 byte ) + sequence number(7), total data size = 1032 bytes
data = ''
data_list = []
seq_num = 1
while 1:
    data = file.read(1024)
    if not data: break
    header = str(seq_num)

    #let header have the same size 
    j = len(header)
    #print("j = " + str(j) )
    for j in range(j,7):
        header = '0' + header
        j  = j + 1
    header = 'd' + header                                                  #add data type 
    #print("header = " + header)     
    data =  header.encode("utf-8") + data
    data_list.append(data)
    seq_num = seq_num + 1
    #print("the data is :" + data + "\n")

#set window,threshold, 
window = 1
threshold = 16

#send the data and receive ack from the server
data_list_num = len(data_list)
#print("total packet number = " + str(data_list_num) )
start_index = 1    
max_send = 1                                                         #first element in window                                                                   #determine whether the data transmission is completed
while (1):                                                                  #todo: resend
    send_num = 0
    for send_num in range(0,window):
        if (start_index + send_num > data_list_num):
            break
        s.sendto(data_list[send_num+start_index-1], (dest_IP,dest_Port))
        #print("send_num = " + str(send_num) + "\n" )
        #print("data_send = " + data_list[send_num + start_index-1] +"\n")
        if( max_send <= start_index + send_num ) :
            print('send    data    #' + str(start_index+send_num) + ',   winsize = ' + str(window) )
        else :    
            print('resnd   data    #' + str(start_index+send_num) + ',   winsize = ' + str(window) )
        send_num = send_num + 1
    max_send = max(start_index + send_num,max_send)    
    if start_index > data_list_num:
        s.sendto("ffffffff",(dest_IP,dest_Port))   
        print("send    fin") 
    #recv ack in timeout    
    #while (1):    
    t0 = time.time()
    t1 = time.time()
    window_index = 0
    data = ''

    #receive ack in 1 sec
    while (time.time() - t0 < 0.5):
            #d = ''
        try:
            d = s.recvfrom(1032)
            d = str(d)
            #print("ack  =" + d + "\n")
            recv_list = []
            recv_list = d.split(',')
            data = recv_list[0]
            if data[2] == 'z':
                print("recv    finack")
                s.close()
                sys.exit()
            elif data[2] == 'a' : 
                rec_num = data[3:10]                                    #rec_num the sequence number in ack file 
                rec_num = int(rec_num) 
                if (rec_num == start_index +  window_index):
                    window_index =  window_index + 1
                t1 = time.time()
                print("recv    ack     #" + str(rec_num))
            else : 
               print("error: recv undefined packet")
        except socket.error:
            if (time.time() - t0 > 0.5)  :
                break
    if ( window == window_index ):                                      #receive all packet
        start_index = start_index + window
        if window < threshold:
            window = window*2
        else:
           window = window + 1
    elif (window > window_index ):   
        threshold = max(math.floor(window/2.0),1)                                   #packet loss
        print("time    out,          threshold = " + str(threshold) )
        start_index = start_index + window_index
        window = 1
    else:
        printf("some error occur")
s.close()






