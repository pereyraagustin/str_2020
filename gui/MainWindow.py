import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class MainWindow(Gtk.Window):
    """Class that creates the main window of the motor management application.

    :param plot: The plot frame to show
    :type plot: class: `gui.Plot`
    :param sliders: The sliders to control kp, ki, kd and desired_speed variables
    :type sliders: class: `gui.Sliders`
    :param labels: The labels that show the current state of the engine
    :type labels: class: `gui.Labels`
    :param connection: A handle to the class :class:`Connection` connection object that works as
    intermediary between the engine and the GUI.
    :type connection: class:`connection`
    """
    def __init__(self, plot, sliders, labels, connection):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_size_request(400, 300)

        #   Variables for updating data
        self.interval = 100
        self.connection = connection

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
        """Run the GUI"""
        Gtk.main()

    def update_labels(self):
        """Function that will be called periodically to update labels with current data"""
        cSpeed, cTorque = self.connection.read_last_data()   #   Just read the last data that was gotten, don't update
        self.labels.update(cSpeed, cTorque)
        return True