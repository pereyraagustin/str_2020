#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/rtc.h>

#include "rtc.h"
#include <errno.h>

#define RTC_NAME "/dev/rtc0"

int rtc_fd;

int rtc_init(int speed) {
    int res;
    rtc_fd = open(RTC_NAME, O_RDONLY);
    if (res < 0) {
        printf("Error when opening of RTC: Errno = %d", errno);
        return 0;
    }
    res = ioctl(rtc_fd, RTC_IRQP_SET, speed);
    if (res < 0) {
        printf("Error when setting speed of RTC: Errno = %d", errno);
        return 0;
    }
    res = ioctl(rtc_fd, RTC_PIE_ON, 0);
    if (res < 0) {
        printf("Error when enabling interruptions of RTC: Errno = %d", errno);
        return 0;
    }
    return rtc_fd;
}

void rtc_tick(void) {
   long data;
   int res;

   res = read(rtc_fd, &data, sizeof(data));
   if (res < 0) {
        printf("Error while reading RTC: Errno = %d", errno);
        return;
    }
}

void rtc_close(void) {
    int res;
    res = ioctl(rtc_fd, RTC_PIE_OFF, 0);
    if (res < 0) {
        printf("Error while disabling interruptions of RTC: Errno = %d", errno);
        return;
    }
    res = close(rtc_fd);
    if (res < 0) {
        printf("Error while closing the RTC: Errno = %d", errno);
        return;
    }
}
