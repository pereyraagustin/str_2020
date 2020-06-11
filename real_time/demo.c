#include <stdio.h>
#include <sys/select.h>
#include <sys/socket.h> 

#include "rtc.h"
#include "pid.h"
#include "motor.h"
#include "socketserver.h"

int main(int argc, char *argv[]) {
    // Initialize 
    int cant = 30;
    int i, fd, res, fd_socket, fd_connected_socket;
    fd_set readfds;
    struct timeval timeout = {1, 0};
    // Initialize motor with torque and velocity
    init_motor(255, 0.015, 15.0);
    //  Allocate memory
    int a = 0, b = 0;
    int* torque_t = &a;
    int* vel_t = &b;

    //  Initialize socket and wait for connection
    struct sockaddr_in address;
    fd_socket = socket_init(INADDR_ANY, 8080, &address);

    FD_ZERO(&readfds);

    fd = rtc_init(16);
    FD_SET(fd, &readfds);
    FD_SET(fd_socket, &readfds);

    //  Initialize pid with delta_t = 2 secs.
    init_pid(2, 255, 0);
    set_variables(1.0, 0.5, 1.0);

    for (i = 0; i < cant; i++) {
        res = select(3, &readfds, NULL, NULL, &timeout);
        //  Check interruption
        if (FD_ISSET(fd_socket, &readfds)) {
            //  Leer conexion entrante
            new_socket = connected_socket(server_fd, &address);
            //  Leer lo que entra en el socket
            valread = read( new_socket , buffer, 1024);
            printf("%s\n",buffer );
        }
        /*
        //  Read the interruption to clean
        rtc_tick();
        if(FD_ISSET())
        *vel_t = get_speed();
        compute_pid(10, torque_t, vel_t);
        set_torque(*torque_t);
        printf("Desired Speed: %d, Torque: %d, Speed: %d\n", 10, *torque_t, *vel_t);
        fflush(stdout);
        */
    }
    printf("\n");
    fflush(stdout);
    rtc_close();
}
