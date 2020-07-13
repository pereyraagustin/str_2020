# Motor + GUI + PID
This README is available in English and Spanish. The Spanish section is available after the Spanish one.

## Description
Project done under the framework of the subject *Real Time Systems*, which consists of managing the speed of an engine through a graphical interface. The project consists of three modules:

1. Interface: implemented in python3, it makes available to the user the modification of the desired speed, and the variables P, I, D of the PID module, which is in charge of calibrating the motor torque.
2. Real Time: which combines a PID module to calibrate the motor torque based on current and desired speed, an RTC module to perform cyclical motor controls, and a motor control module. This engine control module is implemented in two ways:
    * A motor simulator.
    * A motor controller that communicates by UDP with the real motor.
3. The real engine, which is used only if the corresponding *real-time* module is used, and which is expected to be exposed through a server to the Internet, waiting for commands by UDP.

## Communication protocol
The interface sends a character string through the TCP socket in the format:
'desired speed, kp, ki, kd'
Where the desired velocity is an integer in the inclusive range [0-255], and kp, ki, kd are floating point numbers.

The server sends the format string in response to this information as follows:
'real speed, real torque'
Where both are integers in the inclusive range [0-255].

The server sends the string in the format:
'torque, *value*'

And receives from the engine the chain:
'speed, *value*'

## Workgroup
* Members: Brambilla Nicolás Gabriel, Perez Sardi Walter Gabriel, Pereyra Agustín Ezequiel.

* Teacher: Coppens John.

* Subject: Real Time Systems.

* Year: 2020.

* University: CRUC-IUA-UNDEF.

## Requirements
* Python3 or higher.
* Python lybraries: Gtk, GooCanvas.
* gcc
* Makefile

## To use
First run the real time module (PID + RTC + Motor). To do this, depending on the engine you want to use, you must run the commands:

* UDP engine:
`cd real_time /`  
`make demo_udp`  
`sudo. / demo_udp`  

* Simulated Engine:
`cd real_time /`  
`make demo_sim`  
`sudo. / demo_sim`  

Then, to use the interface, open the terminal in the *str_2020/gui* folder (`cd ../ gui`), and run the command  
`python3 main_gui.py`  

## Measurements
To test the commands below, you can use the logs present in the *logs/* directory
### Engine measurements
To analyze the motor measurements (torque and speed per instant, along with the speed you want at each instant), you can do it by passing parameters to the command **python3 main_gui.py** the value `--log = INFO`, this will write the measures, along with other information, in the *logs* file.

If you want to be able to read only that information, cleaner, with the script **logs_to_csv.py**, passing the path to the log file as the first argument, you will get two csv files, one with the information of the engine measurements, and another with the time difference between sending and receiving packages.

In turn, if you want to graph the information of the engine, the same can be done with the script **csv_to_graph.py**, to which you must indicate by parameters the file to use, and the format.

Two formats are currently supported, one called *def*, which is the one used by our **logs_to_csv.py** script, and the other called *jcoppens*, which is described in the same script and in the user manual.

## Time measurements between packages
If you want to parse delays between sending and receiving packets, you can do this using the command line parameter `--log = INFO` by running **python3 main_gui.py**, as indicated in the previous section.

This will load the relative time information between sending and receiving packages in the *logs* file. If you needed to be able to read only that data in a simpler way, with the script **logs_to_csv.py**, passing the path to the log file as the first argument, you will get two csv files, one with the information of the engine measurements, and another with the time difference between sending and receiving packages.

## Problem solving
Below is a small guide on how to analyze the source of some problems that might occur when trying to start the application or making changes to it.

### Interface graph not working
Use `netcat -l 8080`, open the interface and move the sliders. If nothing appears in the terminal where netcat is, the connection to the socket is not being made. The problem is likely to be found in the *Client.py* or *Connection.py* classes. Less likely but also possible is that the *Graphics.py* class is not querying the data as it should, in the *animate (...)* function.


## Descripción
Proyecto hecho bajo el marco de la materia *Sistemas en Tiempo Real*, que consiste en el manejo a través de una interfaz gráfica de la velocidad de un motor. El proyecto consiste en tres módulos:

1. Interfaz: implementada en python3, pone a disposición del usuario la modificación de la velocidad deseada, y las variables P, I, D del módulo PID, que se encarga de calibrar el torque del motor.
2. Tiempo Real: que combina un módulo de PID para calibrar el torque del motor en función de la velocidad actual y la deseada, un módulo RTC para realizar controles cíclicos del motor, y un módulo de control del motor. Éste módulo de control del motor está implementado de dos formas:
    *   Un simulador del motor.
    *   Un controlador del motor que se comunica por UDP con el motor real.
3. El motor real, que se utiliza sólo si se usa el módulo de *tiempo real* correspondiente, y que se espera está expuesto a través de un servidor a Internet, esperando comandos por UDP.

## Protocolo de comunicación
La interfaz envía por el socket TCP una cadena de caracteres con el formato:
'velocidad deseada,kp,ki,kd'
Donde la velocidad deseada es un entero en el rango inclusivo [0,255], y kp, ki, kd son números de punto flotante.

El servidor envía a la interfaz como respuesta a dicha información la cadena de formato:
'velocidad real,torque real'
Donde ambos son enteros en el rango inclusivo [0,255].

El servidor envía al motor la cadena con el formato:
'torque,*valor*'

Y recibe del motor la cadena:
'speed,*valor*'

## Grupo de trabajo
* Integrantes: Brambilla Nicolás Gabriel, Perez Sardi Walter Gabriel, Pereyra Agustín Ezequiel.

* Profesor: Coppens John.

* Materia: Sistemas en Tiempo Real.

* Año: 2020.

* Universidad: UNDEF-CRUC-IUA.

## Requerimientos
* Python3 o superior.
* Librerías: Gtk, GooCanvas.
* gcc
* Makefile

## Para usar
Primero correr el módulo de tiempo real (PID + RTC + Motor). Para ello, según el motor que se desée usar, se deberán correr los comandos:

* Motor UDP:
`cd real_time/`  
`make demo_udp`  
`sudo ./demo_udp`  

* Motor Simulado:
`cd real_time/`  
`make demo_sim`  
`sudo ./demo_sim`  

Luego, para utilizar la interfaz, abrir la terminal en la carpeta *str_2020/gui* (`cd ../gui`), y correr el comando 
`python3 main_gui.py`

## Mediciones
Para probar los comandos a continuación, se pueden utilizar los logs presentes en el directorio *logs/*
### Mediciones del motor
Para analizar las mediciones del motor (torque y velocidad por instante, junto con la velocidad desea en cada instante), puede hacerlo pasandole por parámetros al comando de **main_gui.py** el valor `--log=INFO`, esto escribirá dicha información, junto con otra, en el archivo *logs*.

Si desea poder leer sólo esa información, de manera más limpia, con el script **logs_to_csv.py** pasando como primer argumento el path al archivo de logs obtendrá dos archivos csv, uno con la información de las mediciones del motor, y otro con la diferencia de tiempos entre el envío y la recepción de paquetes.

A su vez, si desea graficar la información del motor, lo mismo lo puede hacer con el script **csv_to_graph.py**, al que debe indicarle por parámetros el archivo a usar, y el formato.

Actualmente se soportan dos formatos, uno denominado *def*, que es el que utiliza nuestro script **logs_to_csv.py**, y otro denominado *jcoppens*, que está descripto en el mismo script y en el manual de usuario.

## Mediciones de tiempos entre paquetes
Si quiere analizar los delays entre el envío y recepción de paquetes, puede hacerlo utilizando el parámetro de línea de comandos `--log=INFO` al ejecutar **main_gui.py**, como se indicó en la sección anterior.

Esto cargará la información de tiempos relativa entre el envío y recepción de paquetes en el archivo *logs*. Si necesitara poder leer sólo esos datos de manera más simple, con el script **logs_to_csv.py**, pasando como primer argumento el path al archivo de logs, obtendrá dos archivos csv, uno con la información de las mediciones del motor, y otro con la diferencia de tiempos entre el envío y la recepción de paquetes.

## Solución de problemas
A continuación se presenta una pequeña guía de cómo analizar la fuente de algunos problemas que podrían ocurrir al intentar arrancar la aplicación o al realizar cambios en la misma.

### Gráfico de la interfaz no funcionando
Usar `netcat -l 8080`, abrir la interfaz y mover los deslizadores. Si en la terminal donde está netcat no aparece nada, la conexión al socket no se está realizando. Es probable que el problema se encuentre en las clases *Client.py* o *Connection.py*. Menos probable pero también posible es que la clase *Graphics.py* no esté consultando los datos como debería, en la función *animate(...)*.

## TODO:
* Refactorizar codigo (esquema get_speed->calcular tque nuevo->set_torque)
* Pasar torque y speed de int a unsigned byte.
* Documentar tests y debuggin.
* Interfaz: adaptacion de espacio entre columnas automatico?
* Pasar print a logging
