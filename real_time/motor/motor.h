#ifndef _MOTOR_H
#define _MOTOR_H

/**
*   Funcion para establecer el tope y la sensibilidad del motor.
*/
int init_motor(int v_max, float sens, float inertia);

/**
* Set the torque of the motor to the desired value
*
* @param torque Integer that represents the torque to set the engine to
*/
void set_torque(int torque);

/**
* Get the current speed of the motor
*
* @returns current_speed Integer that represents the speed of the motor at the call time
*/
int get_speed();
#endif