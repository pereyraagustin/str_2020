#include <sys/select.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <linux/rtc.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

#define RTC_NAME "/dev/rtc0"

int main() {
    fd_set readfds;
    int res;
    //  File descriptors
    int rtc_fd;
    //  RTC BEGIN
    rtc_fd = open(RTC_NAME, O_RDONLY);
    if (rtc_fd < 0) {
        printf("%d", errno);
        return 0;
    }
    res = ioctl(rtc_fd, RTC_IRQP_SET, 2);
    if (res < 0) {
        printf("Error while setting time on rtc");
        fflush(stdout);
        return 0;
    }
    res = ioctl(rtc_fd, RTC_PIE_ON, 0);
    if (res < 0) {
        printf("Error enabling interruptions");
        fflush(stdout);
        return 0;
    }
    //  RTC END
    FD_ZERO(&readfds);
    FD_SET(rtc_fd, &readfds);
    res = select(2, &readfds, NULL, NULL, NULL);
    if (res == -1) {
        printf("Error on select");
        fflush(stdout);
        return 0;
    } else {
        printf("All good.\n");
        if(FD_ISSET(0, &readfds)) {
            printf("FD is set\n");
        } else {
            printf("FD is NOT set\n");
        }
        fflush(stdout);
    }
}