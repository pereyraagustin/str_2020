#include "utils.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int clamp(int n, int min, int max);

int clamp(int n, int min, int max) {
    if (n < min) {
        return min;
    }else if(n > max) {
        return max;
    }else {
        return n;
    }
}

void parse(char* buffer, int* desired_speed, float* kp, float* ki, float* kd) {
    char *pt;
    int b;
    float * floatpointers[3];
    floatpointers[0] = kp;
    floatpointers[1] = ki;
    floatpointers[2] = kd;
    pt = strtok (buffer,",");
    for(int i = 0; i < 3; i++){
      if (pt != NULL) {
        if(i == 0){
          *desired_speed = atoi(pt);
        }
        else {
          *floatpointers[i-1] = atof(pt);
        }
        pt = strtok (NULL, ",");
            
      }
    }
}