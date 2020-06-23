import time
import logging
from Connection import Connection
from Client import Client

class MockSliders():
    """Mock class used to mock :class:`gui.Sliders` sliders in order to make the tests without the
    GUI
    """
    def __init__(self):
        """Constructor method
        """
        self.value = 0

    def set_value(self, value):
        """Statically set the value to return with `MockSliders.get_value()`

        :param value: The value to return when the `MockSliders.get_value()` is called
        :type value: number
        """
        self.value = value

    def get_value(self):
        """Return the value established by `MockSliders.set_value(...)`

        :return: self.value or 0 if not set
        :rtype: number
        """
        return self.value

def test_steady_speed():
    """Function to test if the control algorithm is stable changing the desired speed and reading
    the current speed and torque.
    """
    #   Create socket client and inject to connection
    client = Client('localhost', 7890)
    client.connect()
    client.send("Connezioneee miaaa")
    a = 0
    while(True):
        a += 1
    """
    connection = Connection(client)
    #   Create mock sliders to control kp, ki, kd and desired_speed
    kp_slider = MockSliders()
    ki_slider = MockSliders()
    kd_slider = MockSliders()
    speed_slider = MockSliders()
    connection.watch_slider(kp_slider, 'p')
    connection.watch_slider(ki_slider, 'i')
    connection.watch_slider(kd_slider, 'd')
    connection.watch_slider(speed_slider, 'v')
    #   Set starting values
    kp = 3
    ki = 0.5
    kd = 0.35
    desired_speed = 20
    kp_slider.set_value(kp)
    ki_slider.set_value(ki)
    kd_slider.set_value(kd)
    speed_slider.set_value(desired_speed)
    #   Loop to test, steady, and increment
    stable_range = 5   #   Range of continuous speed values to consider the speed as steady
    speed_step = 20     #   Step to increment the speed
    """

def measure(connection, speed_slider, start_speed=20, stable_range=5, speed_step=20, end_speed=120, time_step=0.5):
    """Start measuring the behavior of the motor and modifying the desired speed when it reaches
    a steady speed

    :param connection: The object that keeps the connection to the motor
    :type connection: class:`Connection`
    :param speed_slider: The slider that controls the desired speed
    :type speed_slider: class: `MockSliders` or similar, that implements set_value and get_value
    methods
    :param start_speed: The initial desired speed
    :type start_speed: integer, default to 20
    :param stable_range: The range of continuous speed measures after which consider the current
    speed as stable
    :type stable_range: integer, default to 5
    :param speed_step: The step to take to increment the desired speed after it has been stadied
    :type speed_step: integer, default to 20
    :param end_speed: The last speed against which to take measures, inclusive
    :type end_speed: integer, default to 120
    :param time_step: The time in seconds to wait between measures
    :type time_step: float, default to 0.5
    :return: The measures, as a dictionary with the keys 'c_speed' (current speed), 'c_torque'
    (current torque), 'd_speed' (desired speed) and 'time' (in seconds), all of them as lists
    :rtype: dictionary"""
    desired_speed = start_speed
    measures = {"c_speed": [], "c_torque": [], "d_speed": []}
    while desired_speed <= end_speed:
        time.sleep(time_step)
        c_speed, c_torque = connection.get_updated_data()
        measures["c_speed"].append(c_speed)
        measures["c_torque"].append(c_torque)
        measures["d_speed"].append(desired_speed)
        #   Check if motor is stable
        if len(measures["c_speed"]) >= stable_range:
            temp_last_speed = measures["c_speed"][0]
            stable_seq = 0   #  Keep track of the number of continuous equal speeds
            for idx in range(1, stable_range, 1):
                last = measures["c_speed"][idx]
                logging.warning("Doubt: Should we check if steady and d_speed?")
                if last == temp_last_speed:
                    #   Count and keep going
                    stable_seq += 1
                else:
                    break
            logging.debug("At changes.py: stable_seq = {}".format(stable_seq))
            #   stable_seq == stable_range-1 -> good, because we compare between two speeds
            if stable_seq == stable_range - 1:
                #   As we have steady speed, increment it
                desired_speed += speed_step
                speed_slider.set_value(desired_speed)
    #   End while
    return measures

if __name__ == '__main__':
    import sys
    logging.basicConfig(level="INFO")
    sys.exit(test_steady_speed())