#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pylab as plt
import numpy as np
import scipy

from simMotor import Simulated_motor
import matplotlib.pyplot as plt
import time
import sys


def main(args):
    input_vel = int(sys.argv[1])    #Max velocity for Engine
    input_sens = float(sys.argv[2]) #Sensibility of Engine
    input_inertia = float(sys.argv[3]) #Inertia of Engine
    input_wait = int(sys.argv[4])      #Wait time between each measured velocity 
    
    motor = Simulated_motor(input_vel, input_sens, input_inertia)
    #Static behavior
    velStatic = staticTest(motor)
    #Restart motor speed to 0
    motor.stop()
    #Dynamic behavior
    velDynamic, torqueDynamic = dynamicTest(motor, input_wait)

    graph(velStatic, velDynamic, torqueDynamic)
    return 0

#Returns the velocity of the motor for each statically tested torque from 0 to 255
def staticTest(motor):
    velStatic = []
    #Static behavior
    for torque in range(256):
        velStatic.append(motor.getVelocityStatic(torque))
    return velStatic

#Returns the velocity of the motor for each tested torque from 0 to 255, waiting 'wait'
#seconds between each torque measure and modification.
def dynamicTest(motor, wait):
    velDynamic = []
    torqueDynamic = []

    #Dynamic behavior
    for t in range(256):
        time.sleep(wait)
        if(t > 60):
            torque = 20
        else:
            torque = 50

        velDynamic.append(motor.getVelocity(torque))
        torqueDynamic.append(torque)
    return (velDynamic, torqueDynamic)

def graph(velStatic, velDynamic, torqueDynamic):
    #Graphs
    t = range(256)
    #Static graph
    plt.subplot(2,1,1)
    plt.title("Motor estático: Velocidad vs Torque")
    plt.xlabel("Torque (0 - 255)")
    plt.ylabel("VelocidadS (0-255)")
    plt.plot(t, velStatic, 'r')

    #Dynamic graph
    plt.subplot(2,1,2)
    plt.plot(t, velDynamic, 'r')
    plt.plot(t, torqueDynamic, 'y')

    plt.title("Motor dinámico: Velocidad vs Tiempo")
    plt.xlabel("Tiempo (en delta_t)")
    plt.ylabel("Velocidad (0-255)")
    plt.tight_layout()
    plt.legend(['Speed', 'Torque'])
    
    plt.show()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
