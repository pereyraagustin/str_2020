#ifndef _SOCKETSERVER_H
#define _SOCKETSERVER_H

#include <stdint.h>
#include <netinet/in.h>

/**
* Default port to connect to
*/
#define DEFAULT_PORT 8080

/**
* Initialize of the service that will listen and communicate through the socket.
*<p>
* The server will be initialize and it will start listening on this socket for incoming connections
*
* @param host The integer value suitable for use as an Internet address, ad indicated by
*     <arpa/inet.h>
* @param port The port number to connecto to, as an integer
* @param *address A pointer to a sockaddr_in structure that will be use to store information needed
*     to work with Internet addresses during connections
* @returns server_fd The file descriptor of the socket where it is waiting incoming connections
* @see [netinet/in.h](https://pubs.opengroup.org/onlinepubs/007908799/xns/netinetin.h.html)
* @see [sockaddr_in](https://www.gta.ufrj.br/ensino/eel878/sockets/sockaddr_inman.html)
* @see [file descriptors](https://en.wikipedia.org/wiki/File_descriptor)
*/
int socket_init(int host, int port, struct sockaddr_in *address);

/**
* Accept an incoming connection. 
*
* To be call if it is known that there is an incoming connection to the passed file descriptor
* (through a select on the file descriptor, for example)
*
* @param server_fd The file descriptor of the socket where there is an incoming connection
* @param *address A pointer to a sockaddr_in structure that will be use to store information needed
*     to work with Internet addresses during connections
* @returns new_socket A file descriptor to the socket with the incoming connection accepted. This
*     file descriptor is ready to be used to communicate through it
* @see [sockaddr_in](https://www.gta.ufrj.br/ensino/eel878/sockets/sockaddr_inman.html)
* @see [file descriptors](https://en.wikipedia.org/wiki/File_descriptor)
*/
int get_connected_socket(int server_fd, struct sockaddr_in *address);

#endif
