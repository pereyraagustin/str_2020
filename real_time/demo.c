#include <stdio.h>
#include <stdlib.h>
#include <sys/select.h>
#include "rtc.h"
#include "pid.h"
#include "motor.h"
#include <sys/socket.h>
#include "socketserver.h"

int main(int argc, char *argv[]) {
    // Initialize 
    int cant = 5;
    int i, fd_rtc, res, fd_socket, fd_connected_socket;
    fd_set readfds;
    struct timeval timeout = {5, 0};
    char read_buffer[1024] = {0};
    // Initialize motor with torque and velocity
    init_motor(255, 0.015, 15.0);
    //  Allocate memory
    int a = 0, b = 0;
    int* torque_t = &a;
    int* vel_t = &b;

    //  Initialize socket and wait for connection
    struct sockaddr_in address;
    fd_socket = socket_init(INADDR_ANY, 8080, &address);


    fd_rtc = rtc_init(2);
    //FD_SET(0, &readfds);
    //FD_SET(fd_socket, &readfds);

    //  Initialize pid with delta_t = 2 secs.
    init_pid(2, 255, 0);
    set_variables(1.0, 0.5, 1.0);

    for (i = 0; i < cant; i++) {
        FD_ZERO(&readfds);
        FD_SET(fd_rtc, &readfds);
        res = select(3, &readfds, NULL, NULL, &timeout);
        if (res < 0) {
            printf("Error on select");
            fflush(stdout);
            return 0;
        }
        //  Check interruption
        if (FD_ISSET(fd_rtc, &readfds)) {
            //  Read the interruption to clean
            rtc_tick();
            *vel_t = get_speed();
            compute_pid(10, torque_t, vel_t);
            set_torque(*torque_t);
            printf("Desired Speed: %d, Torque: %d, Speed: %d\n", 10, *torque_t, *vel_t);
            fflush(stdout);
        } /*else if (FD_ISSET(fd_socket, &readfds)) {
            //  Leer conexion entrante
            fd_connected_socket = get_connected_socket(fd_socket, &address);
            //  Leer lo que entra en el socket
            res = recv(fd_connected_socket, read_buffer, 1024, 0);
            if (res < 0) {
                printf("Error while reading socket");
                return;
            } else {
                printf("%s\n", read_buffer);
            }
        }*/
        else {
            printf("%d", res);
            fflush(stdout);
        }
    }
    rtc_close();
}
