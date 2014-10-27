#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuardos pero con tres cuartos en el primer piso, 
y tres cuartos en el segundo piso. Las acciones totales serán

A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}

Las acción de "subir" solo es legal en el piso de abajo (cualquier cuarto), y la acción de "bajar"
solo es legal en el piso de arriba.

Las acciones de subir y bajar son mas costosas en término de energía que ir a la derecha y a la 
izquierda, por lo que la función de desempeño debe de ser de tener limpios todos los cuartos,
con el menor numero de acciones posibles, y minimozando subir y bajar en relación a ir a los lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara su desempeño con un agente 
aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente sabe en que cuarto se 
encuentra pero no sabe si está limpio o sucio. Diseña un agente racional para este problema, pruebalo
y comparalo con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo para que cuando el agente decida
aspirar, el 80% de las veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
para este problema, pruebalo y comparalo con el agente aleatorio. 

Todos los incisos tienen un valor de 25 puntos sobre la calificación de la tarea.


"""
__author__ = 'escribe_tu_nombre'

import entornos
# Requieres descargar de la página del curso el modulo entornos.py
# Agrega los modulos que requieras de python


