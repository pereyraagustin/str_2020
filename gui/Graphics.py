from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
from matplotlib import animation

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
        self.axis.set_title("Dynamic Motor: Speed vs Time")
        self.axis.set_xlabel("Time (delta_t in seconds)")
        self.axis.set_ylabel("Speed/Torque (0-255)")
        self.axis.set_ylim([-1, 150])    #   Set Y limits between 0 and 255
                                         #   In this case, we use -1 to be able to visualize the bottom
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
