#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
doscuartos.py.py
------------

Example of simple Agent and Enviroment

"""

__author__ = 'Manuel Valle'

import enviroment
from random import choice
from copy import deepcopy

def valid_actions(location):
        floor, room = location
        
        possible_actions = ["goLeft", "goRight", "goUp", "goDown", "clean", "noOp"]
        if floor is 0:
            possible_actions.remove("goDown")
        else:
            possible_actions.remove("goUp")
            
        if room is 0:
            possible_actions.remove("goLeft")
        elif room is 2:
            possible_actions.remove("goRight")
            
        return possible_actions

def is_all_clean(rooms):
        """
        Returns True if all rooms are clean, False otherwise        
        """        
        return reduce(lambda y, z: y and z, map(lambda x: x is "clean", rooms.values()))
    
def is_floor_clean(rooms, floor):
    floor_status = [rooms[(floor,i)] for i in xrange(3)]
    return reduce(lambda y, z: y and z, map(lambda x: x is "clean", floor_status))
        
class SixRooms(enviroment.Enviroment):
    """
    Class for a six-room enviroment.
    Rooms are organized in the following way
    
    room(1,0)   room(1,1)   room(1,2)
    room(0,0)   room(0,1)   room(0,2)

    State is defined as (location, rooms_status)
    * location is a tuple (i,j) containing the coordinates of the current room,
    starting from bottom left
    * rooms_status is a dictionary where a key is a coordinate tuple and 
    a value is either "clean" or "dirty".

    Valid actions are "goLeft", "goRight", "goUp", "goDown", "clean", "noOp".
    You can only "goUp" if you are in the bottom floor and "goDown" 
    if you are in the top floor. You can't "goLeft" in a (x,0) room and you 
    can´t "goRight" in a (x,2) room

    We can sense the location of the robot tuple (i,j) and the state of that location
    ("clean" or "dirty").
    Therefore, sense returns a tuple (location, clean?)

    """

    def state_to_str(self, state):
        location, rooms_state = state
        
        state_str = "loc:" + str(location) + "  "
        for i in range(2):
            state_str += "floor" + str(i) + "[ "
            for j in range(3):
                state_str += "'" + rooms_state[(i,j)] + "' "
            state_str += "]  "
        
        return state_str
        
    def next_state(self, current_state, action):
        if not self.is_valid_action(current_state, action):
            raise ValueError("Action not valid for current state")

        current_location, rooms_state = current_state
        i, j = current_location
        
        if action is 'clean':
            rooms_state[current_location] = "clean"
            return current_location, rooms_state

        return (current_state if action is 'noOp' else
                ((i,j-1), rooms_state)    if action is 'goLeft' else
                ((i,j+1), rooms_state)    if action is 'goRight' else
                ((i-1,j), rooms_state)    if action is 'goDown' else
                ((i+1,j), rooms_state)) # if action is 'goUp'

    def sense(self, state):
        location, rooms_status = state
        return location, rooms_status[location]

    def is_valid_action(self, state, action):
        return action in valid_actions(state[0])
    
    def performance(self, state, action):
        if action is "noOp" and is_all_clean(state[1]):
            return 0
        elif action is "goUp" or action is "goDown":
            return -2
        else:
            return -1
    
        

class SixRoomsRandomAgent(enviroment.Agent):
    """
    An agent that returns a random valid action 

    """        
    def act(self, perception):
        return choice(valid_actions(perception[0]))


class ReflexAgentSixRooms(enviroment.Agent):
    """
    A simple Reflex Agent

    """

    def act(self, perception):
        location, status = perception
        floor, room = location
        
        if status is not 'clean': return 'clean'
        
        # The agent will explore the rooms in a counter-clockwise fashion
        if floor is 0: # Go right until getting to last room, then go up
            if room is not 2:
                return 'goRight'
            else:
                return 'goUp'
        else: # Go left until getting to first room, then go down
            if room is not 0:
                return 'goLeft'
            else:
                return 'goDown'
   

class ModelReflexAgentSixRooms(enviroment.Agent):
    """
    model-based reflex agent

    """
    def __init__(self):
        """
        Starts model in worst-case scenario

        """
        self.rooms = {(1,0):"dirty", (1,1):"dirty", (1,2):"dirty",
                     (0,0):"dirty", (0,1):"dirty", (0,2):"dirty" }
        self.location = (0,0)

    def act(self, perception):
        new_location, status = perception

        # Refresh inner model
        self.location = new_location
        self.rooms[self.location] = status
        
        # Decides based on inner model
        if is_all_clean(self.rooms): return 'noOp'
        if status is not 'clean': return 'clean'
        
        floor, room  = self.location
        vertical_movement = ('goUp' if floor is 0 else 'goDown')        
        
        if is_floor_clean(self.rooms, floor):
            return vertical_movement
        
        if room is 2: return 'goLeft'
        elif room is 1 and self.rooms[floor,0] is not 'clean':
            return 'goLeft'
        else:
            return 'goRight'


def test():
    """
    Enviroment and agents tests

    """
    default_state = ((0,0), {(0,0):"dirty", (0,1):"dirty", (0,2):"dirty", (1,0):"dirty", (1,1):"dirty", (1,2):"dirty"})
    print "Test SixRooms enviroment with random agent"
    enviroment.simulate(SixRooms(),
                       SixRoomsRandomAgent(),
                       deepcopy(default_state),
                        100)

    print "Test SixRooms enviroment with reflex agent"
    enviroment.simulate(SixRooms(),
                       ReflexAgentSixRooms(),
                       deepcopy(default_state),
                        100)

    print "Test SixRooms enviroment with model-based reflex agent"
    enviroment.simulate(SixRooms(),
                       ModelReflexAgentSixRooms(),
                       deepcopy(default_state),
                        100)

if __name__ == '__main__':
    test()
