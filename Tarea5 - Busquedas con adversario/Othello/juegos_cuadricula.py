#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
juegos_cuadricula.py
------------

Modulo para la implementación de una clase de juegos de cuadrícula.

Se asumen juegos de cuadricula, totalmente observables, de dos jugadores, por turnos

"""

__author__ = 'juliowaissman'

from tkMessageBox import showinfo
import Tkinter as tk


class Juego2ZT:
    """
    Juego de tablero para dos jugadores, de suma cero, por turnos.

    Esta es una clase para ser implementada por cada juego en particular.

    Cada metodo aqui hay que implementarlo para un juego en específico. Recuerda TODOS los métodos (incluido __init__)
    hay que implementarlo para cada juego específico.

    Como ejemplo, con el fin de dejar mas claro lo que hay que hacer aqui, se incluye el juego del gato como
    juego por default. Toma en cuenta que el juego del gato es extremadamente simple y tu juego será algo mas
    complicado siempre.

    """

    def __init__(self, columnas, renglones, estado_inicial):
        """
        Inicializa el juego, esto es: el número de columnas y renglones y el estado inicial del juego.

        El estado del juego es una lista de dimensión columnas * renglones, donde la numeración es de la
        siguiente forma: (por ejemplo para un juego de 4 columnas y 3 renglones)


                        0   1   2   3
                        4   5   6   7
                        8   9  10  11

        Los valores que pueden tomar cada una de las variables de estado son valores enteros, que si son positivos
        son del jugador del primer turno, y si son negativos son del jugador del segundo turno. Si el juego es un juego
        de fichas simples como el gato, entonces los valores de 1 y -1 son suficientes. En juegos como las damas,
        es necesario utilizar valores como -2, -1, 1, 2. Si el valor de una variable es 0, significa que esa casilla no
        está ocupada por ningun jugador.

        Solo hay dos jugadores: 1 (el primero en jugar en turnos) y -1 (el último en jugar).

        """
        self.columnas = columnas
        self.renglones = renglones
        self.estado_inicial = estado_inicial

    def jugadas_legales(self, estado, jugador):
        """
        Devuelve una lista con jugadas legales que puede hacer un jugador. Es muy importante especificar
        como son las jugadas legales.

        Las jugadas legales son una tupla (p_ini, p_final) donde p_ini es la posicion de la ficha que puede
        ser movida y p_final es la posición de la ficha despues de moverla. Si la tupla es (None, p_final) significa
        que es una ficha nueva la que se agrega.

        Si la función devuelve [] es que no hay ninguna jugada posible. Si devuelve [(None,None)] es que hay una jugada
        que aplicar, la cual es pasar.

        """
        pass

    def estado_terminal(self, estado):
        """
        Devuelve 1 si el estado es final y gana el jugador 1,
                -1 si el estado es final y gana el jugador -1,
                 0 si es terminal y hay empate
                 None si el estado no es terminal

        """
        pass

    def hacer_jugada(self, estado, jugada, jugador):
        """
        Devuelve estado_nuevo que es el estado una vez que se realizó la juagada por el jugador.
        Hay que recordar que los juegos de tablero los estamos estandarizando para jugadas las cuales
        son (pini, pfinal) donde pini esla posicion inicial y pfinal es la posicion final de una ficha.

        Si el juego solamente implica poner fichas entonces pini no se toma en cuenta pero si tiene que ir para
        guardar homogeneidad entre los diferentes juegos y los diferentes métodos que desarrollaremos.

        """
        pass


class InterfaseTK:
    """
    Clase para implementar cualquier juego de tablero con fichas rojas y negras. Por el momento solo se tienen
    contempladas las imagenes para fichas -2, -1, 0, 1, 2, pero se espera poder hacer otro tipo de fichas tambien

    """
    def __init__(self, juego, jugador1, jugador2, escala):
        """
        Inicializa un tablero utilizando TKInter donde

        @param juego: Juego derivado de la clase abstracta Juego2ZT
        @param jugador1: Objeto derivado de JugadorInterfaseTK
        @param jugador2: Objeto derivado de JugadorInterfaseTK
        @param escala: Escala a la que se ve el juego (depende de las imágenes).

        """
        self.juego = juego
        self.jugadores = {1: jugador1, -1: jugador2}

        color_scheme = ['default', 'greenish'][1]

        if color_scheme == 'greenish':
            self.color_tablero = ['forest green', 'yellow green']
            self.color_fichas = [None, 'black', 'gray20', 'gray80', 'white']
        else: # if color_scheme = 'default'
            self.color_tablero = ['dark grey', 'light grey']
            self.color_fichas = [None, 'light blue', 'DeepSkyBlue1', 'DarkRed', 'red']



        self.root = tk.Tk()
        self.L = L = int(escala) * 50

        self.barra = tk.Frame(self.root)
        self.barra.pack()

        self.boton = tk.Button(self.barra, text='Presiona para iniciar un juego')
        self.boton.pack()
        self.boton.configure(command=self.inicia_juego)

        self.tableroCanvas = tk.Frame(self.root)
        self.tableroCanvas.pack()

        n, m = juego.renglones, juego.columnas
        self.tablero = [None for _ in range(n * m)]
        for i in range(n * m):
            color = self.color_tablero[0] if (i // m + i % m) % 2 == 0 else self.color_tablero[-1]
            self.tablero[i] = tk.Canvas(self.tableroCanvas, height=L, width=L, bg=color,
                                        borderwidth=0, highlightbackground=color,
                                        highlightcolor=color)
            self.tablero[i].grid(row=int(i / m), column=i % m)
            self.tablero[i].id = None
            self.tablero[i].pos = i

            if juego.estado_inicial[i] != 0:
                color = self.color_fichas[juego.estado_inicial[i]]
                self.tablero[i].id = self.tablero[i].create_oval(5, 5, L, L, fill=color)
                self.tablero[i].update()
            #self.tablero[i].itemconfig(self.tablero[i].create_text(L/2, L/2, anchor="center", fill="light goldenrod"), text=str(i))

    def arranca(self):
        """
        Inicia con el juego

        """
        self.root.mainloop()

    def inicia_juego(self, max_pasos=150):
        """
        Desarrolla el juego por pasos de cada jugador

        """
        estado = self.juego.estado_inicial
        estado_anterior = estado
        self.actualiza_tablero(estado)
        
        jugador = -1 # Esta variable empieza como -1, pero el primer jugador es 1
        for paso in range(max_pasos):
            jugador = -jugador
            if not self.juego.jugadas_legales(estado, jugador):
                #print "El jugador ",jugador,"se quedo sin jugadas" #ToDelete
                jugador = -jugador


            #print [j for _, j in self.juego.jugadas_legales(estado, jugador)] #ToDelete

            jugada = self.jugadores[jugador].decide_jugada(self.juego, estado, jugador, self.tablero)
            estado = self.juego.hacer_jugada(estado, jugada, jugador)
            self.actualiza_tablero(estado, estado_anterior)
            resultado = self.juego.estado_terminal(estado)
            if resultado is not None:
                showinfo("Fin de juego", ['Meh... un vil empate', '¡Negras ganan!', '¡Blancas ganan!'][resultado])
                return resultado
            estado_anterior = estado
        showinfo("Fin de juego", 'SE ACABO EL JUEGO POR AGOTAMIENTO, ASI QUE SE TOMA COMO EMPATE')
        return 0

    def actualiza_tablero(self, estado, estado_anterior=None):
        """
        Actualiza la visualización del tablero

        """
        if estado_anterior is None:
            actualizables = range(len(estado))
        else:
            actualizables = [i for i in range(len(estado)) if estado[i] != estado_anterior[i]]

        for i in actualizables:
            if self.tablero[i].id:
                self.tablero[i].delete(self.tablero[i].id)
                self.tablero[i].id = None
                self.tablero[i].update()
            if estado[i] != 0:
                color = self.color_fichas[estado[i]]
                self.tablero[i].id = self.tablero[i].create_oval(5, 5, self.L, self.L, fill=color)
                self.tablero[i].update()
            #self.tablero[i].itemconfig(self.tablero[i].create_text(self.L/2, self.L/2, anchor="center", fill="light goldenrod"), text=str(i))


class JugadorInterfazTK:
    """
    Este objeto es en realidad una función, solo se maneja como objeto con el fin que todos los jugadores
    que se implementen utilicen el mismo API.

    """
    def decide_jugada(self, juego, estado, jugador, tablero):
        raise NotImplementedError("¡Este metodo no está implementado!")


class JugadorHumano(JugadorInterfazTK):
    """
    Jugador humano para aplicarlo en la clase JuegoT2ZT utiliando la clase InterfazTK
    como interaz gráfica.

    Para esto el jugador debe tener un método muy claro:

    def decide_jugada(self, juego, estado, jugador, tablero)

    donde:
        tablero es la variable tablero de un objeto InterfazTK,
        juego es un objeto JuegoT2TK
        estado es una lista que representa el estado actual
        jugador = 1 o -1 dependiendo del jugador que sea.

    """

    def decide_jugada(self, juego, estado, jugador, tablero):
        """
        Entradas:
            tablero es la variable tablero de un objeto InterfazTK,
            juego es un objeto JuegoT2TK
            estado es una lista que representa el estado actual
            jugador = 1 o -1 dependiendo del jugador que sea.
        Salidas:
            accion es la accion legal que se decidió utilizar

        """
        seleccion = tk.IntVar(tablero[0].master, -1, 'seleccion')
        jugadas = juego.jugadas_legales(estado, jugador)
        if jugadas is None:
            return None
        if len(jugadas) == 1:
            return jugadas[0]

        if all(j[0] is None for j in jugadas):
            # Si solo hay que seleccionar un lugar nuevo, como el gato
            # entonces solo selecciona un posible valor
            pini = None
            for (_, casilla) in jugadas:
                self.activa_casilla(tablero[casilla], seleccion)

        else:
            for (casilla, _) in jugadas:
                self.activa_casilla(tablero[casilla], seleccion)
            tablero[0].master.wait_variable('seleccion')
            for (casilla, _) in jugadas:
                tablero[casilla].unbind('<Enter>')
                tablero[casilla].unbind('<Leave>')
                tablero[casilla].unbind('<Button-1>')
            pini = seleccion.get()
            for (salida, casilla) in jugadas:
                if salida == pini:
                    self.activa_casilla(tablero[casilla], seleccion)

        tablero[0].master.wait_variable('seleccion')
        for (_, casilla) in jugadas:
            tablero[casilla].unbind('<Enter>')
            tablero[casilla].unbind('<Leave>')
            tablero[casilla].unbind('<Button-1>')
        return pini, seleccion.get()

    def activa_casilla(self, cuadrito, seleccion):
        """
        Modifica las propiedades de la casilla para que cambie de color cuando pase el raton por encima
        y agrega un comando para que cuando se presione el cuadrito se seleccione la accion como la accion
        que se decidió tomar.

        """

        def entrada(evento):
            evento.widget.color_original = evento.widget['bg']
            evento.widget['bg'] = 'DarkOliveGreen4' #'grey'

        def salida(evento):
            evento.widget['bg'] = evento.widget.color_original

        def presiona_raton(evento):
            evento.widget['bg'] = evento.widget.color_original
            seleccion.set(evento.widget.pos)

        cuadrito.bind('<Enter>', entrada)
        cuadrito.bind('<Leave>', salida)
        cuadrito.bind('<Button-1>', presiona_raton)


class JugadorNegamax(JugadorInterfazTK):
    """
    Jugador simple con un algoritmo de Negamax nada optimizado, sin utilizar ningua funcion de utilidad, ya que
    esta es la parte mas interesante en el desarrollo de jugadores automáticos con cierto grado de inteligencia.
    Por supuesto, este jugador simple funciona bien en el caso del gato.

    """
    def __init__(self, d_max=100):
        """
        Inicializa

        """
        self.dmax = d_max

    def decide_jugada(self, juego, estado, jugador, tablero):
        """
        Decide jugada, inicializa el algoritmo de Negamax

        """
        if not juego.jugadas_legales(estado,jugador):
            decide_jugada(self, juego, estado, -jugador, tablero)
        return max(self.ordena(juego, estado, jugador, juego.jugadas_legales(estado, jugador)),
                   key=lambda jugada: -self.negamax(juego,
                                                    estado=juego.hacer_jugada(estado, jugada, jugador),
                                                    jugador=-jugador,
                                                    alpha=-1e10,
                                                    beta=1e10,
                                                    profundidad=self.dmax))

    def negamax(self, juego, estado, jugador, alpha, beta, profundidad):
        """
        El algoritmo negamax es una adaptación del algoritmo alpha--beta para dos jugadores por turnos
        en el cual no es necesario implementar el módulo min_val y max_val, ya que ambos vienen incluidos
        en el mismo algoritmo, basados en la idea que min(x,y) = -max(-x,-y).

        Devuelve jugada, valor donde juagada es la mejor jugada posible y valor es el mejor valor
        esperado posible.

        """
        acabado = juego.estado_terminal(estado)
        if acabado is not None:
            return jugador * acabado
        if profundidad == 0:
            return jugador * self.utilidad(juego, estado)

        for jugada in self.ordena(juego, estado, jugador, juego.jugadas_legales(estado, jugador)):
            if not juego.jugadas_legales(estado,jugador):
                jugador = -jugador
            alpha = max(alpha,  -self.negamax(juego,
                                              estado=juego.hacer_jugada(estado, jugada, jugador),
                                              jugador=-jugador,
                                              alpha=-beta,
                                              beta=-alpha,
                                              profundidad=profundidad - 1))
            if alpha >= beta:
                return alpha
        return alpha

    def ordena(self, juego, estado, jugador, jugadas):
        """
        Ordena las jugadas en función de las más prometedoras a las menos prometedoras. Por default regresa las
        jugadas en el mismo orden que se generaron.

        """
        return jugadas

    def utilidad(self, juego, estado):
        """
        El corazón del algoritmo, determina fuertemente la calidad de la búsqueda.

        Por default devuelve el valor de juego.estado_terminal(estado)

        """
        return juego.estado_terminal(estado)
