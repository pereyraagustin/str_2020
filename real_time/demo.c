#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include "rtc.h"
#include "pid.h"
#include "motor.h"
#include <sys/socket.h>
#include "socketserver.h"
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include "utils.h"

#define MAX_MSG 1024

int main(int argc, char *argv[]) {
    // Initialize
    int max_fd;
    int fd_rtc, res, fd_socket, fd_motor;
    int fd_connected_socket = -1;
    fd_set readfds;
    //struct timeval timeout = {1, 0};
    char read_buffer[1024] = {0};
    // Initialize motor with torque and velocity
    fd_motor = init_motor(255, 0.015, 15.0);
    //  Allocate memory
    int a = 0, b = 0, c = 0;
    int* torque_t = &a;
    int* vel_t = &b;
    int* desired_v = &c;
    float *kp, *ki, *kd;
    float j = 0.0, k = 0.0, h = 0.0;
    kp = &k;
    ki = &j;
    kd = &h;
    //  Buffer for sending message
    char msg[MAX_MSG];

    //  Initialize socket and wait for connection
    struct sockaddr_in address;
    fd_socket = socket_init(INADDR_ANY, 8080, &address);


    fd_rtc = rtc_init(2);
    //  Initialize pid with delta_t = 2 secs.
    init_pid(2, 255, 0);
    set_variables(1.0, 0.5, 1.0);

    while(1) {
        FD_ZERO(&readfds);
        FD_SET(fd_socket, &readfds);
        FD_SET(fd_motor, &readfds);
        FD_SET(fd_rtc, &readfds);
        max_fd = fd_rtc + 1;
        if (fd_connected_socket != -1) {
            FD_SET(fd_connected_socket, &readfds);
            max_fd = fd_connected_socket + 1;
        }
        res = select(max_fd, &readfds, NULL, NULL, NULL);
        if (res < 0) {
            printf("Error on select");
            fflush(stdout);
            return 0;
        }
        //  Get Speed
        if(FD_ISSET(fd_motor, &readfds)) {
            *vel_t = get_speed();
        } else {
            printf("Timeout\n");
            FD_SET(fd_motor, &readfds);
        }
        //  Check interruption
        if (FD_ISSET(fd_rtc, &readfds)) {
            //  Read the interruption to clean
            rtc_tick();
            compute_pid(*desired_v, torque_t, vel_t);
            set_torque(*torque_t);
        } 
        if (FD_ISSET(fd_socket, &readfds)) {
            //  Leer conexion entrante
            fd_connected_socket = get_connected_socket(fd_socket, &address);
        }
        if (FD_ISSET(fd_connected_socket, &readfds)) {
            //  Leer lo que entra en el socket
            res = recv(fd_connected_socket, read_buffer, 1024, 0);
            if (res < 0) {
                printf("Error while reading socket: %d", errno);
                return 0;
            } else {
                //  Get variables from socket
                parse(read_buffer, desired_v, kp, ki, kd);
                //  Write to PID and get current speed and torque
                compute_pid(*desired_v, torque_t, vel_t);
                set_torque(*torque_t);
                //  Send back
                sprintf(msg, "%d,%d", *vel_t, *torque_t);
                printf("Sending: %s\n", msg);
                fflush(stdout);
                res = write(fd_connected_socket, msg, strlen(msg));
                if (res < 0) {
                    printf("Error while writing to socket: %d", errno);
                    return 0;
                }
            }
        }
    }
    rtc_close();
    return 0;
}
