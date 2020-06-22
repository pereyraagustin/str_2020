all:demo_sim

#TODO: Ver como se hace bien un makefile, tipo: https://stackoverflow.com/questions/11993318/gcc-not-linking-files
demo_sim: demo_sim.c rtc.o pid.o motor.o utils.o socketserver.o
	gcc demo_sim.c rtc.o pid.o motor.o utils.o socketserver.o -o demo_sim.exe -lm -Wall
	rm -rf *.o

demo_udp: demo_udp.c rtc.o pid.o motor_udp.o utils.o socketserver.o
	gcc demo_udp.c rtc.o pid.o motor_udp.o utils.o socketserver.o -o demo_udp.exe -lm -Wall
	rm -rf *.o

test_udp: test_udp.c motor_udp.o
	gcc test_udp.c motor_udp.o -o test_udp.exe -Wall
	rm -rf *.o

test_socket: test_socket.c socketserver.o
	gcc test_socket.c socketserver.o -o test_socket.exe -Wall
	rm -rf *.o

socket_server: ./server/socketserver.c
	gcc ./server/socketserver.c -o socket_server.exe

rtc.o: ./rtc/rtc.c ./rtc/rtc.h
	gcc ./rtc/rtc.c -c

pid.o: ./pid/pid.c ./pid/pid.h
	gcc ./pid/pid.c -c

motor.o: ./motor/sim_motor.c ./motor/motor.h
	gcc ./motor/sim_motor.c -c -o motor.o
	
motor_udp.o: ./motor/motor_udp.c ./motor/motor.h
	gcc ./motor/motor_udp.c -c

utils.o: ./utils/utils.c ./utils/utils.h
	gcc ./utils/utils.c -c

socketserver.o: ./server/socketserver.c ./server/socketserver.h
	gcc ./server/socketserver.c -c
	
clean:
	rm -rf *.o *.exe
