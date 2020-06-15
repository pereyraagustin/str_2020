#include "motor.h"
#include <arpa/inet.h>
#include <string.h>
#include <utils.h>
#include <netinet/in.h>
#include <sys/socket.h> 
#include <stdlib.h>
#include <stdio.h>
 
#include <unistd.h> 

#define MAXLINE 1024

int torque;
int s_max;
float sens;
float inertia;
float current_s;
//  Socket Variables
int sockfd;
struct sockaddr_in servaddr; 

void init_motor(int _s_max, float _sens, float _inertia) {
    s_max = _s_max;
    sens = _sens;
    inertia = _inertia;
    current_s = 0.0;
  
    //  UDP Socket
    // Creating socket file descriptor 
    if ( (sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) { 
        perror("socket creation failed"); 
        exit(EXIT_FAILURE); 
    } 
  
    memset(&servaddr, 0, sizeof(servaddr)); 
      
    // Filling server information 
    servaddr.sin_family = AF_INET; 
    servaddr.sin_port = htons(5678); 
    servaddr.sin_addr.s_addr = inet_addr("181.90.60.24"); 
      
}

void set_torque(int _torque){
    int n; 
    int res, len;
    char msg[11];
    char str[12];
    char buffer[MAXLINE];
    sprintf(msg, "torque,%d", _torque);
    sendto(sockfd, (const char *)msg, strlen(msg), 
        MSG_CONFIRM, (const struct sockaddr *) &servaddr,  
            sizeof(servaddr)); 
    res = recv(sockfd, (char *)buffer, MAXLINE, 0);
    if (res < 0) {
        printf("Error while reading socket");
    } else { 
        current_s = atoi(&buffer[6]);
    }
   
}

int get_speed(){
    return current_s;
}

void close_connection() {
    close(sockfd); 
}