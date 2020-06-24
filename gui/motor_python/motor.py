#!/usr/bin/python3
from abc import ABCMeta, abstractmethod

class Motor():
    """Class that proposes an interface to manage engine torque and velocity

    :param vMax: The maximum physical speed that the motor is able to reach
    :type vMax: number
    :param sens: The sensibility of the motor
    :type sens: number
    """
    __metaclass__ = ABCMeta

    def __init__(self, vMax, sens):
        """Constructor method
        """
        self.vMax = vMax
        self.sens = sens

    @abstractmethod
    def setTorque(self, torque):
        """Set the motor torque to the specified value.

        :param torque: The torque to set the motor to
        :type torque: number
        """
        pass

    @abstractmethod
    def getVelocity(self, torque):
        """Get the speed of the motor given the specified torque.

        :param torque: The torque with which we want to measure the speed
        :type torque: number
        :return: The current speed given the applied torque
        :rtype: number
        """
        pass
        
