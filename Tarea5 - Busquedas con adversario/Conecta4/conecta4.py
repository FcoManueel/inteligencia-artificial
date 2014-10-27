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
from conecta4_original import JugadorConecta4_original

class Conecta4(juegos_cuadricula.Juego2ZT):
    """
    Juego del conecta 4 utilizando la definición de juego utilizada en la clase juego_cuadricula.JuegoT2ZT.
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
        
        self.combinaciones_tablero = []
        for combinaciones in self.combinaciones.values():
            for c in combinaciones:
                if c not in self.combinaciones_tablero:
                    self.combinaciones_tablero.append(c)


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


class JugadorConecta4(juegos_cuadricula.JugadorNegamax):
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


    def ordena(self, juego, estado, jugador, jugadas, debug=False):
        """
        Ordena las jugadas en función de las más prometedoras a las menos prometedoras. Por default regresa las
        jugadas en el mismo orden que se generaron.

        """
        #---------------------------------------------------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        #---------------------------------------------------------------------------------------------------------------
        jugadas_ord = []
        for _, j in jugadas:
            valor = 0
            for linea in juego.combinaciones[j]:
                linea = map(lambda i: estado[i] , linea)
                if linea.count(jugador)==3:
                    valor += float("inf")
                elif linea.count(-1*jugador)==3:
                    valor += 1000
                elif -1*jugador not in linea:
                    valor += (linea.count(jugador)+1)**2
            i = 0
            while i<len(jugadas_ord) and jugadas_ord[i][0] > valor:
                i += 1
            jugadas_ord.insert(i, (valor, j))
        jugadas_ord = [(None, j) for _, j in jugadas_ord]
        if debug:
            print "ordena()--------------------------------------"
            print "orig: ", jugadas
            print "orde: ", jugadas_ord
            print "fin ordena()----------------------------------"
        return jugadas_ord

        #shuffle(jugadas)
        #return jugadas

    def utilidad(self, juego, estado):
        """
        (función de evaluación de tablero)
        El corazón del algoritmo, determina fuertemente la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)

        """
        #---------------------------------------------------------------------------------------------------------------
        #                             (20 puntos)
        #                        INSERTE SU CÓDIGO AQUÍ
        #---------------------------------------------------------------------------------------------------------------
        def criterio(estado, n):
            """
            Contar cuantas lineas de n fichas hay para cada jugador (tal que esa linea de n
            fichas se pueda convertir en una de 4).

            """
            """
            El diccionario "combinaciones" tiene todas las 4-lineas que pasan por una casilla
            dada. En este caso no es lo más útil, nos serviría más saber todas las 4-lineas del
            tablero. (Como cada 4-linea pasa por 4 casillas, dicha 4-linea se encuentra repetida 
            4 veces en el diccionario).
            Por eso agregué al juego una lista de listas llamado combinaciones_tablero, la cual
            no contiene repeticiones
            """
            # una tres_linea es 
            n_linea_a = 0
            n_linea_b = 0
            for combinacion in juego.combinaciones_tablero:
                linea = map(lambda i: estado[i] , combinacion)
                if linea.count(1) == n and -1 not in linea:
                    n_linea_a += 1
                if linea.count(-1) == n and 1 not in linea:
                    n_linea_b += 1
            return n_linea_a - n_linea_b

        val = juego.estado_terminal(estado)
        if val is None:
            w1 = 0.0
            w2 = 4.0
            w3 = 9.0
            w4 = float("inf")
            utilidad = w1*criterio(estado, 1) + w2*criterio(estado, 2) + w3*criterio(estado, 3) + w4*criterio(estado, 4)
            return utilidad
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
            #print "A profundad ", self.dmax, " la mejor jugada es ", jugada
            self.dmax += 1
        print "Se llego al nivel ", self.dmax
        return jugada

if __name__ == '__main__':

    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Conecta4(),
                                          JugadorConecta4(1),
                                          #juegos_cuadricula.JugadorHumano(), #JugadorConecta4(1),#juegos_cuadricula.JugadorHumano(), #JugadorConecta4(1), #
                                          #juegos_cuadricula.JugadorHumano(), #JugadorConecta4(1),#juegos_cuadricula.JugadorHumano(), #JugadorConecta4(1), #
                                          JugadorConecta4_original(5),
                                          2)
    juego.arranca()
    # REVISAR COMO AGREGAR UN JugadorConecta4_orig AL JUEGO (PARA COMPARAR)

