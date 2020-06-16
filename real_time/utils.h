#ifndef _UTILS_PROPIO_H
#define _UTILS_PROPIO_H

int clamp(int n, int min, int max);
void parse(char* buffer, int* desired_speed, float* kp, float* ki, float* kd);

#endif