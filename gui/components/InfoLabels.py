import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class InfoLabels(Gtk.Frame):
    '''Class that creates labels that contain data of current torque and speed, to show throught
    GUI. This data is updated manually throught update(self) method.
    '''
    def __init__(self):
        """Constructor method"""
        super(InfoLabels, self).__init__(
            label = "Current State")

        grid = Gtk.Grid(
                    margin = 4)

        # TODO: Make it adaptative
        grid.set_column_spacing(9)

        # Variables to store current speed and torque
        self.current_speed = 0
        self.current_torque = 0

        # Set labels
        self.labelSpeed = Gtk.Label(label = "Speed")
        self.labelTorque = Gtk.Label(label = "Torque")
        self.labelValueSpeed = Gtk.Label(label = "{:d}".format(self.current_speed))
        self.labelValueTorque = Gtk.Label(label = "{:d}".format(self.current_torque))

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

    def update(self, current_speed, current_torque):
        """Method to manually update speed and torque data.

        :param current_speed: The speed to set the label text to
        :type current_speed: int
        :param current_torque: The torque to set the label text to
        :type current_torque: int"""
        self.current_speed = current_speed
        self.current_torque = current_torque
        self.labelValueSpeed.set_label("{:d}".format(self.current_speed))
        self.labelValueTorque.set_label("{:d}".format(self.current_torque))