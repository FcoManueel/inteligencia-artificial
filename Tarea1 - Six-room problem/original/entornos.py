#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entornos.py
------------


"""

__author__ = 'juliowaissman'

class Entorno(object):
    """
    Clase abstracta para entornos

    """

    def transicion(self, estado, accion):
        """
        @param estado: Tupla con un estado válido para el entorno
        @param accion: Uno de los elementos de acciones_legales( estado)

        @return: el estado a donde transita el entorno cuando el agente aplica la acción o
        una tupla de pares ordenados con el posible estado nuevo y su probabilidad.

        """
        pass

    def sensores(self, estado):
        """
        @param estado: Tupla con un estado válido para el entorno

        @return: Tupla con los valores que se perciben de un entorno

        """
        pass

    def desempeno_local(self, estado, accion):
        """
        @param estado: Lista con un estado válido para el entorno
        @param accion: Uno de los elementos de acciones_legales( estado)

        @return: un número flotante con el desempeño de aplicar la accion en el estado

        """
        pass

    def accion_legal(self, estado, accion):
        """
        @param estado: Tupla con un estado válido para el entorno
        @param accion: Uno de los elementos de acciones_legales( estado)

        @return: Booleano True si la accion es legal en el estado, False en caso contrario

        Por default acepta cualquier acción.
        """
        return True


class Agente(object):
    """
    Clase abstracta para un agente que interactua con un entorno discreto determinista observable.

    """

    def programa(self, percepcion):
        """
        @param percepcion: Lista con los valores que se perciben de un entorno

        @return: accion: Acción seleccionada por el agente, utilizando su programa de agente.

        """
        pass


def simulador(entorno, agente, estado_inicial, pasos=10, verbose=True):
    """
    Realiza la simulación de un agente actuando en un entorno de forma genérica

    """
    estado = estado_inicial
    performance = 0
    performances = [performance]
    estados = [estado]
    acciones = [None]

    for paso in range(pasos):
        percepcion = entorno.sensores(estado)
        accion = agente.programa(percepcion)
        estado_n = entorno.transicion(estado, accion)
        performance += entorno.desempeno_local(estado, accion)

        performances.append(performance)
        estados.append(estado_n)
        acciones.append(accion)
        estado = estado_n

    if verbose:
        print "\n\nSimulacion de entorno tipo " + str(type(entorno)) + " con el agente tipo " + str(type(agente)) + "\n"
        print 'Paso'.center(10) + 'Estado'.center(40) + 'Accion'.center(25) + u'Desempeño'.center(15)
        print '_' * (10 + 40 + 25 + 15)
        for i in range(pasos):
            print (str(i).center(10) + str(estados[i]).center(40) +
                   str(acciones[i]).center(25) + str(performances[i]).rjust(12))
        print '_' * (10 + 40 + 25 + 15) + '\n\n'

    return estados, acciones, performances
