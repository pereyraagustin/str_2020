#include <stdio.h>
#include <sys/select.h>

#include "rtc.h"
#include "pid.h"

int main(int argc, char *argv[]) {
    int cant = 30;
    int i, fd, res;
    fd_set readfds;
    struct timeval timeout = {1, 0};

    FD_ZERO(&readfds);

    fd = rtc_init(16);
    FD_SET(fd, &readfds);

    //  Initialize pid with delta_t = 2 secs.
    init_pid(2);
    set_variables(1.0, 1.0, 1.0);
    //  Allocate memory
    int a = 0, b = 0;
    int* torque_t = &a;
    int* vel_t = &b;

    for (i = 0; i < cant; i++) {
        res = select(1, &readfds, NULL, NULL, &timeout);
        rtc_tick();
        compute_pid(i, torque_t, vel_t);
        printf("Desired Speed: %d, Torque: %d, Speed: %d\n", i, *torque_t, *vel_t);
        fflush(stdout);
    }
    printf("\n");
    fflush(stdout);
    rtc_close();
}
