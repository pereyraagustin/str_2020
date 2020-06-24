#!/usr/bin/python3
from abc import ABCMeta, abstractmethod

class Motor():
    __metaclass__ = ABCMeta

    def __init__(self, vMax, sens):
        self.vMax = vMax
        self.sens = sens

    @abstractmethod
    def setTorque(self, torque):
        pass

    @abstractmethod
    def getVelocity(self, torque):
        pass
        
