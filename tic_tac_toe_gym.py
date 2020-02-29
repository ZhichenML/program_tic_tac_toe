import random
import collections
import os
import sys
import numpy as np


def save_experience(states, file):
    with open(file, 'w') as exp:
        for s in states:
            dat = [str(x) for x in s[0]]
            dat = ','.join(dat)
            exp.write(dat+'\n')
            dat = [str(x) for x in s[1]]
            dat = ','.join(dat)
            exp.write(dat+'\n')

def load_experience(file):
    states = []
    with open(file, 'r') as exp:
        lines = [x.strip() for x in exp.readlines()]
        lines = [x.split(',') for x in lines]
        dat  = []
        for e in lines:
            temp = [int(x) for x in e]
            dat.append(temp)
        states = []
        for i in range(0,len(dat),2):
            states.append([dat[i], dat[i+1]])

    return states

# zhichen: expand the decision tree level
def next_level(statesa, statesb, move): # states1 = [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0], [0,0,0,0,1,0,0,0,0]], states2 = [], 2
    for i in range(len(statesa)):
        for j in range(9):
            ns = []
            if statesa[i][j]==0:
                ns = list(statesa[i])
                ns[j] = move
                statesb.append(ns)

# zhichen: vertical flip and rotation covers all possible transformations
def flip_vertical(state):
    f_state = list(state)
    f_state[2] = state [0]
    f_state[5] = state [3]
    f_state[8] = state [6]

    f_state[0] = state [2]
    f_state[3] = state [5]
    f_state[6] = state [8]

    return f_state

def rotate_right(state):
    r_state = list(state)
    r_state[0] = state[6]
    r_state[2] = state[0]
    r_state[8] = state[2]
    r_state[6] = state[8]

    r_state[1] = state[3]
    r_state[5] = state[1]
    r_state[7] = state[5]
    r_state[3] = state[7]

    return r_state

def inverse_transform_state(state, rotate_right, flip):

    rotate_right = 4 - rotate_right
    st = list(state)
    while rotate_right > 0:
        rotate_right = rotate_right - 1
        st = rotate_right(st)

    if flip == 1:
        st = flip_vertical(st)

    return st


def inverse_transform_action(action, rotate_right, flip):

    rotate_right = 4 - rotate_right
    while rotate_right > 0:
        rotate_right = rotate_right - 1
        if action == 1:
            action = 5
        elif action == 5:
            action = 7
        elif action == 7:
            action = 3
        elif action == 3:
            action = 1
        elif action == 0:
            action = 2
        elif action == 2:
            action = 8
        elif action == 8:
            action = 6
        elif action == 6:
            action = 0

    if flip == 1:
        if action == 0:
            action = 2
        elif action == 3:
            action = 5
        elif action == 6:
            action = 8
        elif action == 2:
            action = 0
        elif action == 5:
            action = 3
        elif action == 8:
            action = 6

    return action

def forward_transform_action(action, rotate_right, flip):

    if flip == 1:
        if action == 0:
            action = 2
        elif action == 3:
            action = 5
        elif action == 6:
            action = 8
        elif action == 2:
            action = 0
        elif action == 5:
            action = 3
        elif action == 8:
            action = 6

    while rotate_right > 0:
        rotate_right = rotate_right - 1
        if action == 1:
            action = 5
        elif action == 5:
            action = 7
        elif action == 7:
            action = 3
        elif action == 3:
            action = 1
        elif action == 0:
            action = 2
        elif action == 2:
            action = 8
        elif action == 8:
            action = 6
        elif action == 6:
            action = 0

    return action

def delete_duplicates(states):
    indices = []
    # zhichen: if i in indices, do not need to compare
    for i in range(len(states) - 1):
        temp = list(states[i])
        for j in range(i+1, len(states)):
            match, rot, flip = isequal(states[j], temp)
            if(match): # All orientation of temp will be checked here
                    indices.append(j)
            else:
                continue

    indices = list(set(indices))

    unique_states = []
    for k in range(len(states)):
        if(bool(indices.count(k))):
            continue
        else:
            unique_states.append(states[k])

    return unique_states


def set_random_moves(states):
    states_action = []
    for i in range(len(states)):
        actions = []
        for j in range(len(states[i])):
            if states[i][j] == 0:
                actions.append(j)
                actions.append(j)

        sa = [states[i] , actions]
        states_action.append(sa)
        print(i)
    return states_action




def isequal(state, present_state):
    rotation = 0
    flip = 0

    temp = list(present_state)
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip


    temp = rotate_right(temp) #1st rotation
    rotation = rotation + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = rotate_right(temp) #2nd rotation
    rotation = rotation + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = rotate_right(temp) #3rd rotation
    rotation = rotation + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = list(present_state)
    rotation = 0
    temp = flip_vertical(temp) #Flip
    flip = flip + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = rotate_right(temp) #1st rotation
    rotation = rotation + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = rotate_right(temp) #2nd rotation
    rotation = rotation + 1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    temp = rotate_right(temp) #3rd rotation
    rotation = rotation +1
    matched = True
    for i in range(len(state)):
        if state[i] != temp[i]:
            matched = False
            break
    if matched:
        return True, rotation, flip

    return False, rotation, flip

# zhichen: epsilon is like 0.1
def action_epsilon_greedy(actions, epsilon):

    a = list(set(actions))
    confidence = dict()

    if len(a) == 1:
        return a[0]

    best_action = max(set(actions), key=actions.count)
    random_action = random.choice(a)

    for move in actions:
        confidence[move] = float(actions.count(move))/float(len(actions)) * 100

    if np.random.uniform() > epsilon:
        return best_action, confidence
    else:
        return random_action, confidence



class Agent():
    def __init__(self):
        states1 = [[1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0], [0,0,0,0,1,0,0,0,0]]
        states2 = []
        states3 = []
        states4 = []
        states5 = []
        states6 = []
        states7 = []
        states8 = []
        states9 = []
        
        try:
            print("Trying to load experience.dat..")
            states = load_experience('experience.dat')
            print("Successfully load! ", "No of state: ", len(states))
        except:
            print("STATUS: experience.dat not found.")
            print("Generating states...")
        
            next_level(states1,states2,2)
            print("1st level state reduction..")
            states2 = delete_duplicates(states2)
        
            next_level(states2,states3,1)
            print("2nd level state reduction..")
            states3 = delete_duplicates(states3)
        
            next_level(states3,states4,2)
            print("3rd level state reduction..")
            states4 = delete_duplicates(states4)
        
            next_level(states4,states5,1)
            print("4th level state reduction..")
            states5 = delete_duplicates(states5)
        
            next_level(states5,states6,2)
            print("5th level state reduction..")
            states6 = delete_duplicates(states6)
        
            next_level(states6,states7,1)
            print("6th level state reduction..")
            states7 = delete_duplicates(states7)
        
            next_level(states7,states8,2)
            print("7th level state reduction..")
            states8 = delete_duplicates(states8)
        
            next_level(states8,states9,1)
            print("8th level state reduction..")
            states9 = delete_duplicates(states9)
        
            states = states1 + states2 + states3 + states4 + states5 + states6 + states7 + states8 + states8
            states = set_random_moves(states)
            states = states + [[[0,0,0,0,0,0,0,0,0],[0,0,1,1,4,4]]]
            save_experience(states, 'zero_experience.dat')
            print("No of state: ", len(states))

        self.states = states


    def act(self, state, epsilon):
        found = False
        for s in self.states:
            match, rot, flip = isequal(s[0], state)
            if match:

                move1_internal, confidence = action_epsilon_greedy(s[1], epsilon)

                move1_actual = inverse_transform_action(move1_internal, rot, flip)

                found = True
                break

        if(found == False):
            print(state)
            print("Game error: Unable to find state")
            save_experience(self.states, 'log.dat')
            sys.exit()

        return move1_actual, confidence






    def learn(self, game_state, win):
        rew = int((10 - len(game_state))/2) # More addition for shorter game length
        for i in range(len(game_state)-1):
            action_actual = (game_state[i][1])[0]
            for j in range(len(self.states)):
                match, rot, flip = isequal(self.states[j][0],game_state[i][0])
                if match:
                    action_internal = forward_transform_action(action_actual, rot, flip)
                    if win == 1:
                        if((i+1) % 2 != 0):
                            loop = rew  + int((9 - (len(game_state) - i - 2))/2)
                            # print "rew: " , rew
                            # print "Bonus: ", int((9 - (len(game_state) - i - 2))/2)
                            # sss = input("sss ")
                            for n in range(loop):
                                self.states[j][1].append(action_internal)
                            if((self.states[j][0])[action_internal] != 0):
                                print("Wrong insertion")
                                print(self.states[j][0])
                                print(action_actual)
                                print(rot, ' ', flip)
                                print(action_internal)
                                sys.exit()

                        else:
                            loop = rew  + int((9 - (len(game_state) - i - 2))/2)
                            for n in range(loop):
                                if(self.states[j][1].count(action_internal) > 1):
                                    self.states[j][1].remove(action_internal)
                    if win == 2:
                        if((i+1) % 2 != 0):
                            loop = rew  + int((9 - (len(game_state) - i - 2))/2)
                            for n in range(loop):
                                if(self.states[j][1].count(action_internal) > 1):
                                    self.states[j][1].remove(action_internal)
                        else:
                            loop = rew  + int((9 - (len(game_state) - i - 2))/2)
                            for n in range(loop):
                                self.states[j][1].append(action_internal)
                            if((self.states[j][0])[action_internal] != 0):
                                print("Wrong insertion")
                                print(self.states[j][0])
                                print(action_actual)
                                print(rot, ' ', flip)
                                print(action_internal)
                                sys.exit()

        print("New experience gained")







class Tic_tac_toe():
    def __init__(self):
        self.game_state = [[[0,0,0,0,0,0,0,0,0],[]]]

    def reset(self):
        self.game_state = [[[0,0,0,0,0,0,0,0,0],[]]]
        return self.game_state[-1][0]

    def step(self, action, turn):
        self.game_state[-1][1].append(action)
        new_state = list(self.game_state[-1][0])
        new_state[action] = turn
        self.game_state.append([new_state, []])

        self.display()

        r = 0
        done = False

        win = self.check_win()
        if win != 0:
            done = True

        if win == 1:
            print("PLAYER 1 WON")
            r = 1
        elif win == 2:
            print("PLAYER 2 WON")
            r = -1

        if sum(self.game_state[-1][0]) == 13 or sum(self.game_state[-1][0]) == 14:
            print("GAME DRAW")
            r = 0

        return self.game_state[-1][0], r, done, win

    def check_win(self):
        state = self.game_state[-1][0]
        if state[0] == 1 and state[1] == 1 and state[2] == 1:
            return 1
        if state[3] == 1 and state[4] == 1 and state[5] == 1:
            return 1
        if state[6] == 1 and state[7] == 1 and state[8] == 1:
            return 1
        if state[0] == 1 and state[3] == 1 and state[6] == 1:
            return 1
        if state[1] == 1 and state[4] == 1 and state[7] == 1:
            return 1
        if state[2] == 1 and state[5] == 1 and state[8] == 1:
            return 1
        if state[0] == 1 and state[4] == 1 and state[8] == 1:
            return 1
        if state[2] == 1 and state[4] == 1 and state[6] == 1:
            return 1


        if state[0] == 2 and state[1] == 2 and state[2] == 2:
            return 2
        if state[3] == 2 and state[4] == 2 and state[5] == 2:
            return 2
        if state[6] == 2 and state[7] == 2 and state[8] == 2:
            return 2
        if state[0] == 2 and state[3] == 2 and state[6] == 2:
            return 2
        if state[1] == 2 and state[4] == 2 and state[7] == 2:
            return 2
        if state[2] == 2 and state[5] == 2 and state[8] == 2:
            return 2
        if state[0] == 2 and state[4] == 2 and state[8] == 2:
            return 2
        if state[2] == 2 and state[4] == 2 and state[6] == 2:
            return 2

        return -1


    def display(self):
        game_state = self.game_state[-1][0]
        gs = list(game_state)
        for i in range(len(gs)):
            if gs[i] == 1:
                gs[i] = "X"
            if gs[i] == 2:
                gs[i] = "O"
            if gs[i] == 0:
                gs[i] = " "

        line1 = gs[0:3]
        line2 = gs[3:6]
        line3 = gs[6:9]
        print("")
        print("  ",line1[0],"  |  ",line1[1],"  |  ", line1[2])
        print("----------------------")
        print("  ",line2[0],"  |  ",line2[1],"  |  ", line2[2])
        print("----------------------")
        print("  ",line3[0],"  |  ",line3[1],"  |  ", line3[2])

        print("\n\nMAP\n\n")
        print("  ","0","  |  ","1","  |  ", "2")
        print("----------------------")
        print("  ","3","  |  ","4","  |  ", "5")
        print("----------------------")
        print("  ","6","  |  ","7","  |  ", "8")
        print("")

def start_self_play(iteration):
    for i in range(iteration):

        if i < iteration * 0.25:
            #random game
            epsilon1 = 0
            epsilon2 = 0

        elif i < iteration * 0.5:
            #Random strategy with best opponent
            epsilon1 = 1
            epsilon2 = 0

        elif i < iteration * 0.75:
            #Best strategy With random opponent
            epsilon1 = 0
            epsilon2 = 1

        elif i < iteration * 1.0:
            #mixed strategy
            epsilon1 = 0.3
            epsilon2 = 0.3

        # epsilon1 = 1
        # epsilon2 = 1
        env = Tic_tac_toe()
        state = env.reset()
        player1 = Agent()
        player2 = player1

        win = 0
        print("\n\n\nNew Game "+ str(i))
        print("==========")
        print("")
        print("epsilon1: ",epsilon1,"   epsilon2: ",epsilon2)
        while True:
            # print "\n\nSearching move 1...\n"
            # print "Game state: ", game_state[-1][0]
            action1, confidence = player1.act(state, epsilon1)
            new_state, r, done, win = env.step(action1, turn=1)
            if win != 0:
                player1.learn(env.game_state, win=1)
                break

            action2, confidence = player2.act(new_state, epsilon2)
            print(action2)
            new_state2, r, done, win = env.step(action2, turn=2)
            if win != 0:
                player2.learn(env.game_state, win=2)
                break


def start_human_play():
    for i in range(1):
        env = Tic_tac_toe()
        state = env.reset()
        player = Agent()
        win = 0
        print("\n\n\nNew Game "+ str(i))
        print("==========\n\n")
        print("")
        while True:
            print("Machine played.....")

            action, confidence = player.act(state, epsilon=0)
            for key,value in confidence.items():
                print('Move {key}: Confidence {value}%'.format(key = key, value = value))
            new_state, r, done, win = env.step(action, turn=1)

            if win !=0:
                break


            while True:
                print("Your move...")
                move2 = int(eval(input("Index: ")))

                if new_state[move2] !=0:
                    continue
                new_state, r, done, win = env.step(move2, turn=2)
                break

            state = new_state
            if win !=0:
                break



def start_human_play2():
    for i in range(1):
        env = Tic_tac_toe()
        state = env.reset()
        player = Agent()
        win = 0
        print("\n\n\nNew Game "+ str(i))
        print("==========\n\n")
        print("")
        while True:
            while True:
                print("Your move...")
                move2 = int(eval(input("Index: ")))

                if state[move2] !=0:
                    continue
                new_state, r, done, win = env.step(move2, turn=1)
                break

            if win !=0:
                break

            print("Machine played.....")

            action, confidence = player.act(new_state, epsilon=0)
            for key,value in confidence.items():
                print('Move {key}: Confidence {value}%'.format(key = key, value = value))
            new_state, r, done, win = env.step(action, turn=2)


            state = new_state
            if win !=0:
                break


from Program_strategy import program_policy


def start_program_human_play():
    for i in range(1):
        env = Tic_tac_toe()
        state = env.reset()
        player = program_policy()
        win = 0
        print("\n\n\nNew Game "+ str(i))
        print("==========\n\n")
        print("")
        while True:
            print("Machine played.....")

            action = player.act(state)
            new_state, r, done, win = env.step(action, turn=1)

            if win ==1 or win ==2 or sum(new_state) == 13 or sum(new_state) == 14:
                break


            while True:
                print("Your move...")
                move2 = int(eval(input("Index: ")))

                if new_state[move2] !=0:
                    continue
                new_state, r, done, win = env.step(move2, turn=2)
                break

            state = new_state
            if win ==1 or win ==2 or sum(new_state) == 13 or sum(new_state) == 14:
                break

def start_program_human_play2():
    for i in range(1):
        env = Tic_tac_toe()
        state = env.reset()
        player = program_policy()
        win = 0
        print("\n\n\nNew Game "+ str(i))
        print("==========\n\n")
        print("")
        while True:
            print("Your move...")
            while True:
                move2 = int(eval(input("Index: ")))

                if state[move2] !=0:
                    continue
                new_state, r, done, win = env.step(move2, turn=2)
                break

            if win ==1 or win ==2 or sum(new_state) == 13 or sum(new_state) == 14:
                break


            print("Machine played.....")

            action = player.act(new_state)
            new_state, r, done, win = env.step(action, turn=1)

            state = new_state
            if win ==1 or win ==2 or sum(new_state) == 13 or sum(new_state) == 14:
                break



##############################################################

####################################################################################################

# start_self_play(10000)
# save_experience(states, 'experience.dat')
#start_human_play2()

start_program_human_play2()


