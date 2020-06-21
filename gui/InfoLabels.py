import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

'''
Class that creates labels that contain data of current torque and speed,
to show throught GUI.
This data is updated manually throught update(self) method.
'''
class InfoLabels(Gtk.Frame):
    def __init__(self):
        super(InfoLabels, self).__init__(
            label = "Current State")

        grid = Gtk.Grid(
                    margin = 4)

        # TODO: Make it adaptative
        grid.set_column_spacing(9)

        # Variables to store current speed and torque
        self.cSpeed = 0
        self.cTorque = 0

        # Set labels
        self.labelSpeed = Gtk.Label(label = "Speed")
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