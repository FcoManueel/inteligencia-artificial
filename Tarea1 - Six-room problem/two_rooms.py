#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Example of simple Agent and Enviroment

"""

__author__ = 'juliowaissman, Manuel Valle (translation)'
# thanks to eduardo.acye for sugesstions in variable naming

import enviroment
from random import choice


class TwoRooms(enviroment.Enviroment):
    """
    Class for a two-room enviroment.

    State is defined as (location, A, B), where location can have values "A" and "B"
    A and B can have the values "clean", "dirty"

    Valid actions are "goA", "goB", "clean", "noOp". 
    All actions are valid in all states.

    We can sense the location of the robot (A or B) and the state of that location (clean or dirty).
    Therefore, sense returns a tuple (location, clean?)

    """
    def state_to_str(self, state):
        return str(state)
        
    def next_state(self, current_state, action):
        if not self.is_valid_action(current_state, action):
            raise ValueError("Action not valid for current state")

        location, A, B = current_state

        return (current_state if action is 'noOp' else
                ('A', A, B)    if action is 'goA' else
                ('B', A, B)    if action is 'goB' else
                ('A', 'clean', B) if (action is 'clean' and location == 'A') else
                ('B', A, 'clean'))

    def sense(self, state):
        location, A, B = state
        return location, A if location is 'A' else B

    def is_valid_action(self, state, action):
        return action in ('goA', 'goB', 'clean', 'noOp')

    def performance(self, state, action):
        location, A, B = state
        return 0 if action == 'noOp' and A == B == 'clean' else -1


class RandomAgent(enviroment.Agent):
    """
    An agent that returns a random valid action 

    """
    def __init__(self, actions):
        self.actions = actions

    def act(self, percepcion):
        return choice(self.actions)


class ReflexAgentTwoRooms(enviroment.Agent):
    """
    A simple Reflex Agent

    """

    def act(self, percepcion):
        location, status = percepcion
        return ('clean' if status == 'dirty' else
                'goA' if location == 'B' else
                'goB')


class ModelReflexAgentTwoRooms(enviroment.Agent):
    """
    model-based reflex agent

    """
    def __init__(self):
        """
        Starts model in worst-case scenario

        """
        self.model = ['A', 'dirty', 'dirty']
        self.locations = {'A': 1, 'B': 2}

    def act(self, perception):
        current_location, status = perception

        # Updates inner model
        self.model[0] = current_location
        self.model[self.locations[current_location]] = status

        # Decides based on inner model
        A, B = self.model[1], self.model[2]
        return ('noOp' if A == B == 'clean' else
                'clean' if status == 'dirty' else
                'goA' if current_location == 'B' else
                'goB')


def test():
    """
    Prueba del entorno y los agentes

    """
    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    enviroment.simulate(TwoRooms(),
                       RandomAgent(['goA', 'goB', 'clean', 'noOp']),
                       ('A', 'dirty', 'dirty'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    enviroment.simulate(TwoRooms(),
                       ReflexAgentTwoRooms(),
                       ('A', 'dirty', 'dirty'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo"
    enviroment.simulate(TwoRooms(),
                       ModelReflexAgentTwoRooms(),
                       ('A', 'dirty', 'dirty'), 100)

if __name__ == '__main__':
    test()
