#!/usr/bin python3

import paho.mqtt.client as mqtt
#Lets say that if there is an 'array' at the beginning of the string [],
#it will include the list of the actual recipients

class RoboServer:                      
    
    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe("connection")
    
               
    def check_if_recipient(self,msg):
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
    
    def callback_junction(self,client, userdata, msg):
        #Ofc note the client who is sending the junction message..
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
            pass
        else:
            print('***ERROR: Invalid JUNCTION message format')
            
    def callback_colision(self,client,userdata,msg):
        #Check who is the client Robot who detected the colision,
        #and find which robot is at the same junction.
        #Send stop signal for one robot (for few seconds) and let otherone pass 
        #Priority can be just index in the list of Robot Agents
        pass
    
    def callback_goal(self,client,userdata,msg):
        #Agent found an object.
        #Just send everyone instruction to return home
        print('Agent ',client,' found THE OBJECT! Everyone go back home!')
        self.client.publish("instruction", "exit");
                   
    def callback_connection(self,client,userdata,msg):
        #Server listens to the new agents that want to connect to the system,
        #It adds their communication handlers to the list,
        #And responds to those agents that they have been successfully registered 
        if client not in self.ROBOTS_COMMUNICATION:
            self.ROBOTS_COMMUNICATION.append(client)
        self.client.publish('[',client,'] registred')    
    
        
    def callback_instruction(self,client,userdata,msg):
        pass
            
    def __init__(self,broker_address):
        self.ROBOTS_COMMUNICATION = [] #List of Robot identifiers for communication purposes
        self.ROBOTS_LOCATIONS = {} #Key is robots ID and value is a list
                              #of directions at each consequtive crossection
        self.CROSSECTIONS = {} #dictionary of dictionaryes of distionaryes of...
        self.client = mqtt.Client()
        self.client.connect(broker_address,1883,60)
        print("***Connection to message broker server established!")
        self.client.on_connect = self.on_connect
        self.client.message_callback_add("junction",self.callback_junction)
        self.client.message_callback_add("colision",self.callback_colision)
        self.client.message_callback_add("goal",self.callback_goal)
        self.client.message_callback_add("instruction",self.callback_instruction)
        self.client.message_callback_add("connection",self.callback_connection)
        self.client.loop_forever()
        self.client.disconnect()
        
        