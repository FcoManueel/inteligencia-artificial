#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_2.py
------------

Tarea 2a: Dibujar un grafo utilizando métodos de optimización

Si bien estos métodos no son los que se utilizan en el dibujo de gráfos por computadora (son
algoritmos realmente muy complejos lo que se usan actualmente). Si da una idea de la utilidad de
los métodos de optimización en un problema divertido.

Obviamente el problema se encuentra muy simplificado para poder ser visto dentro de una práctica.

Para realizar este problema es ecesario contar con el módulo PIL (Python Image Library) instalada.
Si instalaste EPD o EPD free, no hay problema, PIL viene ya incluido. Si no, hay que instalarlo.

Para que funcione, este modulo debe de encontrarse en la misma carpeta que blocales.py (incluida en piazza)

"""

__author__ = 'Escribe aquí tu nombre'

import blocales
import random
import itertools
import math
import Image
import ImageDraw
import time
import numpy
    
class problema_grafica_grafo(blocales.Problema):
    """
    Clase para un grafo simple no dirigido, únicamente para fines de graficación

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, representado por una lista (no conjunto, el orden importa
        a la hora de graficar), y un conjunto (tambien en forma de lista) de pares ordenados de vertices, lo que
        forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con el nombre de las aristas.
        @param dimension_imagen: Entero con la dimansion de la imagen en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def keep_in_canvas(self, component_value, padding = 10):
        # Receives the value of a coordinate component (e.g. x is a component of (x,y)) and a 
        # padding which is a quantity of pixels beside the edges that will be taken as outside of the canvas.
        # If coordinate_component is outside the canvas (or over the padding zone) it returns the nearest
        # in-canvas value. Only works for squared canvas
        return max(padding, min(self.dim - padding, component_value))

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema se define como s = [s(1), s(2), ..., s(2*len(vertices))] en donde:

        s(i) \in {10, 11, ..., 390} es la posición en x del nodo i/2 si i es par, o la posicion en y del
        nodo (i-1)/2 si i es non (osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in range(2 * len(self.vertices)))

    def vecino_aleatorio(self, estado):
        """
        Encuentra un vecino en forma aleatoria. En esta primera versión lo que hacemos es tomar un valor aleatorio,
        y sumarle o restarle uno al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar como hacer un mejor vecino aleatorio y comparar
        las ventajas de hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        # Basicamente muevo 3 veces algún punto (pueden o no ser distintos) de tal manera que el
        # movimiento se da dentro de un area cuadrada de lado 17 pixeles alrededor del punto
        # Como se cambian las dos componentes se permite movimientos diagonales, y más amplios
        # que en la versión anterior del vecino
        
        vecino = list(estado)
        for _ in range(3): # Mover tres puntos
            i = random.randint(0, len(vecino) - 1) # i es el indice de un elemento del estado
            if i%2 == 0:
                j = i+1 # j es el elemento tal que i y j forman la coordenada de un punto 
            else:
                j = i-1
            alpha1 = random.randint(1,8) # alpha1 es el movimiento que tendrá el vecino en indice [i]
            alpha2 = random.randint(1,8) # alpha2 es el movimiento que tendrá el vecino en indice [j]
            vecino[i] = self.keep_in_canvas(vecino[i] + random.choice([-1, 1])*alpha1, 10) # mover la componente i
            vecino[j] = self.keep_in_canvas(vecino[j] + random.choice([-1, 1])*alpha2, 10) # mover la componente j
        return vecino
        
        
        # 
#################################################################################################
#                          20 PUNTOS
#################################################################################################
        # Por supuesto que esta no es la mejor manera de generar vecino para este problema.
        # Al ser muchos los pixeles, dentro del temple simulado, se podría generar los vecinos como
        # si fuera un problema continuo, y solamente se redondea el resultado obtenido (y se evita 
        # que un valor se salga de los valores máximos posibles, por supuesto).
        #
        # Prueba y ajusta el algoritmo de temple simulado para espacios continuos y redondea a 1 al
        # generar vecino aleatorio. Esto lo puedes agregar en este método, recibiendo no únicamente 
        # el estado actual, si no además información de la temperatura, por ejemplo, y algo más 
        # posiblemente. 
        #        
        # -- Escribe inmediatamenta arriba de este comentario tus respuestas a la pregunta, comenta el 
        #    código propuesto y agrega el tuyo.
            # Código agregado y comentado arriba.


    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado es la cantidad de veces que dos
        aristas se cruzan cuando se dibujan. Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.
|
        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes (default solo cuanta el criterio 1)
        K1 = 50.0
        K2 = 30.0
        K3 = 5.0
        K4 = 3.5

        # Genera un diccionario con el estado y la posición para facilidad
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) + 
                K2 * self.separacion_vertices(estado_dic) + 
                K3 * self.costo_angulos_aristas(estado_dic) + 
                K4 * self.criterio_propio(estado_dic))


        # Como podras ver en los resultados, este costo no hace figuras particularmente
        # bonitas, y esto es porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el costo el angulo entre dos aristas conectadas
        # al mismo vertice, dandole un mayor costo si el angulo es muy pequeño (positivo o negativo). Igualemtente
        # se puede penalizar el que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en tres partes, una es el numero de cruces (ya programada), otra
        # la distancia entre nodos (ya programada) y otro el angulo entre arista de cada nodo (para programar) y cada
        # uno de estos criterios hay que agregarlo a la función de costo con un peso.
        #


    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo si se grafica como dice estado

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los vartices de una arista
            # y los valores (x0B,y0B), (x0B, y0B) para los vertices de la otra arista
            (x0A, y0A), (xFA, yFA) = estado_dic[aristaA[0]], estado_dic[aristaA[1]]
            (x0B, y0B), (xFB, yFB) = estado_dic[aristaB[0]], estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar interseccion entre dos lineas
            # cuidando primero de asegurarse que las lineas no son paralelas (para evitar la
            # división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A) + 0.0
            if den == 0:
                continue

            # Y entonces sacamos el largo del cruce, normalizado por den. Esto significa que en 0
            # se encuentran en la primer arista y en 1 en la última. Si los puntos de cruce de ambas
            # lineas se encuentran en valores entre 0 y 1, significa que se cruzan
            puntoA = ((xFB - x0B) * (y0A - y0B) - (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) - (yFA - y0A) * (x0A - x0B)) / den

            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización proporcional a cada par de vertices que se
        encuentren menos lejos que min_dist. Si la distancia entre vertices es menor a min_dist, entonces calcula una
        penalización proporcional a esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.
        @param min_dist: Mínima distancia aceptable en pixeles entre dos vértices en el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total
    
    def costo_angulos_aristas(self, estado_dic):
        """
        A partir de una posicion "estado", devuelve una penalizacion proporcional a cada angulo entre aristas
        menor a pi/6 rad (30 grados). Los angulos de pi/6 o mayores no llevan ninguna penalización, y la penalizacion
        crece conforme el angulo es menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número que representa costo.

        """
        #################################################################################################
        #                          20 PUNTOS
        #################################################################################################
        # Agrega el método que considere el angulo entre aristas de cada vertice. Dale diferente peso a cada criterio
        # hasta lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
            # K1 = 50 
            # K2 = 30
            # K3 = 5
            # Consideré que fuera más prioritario obtener una gráfica plana (de ser posible)
            # asi que K1 tiene el mayor valor. su representación más bonita es esa.
            # No pensé en poner tanta diferencia entre K1 y K3, pero jugando con los valores esta fue
            # una combinacion que me dio buenos valores.
            #
            # Hice pruebas con una gráfica completa de 5 vertices, la cual era dibujada de manera
            # perfecta (las adjuntare con el codigo como fig1) usando los siguientes valores para las K mencionadas:
            # K1 = 20.0
            # K2 = 100.0
            # K3 = 50.0
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------        
        #
        def aristas_incidentes(vertice):
            """
            @param vertice: string representando un vértice de self.vertices
            @return: lista con todas las aristas (2-tuplas) que inciden en "vértice".
            """
            return filter(lambda coord: vertice in coord, self.aristas)

        def angulo_vectores(x1,y1,x2,y2):
            # la clasica formula del arcoseno para sacar el angulo entre vectores
            magn1 = math.sqrt(x1*x1 + y1*y1) + 0.01
            magn2 = math.sqrt(x2*x2 + y2*y2) + 0.01
            prod_punto = math.fabs(x1*x2+y1*y2)
            cos_rads = prod_punto/(magn1*magn2)
            cos_rads = round(cos_rads, 4)  # la imprecisión de los flotantes me causo algunos problemas
            rads = math.acos(cos_rads) % 2*math.pi
            return math.degrees(rads)
        
        costo = 0
        for incidencias in map(lambda v: aristas_incidentes(v), self.vertices):
            pares_aristas = itertools.combinations(incidencias, 2)
            for par_aristas in pares_aristas:
                a1, a2 = par_aristas
                a, b = a1
                c, d = a2
                ax, ay = estado_dic[a]
                bx, by = estado_dic[b]
                cx, cy = estado_dic[c]
                dx, dy = estado_dic[d]
                if a in [c,d]: # a es el vértice en común. Convertirlo en el origen                    
                    if a == c:
                        angulo = angulo_vectores(bx-ax, by-ay, dx-ax, dy-ay)
                    else:
                        angulo = angulo_vectores(bx-ax, by-ay, cx-ax, cy-ay)
                else: # b es el vértice en común.
                    if b == c:
                        angulo = angulo_vectores(ax-bx, ay-by, dx-bx, dy-by)
                    else:
                        angulo = angulo_vectores(ax-bx, ay-by, cx-bx, cy-by)

                if math.fabs(angulo) < 35:
                    costo += 70/(angulo+1)
        return costo
        
        
    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea conveniente para que un grafo
        luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices del grafo y cuyos valores es una
                           tupla con la posición (x, y) de ese vértice en el dibujo.

        @return: Un número.

        """
        #################################################################################################
        #                          20 PUNTOS
        #################################################################################################
        # ¿Crees que hubiera sido bueno incluir otro criterio? ¿Cual?
        #
            # Quizá uno que acercara el grafo al centro del canvas.
            # Quizá otro que prefiriera lineas horizontales y verticales quizá podría mejorar 
            # algunos detalles con algunas gráficas, pero creo que tendría que tener muy poco 
            # peso, y no estoy seguro de si hiciera mejora
        #
        # Desarrolla un criterio propio y ajusta su importancia en el costo total con K4 ¿Mejora el resultado? ¿En
        # que mejora el resultado final?
        #
            # Me parece que si
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
        #
        def longitud_arista(x1,y1,x2,y2):
            return math.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        costo = 0
        longitudes = []
        for arista in self.aristas:
            x1,y1 = estado_dic[ arista[0] ]
            x2,y2 = estado_dic[ arista[1] ]
            longitudes.append( longitud_arista(x1,y1,x2,y2) )
        desv_std = numpy.std(longitudes)
        #median = numpy.mean(longitudes)
        #for longitud in longitudes:
        #    costo += abs(longitud - median)
        return desv_std
            

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1]) for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None):
        """
        Dibuja el grafo utilizando PIL, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es
        la posición en x y y respectivamente de cada vertice. dim es
        la dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))  # Imagen en blanco
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))

        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))
        
        """
        # Metodo rebuscado para nombrar los archivos. Toda la mugre que prosigue 
        # es sustituible por "imagen.show()", funcion que a mi no me funciona
        
        # Tengo un archivo "numbering" guardado en "fpath" que inicialmente tiene
        # escrito un numero (0 o 1, al gusto) (sin saltos de linea)
        # Cada vez que guarda un archivo le 'appenda'  el numero al final, y aumenta
        # el numero del archivo en 1. 
        def get_number():
            fpath = r"C:\Users\ManueelVR\Desktop\7mo Semstre\Inteligencia Artificial\Tarea2 - busquedas locales\numbering"
            f = open(fpath, 'r')
            fnum_corrida = f.read()
            f.close()
            f = open(fpath, 'w')
            f.write(str(int(fnum_corrida)+1))
            f.close()
            return  fnum_corrida
        
        fname = "prueba-"
        fname += get_number()
        fname += ".jpg"
        print "Guardando archivo " + fname
        imagen.save(fname)
        """
        imagen.show()


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F')]
    # Y uno completo
    vertices_K5 = ['1','2','3','4','5']
    aristas_K5 = [('1','2'),
                  ('1','3'),
                  ('1','4'),
                  ('1','5'),
                  ('2','3'),
                  ('2','4'),
                  ('2','5'),
                  ('3','4'),
                  ('3','5'),
                  ('4','5')]
                  
    ##################################
    #######  Definir grafica  ########
    ##################################
    #G_vertices = vertices_sencillo
    #G_aristas = aristas_sencillo
    G_vertices = vertices_K5
    G_aristas = aristas_K5
    
    dimension = 400

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para ajustarlo.
    grafo_sencillo = problema_grafica_grafo(G_vertices, G_aristas, dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    grafo_sencillo.dibuja_grafo(estado_aleatorio)
    print "Costo del estado aleatorio: ", grafo_sencillo.costo(estado_aleatorio)

    # Ahora vamos a encontrar donde deben de estar los puntos
    tiempo_inicial = time.time()
    K = 1500
    delta = 0.001
    solucion = blocales.temple_simulado(grafo_sencillo, lambda i: 1000/math.log(i+2))#lambda i: blocales.cal_expon(i, K, delta))
    tiempo_final = time.time()
    grafo_sencillo.dibuja_grafo(solucion)
    print "\nUtilizando una calendarización exponencial con K = " + str(K) + " y delta = " + str(delta)
    print "Costo de la solución encontrada: ", grafo_sencillo.costo(solucion)
    print "Tiempo de ejecución en segundos: ", tiempo_final - tiempo_inicial
    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # ¿Que valores para ajustar el temple simulado (Temp inicial y vel de enfriamiento) son los que mejor resultado dan?
    # 
        # En clase vimos que dada una temperatura inicial dada lo suficientemente alta y una
        # calendarización suave se garantizaba la convergencia al óptimo.
        # A pesar de ello, me parece que a partir de dicha temperatura 'alta' se deja de notar gran diferencia
        # al aumentarse más, y cambiar la velocidad de enfriamiento da más oportunidad para obtener mejoras
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
        # ¿De las 4 heuristicas incluidas?
        # Mi parecer era que la de procurar evitar ángulos chicos, pero al moverle me parecio que 
        # obtenia mejores resultados con el que minimiza cruces


    #################################################################################################
    #                          20 PUNTOS
    #################################################################################################
    # En general para obtener mejores resultados del temple simulado, es necesario utilizar una
    # función de calendarización acorde con el metodo en que se genera el vecino aleatorio.
    # Existen en la literatura varias combinaciones. Busca en la literatura diferentes métodos de
    # calendarización (al menos uno más diferente al exponencial) y ajusta los parámetros de cada
    # metodo para que obtenga la mejor solución posible en el menor tiempo posible.
    #
    # Escribe aqui tus comentarios y prueba otro metodo de claendarización para compararlo con el
    # exponencial.
        # Se me pide que la impemente aquí abajo, pero si lo pongo acá abajo no me corre, asi que
        # en mis pruebas lo puse como una lambda arriba (en la llamada de la funcion temple_simulado)
        #
        # Usé como alternativa el boltzman, pero me dio (significativamente mucho) 
        # menor rendimiento que la calendarización exponencial
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------------------------------------------
    #

    def boltzman(iteracion):
        Tmax = 1000
        return Tmax/math.log(iteracion+2)





if __name__ == '__main__':
    main()
