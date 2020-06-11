#ifndef _SOCKETSERVER_H
#define _SOCKETSERVER_H

#include <stdint.h>
#define DEFAULT_PORT 8080

struct sockaddr_in {
    int sin_family;
    uint16_t sin_port;
    struct sin_addr {
        int s_addr;
    }
}

int socket_init(int host, int port, struct sockaddr_in *address);
int get_connected_socket(int server_fd, struct sockaddr_in *address);

#endif