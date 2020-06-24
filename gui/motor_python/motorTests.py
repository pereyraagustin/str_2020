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
    """Function that runs the static and dynamic tests of the simulated motor.

    :param args: The parameters of the test, as:
        1: Maximum speed of engine
        2: Sensibility of engine
        3: Inertia of engine
        4: The time to wait between each measured speed
    :type args: str
    """
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

def staticTest(motor):
    """Returns the velocity of the motor for each statically tested torque from 0 to 255.

    :param motor: The motor to test
    :type motor: class: `Simulated_motor`
    :return: An array of the measured static speeds
    :rtype: list"""
    velStatic = []
    #Static behavior
    for torque in range(256):
        velStatic.append(motor.getVelocityStatic(torque))
    return velStatic

def dynamicTest(motor, wait):
    """Returns the velocity of the motor for each tested torque from 0 to 255, waiting 'wait'
    seconds between each torque measure and modification.

    :param wait: Time in seconds to wait between each measure
    :type wait: number
    :return: Two lists, of the measures of the dynamic speed and the applied torque for each of
    them, in order
    :rtype: tuple
    """
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
    """Generate and show the graph of the dynamic and static behavior of the motor.

    :param velStatic: The list of the static measured speeds
    :type velStatic: tuple or list
    :param velDynamic: The list of the dynamically measured speeds
    :type velDynamic: tuple or list
    :param torqueDynamic: The torque used at the dynamic measures
    :type torqueDynamic: tuple or list
    """
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
