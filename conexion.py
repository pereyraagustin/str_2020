import sys
sys.path.insert(1, './motor')
from simMotor import Simulated_motor

#   Class that intermediates between GUI and Motor
class Conexion():
    def __init__(self, motor = None):
        if motor is not None:
            self.motor = motor
        else:
            self.motor = Simulated_motor(
                255, 0.016, 15
            )
        self.value_slider = [0, 0]
    
    #   Sets slider to observe
    def watch_slider (self, slider):
        self.slider = slider
                
    #   Returns value of observed slider
    def get_scale (self):
        torque = self.slider.get_value()
        vel = self.motor.getVelocity(torque)
        return (vel, torque)