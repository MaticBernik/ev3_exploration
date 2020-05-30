#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sensor.lego import GyroSensor
import Sensor
import math

class Drive:
    def __init__(self,speed):
         self.speed = speed
      
         self.both = MoveTank(OUTPUT_A, OUTPUT_D)
         self.drive_right = LargeMotor(OUTPUT_A)
         self.drive_left = LargeMotor(OUTPUT_D)
     
         

    def right(self):
        #sensor = Sensor.Sensor()
       
     
   
        self.drive_right.on_for_degrees(SpeedPercent(self.speed),160)
        self.drive_left.on_for_degrees(SpeedPercent(self.speed),-160)
     
        #self.drive_right.stop()
        #self.drive_left.stop()
    def left(self):
 
        self.drive_left.on_for_degrees(SpeedPercent(self.speed),+160)
        self.drive_right.on_for_degrees(SpeedPercent(self.speed),-160)
        
   
    def forward(self):
        self.both.on_for_degrees(SpeedPercent(self.speed),SpeedPercent(self.speed),60)
    def backward(self):
        self.both.on_for_degrees(SpeedPercent(self.speed),SpeedPercent(self.speed),-60)
        
    



