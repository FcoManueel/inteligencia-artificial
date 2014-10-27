#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
csp.py
------------

Implementación de los algoritmos más clásicos para el problema
de satisfacción de restricciones. Se define formalmente el
problema de satisfacción de restricciones y se desarrollan los
algoritmos para solucionar el problema por búsqueda.

En particular se implementan los algoritmos de forward checking y
el de arco consistencia. Así como el algoritmo de min-conflics.

En este modulo no es necesario modificar nada.

"""

__author__ = 'juliowaissman'

import random


class ProblemaCSP:
    """
    Clase abstracta para hacer un problema CSP en entornos discretos finitos.

    """

    def __init__(self):
        """
        Inicializa los valores de la clase

        """
        self.dominio = {}
        self.vecinos = {}
        self.backtracking = 0  # Solo para efectos de comparación

    def restriccion_binaria(self, (xi, vi), (xj, vj)):
        """
        Verifica si se cumple la restriccion binaria entre las variables xi
        y xj cuando a estas se le asignan los valores vi y vj respectivamente.

        @param xi: El nombre de una variable
        @param vi: El valor que toma la variable xi (dentro de self.dominio[xi]
        @param xj: El nombre de una variable
        @param vj: El valor que toma la variable xi (dentro de self.dominio[xj]

        @return: True si se cumple la restricción

        """
        raise NotImplementedError("Método a implementar en la subclase que hereda de ProblemaCSP")


def solucion_CSP_bin(problemaCSP):
    """
    Encuentra una asignación que solucione un problema CSP con únicamente restricciones binarias

    @param problemaCSP: Un objeto de una clase decendiente de ProblemaCSP

    @return: Un diccionario tal que asignacion[var] = val para toda val en problemaCSP.variables,
    y tal que val pertenece a problemaCSP.dominio de tal manera que se satisfagan todas las
    restricciones binarias. En caso que no exista una asignación que satisfaga las restricciones,
    regresa None

    """
    asignacion = {}
    if sol_CSP_bin_rec(problemaCSP, asignacion):
        return asignacion
    return None


def sol_CSP_bin_rec(problemaCSP, asignacion):
    """
    Algoritmo recursivo para la solución de CSP binarios. Funcion interna. Modifica en forma recursiva la
    variable mutable asignación

    @param problemaCSP: Un problema tipo CSP binario
    @param asignacion: Un diccionario con la aignación

    """
    # Checa si la asignación es completa
    if set(asignacion.keys()) == set(problemaCSP.dominio.keys()):
        return True

    var = selecciona_variable(problemaCSP, asignacion)
    for val in ordena_valores(problemaCSP, asignacion, var):
        reduccion = consistencia(problemaCSP, asignacion, var, val)
        if reduccion is None:
            continue
        asignacion[var] = val
        bandera = sol_CSP_bin_rec(problemaCSP, asignacion)
        restaura(problemaCSP, reduccion)
        if bandera:
            return True
        del(asignacion[var])
    problemaCSP.backtracking += 1  # Esta linea es solo para probar el método, significa que hay un backtracking
    return False


def selecciona_variable(problemaCSP, asignacion):
    """
    Si asignacion esta vacío, grado heurístico.
    Si no, heurística de la variable más restringida (se selecciona la variable
    que menos valores en su dominio tiene).

    """
    if len(asignacion) == 0:
        return max(problemaCSP.dominio.keys(), key=lambda var: len(problemaCSP.vecinos[var]))

    return min([var for var in problemaCSP.dominio.keys() if var not in asignacion],
               key=lambda var: len(problemaCSP.dominio[var]))

def ordena_valores(problemaCSP, asignacion, variable):
    """
    Heurística del valor menos restrictivo. Ordena los valores de un dominio en orden
    en el que los valores pueden restringir menos los posibles valores de los vecinos de la variable.

    Esta heurística es lenta pero suele dar muy buenos resultados, evitando una gran cantidad de backtrackings.

    """
    def num_conflictos(valor):    
        conflictos = 0
        for otra_variable in problemaCSP.vecinos[variable]:
            if otra_variable not in asignacion:
                for otro_valor in problemaCSP.dominio[otra_variable]:
                    if not problemaCSP.restriccion_binaria((variable, valor), (otra_variable, otro_valor)):
                        conflictos += 1
        return conflictos
        
    return sorted(problemaCSP.dominio[variable], 
                  key=lambda val: num_conflictos(val))

def num_conflictos(problemaCSP, asignacion, var, valor=None):
        """
        Devuelve la cantidad de conflictos que tiene una variable "var" de una "asignacion" en problemaCSP.
        Si se da un "valor", devuelve la cantidad de conflictos que habría si "asignacion[var] =  valor"
        """
        if valor is None:
            valor = asignacion[var]
        
        return sum(map(lambda vecino: int(not problemaCSP.restriccion_binaria((var,valor),(vecino,asignacion[vecino]))),
                             problemaCSP.vecinos[var]))
        
def conflicted_variables(problemaCSP, current_state): 
    return filter(lambda var: num_conflictos(problemaCSP, current_state, var) > 0,problemaCSP.dominio.keys())

def min_conflictos(problemaCSP, maxiter=10000):
    def repetition(previous_state, current_state):
        if previous_state == current_state:
            repetition.counter += 1
        else:
            repetition.counter = 0
    
    current_state = {i:random.choice(problemaCSP.dominio[i]) for i in problemaCSP.dominio.keys()}
    previous_state = None
    repetition.counter = 0 # repeticiones: para revisar si se esta en un minimo local
    for it in range(maxiter):
        repetition(previous_state, current_state)
        if repetition.counter == 15: # si se repite la misma asignacion 15 veces
            current_state = {i:random.choice(problemaCSP.dominio[i]) for i in problemaCSP.dominio.keys()} # revolver todo
        
        conflicted = conflicted_variables(problemaCSP, current_state) # Encontrar variables con conflictos
        if not conflicted:   # Si es no hay conflictos (es meta) regresar estado
            return current_state
        var_to_change = random.choice(conflicted) # Elegir valor conflictivo al azar
        previous_state = current_state
        current_state[var_to_change] = min(problemaCSP.dominio[var_to_change], key=lambda val: num_conflictos(problemaCSP, current_state, var_to_change, val)) # Asignarle el valor que minimize
    print "best at end:", current_state
    return None


def consistencia(problemaCSP, asignacion, variable, valor):
    """
    Reduce los valores de los dominios de las variables que no están asignadas.

    """
    # 0-consistencia (reducción de su propio dominio)
    reduccion = {var: [] for var in problemaCSP.vecinos}
    if len(problemaCSP.dominio[variable]) == 0:
        return None
    for vecino, val_vecino in asignacion.iteritems():
        if not problemaCSP.restriccion_binaria((variable, valor), (vecino, val_vecino)):
            return None
    if len(problemaCSP.dominio[variable]) > 1:
        reduccion[variable] = [x for x in problemaCSP.dominio[variable] if x != valor]
        problemaCSP.dominio[variable] = [valor]

    # 1-consistencia (reducción del dominio de los vecinos inmediatos
    for vecino in problemaCSP.vecinos[variable]:
        if vecino not in asignacion:
            for val_vecino in problemaCSP.dominio[vecino]:
                if not problemaCSP.restriccion_binaria((variable, valor), (vecino, val_vecino)):
                    reduccion[vecino].append(val_vecino)
                    problemaCSP.dominio[vecino].remove(val_vecino)
            if len(problemaCSP.dominio[vecino]) == 0:
                restaura(problemaCSP, reduccion)
                return None

    # 2-consistencia (reducción del dominio por arcos)
    #""""
    cola = [(xi, xj) for xi in problemaCSP.vecinos[variable] 
                     for xj in problemaCSP.vecinos[xi] 
                     if xi not in asignacion]

    while len(cola) > 0:
        (var1, var2) = cola.pop()
        redujo = False
        for val2 in problemaCSP.dominio[var2]:
            for val1 in problemaCSP.dominio[var1]:
                if problemaCSP.restriccion_binaria((var1, val1), (var2, val2)):
                    break
            else:
                reduccion[var2].append(val2)
                problemaCSP.dominio[var2].remove(val2)
                redujo = True
        if redujo:
            if len(problemaCSP.dominio[var2]) == 0:
                restaura(problemaCSP, reduccion)
                return None
            cola.extend([(var2, var3) for var3 in problemaCSP.vecinos[var2]])
    #"""
    return reduccion


def restaura(problemaCSP, reduccion):
    """
    Recupera los valores del dominio original antes de modificarse

    """
    for variable in reduccion:
        problemaCSP.dominio[variable] += reduccion[variable]

