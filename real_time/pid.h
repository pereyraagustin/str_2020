#ifndef _PID_H
#define _PID_H

#define DEFAULT_KP 0.0
#define DEFAULT_KI 0.0
#define DEFAULT_KD 0.0
#define INITIAL_ERROR 0.0

void init_pid(double delta_t);
void set_variables(double kp, double ki, double kd);
void compute_pid(int desired_v, int* torque_t, int* vel_t);

#endif