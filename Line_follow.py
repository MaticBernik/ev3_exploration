#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1,INPUT_2,INPUT_3
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.button import Button
import Sensor
import math
# ------Input--------
class Line_follow():
    def __init__(self):
        self.status=False
        self.power = 30
        self.target = 55
        self.kp = float(0.5) # Proportional gain, Start value 1 0.65
        self.kd = 0.5       # Derivative gain, Start value 0
        self.ki = 0#float(0.6) # Integral gain, Start value 0 0.02
        self.direction = -1
        self.minRef = 25
        self.maxRef = 45
        self.sensor = Sensor.Sensor()
        self.ticks=0
        # -------------------
        
        # Connect two large motors on output ports B and C and check that
        # the device is connected using the 'connected' property.
        self.left_motor = LargeMotor(OUTPUT_D); # assert left_motor.connected
        self.right_motor = LargeMotor(OUTPUT_A); #assert right_motor.connected
        # One left and one right motor should be connected
        
        # Connect color and touch sensors and check that they
        # are connected.
        # ir = InfraredSensor(); 	assert ir.connected
        #ts = TouchSensor();    	assert ts.connected
        self.col= ColorSensor(INPUT_1); 	#assert col.connected
        self.col_2= ColorSensor(INPUT_2); #	assert col.connected

        # Change color sensor mode
        self.col.mode = 'COL-REFLECT'
        self.col_2.mode = 'COL-REFLECT'
 
        
        # Adding button so it would be possible to break the loop using
        # one of the buttons on the brick
        self.btn = Button()
    def status_true(self):
        self.status=True
    def status_false(self):
        self.status=False
        
    def steering(self,course):
            """
        	Computes how fast each motor in a pair should turn to achieve the
        	specified steering.
        	Input:
        		course [-100, 100]:
        		* -100 means turn left as fast as possible,
        		*  0   means drive in a straight line, and
        		*  100  means turn right as fast as possible.
        		* If >100 pr = -power
        		* If <100 pl = power        
        	power: the power that should be applied to the outmost motor (the one
        		rotating faster). The power of the other motor will be computed
        		automatically.
        	Output:
        		a tuple of power values for a pair of motors.
        	Example:
        		for (motor, power) in zip((left_motor, right_motor), steering(50, 90)):
        			motor.run_forever(speed_sp=power)
            """
            power_left = power_right = self.power
            s = (50 - abs(float(course))) / 50
            if course >= 0:
                power_right *= s
                if course > 100:
                    power_right = - self.power
            else:
                power_left *= s
                if course < -100:
                    power_left = - self.power
            return (int(power_left), int(power_right))

    def run(self):
            """
        	PID controlled line follower algoritm used to calculate left and right motor power.
        	Input:
        		power. Max motor power on any of the motors
        		target. Normalized target value.
        		kp. Proportional gain
        		ki. Integral gain
        		kd. Derivative gain
        		direction. 1 or -1 depending on the direction the robot should steer
        		minRef. Min reflecting value of floor or line
        		maxRef. Max reflecting value of floor or line 
            """
            lastError = error = integral = 0
            self.left_motor.run_direct()
            self.right_motor.run_direct()
            
            old_ticks=(self.left_motor.position+self.right_motor.position)/2 # old ticks
            while not self.status:
                
                self.ticks=((self.left_motor.position+self.right_motor.position)/2)-old_ticks #driven ticks
                if self.sensor.measure_distance()<20: # measure distance detect robot
                    self.status_true()
                    print('Breaking loop')
                    self.left_motor.stop()
                    self.right_motor.stop()
                    break
                #calculate the error from the values
                #calculate the error for the I,D,P ->define the course
                refRead = self.col.value()+2
                refRead_2 = self.col_2.value()
              
                error = -(refRead - refRead_2) 
                derivative = error - lastError
                lastError = error
                integral = float(0.5) * integral + error
                course = (self.kp * error + self.kd * derivative +self.ki * integral) * self.direction
                #
                for (motor, pow) in zip((self.left_motor, self.right_motor), self.steering(course)):
                    motor.duty_cycle_sp = pow
                sleep(0.01) # Aprox 100 Hz
        
        #run(power, target, kp, kd, ki, direction, minRef, maxRef)
        
        # Stop the motors before exiting.
            print('Stopping motors')
            self.left_motor.stop()
            self.right_motor.stop()
