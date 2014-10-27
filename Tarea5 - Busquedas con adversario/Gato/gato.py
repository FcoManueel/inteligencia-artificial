#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gato.py
------------

Ejemplo de juego con el clasico juego del gato

"""

__author__ = 'juliowaissman'


import juegos_cuadricula


class Gato(juegos_cuadricula.Juego2ZT):

    def __init__(self):
        juegos_cuadricula.Juego2ZT.__init__(self, 3, 3, tuple([0 for _ in range(9)]))

    def jugadas_legales(self, estado, jugador):
        return [(None, i) for i in range(9) if estado[i] == 0]

    def estado_terminal(self, estado):
        e = estado
        if e[4] != 0 and (e[0] == e[4] == e[8] or e[2] == e[4] == e[6]):
            return e[4]
        for i in range(3):
            if e[i] != 0 and e[i] == e[i + 3] == e[i + 6]:
                return e[i]
            if e[3 * i] != 0 and e[3 * i] == e[3 * i + 1] == e[3 * i + 2]:
                return e[3 * i]
        if 0 not in e:
            return 0
        return None

    def hacer_jugada(self, estado, jugada, jugador):
        e = list(estado)
        e[jugada[1]] = jugador
        return tuple(e)


if __name__ == '__main__':

    # Ejemplo donde empieza el jugador humano
    #juego = juegos_cuadricula.InterfaseTK(Gato(),
    #                                       juegos_cuadricula.JugadorHumano(),
    #                                       juegos_cuadricula.JugadorNegamax(),
    #                                       2)

    # Ejemplo donde empieza el jugador Negamax
    juego = juegos_cuadricula.InterfaseTK(Gato(),
                                          juegos_cuadricula.JugadorNegamax(),
                                          juegos_cuadricula.JugadorHumano(),
                                          2)

    #juego = juegos_cuadricula.InterfaseTK(Gato(),
    #                                      juegos_cuadricula.JugadorNegamax(),
    #                                      juegos_cuadricula.JugadorNegamax(),
    #                                      2)
    juego.arranca()
