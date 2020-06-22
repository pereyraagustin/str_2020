#include <stdio.h>
#include <unistd.h>
#include <sys/select.h>
#include <errno.h>

#include "motor/motor.h"

//  Test of MotorUDP
int main(int argc, char *argv[]) {
    //  FD of UDP
    int udp_fd, res;
    fd_set readfds;

    udp_fd = init_motor(255, 0.3, 0.3);  
    FD_ZERO(&readfds);
    FD_SET(udp_fd, &readfds);

    //  Set timeout
    struct timeval timeout = {1, 0};

    for (int i = 0; i < 100; i ++) {
        //  Set torque to i
        set_torque(i);
        sleep(1);
        //  Read speed
        printf("Sent torque: %d;", i);
        res = select(udp_fd + 1, &readfds, NULL, NULL, &timeout);
        if (res < 0) {
            printf("Error no select: %d", errno);
            fflush(stdout);
        }
        if(FD_ISSET(udp_fd, &readfds)) {
            printf("Current Speed: %d\n", get_speed());
        } else {
            printf("Timeout\n");
            FD_SET(udp_fd, &readfds);
        }
        fflush(stdout);
    }
    close_connection();
}