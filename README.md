# Motor + GUI + PID

## Descripción
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

Luego, para utilizar la interfaz, abrir la terminal en la carpeta *str_2020* (`cd ../`), y correr el comando `python3 interfaz.py`

## TODO:
* Refactorizar codigo (esquema get_speed->calcular tque nuevo->set_torque)
* Pasar torque y speed de int a unsigned byte.
* Documentar tests y debuggin.