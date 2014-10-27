#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lightsout.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""
__author__ = 'Manuel Valle'


from busquedas import *
import heapq

def get_vecindad(a):
    # Devuelve una lista con los indices de la vecindad afectada por la accion a
    N = 5 # Board side size
    if a<0 or a>=N*N:
        return []
    vecinos = [a]

    for i in (-1, 1): # First checks up and left, then down and right
        if 0 <= a + i*N < N*N: # To check up/down 
            vecinos.append(a+i*N)
        if (a+i)%N == (a%N)+i: # To check left/right 
            vecinos.append(a+i)
    return vecinos

class Lights_out(ProblemaBusqueda):
#---------------------------------------------------------------
# Problema 1 (25 puntos): Desarrolla la clase para el problema de lights out
#
#---------------------------------------------------------------

    """
    Problema del jueguito "Ligths out".

    La idea del juego es el apagar o prender todas las luces.
    Al seleccionar una casilla, la casilla y sus casillas adjacentes cambian
    (si estan prendidas se apagan y viceversa). El juego consiste en una matriz
    de 5 X 5, cuyo estado puede ser apagado 0 o prendido 1. Por ejemplo el estado

       (0,0,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0)

    corresponde a:

    ---------------------
    |   |   | X |   |   |
    ---------------------
    | X | X |   |   | X |
    ---------------------
    |   |   | X | X |   |
    ---------------------
    | X |   | X |   | X |
    ---------------------
    |   |   |   |   |   |
    ---------------------
    
    Las acciones posibles son de elegir cambiar una luz y sus casillas adjacentes, por lo que la accion es
    un número entre 0 y 24.

    Para mas información sobre el juego, se puede consultar

    http://en.wikipedia.org/wiki/Lights_Out_(game)

    """
    def __init__(self, pos_inicial):
        # ¡El formato y lo que lleva la inicialización de la super hay que cambiarlo al problema!
        super(Lights_out, self).__init__(pos_inicial, lambda s: s.count(1) == 0)
        self.acciones = range(5*5)

    def acciones_legales(self, state):
        return self.acciones

    def sucesor(self, state, action):
        # version ofuscada:
        # return tuple([state[j] if j not in filter(lambda i: i>=0 and i<5*5, [action-5, action, action+5] + [action+i for i in (-1, +1) if (action+i)%5==(action%5)+i]) else (state[j]+1)%2 for j in range(5*5)])
        
        N = 5 # size of the board side
        a = action # for readability
        
        new_state = list(state)
        afectados = get_vecindad(action)
        for i in afectados:
            new_state[i] = (new_state[i]+1)%2

        return tuple(new_state)
        
    def costo_local(self, estado, accion):
        return 1

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        cadena = ".-------------------.\n"
        for i in range(5):
            for j in range(5):
                if estado[5 * i + j]:
                    cadena += "| X "
                else:
                    cadena += "|   "
            cadena += "|\n.-------------------.\n"
        return cadena


#-------------------------------------------------------------------------------------------------
# Problema 2 (25 puntos): Desarrolla el método de búsqueda de A* siguiendo las especificaciones de la función 
#
# RESUELVE ESTE PROBLEMA EN EL OCHO_PUZZLE Y LUEGO SIMPLEMENTE COPIALA, YA QUE LAS HEURÍSTICAS SON 
# MUY DIFICILES PARA ESTE PROBLEMA
#-------------------------------------------------------------------------------------------------
def busqueda_A_estrella(problema, heuristica):
    """
    Búsqueda A*

    @param problema: Un objeto de una clase heredada de ProblemaBusqueda
    @param heuristica: Una funcion de heuristica, esto es, una función heuristica(nodo), la cual devuelva´<x}
                       objetivo.

    @return Un objeto tipo Nodo con la estructura completa
    
    """
    frontera = []
    heapq.heappush(frontera, (0, Nodo(problema.s0)))
    visitados = {problema.s0: 0}
    
    while frontera:
        (_, nodo) = heapq.heappop(frontera)
        if problema.es_meta(nodo.estado):
            nodo.nodos_visitados = problema.num_nodos
            return nodo
        for hijo in nodo.expande(problema):
            if hijo.estado not in visitados or visitados[hijo.estado] > hijo.costo:
                heapq.heappush(frontera, (hijo.costo+heuristica(hijo), hijo))
                visitados[hijo.estado] = hijo.costo
    return None


def prueba_clase():
    """
    Prueba la clase Lights_out
    
    """
    
    
    pos_ini = (0, 1, 0, 1, 0,
               0, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a0 =  (1, 0, 0, 1, 0,
               1, 0, 1, 1, 0,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a4 =  (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 1,
               0, 0, 0, 1, 1)

    pos_a24 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               0, 0, 0, 1, 1,
               0, 0, 1, 1, 0,
               0, 0, 0, 0, 0)

    pos_a15 = (1, 0, 0, 0, 1,
               1, 0, 1, 1, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 1, 0,
               1, 0, 0, 0, 0)

    pos_a12 = (1, 0, 0, 0, 1,
               1, 0, 0, 1, 1,
               1, 1, 1, 0, 1,
               1, 1, 0, 1, 0,
               1, 0, 0, 0, 0)


    entorno = Lights_out(pos_ini)
"""
    print "Prueba 1: "
    assert entorno.acciones_legales(pos_ini) == range(25)
    print "Prueba 2: "
    print "     entorno.acciones_legales(pos_ini, 0): ", entorno.sucesor(pos_ini, 0)
    print "                                   pos_a0: ", pos_a0
    assert entorno.sucesor(pos_ini, 0) == pos_a0
    print "Prueba 3: "
    assert entorno.sucesor(pos_a0, 4) == pos_a4
    print "Prueba 4: "
    assert entorno.sucesor(pos_a4, 24) == pos_a24
    print "Prueba 5: "
    assert entorno.sucesor(pos_a24, 15) == pos_a15
    print "Prueba 6: "
    assert entorno.sucesor(pos_a15, 12) == pos_a12
    print "Paso la prueba de la clase"
"""
def prueba_busqueda(pos_inicial, metodo, heuristica=None, max_prof=None):
    """
    Prueba un método de búsqueda para el problema del ligths out.

    @param pos_inicial: Una tupla con una posicion inicial
    @param metodo: Un metodo de búsqueda a probar
    @param heuristica: Una función de heurística, por default None si el método de búsqueda no requiere heuristica
    @param max_prof: Máxima profundidad para los algoritmos de DFS y IDS.

    @return nodo: El nodo solución

    """
    if heuristica:
        return metodo(Lights_out(pos_inicial), heuristica)
    elif max_prof:
        return metodo(Lights_out(pos_inicial), max_prof)
    else:
        return metodo(Lights_out(pos_inicial))


def compara_metodos(pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución de varios métodos de búsqueda

    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    @return None (no regresa nada, son puros efectos colaterales)

    Si la búsqueda no informada es muy lenta, posiblemente tendras que quitarla de la función
    """
    print '\n\n' + '-' * 50
    print u'Método'.center(10) + 'Costo de la solucion'.center(20) + 'Nodos explorados'.center(20)
    print '-' * 50

    #n1 = prueba_busqueda(pos_inicial, busqueda_ancho)
    #print 'BFS'.center(10) + str(n1.costo).center(20) + str(n1.nodos_visitados)
    
    #n2 = prueba_busqueda(pos_inicial, busqueda_profundidad_iterativa)
    #print 'IDS'.center(10) + str(n2.costo).center(20) + str(n2.nodos_visitados)
    
    #n3 = prueba_busqueda(pos_inicial, busqueda_costo_uniforme)
    #print 'UCS'.center(10) + str(n3.costo).center(20) + str(n3.nodos_visitados)
    
    #n4 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_1)
    #print 'A* con h1'.center(10) + str(n4.costo).center(20) + str(n4.nodos_visitados)
    
    n5 = prueba_busqueda(pos_inicial, busqueda_A_estrella, heuristica_2)
    print 'A* con h2'.center(10) + str(n5.costo).center(20) + str(n5.nodos_visitados)
    
    print ''
    print '-' * 50 + '\n\n'

if __name__ == "__main__":

    print "Antes de hacer otra cosa vamos a verificar medianamente la clase Lights_out"
    prueba_clase()



#-------------------------------------------------------------------------------------------------
# Problema 3 (25 puntos): Desarrolla una política admisible. 
#-------------------------------------------------------------------------------------------------
    def h_1(nodo):
        """
        DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
        LA HEURÍSTICA ES ADMISIBLE

        """
        """
        # En cada movimiento se arreglan (i.e. pasan de 1 a 0) máximo 5 casillas.

        # Por lo tanto, si dividimos la cantidad de unos en el tablero sobre 5 obtenemos el minimo
        # de movimientos necesarios para resolverlo. (Ademas de que h_1(meta) devuelve 0. i.e. la heuristica es admisible)

        # Es demasiado optimista. Por lo general no se arreglan 5 casillas por movimiento, e incluso
        # algunos se vuelven a prender, de manera que la cantidad de pasos real puede ser mucho mayor
        # asi que no es muy buena.
        # Uso flotantes para aprovechar su precision  
        """
        estado = nodo.estado
        num_unos = estado.count(1)
        return num_unos/5.0

#-------------------------------------------------------------------------------------------------
# Problema 4 (25 puntos): Desarrolla otra política admisible. 
# Analiza y di por qué piensas que es (o no es) dominante una respecto otra política
#-------------------------------------------------------------------------------------------------
    def h_2(nodo):
        """
        DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN PLATICADA DE PORQUÉ CREES QUE
        LA HEURÍSTICA ES ADMISIBLE

        """
        """
        Esta medio raro de explicar. 
        Primero tenemos que imaginar que el tablero se encuentra sobre una dona, de manera que están
        conectados los cuadros de arriba con los de abajo y los de la derecha con los de la izquierda.

        Tambien imaginemos que al aplicar una accion 'a' sobre el tablero, en lugar de 'switchear' el valor
        de 'a' y sus vecinos, los convirtiera a todos en 0. Osea que las acciones solo apagaran luces
        y no las prendieran.

        Hay que tomar en cuenta que el alcance de una acción es de 5 casillas, y que el tablero tiene 25, 
        así que el minimo de acciones que necesitamos para llenar el tablero es el dado por casillas_por_turno/total_casillas
        que en este caso es 5/25 = 5. Al menos 5 movimiento.

        Queda la duda de si en verdad se puede afectar todo el tablero solo con 5 acciones. 
        Resulta que en la versión normal no se puede, pero en la versión dona (relajada) si se puede.
        Yo argumento que no sólo si se puede, si no que existen exactamente 10 diferentes configuraciones 
        (conjuntos de 5 acciones) que cumplen lo ya mencionado. 
        No voy a probarlo completamente, daré .
                .-------------------.
                | Xa| a | b | e | a |
                .-------------------.
                | a | b | Xb| b | c |   Algo así es a lo que me refiero con 
                .-------------------.   "5 acciones de afecten todo el tablero dona".
                | c | d | b | c | Xc|   Las casillas con Xi son las 5 casillas donde 
                .-------------------.   se realizan las acciones, y las casillas i son 
                | d | Xd| d | e | c |   las demás afectadas por la acción Xi:
                .-------------------.
                | a | d | e | Xe| e |
                .-------------------.

        En estas 10 configuraciones podemos ver 3 configuraciones con patrones realmente diferentes entre sí, 
        ademas de todas las rotaciones de 2 de ellas y el reflejo de otra.



        Y los 10 patrones que decía antes son los siguientes:

        .-------------------.           .-------------------.           .-------------------.
        | X |   |   |   |   |           | X |   |   |   |   |           |   |   |   | X |   |
        .-------------------.           .-------------------.           .-------------------.
        |   |   | X |   |   |           |   |   |   | X |   |           | X |   |   |   |   |
        .-------------------.           .-------------------.           .-------------------.
        |   |   |   |   | X |           |   | X |   |   |   |           |   |   | X |   |   |
        .-------------------.           .-------------------.           .-------------------.
        |   | X |   |   |   |           |   |   |   |   | X |           |   |   |   |   | X |
        .-------------------.           .-------------------.           .-------------------.
        |   |   |   | X |   |           |   |   | X |   |   |           |   | X |   |   |   |
        .-------------------.           .-------------------.           .-------------------.
        y sus 3 rotaciones               y sus 3 rotaciones              y su reflejo (horizontal, 
                                                                         vertical, diagonal, da igual)

        
        También se ve padre si sobre cada X dibujamos una cruz que pase por las 5 casillas que afecta X
                              |   
        que se vea tipo    ---x---    Da la impresión de que hubiera un gran patron de cruces y cada una de las
                              |       configuraciones es una manera de elegir un segmento de 5x5 de ese patrón.

        
        Gracias a esa manera de visualizarlo saqué el siguiente rectangulo de 9x5
        del cual se pueden sacar 5 de las 10 configuraciones:
            .-----------------------------------.
            |   |   |   | X |   |   |   |   | X |
            .-----------------------------------.
            | X |   |   |   |   | X |   |   |   |
            .-----------------------------------.
            |   |   | X |   |   |   |   | X |   |
            .-----------------------------------.
            |   |   |   |   | X |   |   |   |   |
            .-----------------------------------.
            |   | X |   |   |   |   | X |   |   |
            .-----------------------------------.

        Y de este otro las otras 5:
            .-----------------------------------.
            |   | X |   |   |   |   | X |   |   |
            .-----------------------------------.
            |   |   |   |   | X |   |   |   |   |
            .-----------------------------------.
            |   |   | X |   |   |   |   | X |   |
            .-----------------------------------.
            | X |   |   |   |   | X |   |   |   |
            .-----------------------------------.
            |   |   |   | X |   |   |   |   |  X |
            .-----------------------------------.
        
        En fin, esas son curiosidades con las que me topé, pero me sirvió para calcular las
        10 configuraciones en lugar de escribirlas a mano. Dejó más abajo comentado el código
        con el que las saqué.

        Entonces, al resolver el juego lo que en realidad nos interesa no es tanto el cómo 
        afectar a todo el tablero, sino como afectar a unas cuantas casillas (aquellas con 1).
        Y como las configuraciones de arriba son las mejores (manera de distribuir las acciones), 
        entonces la configuración minima de acciones que tenemos realizar para resolver un problema
        específico (en la versión relajada) debe de ser un subconjunto de alguna de las 10 configuraciones de arriba.

        Entonces, cuento para cada una de las 10 configuraciones cuantos de sus elementos (i.e. acciones) se necesitan
        para resolver la versión relajada del problema. Entonces selecciono la menor de todas.

        Básicamente es una heuristica con un espiritu parecido al de la h_1, pero que toma en cuenta no sólo la cantidad
        de 1's en el tablero, sino que tambien se fija en su distribución. Por lo tanto, h_2 es dominante sobre h_1

        Como notas finales, creo que la parte de plasmar el tablero sobre una dona se convierte en
        una desventaja al momento de tener tableros con situaciones como la siguiente:

        .-------------------.
        | 1 | 1 |   |   | 1 |
        .-------------------.
        |   |   |   |   |   |
        .-------------------.
        | 1 |   |   |   | 1 |
        .-------------------.
        |   |   |   |   | 1 |
        .-------------------.
        | 1 |   |   |   |   |
        .-------------------.           
        ( <--# ) 

        En donde en el problema relajado versión dona se ocupan solo 2 acciones, pero en el relajado
        normal se necesitan al menos 4.

        [
                                          .-------------------.
            La X marcan las acciones      | X |   |   |   |   |
            que se necesitarían realizar  .-------------------.
            en el tablero de arriba.      |   |   | o |   |   |
            Las 'o' son el resto de       .-------------------.
            las acciones que forman       |   |   |   |   | x |
            Las X son acciones.           .-------------------.
            Las 'X' y las 'o' forman      |   | o |   |   |   |
            la configuración comentada    .-------------------.
            la linea 340                  |   |   |   | o |   |
                                          .-------------------.
        ]


        Entonces h_2 se ve perjudicado en cierta manera por ser tan relajado en ese aspecto, sin
        embargo me sirvió para pensar las cosas.

        Una posible forma de mejorar la heuristica sería buscar como desrelajarla en ese aspecto.
        Dejo el siguiente codice sin mucha explicación pues en escencia aplico lo descrito arriba.
        """
        estado = nodo.estado
        configs = [[0, 7, 14, 16, 23],
                   [0, 8, 11, 19, 22],
                   [1, 8, 10, 17, 24],
                   [1, 9, 12, 15, 23],
                   [2, 9, 11, 18, 20],
                   [2, 5, 13, 16, 24],
                   [3, 5, 12, 19, 21],
                   [3, 6, 14, 17, 20],
                   [4, 6, 13, 15, 22],
                   [4, 7, 10, 18, 21]]
        """
        # Como sacar lo de arriba ^
        configs = []
        for i in range(5):
            # los valores de cada pi son un valor base 
            # (dado por una config inicial arbitraria) 
            # más un aumento que esta en los enteros en [0, 4]
            # (va 'dando vueltas' sobre un renglón, para simular los rectángulos de 9x5 mencionados arriba)

            p0  = (0 + i%5) 
            p1  = (5 + (2+i)%5)
            p2 = (10 + (4+i)%5) 
            p3 = (15 + (1+i)%5)
            p4 = (20 + (3+i)%5)
            config = [p0,p1,p2,p3,p4]
            configs.append(config)

            p0  = (0 + i%5)
            p1  = (5 + (3+i)%5)
            p2 = (10 + (1+i)%5)
            p3 = (15 + (4+i)%5)
            p4 = (20 + (2+i)%5)
            config = [p0,p1,p2,p3,p4]
            configs.append(config)
            """

        #configs tiene las 10 configuraciones a probar
        
        def se_apaga(estado, a):
            # Devuelve True si hay algun 1 afectado por la accion a
            for i in get_vecindad(a):
                if estado[i] == 1:
                    return True
            return False


        min_general = float("inf")
        for conf in configs:
            tot_apagados = map(lambda i: se_apaga(estado, i), conf).count(True)
            min_general = min(min_general, tot_apagados)
        return min_general

    diagonal = (0, 0, 0, 0, 1,
                0, 0, 0, 1, 0,
                0, 0, 1, 0, 0,
                0, 1, 0, 0, 0,
                1, 0, 0, 0, 0)

    simetria = (1, 0, 1, 0, 1,
                1, 0, 1, 0, 1,
                0, 0, 0, 0, 0,
                1, 0, 1, 0, 1,
                1, 0, 1, 0, 1)

    problemin = (0, 1, 0, 1, 0,
                 0, 0, 1, 1, 0,
                 0, 0, 0, 1, 1,
                 0, 0, 1, 1, 1,
                 0, 0, 0, 1, 1)

    print u"\n\nVamos a ver como funcionan las búsquedas para el ejemplo 'diagonal'"
    print "\n" + Lights_out.bonito(diagonal)
    compara_metodos(diagonal, h_1, h_2)

    print u"\n\nVamos a ver como funcionan las búsquedas para el ejemplo 'simetria'"
    print "\n" + Lights_out.bonito(simetria)
    compara_metodos(simetria, h_1, h_2)
    
    print u"\n\nVamos a ver como funcionan las búsquedas para el ejemplo 'problemin'"
    print "\n" + Lights_out.bonito(problemin)
    compara_metodos(problemin, h_1, h_2)
    
