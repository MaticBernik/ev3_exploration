#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_2,INPUT_3
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds

class Sensor():
    def __init__(self):
         self.color = ColorSensor(INPUT_1)
         self.color_2 = ColorSensor(INPUT_2)
         #self.touch = TouchSensor(INPUT_1)
         self.ultra = UltrasonicSensor(INPUT_3)
         #self.gyro = GyroSensor(INPUT_3)
         
         print("Initialisation done")
    def calibrate(self):
        self.color.calibrate_white()
        self.gyro.mode='GYRO-ANG'
        print("not avalibe")
    def measure_color(self):
        #print("not avalibe")
        #color=self.color.rgb
        #print(color[0])
        #print(color[1])
        #print(color[2])
        return self.color.rgb
    def measure_color_2(self):
        #print("not avalibe")
        #color=self.color.rgb
        #print(color[0])
        #print(color[1])
        #print(color[2])
        return self.color_2.rgb
    def measure_distance(self):
        #print(self.ultra.distance_centimeters)
        return self.ultra.distance_centimeters_continuous
    def measure_gyro(self):
        print(self.gyro.angle)
        print(self.gyro.rate)
        print(self.gyro.angle_and_rate)
        self.gyro.angle
        return self.gyro.angle
    #def measure_touch(self):
        #print(self.ultra.distance_centimeters)
        #return self.touch.is_pressed
        
#print(ColorSensor(INPUT_1).rgb)
#sensor = Sensor()
#sensor.measure_color()
#sensor.measure_distance()
#sensor.measure_gyro()