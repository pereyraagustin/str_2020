#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/rtc.h>

#include "rtc.h"

#define RTC_NAME "/dev/rtc0"

int rtc_fd;

int rtc_init(int speed) {
    int res;
    rtc_fd = open(RTC_NAME, O_RDONLY);
    res = ioctl(rtc_fd, RTC_IRQP_SET, speed);
    res = ioctl(rtc_fd, RTC_PIE_ON, 0);
    return rtc_fd;
}

void rtc_tick(void) {
   long data;
   int res;

   res = read(rtc_fd, &data, sizeof(data));
}

void rtc_close(void) {
    int res;
    res = ioctl(rtc_fd, RTC_PIE_OFF, 0);
    res = close(rtc_fd);
}
