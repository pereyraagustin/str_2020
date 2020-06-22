#include <sys/select.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <linux/rtc.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <netinet/in.h>

#include "server/socketserver.h"

#define RTC_NAME "/dev/rtc0"

int main() {
    fd_set readfds;
    int res;
    //  File descriptors
    int rtc_fd;
    int fd_socket;
    int fd_connected_socket;
    //
    char read_buffer[1024] = {0};
    struct sockaddr_in address;
    fd_socket = socket_init(INADDR_ANY, 8080, &address);
    fd_connected_socket = get_connected_socket(fd_socket, &address);
    res = recv(fd_connected_socket, read_buffer, 1024, 0);
    printf("%d", res);
    fflush(stdout);
    printf("%s", read_buffer);
    fflush(stdout);

}