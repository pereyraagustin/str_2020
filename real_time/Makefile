all:pid_demo

#TODO: Ver como se hace bien un makefile, tipo: https://stackoverflow.com/questions/11993318/gcc-not-linking-files
pid_demo: demo.c rtc.o pid.o motor.o
	gcc demo.c rtc.o pid.o motor.o -o pid_demo -lm -Wall
	rm -rf *.o

rtc.o: rtc.c rtc.h
	gcc rtc.c -c

pid.o: pid.c pid.h
	gcc pid.c -c

motor.o: sim_motor.c motor.h
	gcc sim_motor.c -c -o motor.o

clean:
	rm -rf *o pid_demo
#socket_server: socketserver.c
#	gcc socketserver.c -o socket_server
