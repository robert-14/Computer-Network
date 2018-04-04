import sys
import socket
import string
import time 


#read channel from config
file = open("config","r")
channel = file.read()
cha_len = len(channel)
channel = channel[6:cha_len-1]
#print (channel)
s = socket.socket( socket.AF_INET, socket.SOCK_STREAM) 
#HostIP = 'irc.freenode.net'
Port = 6667
#print(channel)
s.connect( ('irc.freenode.net', Port) )
print("hi")
s.send(bytes("USER irobot17 irobot17 irobot17: irobot17\r\n" , "UTF-8"))
#print("############################################\n")
s.send(bytes("NICK irobot17\r\n" , "UTF-8"))
#text = s.recv(2040)
#s.send(bytes('PONG ' + text.split() [1] + '\r\n'),"UTF-8")
#print("############################################\n")
s.send( bytes("JOIN #%s\r\n" %channel, "UTF-8") )
#print("############################################\n")
#ircmsg = ""
#while ircmsg.find("End of /NAMES list.") == -1:  
 #   ircmsg = s.recv(2048).decode("UTF-8")
  #  ircmsg = ircmsg.strip('\n\r')
   # print(ircmsg)
s.send( bytes("PRIVMSG #" + channel + " : Hello! I am robot.\r\n", "UTF-8") )
#print("############################################\n")
#print(channel +"\n")
while 1:
    text = ""
    text = s.recv(2040).decode("UTF-8")
    text_len = len(text)
    print(text)
    print(text.find("@repeat"))
    if text.find('PING') != -1:
        #print("send suc\n")
        #print("%s\n"%text.split()[1])
        s.send(bytes('PONG ' + text.split() [1] + '\r\n',"UTF-8"))
    if (text.find('@repeat')) != -1 :
        print("i am repeat\n")
        ans = text[ text.find('@repeat') + 8:text_len]
        print(ans)
        print("\n")
        s.send( bytes("PRIVMSG #" + channel + " : "+ ans +"\r\n" , "UTF-8") )
    if text.find('@convert') != -1 :
        if text.find("0x") != -1:	
            input = text[text.find('@convert') + 11:text_len]
            ans = int(input,16)
            print(ans)
            s.send( bytes("PRIVMSG #" + channel + " : %d\r\n" %(ans), "UTF-8") )
        else:
            input = text[text.find('@convert')+9:text_len]
            input = int(input)
            ans = hex(input)
            ans = ans[2:len(ans)]
            print(ans)
            s.send( bytes("PRIVMSG #" + channel + " : "+ ans +"\r\n", "UTF-8") )
    if text.find('@ip') != -1:	
        input1 = text[ text.find("@ip")+4 : text_len]
        i_len = len(input1) - 2     #because input1 has \r\n
        ip_num = 0
        ans = []
        for i in range(1,i_len+1):
            for j in range(i+1,i_len+1):
                for k in range(j+1,i_len+1):
                    s1 = input1[0:i]
                    s2 = input1[i:j]
                    s3 = input1[j:k]
                    s4 = input1[k:i_len]
                    print(s1 +" len = " + str(len(s1))+"\r\n") 
                    print(s2 + " len = " +str(len(s2)) +"\r\n") 
                    print(s3 + " len = " + str(len(s3)) +"\r\n") 
                    print(s4 + " len = " + str(len(s4)) + "\r\n\r\n\r\n") 
                    if ( ((len(s1) > 1) and (s1[0] == '0')) or ((len(s2) > 1) and (s2[0] == '0')) or ((len(s3) > 1) and (s3[0] == '0')) or ((len(s4) > 1) and (s4[0] == '0')) ):
                        continue
                    if len(s1) == 0 or len(s2) == 0 or len(s3) == 0 or len(s4) == 0:
                        continue
                       
                    if int(s1,10) > 255 or int(s2,10) > 255 or int(s3,10) > 255 or int(s4,10) > 255:
                        continue
                    ip_num += 1 
                    full_str = s1+"."+s2+"."+s3+"."+s4
                    ans.append(full_str)
        s.send( bytes("PRIVMSG #" + channel + " : " + str(ip_num) + "\r\n", "UTF-8") )
        for i in range(0,ip_num):
            s.send( bytes("PRIVMSG #" + channel + " : " + ans[i] + "\r\n", "UTF-8") )



    if text.find('@help') != -1 :
   	    s.send( bytes("PRIVMSG #" + channel + " : @repeat <Message>\r\n", "UTF-8") )
   	    s.send( bytes("PRIVMSG #" + channel + " : @convert <Number>\r\n", "UTF-8") )
   	    s.send( bytes("PRIVMSG #" + channel + " : @ip <String>\r\n", "UTF-8") )


    














