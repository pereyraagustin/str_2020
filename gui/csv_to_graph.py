import csv
import matplotlib.pyplot as plt
import re

def graph(speed, torque, time):
    """Generate and show the graph of the behavior of the motor.

    :param speed: The speed of the engine
    :type speed: tuple or list
    :param torque: The torque send to the engine
    :type torque: tuple or list
    :param time: The delta time of each couple of torque/speed, in miliseconds
    :type time: tuple or list
    """
    #Graph
    axis = plt.gca()
    axis.set_ylim([-1, 150])
    axis.plot(time, speed, 'r')
    axis.plot(time, torque, 'y')

    plt.title("Velocidad en Tiempo")
    plt.xlabel("Tiempo (en delta_t en milisegundos)")
    plt.ylabel("Velocidad/Torque")
    plt.tight_layout()
    plt.legend(['Speed', 'Torque'], loc="upper right")
    
    plt.show()

def main(params):
    """Function that generates the .png images of the graphs from the csv files and saves them

    :param params: The command line parameters, passed as dictionary. It can be: 
        --from='filename'
    :type params: dictionary
    """
    measures = {
        "packet_delays": [],
        "torque_vs_speed": {
            "torque": [],       #   Attention! order matters, as it should mirror the relation
            "speed": []         #   between torque and speed (each torque has the same position of
                                #   it corresponding speed)
        }
    }
    #   Read file and get data
    with open(params["from_file"], 'r') as tests_file:
        csvreader = csv.reader(tests_file, delimiter=',')
        for row in csvreader:
            #   Set torque and packet delays
            if row[0] == 'T':
                measures["torque_vs_speed"]["torque"].append(int(row[2]))
                measures["packet_delays"].append(float(row[3]))
            #   Set speed
            elif row[0] == 'S':
                measures["torque_vs_speed"]["speed"].append(int(row[2]))
    #   Get graph
    #   Slightly change time measures to make the graph possible
    send_time_step = 50     #   The time in miliseconds each which the torque is sent
    measures["torque_vs_speed"]["times"] = []
    for count, time in enumerate(measures["packet_delays"]):
        measures["torque_vs_speed"]["times"].append(time + send_time_step * count)
        measures["torque_vs_speed"]["times"][count] = measures["torque_vs_speed"]["times"][count] / 1000 #  Show seconds
    #   Make sure we start at 0
    measures["torque_vs_speed"]["times"][0] = 0
    graph(measures["torque_vs_speed"]["speed"], measures["torque_vs_speed"]["torque"], measures["torque_vs_speed"]["times"])

def get_params(argv):
    """Method that translates the expected command line parameters to a dictionary

    :param argv: The command line parameters
    :type argv: list
    :return: A dictionary which has as a key the parameter name and as the value the parameter
    value
    :rtype: dictionary
    """
    #   Get file to read through command line arguments as dictionary.
    #   The '(?P<>)' part is for named groups, see: https://docs.python.org/3/howto/regex.html
    from_file_pattern = r"--from=(?P<from_file>.+)"
    regex = re.compile(from_file_pattern)
    argv_string = ' '.join(argv)    #   Get as one string to match pattern
    result = regex.search(argv_string)
    if result == None:
        raise Exception("Input file not specified")
    return result.groupdict()

if __name__ == '__main__':
    import sys
    params = get_params(sys.argv)
    sys.exit(main(params))
