#include "pid.h"
#include "motor.h"
#include <math.h>

void init_pid(double delta_t);
void set_variables(double kp, double ki, double kd);
void compute_pid(int desired_v, int* torque_t, int* vel_t);

/* Dudas:
1. delta T va por parametros?
2. delta T seria float?
3. Declaramos old_error en un init?
4. delta T en segundos?
5. Esperamos entre set_torque y get_speed?
6. Torque es entero?
*/

double kp = DEFAULT_KP;
double ki = DEFAULT_KI;
double kd = DEFAULT_KD;
double old_error = INITIAL_ERROR; 
double sum_error = INITIAL_ERROR;
double delta_error = INITIAL_ERROR;
double delta_t = 1.0;

void init_pid(double _delta_t) {
    delta_t = _delta_t;
    init_motor(255, 0.015, 15.0);
}

void set_variables(double _kp, double _ki, double _kd) {
    kp = _kp;
    ki = _ki;
    kd = _kd;
}

void compute_pid(int desired_v, int* torque_t, int* vel_t){
    double temp_torque;
    temp_torque = kp * desired_v + delta_t * ki * sum_error + kd * delta_error / delta_t;

    //  Send torque to motor
    *torque_t = (int) round(temp_torque);
    set_torque(*torque_t);
    //  Read current speed
    *vel_t = get_speed();

    //  Acumular error
    double new_error = (*vel_t - desired_v);
    sum_error = new_error + sum_error;
    //  Calcular error viejo
    if ( delta_t > 0 ) {
        delta_error = new_error - old_error;
    }else{
        delta_error = old_error - new_error;
    }

    //  Almacenar error para proxima pasada
    old_error = new_error;
}
