from datetime import datetime

def translate(source_file):
    """Function that passes the application log info to two csv files: one that contains the engine
    behavior and other that contains the delays between sending and receiveng torque and speed
    respectively.
    The created files will be measures.csv and packet_times.csv. If the files exist, the data will be
    appended, with the corresponding 

    :param source_file: The path to the file of logs
    :type source_file: str
    """
    measures = "current_speed, current_torque, desired_speed, time_ms\n"
    packet_times = "direction,relative_time_ms\n"
    #   Strings that preceed the searched data in logs
    measures_header = "INFO:root:At Graphics.animate:"
    sent_data_header = "INFO:root:Sent data at Connection.get_updated_data:"
    received_data_header = "INFO:root:Received data at Connection.read_data at relative time:"
    #   Cache their length
    measures_header_len = len(measures_header)
    sent_data_header_len = len(sent_data_header)
    received_data_header_len = len(received_data_header)
    with open(source_file, 'r') as logs:
        for row in logs:
            if measures_header in row:
                #   Add data to measures.csv
                measures += row[measures_header_len:].strip() + "\n"
            #   Add data to packet_times.csv
            elif sent_data_header in row:
                packet_times += row[sent_data_header_len:].strip() + "\n"
            elif received_data_header in row:
                packet_times += row[received_data_header_len:].strip() + "\n"

    #   Write files
    with open("measures.csv", "a") as measures_file:
        measures_file.write("Starting measures writen at: {}\n".format(datetime.now()))
        measures_file.write(measures)
    with open("packet_times.csv", "a") as packet_times_file:
        packet_times_file.write("Starting measures writen at: {}\n".format(datetime.now()))
        packet_times_file.write(packet_times)

if __name__ == "__main__":
    """ Expects first command line argument to be the file name of the logs or its path
    """
    import sys
    sys.exit(translate(sys.argv[1]))