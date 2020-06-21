import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Sliders(Gtk.Frame):
    """Class that creates the four sliders needed to control the PID variables p (proportional),
    i (integral), d (derivative), and v (the desired speed)."""
    def __init__(self):
        super(Sliders, self).__init__(
            label = "Control")
        
        #self.set_size_request(200, 150) #Not needed
        
        grid = Gtk.Grid(
                    margin = 4)	
        # TODO: Make it adaptative
        grid.set_column_spacing(23)
        self.scales = {}
        for x, (ref, vmin, vmax, step, label, hasbtn) in enumerate((
                    ("p", 0, 5, 0.001, "Kp", False),
                    ("i", 0, 5, 0.0001, "Ki", False),
                    ("d", 0, 5, 0.001, "Kd", False),
                    ("v", 0, 255, 1, "Speed", False))):
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

    def set_observer(self, watch_slider, slider):
        """Set the observer method to watch the specified slider.

        :param watch_slider: The function to pass the slider and the slider name so it keeps
        track of it. It is expected to receive two parameters, in the order: (slider, slider_name)
        :type watch_slider: function
        :param slider: The name of the slider to observe
        :type slider: str"""
        watch_slider(self.scales[slider], slider)