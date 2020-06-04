#include "utils.h"

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