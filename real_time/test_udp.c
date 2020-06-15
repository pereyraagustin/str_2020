#include "motor.h"
#include <stdio.h>
#include <unistd.h>

//  Test of MotorUDP
int main(int argc, char *argv[]) {
    init_motor(255, 0.3, 0.3);  
    for (int i = 0; i < 100; i ++) {
        //  Set torque to i
        set_torque(i);
        sleep(1);
        //  Read speed
        printf("Sent torque: %d;", i);
        printf("Current Speed: %d\n", get_speed());
        fflush(stdout);
    }
    close_connection();
}