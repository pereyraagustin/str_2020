#ifndef _MOTOR_H
#define _MOTOR_H

/**
*   Funcion para establecer el tope y la sensibilidad del motor.
*/
int init_motor(int v_max, float sens, float inertia);
void set_torque(int torque);
int get_speed();
#endif