#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#  
#  Copyright 2014 John Coppens <john@jcoppens.com>
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

import socket as skt
import sys
from gi.repository import GLib as glib
from gi.repository import GObject as gobject

HOST = "localhost"
PORT = 8080

class Client():
    """ The Client class takes care of our communications by socket.
    """
    def __init__(self, host, port):
        """ Create the socket, but do NOT connect yet. That way we
            can still change some parameters of the 
        """
        self.host = host
        self.port = port
        self.socket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
                                                   # Construir el zocalo
        self.show_status_cb = None
        self.show_data_cb = None
        self.data = '\n'

    def connect(self):
        """ Now really try to connect to the server.
            I really need to add an exception handler in case the server
            is not on-line.
        """
        self.socket.connect((HOST, PORT))
        self.socket.setblocking(False)
        self.fd = self.socket.fileno()             # Obtener el file descriptor
        self.show_status("Connected to " + self.host)
        glib.io_add_watch(self.fd, glib.IO_IN, self.process_input)
                                                   # Instalar la funcion en caso
                                                   # de datos recibidos

    def process_input(self, skt, cond):
        """ This function is called asynchronously when data is received.
        """
        msg = self.socket.recv(100)                # Recibir el mensage de la red
        self.show_data(msg)                        # Enviar los datos a show_data
        return True                                # Queremos quedar activos

    def send(self, msg):
        self.socket.send(msg)

    def show_status(self, msg):
        """ Show status changes from this class, either on the terminal,
            or else by calling the callback installed by set_status_show().
        """
        if self.show_status_cb == None:
            print("Status: ", msg)
        else:
            self.show_status_cb(msg)

    def show_data(self, msg):
        """ Show received messages, either on the terminal,
            or else by calling the callback installed by set_data_show().
        """
        if self.show_data_cb == None:
            print("Data: ", msg)
        else:
            self.show_data_cb(msg)

    def set_status_show(self, show_status_cb):
        self.show_status_cb = show_status_cb

    def set_data_show(self, show_data_cb):
        self.show_data_cb = show_data_cb


def main():
    client = Client(HOST, PORT)        # and the communications package
    client.connect()                   # and try to do the real connection
    return 0

if __name__ == '__main__':
    main()
