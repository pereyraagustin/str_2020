// Server side C/C++ program to demonstrate Socket programming 
//  Source: https://www.geeksforgeeks.org/socket-programming-cc/
#include "socketserver.h"
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h> 

int socket_init(int host, int port, struct sockaddr_in *address) {
    int server_fd;
    int opt = 1;
    // Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) { 
		perror("Socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	// Forcefully attaching socket to the port 8080 
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 
												&opt, sizeof(opt))) {
		perror("Setsockopt failed"); 
		exit(EXIT_FAILURE); 
	} 
	// AF_INET = IPV4
	address->sin_family = AF_INET; 
	address->sin_addr.s_addr = host; 
	address->sin_port = htons( port ); 
	
	// Forcefully attaching socket to the port
	if (bind(server_fd, (struct sockaddr *)address, 
								sizeof(*address))<0){ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	}  
    if (listen(server_fd, 3) < 0) { 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	}
    return server_fd;   
}

// sockaddr_in = Informacion de la dir. socket
int get_connected_socket(int server_fd, struct sockaddr_in *address){
    int new_socket;
    int addrlen = sizeof(address);
	if ((new_socket = accept(server_fd, (struct sockaddr *)address, 
					(socklen_t*)&addrlen))<0){ 
		perror("Error on accepting socket"); 
		exit(EXIT_FAILURE); 
	}
    return new_socket;
}
