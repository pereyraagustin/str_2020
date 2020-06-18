# Motor + GUI + PID

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

Luego, para utilizar la interfaz, abrir la terminal en la carpeta *str_2020* (`cd ../`), y correr el comando 
`python3 interfaz.py`

## TODO:
* Refactorizar codigo (esquema get_speed->calcular tque nuevo->set_torque)
* Pasar torque y speed de int a unsigned byte.
* Documentar tests y debuggin.
* Interfaz: adaptacion de espacio entre columnas automatico?
* Interfaz: actualizar vel y torque por clock