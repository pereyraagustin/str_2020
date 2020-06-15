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
    
    //  READ RTC BEGIN
    long data;
    printf("a\n");
    fflush(stdout);
    res = read(rtc_fd, &data, sizeof(data));
    printf("b");
    fflush(stdout);
    //  READ RTC END
    return 0;
}