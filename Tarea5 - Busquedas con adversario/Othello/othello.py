#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
othello.py
------------

El juego de Othello implementado por ustes mismos, con jugador inteligente

"""

__author__ = 'Manuel Valle'
"""
Tablero:
   .----.----   .----.----.----.----.   ----.----.
   | 0  |  1    |  2 |  3 |  4 |  5 |     6 |  7 |
   .----.----   .----.----.----.----.   ----.----.
   | 8  |  9    | 10 | 11 | 12 | 13 |    14 | 15 |

   .----.----   .----.----.----.----.   ----.----.
   | 16 | 17    | 18 | 19 | 20 | 21 |    22 | 23 |
   .----.----   .----.----.----.----.   ----.----.
   | 24 | 25    | 26 | 27 | 28 | 29 |    30 | 31 |
   .----.----   .----.----.----.----.   ----.----.
   | 32 | 33    | 34 | 35 | 36 | 37 |    38 | 39 |
   .----.----   .----.----.----.----.   ----.----.
   | 40 | 41    | 42 | 43 | 44 | 45 |    46 | 47 |

   .----.----   .----.----.----.----.   ----.----.
   | 48 | 49    | 50 | 51 | 52 | 53 |    54 | 55 |
   .----.----   .----.----.----.----.   ----.----.
   | 56 | 57    | 58 | 59 | 60 | 61 |    62 | 63 |
   .----.----   .----.----.----.----.   ----.----.

12
"""

#-----------------------------------------------------------------------------------------------------------------------
#              (60 puntos)
#          INSERTE AQUI SU CÓDIGO
#-----------------------------------------------------------------------------------------------------------------------
import juegos_cuadricula
import time
from random import shuffle
from othello_basico import JugadorOthello_basico

def capturar(estado, jugador, a, paso = +8, requerimientos_extras = lambda a,i: True):
    """
    Esta funcion muta la variable <estado> de manera que se reflejen las capturas
    realizadas
    Regresa False si no habrían capturas en la casilla <a> al jugar <jugador>.
    De lo contrario regresa la cantidad de fichas que se capturarían.
    """
    vecino_valido = lambda a,i: 0<= a+i <64 and requerimientos_extras(a,i)
    indices_a_capturar = []
    offset = paso

    while vecino_valido(a,offset) and estado[a+offset]==(-1*jugador):
        indices_a_capturar += [a+offset]
        offset += paso

    if offset!=paso and vecino_valido(a,offset) and estado[a+offset] == jugador:
        for indice in indices_a_capturar:
            estado[indice] = jugador
        return (offset/paso)-1
    else:
        return False

def hay_capturas(estado,jugador,a):
    """
    Regresa True or False dependiendo de si hay o no capturas disponibles para <jugador> en la casilla <a>.
    """
    e = list(estado) # Copia del estado sobre la que se intenta realizar una captura
    mismo_renglon = lambda a,i: a//8==(a+i)//8
    misma_diagonal_ascendente = lambda a,i: (a//8)+(a%8) == ((a+i)//8)+((a+i)%8)
    misma_diagonal_descendente = lambda a,i: (a//8)-(a%8) == ((a+i)//8)-((a+i)%8)
    """
    A_ren, A_col = a//8, a%8
    B_ren, B_col = (a+i)//8, (a+i)%8

    A_ren + A_col == B_ren + B_col   #misma diagonal ascendente
    A_ren - A_col == B_ren - B_col   #misma diagonal descendente
    """

    return (# Revision vertical
            capturar(e, jugador, a, -8) or 
            capturar(e, jugador, a, +8) or
            # Revision horizontal
            capturar(e, jugador, a, -1, requerimientos_extras = mismo_renglon) or
            capturar(e, jugador, a, +1, requerimientos_extras = mismo_renglon) or
            # Revisiones diagonales
            capturar(e, jugador, a, -9, requerimientos_extras = misma_diagonal_descendente) or
            capturar(e, jugador, a, +9, requerimientos_extras = misma_diagonal_descendente) or
            capturar(e, jugador, a, -7, requerimientos_extras = misma_diagonal_ascendente) or
            capturar(e, jugador, a, +7, requerimientos_extras = misma_diagonal_ascendente))

class Othello(juegos_cuadricula.Juego2ZT):
    """
    Othello / Reversi.

    """

    def __init__(self):
        """
        Inicializa el juego, esto es: el número de columnas y renglones y el estado inicial del juego.

                         0   1   2   3   4   5   6   7
                         8   9  10  11  12  13  14  15
                        16  17  18  19  20  21  22  23  
                        24  25  26  27  28  29  30  31  
                        32  33  34  35  36  37  38  39  
                        40  41  42  43  44  45  46  47
                        48  49  50  51  52  53  54  55
                        56  57  58  59  60  61  62  63
        """
        inicial = [0 for _ in xrange(64)]
        inicial[27] = inicial[36] = -1
        inicial[28] = inicial[35] = 1
        juegos_cuadricula.Juego2ZT.__init__(self, 8, 8, tuple(inicial))


    def jugadas_legales(self, estado, jugador, debug = False):
        casillas_libres = [i for i in range(64) if estado[i]==0]
        jugadas = filter(lambda i: hay_capturas(estado,jugador,i), casillas_libres)
        #jugadas = [i for i in indices if hay_capturas(estado,jugador,i)] #ToDelete
        if debug:
            print "Jugador:", jugador
            print "Estado: ",estado
            print "Jugadas legales: ", jugadas #ToDelete
        #assert jugadas == [19,26,37,44]
        return [(None, jugada) for jugada in jugadas]

    def estado_terminal(self, estado):
        """
        Devuelve 1 si el estado es final y gana el jugador 1,
                -1 si el estado es final y gana el jugador -1,
                 0 si es terminal y hay empate
                 None si el estado no es terminal

        """
        jugadorA = estado.count(1)
        jugadorB = estado.count(-1)

        if jugadorA+jugadorB!=64 or self.jugadas_legales(estado, 1) or self.jugadas_legales(estado, -1):
            return None
        elif jugadorA==jugadorB:
            return 0
        else:
            return 1 if jugadorA>jugadorB else -1
        
    def hacer_jugada(self, estado, jugada, jugador):
        """
        Devuelve estado_nuevo que es el estado una vez que se realizó la jugada por el jugador.
        Hay que recordar que los juegos de tablero los estamos estandarizando para jugadas las cuales
        son (p_ini, p_final) donde p_ini esla posicion inicial y p_final es la posicion final de una ficha.

        Si el juego solamente implica poner fichas entonces p_ini no se toma en cuenta pero si tiene que ir para
        guardar homogeneidad entre los diferentes juegos y los diferentes métodos que desarrollaremos.

        """
        e = list(estado)
        _, a = jugada
        mismo_renglon = lambda a,i: a//8==(a+i)//8
        misma_diagonal_ascendente = lambda a,i: (a//8)+(a%8) == ((a+i)//8)+((a+i)%8)
        misma_diagonal_descendente = lambda a,i: (a//8)-(a%8) == ((a+i)//8)-((a+i)%8)

        # Realizar capturas verticales
        capturar(e, jugador, a, -8),
        capturar(e, jugador, a, +8)

        # Realizar capturas horizontales
        capturar(e, jugador, a, -1, requerimientos_extras = mismo_renglon) 
        capturar(e, jugador, a, +1, requerimientos_extras = mismo_renglon) 

        # Realizar capturas diagonales
        capturar(e, jugador, a, -9, requerimientos_extras = misma_diagonal_descendente)
        capturar(e, jugador, a, +9, requerimientos_extras = misma_diagonal_descendente)
        capturar(e, jugador, a, -7, requerimientos_extras = misma_diagonal_ascendente)
        capturar(e, jugador, a, +7, requerimientos_extras = misma_diagonal_ascendente)
        e[a] = jugador
        return tuple(e)

class JugadorOthello(juegos_cuadricula.JugadorNegamax):
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
        jugadas_ord = []
        for _, j in jugadas:
            estado_aux = list(estado)
            estado_aux[j] = jugador
            valor = len(juego.jugadas_legales(estado_aux, jugador))

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
        def casillas_deseables(estado, casillas):
            casillas = map(lambda c: estado[c], casillas)
            return casillas.count(1) - casillas.count(-1) 

        def casillas_no_deseables(estado, casillas):
            return -1*casillas_deseables(estado, casillas)

        val = juego.estado_terminal(estado)
        if val is None:
            w1 = 100.0
            w2 = 100.0
            w3 = 20.0
            
            x_squares = [9,14,49,54]
            corners = [0,7,56,63]
            edges = [1,2,3,4,5,6, 8,16,24,32,40,48, 15,23,31,39,47,55,  57,58,59,60,61,62 ]

            return (w1*casillas_no_deseables(estado, x_squares) +
                    w2*casillas_deseables(estado, corners) + 
                    w3*casillas_deseables(estado, edges))
        return val

    def decide_jugada(self, juego, estado, jugador, tablero):
        self.dmax = 0
        t_ini = time.time()
        while time.time() - t_ini < self.tiempo and self.dmax < self.maxima_d:
            jugada = max(self.ordena(juego, estado, jugador, juego.jugadas_legales(estado, jugador)),
                         key=lambda jugada: -self.negamax(juego,
                                                    estado=juego.hacer_jugada(estado, jugada, jugador),
                                                    jugador=-jugador,
                                                    alpha=float("-inf"),
                                                    beta=float("inf"),
                                                    profundidad=self.dmax))
            #print "A profundad ", self.dmax, " la mejor jugada es ", jugada
            self.dmax += 1
        print "Se llego al nivel ", self.dmax
        return jugada


if __name__ == '__main__':
    # Ejemplo donde empieza el jugador humano
    juego = juegos_cuadricula.InterfaseTK(Othello(),
                                          #JugadorOthello_basico(1),
                                          JugadorOthello(1),
                                          juegos_cuadricula.JugadorHumano(), #JugadorOthello(1),
                                          #juegos_cuadricula.JugadorHumano(), #JugadorOthello(1),
                                          1)
    juego.arranca()