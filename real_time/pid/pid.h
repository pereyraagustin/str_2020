#ifndef _PID_H
#define _PID_H

/**
* Default value for kp variable
*/
#define DEFAULT_KP 0.0
/**
* Default value for ki variable
*/
#define DEFAULT_KI 0.0
/**
* Default value for kd variable
*/
#define DEFAULT_KD 0.0
/**
* Initial value of the cumulative and old error variables
*/
#define INITIAL_ERROR 0.0
/**
* Default maximum boundary for the torque to compute
*/
#define DEFAULT_MAX_TORQUE 255
/**
* Default minimal boundary for the torque to compute
*/
#define DEFAULT_MIN_TORQUE 0

/**
* Set delta of time in seconds, and boundaries for the torque.
*
* Should only be called before starting using the PID, because if it is called between two
* calls to compute_pid, as any of the three variables change, the result will no longer be akin the
* last computed value
*
* @param delta_t Double value that represents the delta of time in seconds used to compute the new
*     torque
* @param max_torque Integer that represents the upper threshold to limit the computed torque to
* @param min_torque Integer that represents the lower threshold to limit the computed torque to
* @see [PID parameters](https://en.wikipedia.org/wiki/PID_controller)
*/
void init_pid(double delta_t, int max_torque, int min_torque);

/**
* Set kp, ki and kd values
*
* Can be called between calls of compute_pid
*
* @param kp Double that represents the new value of kp variable
* @param ki Double that represents the new value of ki variable
* @param kd Double that represents the new value of kd variable
* @see [PID parameters](https://en.wikipedia.org/wiki/PID_controller)
*/
void set_variables(double kp, double ki, double kd);

/**
* Compute the needed torque in order to reach the desired speed, acconrding to the error computed
* in base of the current speed and the error cumulated from previous executions
*
* @param desired_v Integer that represents the desired speed to reach by the motor
* @param *torque_t Integer pointer that will contain at the end of execution the torque
*     to apply to reach the desired speed, with the value clamped between the previously
*     established limits
* @param vel_t Integer that contains the current speed of the motor
* @see [PID parameters](https://en.wikipedia.org/wiki/PID_controller)
* @see [motor project](https://github.com/AguPereyra/str_2020)
*/
void compute_pid(int desired_v, int* torque_t, int vel_t);

#endif