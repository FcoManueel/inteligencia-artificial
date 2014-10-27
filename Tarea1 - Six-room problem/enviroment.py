#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entornos.py
------------


"""

__authors__ = 'juliowaissman, Manuel Valle (translation)'
from copy import deepcopy


class Enviroment(object):
    """
    Abstract class for enviroments

    """
    def state_to_str(self, state):
        """
        @param state: Tuple representing a valid state of the enviroment
        @param action: An element of valid_actions(state)

        @return: Boolean; True if "action" is valid in "state", False otherwise

        (Accepts all actions by default)
        """
        return True

    def next_state(self, state, action):
        """
        @param state: Tuple representing a valid state of the enviroment
        @param action: An element of valid_actions(state)

        @return: Tuple representing the state of the enviroment when agent applies "action" while being in "state",
        Or a tuple of ordered pairs (possibly new state, chance of getting this state).

        """
        pass

    def sense(self, state):
        """
        @param state: Tuple representing a valid state of the enviroment

        @return: Tuple with perceived values of the enviroment

        """
        pass

    def performance(self, estado, accion): #desempeño_local
        """
        @param state: Tuple representing a valid state of the enviroment
        @param action: An element of valid_actions(state)

        @return: floating number representing performance of applying "action" in "state"

        """
        pass

    def is_valid_action(self, state, action):
        """
        @param state: Tuple representing a valid state of the enviroment
        @param action: An element of valid_actions(state)

        @return: Boolean; True if "action" is valid in "state", False otherwise

        (Accepts all actions by default)
        """
        return True


class Agent(object):
    """
    Abstract class for an agent that interacts with a discrete determinist non-observable enviroment

    """

    def act(self, percept):
        """
        @param percept: List with values perceived in the enviroment

        @return: action: Action selected by the agent

        """
        pass


def simulate(enviroment, agent, init_state, max_steps=100, verbose=True):
    """
    Perform agent simulation acting on a generic-form enviroment

    """
    state = init_state
    performance = 0
    performances = [performance]
    states = [deepcopy(state)]
    actions = [None]

    for _ in xrange(    max_steps): # Changed "step" to "_" and "range" to "xrange". Change later if gives any problem.
        percept = enviroment.sense(state)
        #   print "State is " + str(percept) + "     Action is " + agent.act(percept)
        action = agent.act(percept)
        new_state = enviroment.next_state(state, action)
        performance += enviroment.performance(state, action)

        performances.append(performance)
        states.append(deepcopy(new_state))
        actions.append(action)
        state = new_state
    if verbose:
        print "\n\nEnviroment simulation type " + str(type(enviroment)) + " with agent type " + str(type(agent)) + "\n"
        print 'Step'.center(10) + 'State'.center(80) + 'Action'.center(22) + u'Performance'.center(11)
        print '_' * (10 + 80 + 22 + 11)
        for i in range(max_steps):
            print (str(i).center(10) + enviroment.state_to_str(states[i]) .center(40) +
                   str(actions[i]).center(25) + str(performances[i]).rjust(4))
        print '_' * (10 + 80 + 22 + 11) + '\n\n'

    return states, actions, performances
