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

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas, GLib
from conexion import Conexion
from client import Client
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib import animation

'''
Class that creates labels that contain data of current torque and speed,
to show throught GUI.
This data is updated manually throught update(self) method.
'''
class InfoLabels(Gtk.Frame):
    def __init__(self):
        super(InfoLabels, self).__init__(
            label = "Estado Actual")

        grid = Gtk.Grid(
                    margin = 4)

        # TODO: Make it adaptative
        grid.set_column_spacing(9)

        # Variables to store current speed and torque
        self.cSpeed = 0
        self.cTorque = 0

        # Set labels
        self.labelSpeed = Gtk.Label(label = "Velocidad")
        self.labelTorque = Gtk.Label(label = "Torque")
        self.labelValueSpeed = Gtk.Label(label = "{:d}".format(self.cSpeed))
        self.labelValueTorque = Gtk.Label(label = "{:d}".format(self.cTorque))

        # Justify
        self.labelSpeed.set_justify(Gtk.Justification.LEFT)
        self.labelTorque.set_justify(Gtk.Justification.LEFT)
        self.labelValueSpeed.set_justify(Gtk.Justification.RIGHT)
        self.labelValueTorque.set_justify(Gtk.Justification.RIGHT)
        # Align
        # To the right
        self.labelSpeed.set_halign(Gtk.Align.START)
        self.labelTorque.set_halign(Gtk.Align.START)
        # To the left
        self.labelValueSpeed.set_halign(Gtk.Align.END)
        self.labelValueTorque.set_halign(Gtk.Align.END)

        # Set into grid
        for y, labelPair in enumerate(((self.labelSpeed, self.labelValueSpeed),
                                        (self.labelTorque, self.labelValueTorque))):
            for x, label in enumerate(labelPair):
                grid.attach(label, x, y, 1, 1)

        self.add(grid)

    # Method to manually update speed and torque data
    def update(self, cSpeed, cTorque):
        self.cSpeed = cSpeed
        self.cTorque = cTorque
        self.labelValueSpeed.set_label("{:d}".format(self.cSpeed))
        self.labelValueTorque.set_label("{:d}".format(self.cTorque))
        


class Sliders(Gtk.Frame):
    def __init__(self):
        super(Sliders, self).__init__(
            label = "Control")
        
        #self.set_size_request(200, 150) #No es necesaria
        
        grid = Gtk.Grid(
                    margin = 4)	
        # TODO: Make it adaptative
        grid.set_column_spacing(23)
        self.scales = {}
        for x, (ref, vmin, vmax, step, label, hasbtn) in enumerate((
                    ("p", 0, 5, 0.001, "Kp", False),
                    ("i", 0, 5, 0.001, "Ki", False),
                    ("d", 0, 5, 0.001, "Kd", False),
                    ("v", 0, 255, 1, "Vel", False))):
            self.scales[ref] = Gtk.Scale.new_with_range(
                            Gtk.Orientation.VERTICAL,
                            vmin,#Min
                            vmax,#Max
                            step)#Paso				
            self.scales[ref].set_vexpand(True)
            self.scales[ref].set_inverted(True)
            grid.attach(self.scales[ref], x, 0, 1, 1)
            grid.attach(Gtk.Label(label = label), x, 1, 1, 1)
            
            if hasbtn:
                btn = Gtk.ToggleButton(label = "No")
                grid.attach(btn, x, 2, 1, 1)            
        self.add(grid)

    #   Method that sets an observer function to
    #   the specified slider, specified by name
    def set_observer(self, watch_slider, slider):
        watch_slider(self.scales[slider], slider)

class Plot(Gtk.Frame):
    def __init__(self, canvas):
        super(Plot, self).__init__(
            label = "Graph")
        
        scroller = Gtk.ScrolledWindow(
                    hexpand = True)
        scroller.add(canvas)
        
        self.add(scroller)

class MainWindow(Gtk.Window):
    def __init__(self, canvas, sliders, labels, conexion):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)

        #   Variables for updating data
        self.interval = 500
        self.conexion = conexion

        mainGrid = Gtk.Grid()
        managementGrid = Gtk.Grid()
        self.plot = Plot(canvas)
        self.sliders = sliders
        self.labels = labels
        managementGrid.attach(self.sliders, 0, 0, 1, 1)
        managementGrid.attach(self.labels, 0, 1, 1, 1)
        mainGrid.attach(managementGrid, 0, 0, 1, 1)
        mainGrid.attach(self.plot, 1, 0, 1, 1)

        #Meterlo adentro de la ventana
        self.add(mainGrid)

        #   Update each N miliseconds
        GLib.timeout_add(self.interval, self.update_labels)

        self.show_all()
	
    def run(self):
        Gtk.main()

    def update_labels(self):
        cSpeed, cTorque = self.conexion.read_last_data()   #   Just read the last data that was gotten, don't update
        self.labels.update(cSpeed, cTorque)
        return True

class Graphics():	

    def __init__(self, conexion):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axis = self.fig.add_subplot()
        self.canvas = FigureCanvas(self.fig)
        self.conexion = conexion
        #   Variable that stores the time duration of intervals for animation in miliseconds
        self.time_interval = 50
        #   Variable that stores how many seconds we are showing in animation
        self.time_show = 10

    def create_animation(self):
        self.anim = animation.FuncAnimation(self.fig, self.animate, init_func = self.init,
            interval = self.time_interval)

    def init(self):
        self.velDynamic = []
        self.torqueDynamic = []
        self.time = []
        #   Only show delta time of self.time_show seconds
        for t in range(0, self.time_show * 1000 // self.time_interval):
            self.time.append(t * self.time_interval / 1000)
            self.velDynamic.append(0)   #   Initiate with 0s
            self.torqueDynamic.append(0)    #   Initiate with 0s

    def animate(self, i):
        #   Clear animation axis
        self.axis.clear()
        #   Rewrite axis
        self.axis.set_title("Motor dinámico: Velocidad vs Tiempo")
        self.axis.set_xlabel("Tiempo (delta_t en segundos)")
        self.axis.set_ylabel("Velocidad (0-255)")
        self.axis.set_ylim([-1, 290])    #   Set Y limits between 0 and 255
                                         #   In this case, we use -1 to be able to visualize the bottom
                                         #   and 290 to let the legend not to bother the lines
        #   Get data
        vel, torque = self.conexion.get_updated_data()
        #   Only keep self.time_show seconds window of data
        #   Overwrite last value
        self.velDynamic.pop(0)
        self.torqueDynamic.pop(0)
        self.velDynamic.append(vel)
        self.torqueDynamic.append(torque)
        self.axis.plot(self.time, self.velDynamic, 'r')
        self.axis.plot(self.time, self.torqueDynamic, 'y')
        #   Set legends here because before plotting doesn't work
        self.axis.legend(['Speed', 'Torque'], loc='upper right')

def main(args):
    #   Create socket client and inject to conexion
    client = Client('localhost', 8080)
    conexion = Conexion(client)
    #   Create sliders and set them to be obversverd by conexion
    sliders = Sliders()
    sliders.set_observer(conexion.watch_slider, 'p')
    sliders.set_observer(conexion.watch_slider, 'i')
    sliders.set_observer(conexion.watch_slider, 'd')
    sliders.set_observer(conexion.watch_slider, 'v')
    #   Create graph and get canvas
    graphics = Graphics(conexion)
    graphics.create_animation()
    canvas = graphics.canvas
    canvas.set_size_request(800, 600)
    #   Create labels with current speed and torque
    labels = InfoLabels()
    #   Create Main Window
    mainwdw = MainWindow(canvas, sliders, labels, conexion)
    mainwdw.run()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
