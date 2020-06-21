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

from Connection import Connection
from Client import Client
from gui.Graphics import Graphics
from gui.MainWindow import MainWindow
from gui.Sliders import Sliders
from gui.InfoLabels import InfoLabels
from gui.Plot import Plot

def main():
    """Function that creates the interface in charge of managing the engine that is connected
    through a socket at localhost:8080.
    """
    #   Create socket client and inject to connection
    client = Client('localhost', 8080)
    connection = Connection(client)
    #   Create sliders and set them to be obversverd by connection
    sliders = Sliders()
    sliders.set_observer(connection.watch_slider, 'p')
    sliders.set_observer(connection.watch_slider, 'i')
    sliders.set_observer(connection.watch_slider, 'd')
    sliders.set_observer(connection.watch_slider, 'v')
    #   Create graph and get canvas
    graphics = Graphics(connection)
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
    sys.exit(main())
