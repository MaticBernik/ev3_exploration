#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:42:14 2020

@author: gideon
"""
from time import sleep,process_time
from ev3dev2.sensor import INPUT_1,INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
import Drive
import math


import Line_follow
from threading import Thread
"""
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Instructions")

def on_message(client, userdata, msg):
    if msg.payload.decode() == "left":
        return 0
    if msg.payload.decode() == "forward":
        return 1
    if msg.payload.decode() == "right":
        return 2
  
    #client.disconnect()

def instructions(client, userdata, msg):
    print("Instruction:"+str(msg.payload))
    """
class cross():
    def __init__(self,color_1,color_2,follow,drive):
        self.color1=color_1
        self.color2=color_2
        #self.thread = t
        self.follow = follow
        self.drive=drive
        self.state=False
        self.state_cross=False
        self.stop =False
        self.right=False
        self.left=False
        self.forward=False
        self.dead_end=False
        self.goal=False
    def reset_direction(self):
        self.right=False
        self.left=False
        self.forward=False
        self.dead_end=False
    def state_true(self):
        self.state=True
    def state_false(self):
        self.state=False
    def state_cross_true(self):
        self.state_cross=True
    def state_cross_false(self):
        self.state_cross=False
    def cross_test(self):
        start_time=start_time2=start_time3=process_time()
        self.state=True
        while self.state:
            #---------------------
            #missing stop function and reading
            print('Color1:',self.color1.value()+2)
            print('Color2:',self.color2.value())
            
            #-------------------------
            if self.color2.value()<34:
                
                start_time=process_time()
                #print(self.color1.value())
            #print('Starttime_1:',(process_time()-start_time))
            if (process_time()-start_time)>0.09:
                print('Color1:',(self.color1.value()+2))
                print('Color2:',self.color2.value())
                self.follow.status_true()
                print('Right cross')
                #print('Time',(process_time()-start_time2))
                self.right=True
                if (process_time()-start_time2)>0.1:
                    print('Left cross')
                    self.left=True
                self.drive.forward()
                sleep(1)
                if (self.color1.value()+2)>30 or self.color2.value()>30:
                    print('Straight aswell')
                    self.forward=True
                else:
                    print('not Straight')
                
                #self.thread.stop()
                self.state_cross=True
                
                break
            if (self.color1.value()+2)<34:
                start_time2=process_time()
                #print('color2:'self.color2.value())
            #print('Starttime_2:',(process_time()-start_time2))
            if (process_time()-start_time2)>0.09:
                print('Color1:',(self.color1.value()+2))
                print('Color2:',self.color2.value())
                self.follow.status_true()
                print('Left cross')
                self.left=True
                self.drive.forward()
                sleep(1)
                if (process_time()-start_time)>0.1:
                    print('Right cross')
                    self.right=True
                if (self.color1.value()+2)>30 or self.color2.value()>30:
                    print('Straight aswell')
                    self.forward=True
                else:
                    print('not Straight')
                
                #self.thread.stop()
                self.state_cross=True
                break
            if self.follow.status == True:
                print('See a Robot or the end')
                break
            if self.stop==True:
                self.state=False
                self.follow.status_true()
                break
            if (self.color1.value()+2)>60 and self.color2.value()>60:
                self.state_cross=True
                self.follow.status_true()
                self.goal=True
                break
            if (self.color1.value()+2)>23 and self.color2.value()>23:
                start_time3=process_time()
            if (process_time()-start_time3)>0.5:
                    print('Dead End')
                    self.state_cross=True
                    self.follow.status_true()
                    self.dead_end=True
                    break
                    #----------------------------
                    #implement dead end state
        #--------------------------------
            
    
if __name__ == "__main__":
    #Init:
    drive=Drive.Drive(20)
    color = ColorSensor(INPUT_1)

    color.mode = 'COL-REFLECT'
    color2 = ColorSensor(INPUT_2)

    color2.mode = 'COL-REFLECT'
    
   
    follow=Line_follow.Line_follow()
    cross_run=cross(color,color2,follow,drive)
    sound = Sound()
    """
    client = mqtt.Client()
    client.connect("192.168.44.201",1883,60)
    client.on_connect = on_connect
"""
    #start first run
    follow.status_false()
    t = Thread(target=follow.run)
    t.start()  
    sleep(1.5)
    t_2 = Thread(target=cross_run.cross_test)
    t_2.start()
    while True:
        if cross_run.stop==False:
            if cross_run.state_cross==True:
                """
                client.publish("Obstacle/Collision",'right');
                client.loop();
                client.on_message = on_message
                """
                t.join()
                t_2.join()
                print('Ticks:',follow.ticks)
                distance=follow.ticks *((math.pi*(70/1000))/360)                               #distance in m
                print('distance:',distance)
                message_send=""
                print(message_send)
                if cross_run.dead_end==True:
                    message_send+="d"
                if cross_run.left==True:
                    message_send+="l"
                if cross_run.forward==True:
                    message_send+="f"
                if cross_run.right==True:
                    message_send+="r"
                print(message_send)
                
                """
                if client.on_message == 0:
                    drive.backward()
                    drive.left()
                elif client.on_message == 1:
                    drive.forward()
                elif client.on_message == 2:
                    drive.backward()
                    drive.right()
                """
                if cross_run.goal==True:
                    sound.speak('yeah found the end')
                    drive.right()
                    drive.right()
                    drive.right()
                    drive.right()
                    break
                elif cross_run.left==True:
                    drive.backward()
                    drive.left()  
                elif cross_run.right==True:
                    drive.backward()
                    drive.right()
                elif cross_run.dead_end==True:
                    drive.backward()
                    drive.right()
                    drive.right()
                cross_run.reset_direction()
                print('cross')
                cross_run.state_cross_false()
                cross_run.state_false()
            #
            else:
                
                if cross_run.state == False:
                    follow.status_false()
                    t = Thread(target=follow.run)
                    t.start()
            
                    print('start thread_2')    
                    sleep(1.0)
                    t_2 = Thread(target=cross_run.cross_test)
                    t_2.start()
        else:
            print('hello')
            break
            #-----------------
            
            #read the stop again and if the master say go run again and change the state
            
            #------------
        
            
       
    
