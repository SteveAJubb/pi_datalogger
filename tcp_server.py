#!/usr/bin/env python3

import time
import socket
import os
directory="/home/pi/datalogger/" #the location of the datalogger folder
TCP_IP='raspberrypi.fritz.box' #the IP of the raspberry pi
TCP_PORT = 5005
BUFFER_SIZE = 1024

os.chdir(directory)



############### initialize and start TCP ###############
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
########################################################

def receivedata():
    datapoints = "" #A string that holds the received data

    s.listen(1)
    
    conn, addr = s.accept() #accept a connection and store it's address
    print ('Connection address:', addr)

    dataAmount = int(conn.recv(BUFFER_SIZE)) #read the first piece of data containing a number which contains the amount of data that is coming
    print(dataAmount)
    
    loggerID = ""
    loggerID = int(conn.recv(BUFFER_SIZE)) #read the second piece of data containing the id of the datalogger
    print(loggerID)

    counter = 0 #a variable that stores how many packets are received
    while 1:
        counter += 1

        if counter > dataAmount: #if all the data is received
            print("all data received sending back a conformation")
            conn.send("y".encode('utf-8')) #send a conformation back
            break  #stop the loop

        data = conn.recv(BUFFER_SIZE) #save the received data
        if not data: break #if nothing was received stop the loop

        datapoints += str(data) + "\n" #add the data to the datapoints variable


    print('data received')

    conn.close()    # close the connection
    #s.close()       #

    log = "newlog\n" #create a new string for data that will be written to a file and add a newlog indication
    
    counter = 0
    for i in range(0,len(datapoints)): #for each character in the received data
        if ord(datapoints[i]) > 47 and ord(datapoints[i]) < 58: #if the character is a number
            log += datapoints[i] #add the character to log
            if counter % 10 == 9:#if a new datapoint is about to begin
                log += "\n"      #add an enter
            counter += 1;
    print(log)
    
    os.chdir(directory + "logs") #go to the logs directory
   
    f = open(str(loggerID),"a")  #open a file with the loggerID as name in append mode
    f.write(log) #append log to the file
    f.close()    #close the file
    
while 1:
    receivedata() #keep receiving data
