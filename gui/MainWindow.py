import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class MainWindow(Gtk.Window):
    def __init__(self, plot, sliders, labels, conexion):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)

        #   Variables for updating data
        self.interval = 100
        self.conexion = conexion

        mainGrid = Gtk.Grid()
        managementGrid = Gtk.Grid()
        self.plot = plot
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