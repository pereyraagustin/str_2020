#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  interfaz.jpeg
#
#  Copyright 2020 Unknown <raiz@pc-piola>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from utils.Connection import Connection
from utils.Client import Client
from utils.SpeedObserver import SpeedObserver
from components.Graphics import Graphics
from components.MainWindow import MainWindow
from components.Sliders import Sliders
from components.InfoLabels import InfoLabels
from components.Plot import Plot
from datetime import datetime
import logging
import re

def get_params(argv):
    """Method that translates the expected command line parameters to a dictionary

    :param argv: The command line parameters
    :type argv: list
    :return: A dictionary containing the command line parameters that were passed
    :rtype: dictionary or None if there were not parameters found
    """
    argv_string = ' '.join(argv)    #   Get as one string to match pattern
    #   Get logging arguments and other through command line arguments as dictionary.
    #   The '(?P<>)' part is for named groups, see: https://docs.python.org/3/howto/regex.html
    log_pattern = r"--log=(?P<log_level>DEBUG\b|INFO\b|WARNING\b|ERROR\b|CRITICAL\b)"
    kp_pattern = r"--kp=(?P<kp>[0-9]+.?[0-9]*)"
    ki_pattern = r"--ki=(?P<ki>[0-9]+.?[0-9]*)"
    kd_pattern = r"--kd=(?P<kd>[0-9]+.?[0-9]*)"
    speed_pattern = r"--speed=(?P<speed>[0-9]+)" #   Only integers

    params_dict = None
    for pattern, name in ([log_pattern, "log_level"],   #   Carefull! If names change, patterns will have to change
                    [kp_pattern, "kp"],
                    [ki_pattern, "ki"],
                    [kd_pattern, "kd"],
                    [speed_pattern, "speed"]):
        match = re.search(pattern, argv_string)
        if match:
            if params_dict is None:
                params_dict = {}
                params_dict[name] = match.groupdict()[name]
            else:
                params_dict[name] = match.groupdict()[name]
            
    return params_dict

def main(argv):
    """Function that creates the interface in charge of managing the engine that is connected
    through a socket at localhost:8080.

    :param argv: The command line arguments to be processes. It expects:
        --log=LOG_LEVEL
            where LOG_LEVEL can be DEBUG, INFO, WARNING, ERROR or CRITICAL, upper or lower case. If not
            passed, the default value is WARNING.
        --kp=value
        --ki=value
        --kd=value
        --speed=value
            If kp, ki, kd, and/or speed are not passed, their default value is 0
    :type argv: str
    """
    params_dict = get_params(argv)
    #   Set defaults or passed values
    if (params_dict == None):
        log_level = "WARNING"
        kp_init = 0.0
        ki_init = 0.0
        kd_init = 0.0
        speed_init = 0
    else:
        if 'log_level' in params_dict:
            log_level = params_dict['log_level'].upper()
        else:
            log_level = "WARNING"
        if 'kp' in params_dict:
            kp_init = float(params_dict['kp'])
        else:
            kp_init = 0.0
        if 'ki' in params_dict:
            ki_init = float(params_dict['ki'])
        else:
            ki_init = 0.0
        if 'kd' in params_dict:
            kd_init = float(params_dict['kd'])
        else:
            kd_init = 0.0
        if 'speed' in params_dict:
            speed_init = int(params_dict['speed'])
        else:
            speed_init = 0
    #   Set logging config
    logging.basicConfig(filename="logs" ,level=log_level)
    logging.info("Starting program at time: {}".format(datetime.now()))
    #   Create socket client and inject to connection
    client = Client('localhost', 8080)
    connection = Connection(client)
    #   Create sliders and set them to be obversverd by connection
    sliders = Sliders()
    sliders.set_observer(connection.watch_slider, 'p')
    sliders.set_observer(connection.watch_slider, 'i')
    sliders.set_observer(connection.watch_slider, 'd')
    sliders.set_observer(connection.watch_slider, 'v')
    #   Set the sliders to the initial values
    sliders.scales['p'].set_value(kp_init)
    sliders.scales['i'].set_value(ki_init)
    sliders.scales['d'].set_value(kd_init)
    sliders.scales['v'].set_value(speed_init)
    #   Create and set speed observer
    speed_observer = SpeedObserver()
    sliders.set_observer(speed_observer.watch_slider, 'v')
    #   Create graph and get canvas
    graphics = Graphics(connection, speed_observer)
    graphics.create_animation()
    canvas = graphics.canvas
    canvas.set_size_request(800, 600)
    #   Create plot of GUI with animated graph
    plot = Plot(canvas)
    #   Create labels with current speed and torque
    labels = InfoLabels()
    #   Create Main Window
    mainwdw = MainWindow(plot, sliders, labels, connection)
    mainwdw.run()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
