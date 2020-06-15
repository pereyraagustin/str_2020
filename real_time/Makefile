all:pid_demo

#TODO: Ver como se hace bien un makefile, tipo: https://stackoverflow.com/questions/11993318/gcc-not-linking-files
pid_demo: demo.c rtc.o pid.o motor.o utils.o socketserver.o
	gcc demo.c rtc.o pid.o motor.o utils.o socketserver.o -o pid_demo -lm -Wall
	rm -rf *.o

test_udp: test_udp.c motor_udp.o
	gcc test_udp.c motor_udp.o -o test_udp -Wall
	rm -rf *.o

demo_min: demo_min.c
	gcc demo_min.c -o demo_min -Wall
	rm -rf *.o

rtc.o: rtc.c rtc.h
	gcc rtc.c -c

pid.o: pid.c pid.h
	gcc pid.c -c

motor.o: sim_motor.c motor.h
	gcc sim_motor.c -c -o motor.o
	
motor_udp.o: motor_udp.c motor.h
	gcc motor_udp.c -c

utils.o: utils.c utils.h
	gcc utils.c -c

socketserver.o: socketserver.c socketserver.h
	gcc socketserver.c -c
	
clean:
	rm -rf *o pid_demo

socket_server: socketserver.c
	gcc socketserver.c -o socket_server
