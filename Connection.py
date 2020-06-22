import logging

class Connection():
    """Class that intermediates between GUI and motor through TCP socket. Be careful, as before use
    it needs sliders to be properly set.

    :param client: Socket client to connect to the motor.
    :type Client: class:`Client`
    """
    def __init__(self, client):
        """Constructor method"""
        #   Variable that points to each one of the four sliders
        #   p:  Kp, i:  Ki, d:  Kd, v:  desired speed
        self.sliders = {'p': None, 'i': None, 'd': None, 'v': None}
        #   Variables that contain current speed and velocity,
        #   modified by self.read_data
        self.cSpeed = 0
        self.cTorque = 0
        #   Set and connect socket
        #   (socket should already have defined port and host)
        self.socket_cli = client
        self.socket_cli.set_data_show(self.read_data)
        self.socket_cli.connect()

    
    #   Sets pointer to slider
    def watch_slider (self, slider, name):
        """Saves pointer to slider, under the declared name, so it will be able to read its value
        when sending data to the engine.

        :param slider: The slider to be read in future iterations. It can represent one of the four
        variables that the PID connected to the engine will use: kp, ki, kd, or desired_speed
        :type sliders: class:`gui.Sliders`
        :param name: The name of the passed slider. It can be: p, i, d or v
        :type name: str
        """
        self.sliders[name] = slider

    def read_data (self, data):
        """Called when data is received from socket. It parses and sets self.cSpeed and
        self.cTorque.

        :param data: The bytes of data read from the socket.
        :type data: bytes
        """
        logging.debug("Received data at Connection.read_data: {}".format(data))
        #   Expected format: 'int,int'.format(real_speed, real_torque)
        str_data = data.decode()
        #   TODO: Some checking for ints in range
        res = [int(s) for s in str_data.split(',', 1)]   #   Get 2 integer numbers, separated by coma without spaces
        self.cSpeed = res[0]        
        self.cTorque = res[1]

    def get_updated_data (self):
        """Send new Kp, Ki, Kd, Desired Speed through socket and get current speed and torque
        read from socket or (0, 0) if values were not initialized with it.

        :return: Tuple of (current_speed, current_torque) read from socket, or (0, 0) if nothing
        was received
        :rtype: tuple (int, int)
        """
        #   Read values from sliders
        #   TODO: Check if sliders are None
        logging.info("Connection.get_updated_data called.")
        speed = self.sliders['v'].get_value()
        kp = self.sliders['p'].get_value()
        ki = self.sliders['i'].get_value()
        kd = self.sliders['d'].get_value()
        #   Format data to send it through socket
        #   Expected format: "int, float, float, float" where
        #   float has .2 precision
        formated_data = '{:.0f},{:.2f},{:.2f},{:.2f}'.format(speed, kp, ki, kd) #   Note: Speed shouldn't be able to get float numbers, but just to be sure...
        #   Send it to PID
        self.socket_cli.send(formated_data)
        #   Return read data
        return (self.cSpeed, self.cTorque)

    def read_last_data(self):
        '''Method that returns the last read speed and torque. It is usefull if we want to read
        multiple times, that are close in time between each other (let's say around less than 50
        milisecs between reads). In that case, as reading too fast could cause trouble when
        decoding from the socket, it is better to use the method get_updated_data just once, and
        then use this method, that should have good enough data.

        :return: Tuple of (current_speed, current_torque) read from socket, or (0, 0) if nothing
        was received
        :rtype: tuple (int, int)
        '''
        return (self.cSpeed, self.cTorque)

##  Test classes
class MockSlider():
    def __init__(self, returned_value):
        self.value = returned_value
        self.send_data = None
    
    def get_value(self):
        return self.value

class MockClientSocket():
    def __init__(self):
        self.show_data_cb = None

    def connect(self):
        print('Connecting socket...')

    def send(self, msg):
        print('Sending msg: {}'.format(msg))
        self.send_data = msg

    def set_data_show(self, show_data_cb):
        self.show_data_cb = show_data_cb

    #   Simulate receiving a message from socket
    def receive_msg(self, msg):
        print('Received data: {}'.format(msg))
        print('Calling show_data_cb...')
        self.show_data_cb(msg)

def test():
    #   Create MockSlider, and MockSocketClient, pass to Connection
    #   and try to get and read torque and speed
    countError = 0
    kp = 12.3
    ki = 0.9
    kd = 3.2
    v = 234
    mockSliders = { 'kp': MockSlider(kp), 'ki': MockSlider(ki), 'kd': MockSlider(kd), 'v': MockSlider(v)}
    mockSocket = MockClientSocket()
    #   Set Connection with sliders
    connection = Connection(mockSocket)
    connection.watch_slider(mockSliders['kp'], 'p')
    connection.watch_slider(mockSliders['ki'], 'i')
    connection.watch_slider(mockSliders['kd'], 'd')
    connection.watch_slider(mockSliders['v'], 'v')
    #   Test if read_data works
    rd_string = '200,100'
    print('Testing read_data...')
    mockSocket.receive_msg(rd_string)
    if (connection.cSpeed == 200):
        if (connection.cTorque == 100):
            print('read_data test passed')
        else:
            print('ERROR: cTorque not as expected')
            countError += 1
    else:
        print('ERROR: cSpeed not as expected')
        countError += 1
    #   Test if get_updated_data sends and returns correct data
    expected_send_data = '{:.0f},{:.2f},{:.2f},{:.2f}'.format(v, kp, ki, kd)
    cSpeed, cTorque = connection.get_updated_data()
    if (mockSocket.send_data == expected_send_data):
        print('Sended data well formated')
        if (cSpeed == 200):
            if (cTorque == 100):
                print('get_updated_data test passed')
            else:
                print('ERROR: cTorque not as expected')
                countError += 1
        else:
            print('ERROR: cSpeed not as expected')
            countError += 1
    print('Tests ended, results: {} detected errors'.format(countError))

if __name__ == '__main__':
    test()




