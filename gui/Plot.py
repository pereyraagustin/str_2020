import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Plot(Gtk.Frame):
    def __init__(self, canvas):
        super(Plot, self).__init__(
            label = "Graph")
        
        scroller = Gtk.ScrolledWindow(
                    hexpand = True)
        scroller.add(canvas)
        
        self.add(scroller)