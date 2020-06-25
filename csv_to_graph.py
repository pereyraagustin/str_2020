import csv
import matplotlib.pyplot as plt
import re

def graph(speed, torque, time, desired_speed=None):
    """Generate and show the graph of the behavior of the motor.

    :param speed: The speed of the engine
    :type speed: tuple or list
    :param torque: The torque send to the engine
    :type torque: tuple or list
    :param time: The delta time of each couple of torque/speed, in miliseconds
    :type time: tuple or list
    :param desired_speed: The desired speed at each instant
    :type desired_speed: tuple or list, optional
    :return: The plot with the corresponding graph
    :rtype: class: `matplotlib.pyplot`
    """
    #Graph
    axis = plt.gca()
    axis.set_ylim([-1, 150])
    axis.plot(time, speed, 'r')
    axis.plot(time, torque, 'y')
    if desired_speed is not None:
        axis.plot(time, desired_speed, 'c')
        legends = ['Speed', 'Torque', 'Desired Speed']
    else:
        legends = ['Speed', 'Torque']

    plt.title("Velocidad en Tiempo")
    plt.xlabel("Tiempo (en delta_t en milisegundos)")
    plt.ylabel("Velocidad/Torque")
    plt.tight_layout()
    plt.legend(legends, loc="upper right")
    
    return plt

def jcoppens_parse(from_file):
    """Function that generates a dictionary from the csv file with the format known as jcoppens

    :param from_file: The csv file to read in order to get the data. It should follow the format:
        T, IP source, value of received torque, time in milliseconds of reception of the package with respect to the previous one
        S, IP destination, value of current speed
        Where this two rows should be always present together, there shouldn't be one row without the other,
        and where T and S stand for Torque and Speed, respectively
    :type from_file: str
    :return: The dictionary of the parsed measures, following the format:
        measures = {
        "packet_delays": [],    #   Containing the delays between packets
        "torque_vs_speed": {
            "torque": [],       #   Attention! order matters, as it should mirror the relation
            "speed": []         #   between torque and speed (each torque has the same position of
                                #   it corresponding speed)
        }
    }
    :rytpe: dictionary
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
    with open(from_file, 'r') as tests_file:
        csvreader = csv.reader(tests_file, delimiter=',')
        for row in csvreader:
            #   Set torque and packet delays
            if row[0] == 'T':
                measures["torque_vs_speed"]["torque"].append(int(row[2]))
                measures["packet_delays"].append(float(row[3]))
            #   Set speed
            elif row[0] == 'S':
                measures["torque_vs_speed"]["speed"].append(int(row[2]))
    #   Slightly change time measures to make the graph possible
    send_time_step = 50     #   The time in miliseconds each which the torque is sent
    measures["torque_vs_speed"]["times"] = []
    for count, time in enumerate(measures["packet_delays"]):
        measures["torque_vs_speed"]["times"].append(time + send_time_step * count)
        measures["torque_vs_speed"]["times"][count] = measures["torque_vs_speed"]["times"][count] / 1000 #  Show seconds
    #   Make sure we start at 0
    measures["torque_vs_speed"]["times"][0] = 0
    return measures

def def_parse(from_file):
    """Function that generates a dictionary from the csv file with the format that corresponds to
    the csv file named as measures.csv that is created by logs_to_csv.py from the logs of the app.

    :param from_file: The csv file to read in order to get the data. It should follow the format:
        Two first lines with not usefull data for the algorithm.
        The next lines as:
            current_speed,current_torque,desired_speed,time
                Where time is in milliseconds and represents the step times corresponding to each line
                measures, not the absolute delay between packets.
        Where this two rows should be always present together, there shouldn't be one row without the other,
        and where T and S stand for Torque and Speed, respectively
    :type from_file: str
    :return: The dictionary of the parsed measures, following the format:
        measures = {
        "torque_vs_speed": {
            "torque": [],       #   Attention! order matters, as it should mirror the relation
            "speed": [],        #   between torque and speed (each torque has the same position of
            "desired_speed": [] #   it corresponding speed)
        }
    }
    :rytpe: dictionary
    """
    measures = {
        "torque_vs_speed": {
            "torque": [],        #   Attention! order matters, as it should mirror the relation
            "speed": [],         #   between torque and speed (each torque has the same position of
            "desired_speed": [], #   it corresponding speed)
            "times": []
        }
    }
    #   Read file and get data
    with open(from_file, 'r') as tests_file:
        csvreader = csv.reader(tests_file, delimiter=',')
        for count, row in enumerate(csvreader):
            if count >= 2:  #   Ignore first two rows
                #   Set torque and packet delays
                measures["torque_vs_speed"]["speed"].append(int(row[0]))
                measures["torque_vs_speed"]["torque"].append(int(row[1]))
                measures["torque_vs_speed"]["desired_speed"].append(int(row[2]))
                measures["torque_vs_speed"]["times"].append(float(row[3]) / 1000)   #   Pass to seconds
    #   Slightly change time measures to make the graph possible
    measures["torque_vs_speed"]["times"][0] = 0
    return measures

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
    from_file_pattern = r"--from=(?P<from>.+)"
    #   File format
    format_file_pattern = r"--format=(?P<format>.+)"
    #   Combine patterns
    final_pattern = from_file_pattern + r"\s+" + format_file_pattern
    regex = re.compile(final_pattern)
    argv_string = ' '.join(argv)    #   Get as one string to match pattern
    result = regex.search(argv_string)
    if result == None:
        raise Exception("Input file not specified or format file not specified")
    return result.groupdict()

def main(params):
    """Function that gets the command line parameters, and according to them takes the source csv file
    with the corresponding format and gets the graph.

    :param params: The command line parameters, passed as dictionary. It can be: 
        --from=filename
        --format=format
            Current supported formats are: jcoppens and def
    :type params: dictionary
    """
    if params["format"] == "def":
        measures = def_parse(params["from"])
        plot = graph(measures["torque_vs_speed"]["speed"], measures["torque_vs_speed"]["torque"], measures["torque_vs_speed"]["times"], measures["torque_vs_speed"]["desired_speed"])
    else:
        measures = jcoppens_parse(params["from"])
        plot = graph(measures["torque_vs_speed"]["speed"], measures["torque_vs_speed"]["torque"], measures["torque_vs_speed"]["times"])
    #   Show
    plot.show()

if __name__ == '__main__':
    import sys
    params = get_params(sys.argv)
    sys.exit(main(params))
