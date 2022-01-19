#!/usr/bin/env python3
from __future__ import print_function

import time
import numpy as np

np.set_printoptions(suppress=True)

import robobo
import cv2
import sys
import signal
import prey
from q_learning import *
from data_analysis import save_file


def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)


def make_move(action, rob):
    # actions
    actions = {
        "R": (5, 0),
        "SR": (10, 0),
        "C": (5, 5),
        "L": (0, 5),
        "SL": (0, 10)
    }

    rob_action = actions[action]
    rob.move(rob_action[0], rob_action[1], 2000)


def stop(irs, collision):
    for irs_value in irs:
        if irs_value < collision:
            return True


def main(epsilon, lr, run):
    # 192.168.68.106 Julia's home
    # 192.168.1.213 Chaymae's home
    # 10.15.3.238 Robobo lab

    signal.signal(signal.SIGINT, terminate_program)

    # change to False if Robobo used in real life
    simulation = True

    # q learning agent initialisation
    agent = Agent(simulation=simulation, epsilon=epsilon, lr=lr)

    epochs = 100
    moves_limit = 50
    collision = 0.08
    moves_count = np.zeros(epochs)
    average_rewards = np.zeros(epochs)

    # number of epochs
    for epoch in range(epochs):

        if simulation:
            rob = robobo.SimulationRobobo().connect(address='192.168.68.106', port=19997)
        else:
            rob = robobo.HardwareRobobo(camera=True).connect(address="10.15.3.238")

        if epoch%50 == 0:
            agent.epsilon = agent.epsilon - 0.1

        print("epoch:", epoch)
        rob.play_simulation()
        time.sleep(0.5)

        epoch_rewards = 0

        # number of moves
        for move in range(moves_limit):
            print("move:", move)
            irs = np.array(rob.read_irs())
            irs = [irs[i] for i in [7, 5, 3]]
            current_state = agent.get_current_state(irs)
            print('current state', current_state)

            time.sleep(0.1)
            action = agent.choose_action(current_state)
            make_move(action, rob)
            time.sleep(0.1)

            new_irs = np.array(rob.read_irs())
            new_irs = [new_irs[i] for i in [7, 5, 3]]
            new_state = agent.get_current_state(new_irs)
            print('new state', new_state)

            reward = agent.get_reward(new_state, action)
            if stop(new_irs, collision):
                reward = -10
            print(reward)

            epoch_rewards += reward
            agent.update_q(current_state, action, new_state, reward)

            print('after move', Agent.Q[current_state])

            if stop(new_irs, collision):
                print("Collision!")
                break

        moves_count[epoch] = move
        average_rewards[epoch] = epoch_rewards / move

        print(agent.Q)
        print(moves_count)
        print(average_rewards)

        # Stopping the simulation resets the environment
        if simulation:
            rob.stop_world()

    data = [moves_count, average_rewards]
    save_file(data, epsilon, lr, run)
    save_file(agent.Q, epsilon, lr, run, policy=True)


if __name__ == "__main__":
    main(epsilon=0.3, lr=0.4, run=1)
    main(epsilon=0.3, lr=0.4, run=2)
    main(epsilon=0.3, lr=0.6, run=1)
    main(epsilon=0.3, lr=0.6, run=2)
