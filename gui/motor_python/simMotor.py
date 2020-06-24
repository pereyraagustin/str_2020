#!/usr/bin/python3
from motor import Motor
import math
import time


"""

v(t+1) = (vel - v(t)) / inertia + v(t).
Where vel  = self.vMax * (1 - math.exp(-(torque*self.sens)) ),

"""


class Simulated_motor(Motor):
    """Class that partially implements the :interface:`Motor` to simulate a motor behavior.

    :param vMax: The maximum physical speed that the motor is able to reach
    :type vMax: number
    :param sens: The sensibility of the motor
    :type sens: number
    """
    def __init__(self, vMax, sens, inertia):
        """Constructor method
        """
        super().__init__(vMax, sens)
        self.inertia = inertia
        self.current_v = 0  #Starts with 0
        
    def getVelocity(self, torque):
        """Get the speed of the motor given the specified torque.

        :param torque: The torque with which we want to measure the speed
        :type torque: number
        :return: The current speed given the applied torque
        :rtype: number
        """
        vel = self.vMax * (1 - math.exp(-torque*self.sens) ) 
        self.current_v = (vel - self.current_v) / self.inertia + self.current_v
        return self.current_v

    def getVelocityStatic(self, torque):
        """Get the speed of the motor as a static behavior (ignoring the current speed) given the
        specified torque.

        :param torque: The torque with which we want to measure the speed
        :type torque: number
        :return: The current speed given the applied torque
        :rtype: number
        """
        return self.vMax * (1 - math.exp(-torque*self.sens) ) 
        
    def stop(self):
        """Stop the motor, set it current speed to 0.
        """
        self.current_v = 0















