class SpeedObserver():
    """Utility class that observes the desired slider (:class:`gui.Sliders`) of speed, so it can be
    checked through it method later.

    :param speed_slider: The :class:`gui.Sliders` object that controls the desired speed
    :type speed_slider: class: `gui.Sliders`"""
    def __init__(self):
        self.speed_slider = None

    def watch_slider (self, slider, name=""):
        """Saves pointer to speed slider, so it will be able to read its value when sending data
        to whoever asks.

        :param slider: The speed slider to be read in future iterations.
        :type sliders: class:`gui.Sliders`
        :param name: The name of the passed slider. Not used here, just for compatibility reasons.
        It is assumed that it is the speed slider
        :type name: str, not needed
        """
        self.speed_slider = slider

    def get_desired_speed(self):
        """Function that observes the slider that indicates the desired speed, and returns it if called

        :return: The desired speed read from the slider
        :rtype: integer"""
        return self.speed_slider.get_value()
    