#include "pid.h"
#include <math.h>
#include "../utils/utils.h"

void init_pid(double delta_t, int _max_torque, int _min_torque);
void set_variables(double kp, double ki, double kd);
void compute_pid(int desired_v, int* torque_t, int vel_t);

double kp = DEFAULT_KP;
double ki = DEFAULT_KI;
double kd = DEFAULT_KD;
double old_error = INITIAL_ERROR; 
double sum_error = INITIAL_ERROR;
double delta_error = INITIAL_ERROR;
double delta_t = 1.0;
int max_torque = DEFAULT_MAX_TORQUE;
int min_torque = DEFAULT_MIN_TORQUE;

void init_pid(double _delta_t, int _max_torque, int _min_torque) {
    delta_t = _delta_t;
    max_torque = _max_torque;
    min_torque = _min_torque;
}

void set_variables(double _kp, double _ki, double _kd) {
    kp = _kp;
    ki = _ki;
    kd = _kd;
}

void compute_pid(int desired_v, int* torque_t, int vel_t){
    double temp_torque;

    //  Acumular error
    double new_error = (desired_v - vel_t);
    sum_error = new_error + sum_error;
    //  Calcular error viejo
    if ( delta_t > 0 ) {
        delta_error = new_error - old_error;
    }else{
        delta_error = old_error - new_error;
    }

    temp_torque = kp * desired_v + delta_t * ki * sum_error + kd * delta_error / delta_t;

    //  Send torque to motor
    *torque_t = (int) round(temp_torque);
    //  Clamp between tresholds
    *torque_t = clamp(*torque_t, min_torque, max_torque);
    //  Almacenar error para proxima pasada
    old_error = new_error;
}
