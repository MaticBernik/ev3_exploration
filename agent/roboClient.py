#!/usr/bin python3

import paho.mqtt.client as mqtt


class RoboClient:
    
    def check_if_recipient(self,msg):
        #This is the method that (given a message), check if it is itended for
        #the current agent
        if msg.startswith('['):
            recipient_list=msg[msg.index('[')+1:msg.index(']')]
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
        self.client.subscribe("colision")
    
    
    def check_colision() -> bool:
        '''Here implement reading from UZ sensor and return True
        if there is Robot detected and False otherwise'''
            
    def adjust_course():
        '''Read color/lumen sensors and check the current path location/situation'''        
    
    def callback_junction(self,client, userdata, msg):
        #Ofc note the client who is sending the junction message..
        if not check_if_recipient(msg):
            return
        content = msg.split()
        if content[0]=='turn':
            #direction contains 'L' for left turn and 'R' for right turn
            direction = content[0]
        elif content[0]=='crossection':
            #robot got to the next crossection.
            #Following are the leters denoting possible directions 'L','F','R'
            paths = content[1:]
        elif msg.startswith('endOfTheLine'):
            #self explanatory I think
        else:
            print('***ERROR: Invalid JUNCTION message format')
            
    def callback_colision(client,userdata,msg):
        #Check who is the client Robot who detected the colision,
        #and find which robot is at the same junction.
        #Send stop signal for one robot (for few seconds) and let otherone pass            
        
            
    def __init__(self,broker_address):
        self.client = mqtt.Client()
        self.client.connect(broker_address,1883,60)
        print("***Connection to message broker server established!")
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.message_callback_add("junction",callback_junction)
        self.client.message_callback_add("colision",callback_colision)
        self.client.message_callback_add("goal",callback_goal)
        self.client.message_callback_add("instructions",instructions)
    
    client.loop_forever()
    client.publish("topic/test", "Hello world!")
    client.disconnect()