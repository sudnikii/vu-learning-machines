import numpy as np
import random
from create_states import reformat


class Agent:
    """
    proximity = ['far', 'close', 'very close']
    sensors = ['RR', 'R', 'C', 'L', 'LL'] #only front
    """

    simulation = True

    actions = ['L', 'SL', 'C', 'R', 'SR']
    states = reformat('CFV', 3)

    Q = {}
    very_close_side = 0.1
    very_close_center = 0.12
    close = 0.3
    gamma = 1
    epsilon = None
    lr = None

    def __init__(self, simulation=True, epsilon=0.25, lr=0.6):
        self.simulation = simulation
        self.epsilon = epsilon
        self.lr = lr
        self.initialise_q()

    def initialise_q(self):
        for s in self.states:
            self.Q[s] = {}
            for a in self.actions:
                self.Q[s][a] = 0

    def update_q(self, state, action, new_state, reward):
        new_state_q_values = self.get_new_state_q_values(new_state)
        self.Q[state][action] = round(self.Q[state][action] + self.lr * (
                reward + self.gamma * np.max(new_state_q_values) - self.Q[state][action]), 5)

    def get_new_state_q_values(self, new_state):
        values = []
        for a in self.actions:
            values.append(self.Q[new_state][a])
        return values

    def choose_action(self, state):
        print('before move', self.Q[state])
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
        else:
            action = max(self.Q[state], key=self.Q[state].get)
        print("action chosen", action)
        return action

    def get_current_state(self, irs):
        state = ''
        for i in range(len(irs)):
            if i == 0 or i == 2:
                very_close = self.very_close_side
            else:
                very_close = self.very_close_center

            if self.simulation:
                if irs[i] < very_close:
                    state += "V"
                elif irs[i] < self.close:
                    state += "C"
                else:
                    state += "F"
            else:
                if irs[i] > self.very_close:
                    state += "V"
                elif irs[i] > self.close:
                    state += "C"
                else:
                    state += "F"
        return state

    def get_reward3(self, action, irs):
        # depending on the proximity to the obstacle
        proximity = 10*sum(irs) - 30

        # depending on the action taken, we want to reinforce moving forward
        movement = 0
        if proximity == 0:
            if action != 'C':
                movement = -5

        reward = proximity + movement
        return round(reward, 5)

    def get_reward2(self, state, action):
        if "V" in state:
            return -100
        elif "CCC" in state:
            return -50
        elif "CC" in state:
            return -20
        elif "C" in state:
            return -10
        else:
            if action != 'C':
                return 0
            else:
                return 5

    def get_reward(self, old_irs, new_irs, action):
        proximity = 0
        for sensor in range(len(old_irs)):
            proximity += new_irs[sensor] - old_irs[sensor]

        movement = 0
        if sum(old_irs) == 3:
            if action != 'C':
                movement = -0.1

        reward = proximity + movement
        return round(reward, 5)


