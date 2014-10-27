#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1.- Develop a enviroment with six rooms (two floors and three rooms per floor). Available actions will be:

    A = {"goRight", "goLeft", "goUp", "goDown", "clean", "noOp"}

    You can only "goUp" if you are in the bottom floor and "goDown" if you are in the top floor.

    "goUp" and "goDown" actions have higher cost in terms of energy than "goLeft" and "goRight", therefore 
    the performance function must be one that has all rooms and clean minimize vertical movement.

2.- Design a model-based reflex agent (Agente reactivo basado en modelo) for this enviroment and compare
    performance with a random agent after 100 simulation steps.

3.- Modify the original two-rooms problem in a way that the agent knows only in which room is it (it has no
    idea if its clean or not). Design a rational agent for this problem. Test and compare with random agent.

4.- Modify the original two-rooms problem so when the agent decides to clean there's an 80% chance of cleaning and a 20%
    chance of leaving the room uncleaned. Design a rational agent for this problem. Test and compare with random agent.

Every problem has a 25 point value.

"""
__author__ = 'Manuel Valle'

import enviroment
from six_rooms import *
from two_rooms_blind import *
import two_rooms_stochastic as trs
from copy import deepcopy

six_rooms_default = ((0,0), {(0,0):"dirty", (0,1):"dirty", (0,2):"dirty", (1,0):"dirty", (1,1):"dirty", (1,2):"dirty"})
two_rooms_default = ('A', 'dirty', 'dirty')

print "_"*80
print "Excersice 1,2: SixRooms"
random_performance = enviroment.simulate(SixRooms(), 
                                         SixRoomsRandomAgent(), 
                                         deepcopy(six_rooms_default), 
                                         100, False)[2][-1]
model_performance = enviroment.simulate(SixRooms(), ModelReflexAgentSixRooms(), deepcopy(six_rooms_default), 100, False)[2][-1]
print "Random Agent performance:             " + str(random_performance)
print "Model-based Reflex Agent performance: " + str(model_performance)
print "\nModel-based Agent is " + str(float(random_performance)/float(model_performance)) + " times better than Random Agent."
print "*Based on a 100 step simulation"


print "_"*80
print "\n\nExcersice 3: TwoRoomsBlind"
random_performance = enviroment.simulate(TwoRoomsBlind(), 
                                         RandomAgent(['goA', 'goB', 'clean', 'noOp']),
                                         two_rooms_default, 
                                         100, 
                                         False)[2][-1]
model_performance = enviroment.simulate(TwoRoomsBlind(), 
                                        ModelReflexAgentTwoRoomsBlind(), 
                                        two_rooms_default, 
                                        100, 
                                        False)[2][-1]
print "Random Agent performance:             " + str(random_performance)
print "Model-based Reflex Agent performance: " + str(model_performance)
print "\nModel-based Agent is " + str(float(random_performance)/float(model_performance)) + " times better than Random Agent."
print "*Based on a 100 step simulation"


print "_"*80
print "\n\nExcersice 4: TwoRoomsStochastic"
random_performance = enviroment.simulate(trs.TwoRoomsStochastic(), 
                                         trs.RandomAgent(['goA', 'goB', 'clean', 'noOp']),
                                         two_rooms_default, 
                                         100, 
                                         False)[2][-1]
model_performance = enviroment.simulate(trs.TwoRoomsStochastic(), 
                                        trs.ModelReflexAgentTwoRoomsStochastic(), 
                                        two_rooms_default, 
                                        100, 
                                        False)[2][-1]
print "Random Agent performance:             " + str(random_performance)
print "Model-based Reflex Agent performance: " + str(model_performance)
print "\nModel-based Agent is " + str(float(random_performance)/float(model_performance)) + " times better than Random Agent."
print "*Based on a 100 step simulation"


print "_"*80