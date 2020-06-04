#!/usr/bin/python3
from motor import Motor
import math
import time


"""

v(t+1) = (vel - v(t)) / inertia + v(t).
Donde vel  = self.vMax * (1 - math.exp(-(torque*self.sens)) ),

"""


class Simulated_motor(Motor):
    def __init__(self, vMax, sens, inertia):
        super().__init__(vMax, sens)
        self.inertia = inertia
        self.current_v = 0  #Starts with 0
        
    def getVelocity(self, torque):
        vel = self.vMax * (1 - math.exp(-torque*self.sens) ) 
        self.current_v = (vel - self.current_v) / self.inertia + self.current_v
        return self.current_v

    def getVelocityStatic(self, torque):
        return self.vMax * (1 - math.exp(-torque*self.sens) ) 
        
    def stop(self):
        self.current_v = 0















