#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
conecta4.py.py
------------

El juego de conecta 4

Este juego contiene una parte de la tarea 5, y otra parte es la implementación desde 0 del juego de Otello.

"""

__author__ = 'juliowaissman'

import juegos_cuadricula
import time
from random import shuffle


class Conecta4(juegos_cuadricula.Juego2ZT):
    """
    Juego del conecta 4 utilizando la definición de juego utilizada en la clase juego_tablero.JuegoT2ZT.
    Todos los modulos se deben de reescribir en función del nuevo problema.

    """

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y renglones y el estado inicial del juego.

                         0   1   2   3   4   5   6
                         7   8   9  10  11  12  13
                        14  15  16  17  18  19  20
                        21  22  23  24  25  26  27
                        28  29  30  31  32  33  34
                        35  36  37  38  39  40  41
        """
        juegos_cuadricula.Juego2ZT.__init__(self, 7, 6, tuple([0 for _ in range(42)]))
        self.bases = range(35, 42)

        def f_combinaciones(pos):
            """
            Funcion interna para encontrar todas las combinaciones de una posición

            """
            combinaciones = []
            # Columna
            if pos < 21:
                combinaciones.append(range(pos, pos + 22, 7))
            # Renglones y diagonales
            for i in range(0, 4):
                if 0 <= pos % 7 - i < 4:
                    # Renglones
                    combinaciones.append(range(pos - i, pos - i + 4))
                    # Diagonal hacia abajo
                    pos_d = pos - 8 * i
                    if 0 <= pos_d < 18:
                        combinaciones.append(range(pos_d, pos_d + 25, 8))
                    # Diagonal hacia arriba
                    pos_d = pos + 6 * i
                    if 20 < pos_d < 39:
                        combinaciones.append(range(pos_d, pos_d - 19, -6))
            return tuple(combinaciones)

        self.combinaciones = {i: f_combinaciones(i) for i in range(42)}


    def jugadas_legales(self, estado, jugador):

        indices = [encuentra(estado[base:: -7], 0) for base in self.bases]
        return [(None, base - 7*indice)
                for (base, indice) in zip(self.bases, indices) if indice is not None]

    def estado_terminal(self, estado):

        #Checa para cada valor final. Si es None es que está hasta arriba
        indices = [encuentra(estado[base:: -7], 0) for base in self.bases]
        for (base, indice) in zip(self.bases, indices):
            if indice != 0:
                pos = base - 7 * (indice - 1) if indice is not None else base - 35
                for combinacion in self.combinaciones[pos]:
                    if all(estado[i] == estado[pos] for i in combinacion):
                        return estado[pos]
        if all(x is None for x in indices):
            return 0
        return None

    def hacer_jugada(self, estado, jugada, jugador):
        """
        Devuelve estado_nuevo que es el estado una vez que se realizó la juagada por el jugador.
        Hay que recordar que los juegos de tablero los estamos estandarizando para jugadas las cuales
        son (pini, pfinal) donde pini esla posicion inicial y pfinal es la posicion final de una ficha.

        Si el juego solamente implica poner fichas entonces pini no se toma en cuenta pero si tiene que ir para
        guardar homogeneidad entre los diferentes juegos y los diferentes métodos que desarrollaremos.


        """
        e = list(estado)
        e[jugada[1]] = jugador
        return tuple(e)


def encuentra(tupla, valor):
    """
    Como el método index de una tupla, pero si no se encuentra el valor
    devuelve un None en lugar de una error tipo ValueError.

    """
    try:
        return tupla.index(valor)
    except ValueError:
        return None


class JugadorConecta4_original(juegos_cuadricula.JugadorNegamax):
    """
    Un jugador Negamax ajustado a el juego conecta 4, solamente hay que modificar dos métodos (o uno solo si no
    estamos preocupados por el tiempo de búsqueda: ordena y utilidad.

    """
    def __init__(self, tiempo_espera=10):
        """
        Inicializa el jugador limitado en tiempo y no en profundidad
        """
        juegos_cuadricula.JugadorNegamax.__init__(self, d_max=1)
        self.tiempo = tiempo_espera
        self.maxima_d = 20


    def ordena(self, juego, estado, jugador, jugadas):
        """
        Ordena las jugadas en función de las más prometedoras a las menos prometedoras. Por default regresa las
        jugadas en el mismo orden que se generaron.

        """
        #---------------------------------------------------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        #---------------------------------------------------------------------------------------------------------------
        shuffle(jugadas)
        return jugadas

    def utilidad(self, juego, estado):
        """
        El corazón del algoritmo, determina fuertemente la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)

        """
        #---------------------------------------------------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        #---------------------------------------------------------------------------------------------------------------
        val = juego.estado_terminal(estado)
        if val is None:
            return 0
        return val

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego, estado, jugador, juego.jugadas_legales(estado, jugador)),
                         key=lambda jugada: -self.negamax(juego,
                                                    estado=juego.hacer_jugada(estado, jugada, jugador),
                                                    jugador=-jugador,
                                                    alpha=-1e10,
                                                    beta=1e10,
                                                    profundidad=self.dmax))
            # print "A profundad ", self.dmax, " la mejor jugada es ", jugada
            self.dmax += 1
        return jugada

if __name__ == '__main__':

    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Conecta4(),
                                          juegos_cuadricula.JugadorHumano(),
                                          JugadorConecta4_orig(1),
                                          2)
    juego.arranca()

