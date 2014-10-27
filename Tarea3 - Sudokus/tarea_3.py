#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sudoku.py
------------

Este es el problema que deberán resolver para la tarea 2 sobre satisfacción de restricciones.

En esta tarea no se pide desarrollar o modificar los algoritmos de satisfacción de restricciones
que se ofrecen, sino de utilizarlos para resolver un problema relativamente simple:

    Un solucionador de sudokus

Los Sudokus son unos juegos de origen Japones. El juego tiene un tablero de 9 x 9 casillas.
En cada casilla se debe asignar un número 1, 2, 3, 4, 5, 6, 7, 8 o 9.

La idea principal de juego es establecer los valores de los números en las casillas no
asignadas anteriormente si se considera que:

    a) Las casillas horizontales deben tener números diferentes entre si
    b) Las casillas verticales deben tener números diferentes entre si
    c) Las casillas que pertenecen al mismo grupo deben tener números diferentes entre si.

sea (r1, c1) el renglon y la columna de una casilla y (r2, c2) el renglon y la columna de otra casilla,
se dice que las casillas pertenecen al mismo grupo si y solo si r1/3 == r2/3 y c1/3 == c2/3
donde / es la división entera (por ejemplo 4/3 = 1 o 8/3 = 2).
Esto aplica si se considera 0 como la primer posición.

Para más información sobre sudokus, pueden googlearlo, buscarlos en wikipedia o comprar un librito
de sudokus de 8 pesos (cuidado, se puede perder mucho tiempo resolviendo sudokus).


Para revisar la tarea es necesario seguir las siguientes instrucciones:

Un Sudoku se inicializa como una lista de 81 valores donde los valores se encuentran de la manera siguiente:

    0   1   2 |  3   4   5 |  6   7   8
    9  10  11 | 12  13  14 | 15  16  17
   18  19  20 | 21  22  23 | 24  25  26
   -----------+------------+------------
   27  28  29 | 30  31  32 | 33  34  35
   36  37  38 | 39  ...

hasta llegar a la posición 81.


los valores que puede tener la lista son del 0 al 9. Si tiene un 0 entonces es que el valor es desconocido.


"""

__author__ = 'juliowaissman'


import csp

def son_vecinos(i, j):
    return (columna(i) == columna(j) or  # [comparten columna]
            renglon(i) == renglon(j) or  # [comparten renglón]
            bloque(i) == bloque(j))      # [comparten bloque]
    
def columna(i):
    return i%9
    
def renglon(i):
    return i//9
    
def bloque(i):
    """
    @return devuelve un valor en range(9) que representa el numero de bloque de i
    """
    return (i//27)*3 + (i%9)//3
    
def get_row_of(i):
    """
    @return un arreglo con todos los elementos en la misma linea que i (incluyendo i)
    """
    ren = i//9
    return range(9*ren, 9*(ren+1))

def get_col_of(i):
    """
    @return un arreglo con todos los elementos en la misma columna que i (incluyendo i)
    """
    col = i%9
    return range(col, 9*9+col, 9)

def get_block_of(i):
    block = []
    x = (i%9)//3
    y = (i/9)//3
    block_corner = 27*y + 3*x  # is the value of the index of the top left element in the block
    block += range(block_corner, block_corner+3) 
    block += range(block_corner+9, block_corner+9+3) 
    block += range(block_corner+18, block_corner+18+3)
    return block
    

class Sudoku(csp.ProblemaCSP):
    """
    Esta es la clase que tienen que desarrollar y comentar. Las variables están dadas
    desde 0 hasta 81 (un vector) tal como dice arriba. No modificar nada de lo escrito
    solamente agregar su código.

    """
        
    def __init__(self, pos_ini):
        """
        Inicializa el sudoku

        """
        csp.ProblemaCSP.__init__(self)

        self.dominio = {i: [val] if val > 0 else range(1, 10) for (i, val) in enumerate(pos_ini)}

        #=================================================================
        # 20 puntos: INSERTAR SU CÓDIGO AQUI (para vecinos)
        #=================================================================
        
        for i in range(len(pos_ini)):
            v = get_row_of(i) + get_col_of(i) + get_block_of(i)            
            v = list(set(v))
            v.remove(i)
            self.vecinos[i] = v[:]

    def restriccion_binaria(self, (xi, vi), (xj, vj)):
        """
        El mero chuqui. Por favor comenta tu código correctamente
        @return True si la restriccion se respeta, False si no

        """
        #===========================================================================
        # 20 puntos: INSERTAR SU CÓDIGO AQUI (restricciones entre variables vecinas)
        #===========================================================================
        
        return not ((vi == vj) and son_vecinos(xi,xj)) # False si son iguales y vecinos, else True

               
            

    def imprime_sdk(self, asignacion):
        """
        Imprime un sudoku en pantalla en forma más o menos graciosa. Esta función solo sirve para la tarea y
        para la revisión de la tarea. No modificarla por ningun motivo.

        """ 
        s = [asignacion[i] for i in range(81)]
        c = ''
        for i in range(9):
            c += ' '.join(str(s[9 * i + j]) + ("  |  " if j % 3 == 2 and j < 7 else "   ") for j in range(9))
            c += '\n-------------+----------------+---------------\n' if i % 3 == 2 and i < 7 else '\n'
        print c


if __name__ == "__main__":

    # Vamos a poner unos sudokus famosos pa empezar

    # Una forma de verificas si el código que escribiste es correcto
    # es verificando que la solución sea satisfactoria para estos dos
    # sudokus. (20 puntos)

    s1 = [0, 0, 3, 0, 2, 0, 6, 0, 0,
          9, 0, 0, 3, 0, 5, 0, 0, 1,
          0, 0, 1, 8, 0, 6, 4, 0, 0,
          0, 0, 8, 1, 0, 2, 9, 0, 0,
          7, 0, 0, 0, 0, 0, 0, 0, 8,
          0, 0, 6, 7, 0, 8, 2, 0, 0,
          0, 0, 2, 6, 0, 9, 5, 0, 0,
          8, 0, 0, 2, 0, 3, 0, 0, 9,
          0, 0, 5, 0, 1, 0, 3, 0, 0]

    print "Solucionando un Sudoku dificil"
    sudoku1 = Sudoku(s1)
    sudoku1.imprime_sdk(s1)
    sol1 = csp.solucion_CSP_bin(sudoku1)
    #sol1 = csp.min_conflictos(sudoku1)
    sudoku1.imprime_sdk(sol1)


    s2 = [4, 0, 0, 0, 0, 0, 8, 0, 5,
          0, 3, 0, 0, 0, 0, 0, 0, 0,
          0, 0, 0, 7, 0, 0, 0, 0, 0,
          0, 2, 0, 0, 0, 0, 0, 6, 0,
          0, 0, 0, 0, 8, 0, 4, 0, 0,
          0, 0, 0, 0, 1, 0, 0, 0, 0,
          0, 0, 0, 6, 0, 3, 0, 7, 0,
          5, 0, 0, 2, 0, 0, 0, 0, 0,
          1, 0, 4, 0, 0, 0, 0, 0, 0]


    print "Y otro tambien dificil"
    sudoku2 = Sudoku(s2)
    sudoku2.imprime_sdk(s2)
    sol2 = csp.solucion_CSP_bin(sudoku2)
    #sol2 = csp.min_conflictos(sudoku2)
    sudoku2.imprime_sdk(sol2)


    # 40 puntos:
    # Prueba la solucion de sudokus utilizando minimos conflictos
    # Escribe aqui cual funciona mejor y di porque crees que es mejor uno que otro para este problema
    # Inserta tanto texto en forma de comentario como consideres necesario.
    """
    Sin duda el metodo de CSP es mejor que el de minimo conflictos.
    No se si se deba a algún error en mi algoritmo, pero para o me son insuficientes las iteraciones
    o tarda demasiado sin encontrar solución. (Esperé hasta máximo 15 minutos y lo detuve, entonces 
    no se que iba a pasar, pero no creo que algo bonito)
    Ademas, por la naturaleza del algoritmo de min-conflictos (que es muy parecido a hill climbing)
    podría estancarse.
    
    Éste algoritmo trabaja "corrigiendo" un estado dado.
    Creo que al intentar resolver a mano el problema de las nreinas esta manera de abordar el problema
    es más o menos intuitiva, con unos cuantos cambios puedes llegar a la solución, pero al poner un 
    estado aleatorio en el sudoku se introducen muchisimos errores, que afectan también a las decisiones
    futuras
    
    Quiza sería interesante ver si mejora de alguna manera si cambiamos la manera de elegir el estado
    inicial, por ejemplo elegir un estado inicial que cumpla con alguna restricción más fácil de conseguir
    (e.g. respetar la no repetición en bloques) (pedir que la solución inicial cumpla con todas las 
    restricciones seria equivalente a conocer de antemano la solución, y en ese caso no usaríamos estos
    métodos) y trabajar a partir de ahí. No se si sirviera, pero es una idea.
    
    """