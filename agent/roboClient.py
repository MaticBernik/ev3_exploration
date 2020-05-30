#!/usr/bin python3

import paho.mqtt.client as mqtt
import time


class RoboClient:
    
    def check_if_recipient(self,msg):
        #This is the method that (given a message), check if it is itended for
        #the current agent
        if msg.payload.startswith('['):
            recipient_list=msg[msg.payload.index('[')+1:msg.payload.index(']')]
            if ',' in recipient_list:
                recipient_list = recipient_list.split(',')
            else:
                recipient_list = [recipient_list]
            for recipient in recipient_list:
                if recipient == self.client:
                    return True
                else:
                    return False
        else:
            return True   
        
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("connection")
            
        
    
    def callback_junction(self,client, userdata, msg):
        #Ofc note the client who is sending the junction message..
        if not check_if_recipient(msg):
            return
        if ']' in msg.payload:
            msg.payload=msg.payload[msg.payload.index(']'):]
        content = msg.payload
        if content == 'L':
            #well ... turn left ofc..
            pass
        elif content == 'F':
            #Drive FORWAAAARRDD!!!
            pass
        elif content == 'R':
            #You've guessed it... go right
            pass
        else:
            print('***ERROR: Invalid JUNCTION message format')
     
    '''
    #Actually robot doesn't need to listen to this one...
    #He will recive actions at topic instruction    
    def callback_colision(client,userdata,msg):
        #Check who is the client Robot who detected the colision,
        #and find which robot is at the same junction.
        #Send stop signal for one robot (for few seconds) and let otherone pass            
    '''
    
    def callback_connection(self,client,userdata,msg):
        #Server listens to the new agents that want to connect to the system,
        #It adds their communication handlers to the list,
        #And responds to those agents that they have been successfully registered 
        if not check_if_recipient(msg):
            return
        if ']' in msg.payload:
            msg.payload=msg.payload[msg.payload.index(']'):]
        if msg.payload=='registered':
            self.registered_on_server = True
            
    def callback_instruction(self,client,userdata,msg):
        #Three types of instructions that it can receive:
        #exit (go out of the maze).
        #stop (stop the motors)
        #start (resume operation)
        if not check_if_recipient(msg):
            return
        if ']' in msg.payload:
            msg.payload=msg.payload[msg.payload.index(']'):]
        
        if msg.payload=='exit':
            #traverse the tree structure backwards until you reach the exit
            pass
        elif msg.payload=='stop':
            #stop the robot, until you get start signal
            self.ALLOWED_TO_MOVE = False
        elif msg.payload=='start':
            #start moving the robot again
            self.ALLOWED_TO_MOVE = True
            

        
    def __init__(self,broker_address):
        self.ALLOWED_TO_MOVE = False
        self.registred_on_server = False
        self.client = mqtt.Client()
        self.client.connect(broker_address,1883,60)
        print("***Connection to message broker server established!")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.message_callback_add("junction",self.callback_junction)
        #self.client.message_callback_add("colision",self.callback_colision)
        #self.client.message_callback_add("goal",self.callback_goal)
        self.client.message_callback_add("instruction",self.callback_instruction)
        self.client.message_callback_add("connection",self.callback_connection)
        while not self.registered_on_server:
            self.client.publish('connection','registration request')
            time.sleep(1)
            client.loop()
            print('***Client waiting for server registration confirmation')
        client.loop_forever()
        client.disconnect()