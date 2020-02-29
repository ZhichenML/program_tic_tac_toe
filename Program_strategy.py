import numpy as np
from tic_tac_toe import check_to_win

def set_corner(state):
    corner = [0,2,6,8]
    random_loc = [i for i in corner if state[i]==0]
    available_loc = [i for i in random_loc if state[8-i]==0]
    if available_loc != []:
        loc = np.random.choice(available_loc)
    else:
        loc = np.random.choice(random_loc)
    return loc


def set_side(state):
    side = [1,3,5,7]
    random_loc = [i for i in side if state[i]==0]
    available_loc = [i for i in random_loc if state[8-i]==0]
    if available_loc != []:
        loc = np.random.choice(available_loc)
    else:
        loc = np.random.choice(random_loc)
    return loc

def set_center(state):
    return 4

def empty_center(state):
    if state[4] == 0:
        return True
    else:
        return False

def available_corner(state):
    corner = [0,2,6,8]
    available_corner = [i for i in corner if state[i]==0]
    return available_corner!=[]

def available_side(state):
    side = [1,3,5,7]
    available_side = [i for i in side if state[i]==0]
    return available_side!=[]


class program_policy():

    def act(self, state):

        to_winner, loc = check_to_win(state)
        action = 4
        if to_winner!=0:
            action = loc
        elif empty_center(state) == True:
            print('empty center')
            action = 4
        elif available_corner(state) == True:
            action = set_corner(state)
            print('set_corner', action)
        elif available_side(state) == True:
            action = set_side(state)
            print('set_side', action)

        return action

