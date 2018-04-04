import socket
import sys

myhost = '127.0.0.1'
myport = 8887

dest_IP = '127.0.0.1'
dest_Port = 8787
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

#add file type
name_list = []
filename = s.recvfrom(1032)
filename = str(filename)
#print("filenamee :" + filename)
name_list = []
name_list = filename.split(',')
filename  = name_list[0]
filename = filename[len(filename) - 5:len(filename)-1]
filename = "result" + filename 
#open file
file = open(filename,"wb")

buffer_size = 32
buffer_data = [] 


#receive and reply
ack_start = '0000000'
while (1):
    d = []
    d = s.recvfrom(1032)
    if not d: print("don't get data")
    #print("packet : " + d + "\n")
    #print("received message :" + d +"\n")
    #data_list = []
    #data_list = d.split(',')
    packet = d[0][8:len(d[0])]
    header = d[0][0:8].decode("utf-8")
    #print("received message :" + data_list[1] +"\n")
    

    #recv data => 
    if header[0] == 'd':
        seq_num = header[1:8]
        seq_num = int(seq_num)
        #print("recv    data    #" + str(seq_num) )

        #buffer handling
        if( len(buffer_data) >= buffer_size ):
            print("drop    data    #" + str(seq_num) )
            print("send    ack     #" + str(int(ack_start)) )
            print("flush")
            buffer_data = []

        elif ( int(ack_start) + 1 != seq_num ) :
            print("drop    data    #" + str(seq_num) )
            print("send    ack     #" + str(int(ack_start)) )
        else :
            if ( int(ack_start) + 1 == seq_num ): #in order receive
                print("recv    data    #" + str(seq_num) )
                ack_start = header[1:8]
                file.write(packet)
                buffer_data.append(seq_num)
                #send ack back
                ack = 'a' + ack_start
                s.sendto(ack,(dest_IP,dest_Port))
                print("send    ack     #" + str(int(ack_start)) )     

    elif header[0] == 'f':
        #todo: close socket  
        ack = 'zzzzzzzz'  
        s.sendto(ack,(dest_IP,dest_Port))
        print("send    finack")
        s.close()
        sys.exit()


    #recv termination    

s.close