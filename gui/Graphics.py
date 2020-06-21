from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib import animation

class Graphics():
    """Class that dynamically updates a graph with data of the motor. It keeps the graph at the
    variable :variable:`self.canvas`.

    :param connection: A handle to the class :class:`Connection` connection object that works as
    intermediary between the engine and the GUI.
    :type connection: class:`connection`
    """
    def __init__(self, connection):
        """Constructor method"""
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axis = self.fig.add_subplot()
        self.canvas = FigureCanvas(self.fig)
        self.connection = connection
        #   Variable that stores the time duration of intervals for animation in miliseconds
        self.time_interval = 50
        #   Variable that stores how many seconds we are keeping at the graph
        self.time_show = 10
        self.vel_dynamic = []
        self.torque_dynamic = []
        self.time = []

    def create_animation(self):
        """Start animation loop to refresh graph."""
        animation.FuncAnimation(self.fig, self.animate, init_func=self.init,
                                       interval=self.time_interval)

    def init(self):
        """Set needed variables before starting to draw, such as axes length and put values to
        zero.
        """
        self.vel_dynamic = []
        self.torque_dynamic = []
        self.time = []
        #   Only show delta time of self.time_show seconds
        for delta_t in range(0, self.time_show * 1000 // self.time_interval):
            self.time.append(delta_t * self.time_interval / 1000)
            self.vel_dynamic.append(0)   #   Initiate with 0s
            self.torque_dynamic.append(0)    #   Initiate with 0s

    def animate(self, i):
        """Get new data from :variable:connection variable and re-draw graph with updated data.
        :param i: int, passed by :class:`matplotlib.animation`.
        """
        #   Clear animation axis
        self.axis.clear()
        #   Rewrite axis
        self.axis.set_title("Dynamic Motor: Speed vs Time")
        self.axis.set_xlabel("Time (delta_t in seconds)")
        self.axis.set_ylabel("Speed/Torque (0-255)")
        self.axis.set_ylim([-1, 150])    #   Set Y limits between 0 and 255
                                         #   In this case, we use -1 to be able to visualize the
                                         #   bottom.
        #   Get data
        vel, torque = self.connection.get_updated_data()
        #   Only keep self.time_show seconds window of data
        #   Overwrite last value
        self.vel_dynamic.pop(0)
        self.torque_dynamic.pop(0)
        self.vel_dynamic.append(vel)
        self.torque_dynamic.append(torque)
        self.axis.plot(self.time, self.vel_dynamic, 'r')
        self.axis.plot(self.time, self.torque_dynamic, 'y')
        #   Set legends here because before plotting doesn't work
        self.axis.legend(['Speed', 'Torque'], loc='upper right')
