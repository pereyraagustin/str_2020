#ifndef _UTILS_PROPIO_H
#define _UTILS_PROPIO_H

/**
* Clamp passed value between thresholds
*
* @param n The integer value to clamp between the limits
* @param min Integer that represents the minimum value to allow. If the passed value is smaller,
*     this value will be returned
* @param max Integer that represents the maximum value to allow. If the passed value is greater,
*     this value will be returned
* @returns n Integer that is in the inclusive range of [min, max] attributes
*/
int clamp(int n, int min, int max);

/**
* Parse a message string with the expected format 'int,float,float,float' to the passed parameters
*
* The expected format is to communicate with the GUI that controls the engine, and it should follow
* the order: 'desired_speed, kp, ki, kd'
*
* @param buffer Char pointer to the buffer with the message string
* @param desired_speed Integer that will contain at the end of execution the value of the desired
*     speed passed through the message. This parameter is used for the PID code
* @param kp Float pointer that will contain at the end of execution the value of the KP variable
*     passed through the message. This parameter is used for the PID code
* @param ki Float pointer that will contain at the end of execution the value of the KI variable
*     passed through the message. This parameter is used for the PID code
* @param kd Float pointer that will contain at the end of execution the value of the KD variable
*     passed through the message. This parameter is used for the PID code
* @see [PID parameters](https://en.wikipedia.org/wiki/PID_controller)
* @see pid/pid.h
*/
void parse(char* buffer, int* desired_speed, float* kp, float* ki, float* kd);

#endif