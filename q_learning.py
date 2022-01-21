import numpy as np
import random
from create_states import reformat


class Agent:
    """
    proximity = ['far', 'close']
    sensors = ['RR', 'R', 'C', 'L', 'LL'] #only front
    """

    simulation = None

    actions = ['L', 'SL', 'C', 'R', 'SR']
    states_cat = None
    states = None

    moving_penalty = -0.2
    collision_penalty = -10

    Q = {}
    gamma = 1
    epsilon = 0.6
    lr = 0.6

    def __init__(self, simulation=True, states_cat='CF'):
        self.simulation = simulation
        self.states_cat = states_cat
        self.initialise_states()
        self.initialise_q()

    def initialise_q(self):
        for s in self.states:
            self.Q[s] = {}
            for a in self.actions:
                self.Q[s][a] = 0

    def initialise_states(self):
        self.states = reformat(self.states_cat, 3)

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
        # print('before move', self.Q[state])
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
        else:
            action = max(self.Q[state], key=self.Q[state].get)
        # print("action chosen", action)
        return action

    def get_instant_reward(self, old_irs, new_irs, action):
        proximity = 0
        for sensor in range(len(old_irs)):
            proximity += new_irs[sensor] - old_irs[sensor]

        movement = 0
        if action != 'C':
            movement = self.moving_penalty

        reward = proximity + movement
        return reward

    def get_collision_penalty(self):
        return self.collision_penalty

