#include "motor.h"
#include <math.h>

int torque;
int s_max;
float sens;
float inertia;
float current_s;

int init_motor(int _s_max, float _sens, float _inertia) {
    s_max = _s_max;
    sens = _sens;
    inertia = _inertia;
    current_s = 0.0;
    return -1;
}

void set_torque(int _torque){
    torque = _torque;
}

int get_speed(){
    float speed = s_max * (1 - exp(-torque*sens) );
    current_s = (speed - current_s) / inertia + current_s;
    return (int) round(current_s);
}