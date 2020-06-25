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
import logging
import re

def main(argv):
    """Function that creates the interface in charge of managing the engine that is connected
    through a socket at localhost:8080.

    :param argv: The command line arguments to be processes. It expects nothing or --log=LOG_LEVEL
    where LOG_LEVEL can be DEBUG, INFO, WARNING, ERROR or CRITICAL, upper or lower case. If not
    passed, the default value is WARNING
    :type argv: str
    """
    #   Get logging arguments through command line arguments as dictionary.
    #   The '(?P<>)' part is for named groups, see: https://docs.python.org/3/howto/regex.html
    log_pattern = r"--log=(?P<log_level>DEBUG\b|INFO\b|WARNING\b|ERROR\b|CRITICAL\b)"
    regex = re.compile(log_pattern, flags=re.I)
    argv_string = ' '.join(argv)    #   Get as one string to match pattern
    result = regex.search(argv_string)
    if (result == None):
        log_level = "WARNING"
    else:
        log_level = result.groupdict()['log_level'].upper()
    #   Set logging config
    logging.basicConfig(filename="logs" ,level=log_level)
    #   Create socket client and inject to connection
    client = Client('localhost', 8080)
    connection = Connection(client)
    #   Create sliders and set them to be obversverd by connection
    sliders = Sliders()
    sliders.set_observer(connection.watch_slider, 'p')
    sliders.set_observer(connection.watch_slider, 'i')
    sliders.set_observer(connection.watch_slider, 'd')
    sliders.set_observer(connection.watch_slider, 'v')
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
