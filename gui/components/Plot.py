import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Plot(Gtk.Frame):
    """Class that creates a :class:`Gtk.Frame` with the passed canvas.

    :param canvas: The canvas with the figure to show at the plot
    :type canvas: class: `matplotlib.backends.backend_gtk3agg.FigureCanvasGTK3Agg`"""
    def __init__(self, canvas):
        super(Plot, self).__init__(
            label = "Graph")
        
        scroller = Gtk.ScrolledWindow(
                    hexpand = True)
        scroller.add(canvas)
        
        self.add(scroller)