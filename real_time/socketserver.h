#ifndef _SOCKETSERVER_H
#define _SOCKETSERVER_H

#include <stdint.h>
#include <netinet/in.h>
#define DEFAULT_PORT 8080

int socket_init(int host, int port, struct sockaddr_in *address);
int get_connected_socket(int server_fd, struct sockaddr_in *address);

#endif
