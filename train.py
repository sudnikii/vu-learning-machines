#!/usr/bin/env python3
from __future__ import print_function

import time
import numpy as np
import robobo
import cv2
import signal
import prey

from send_commands import terminate_program, get_current_state, stop, make_move
from data_analysis import save_file
from q_learning import *

np.set_printoptions(suppress=True)


def main(run):
    signal.signal(signal.SIGINT, terminate_program)

    # change to False if Robobo used in real life
    simulation = True

    # threshold categories CF or VCF
    states_cat = 'VCF'

    # q learning agent initialisation
    agent = Agent(simulation=True, states_cat=states_cat)

    # start with pretrained policy
    # policy = open_file('data/policy_1_5.json')

    # parameters
    epochs = 150
    moves_limit = 100

    # proximity thresholds
    very_close = 0.12  # if using CF change to None
    close_side = 0.16
    close_center = 0.18
    collision = 0.1

    # epsilon
    ep_init = 0.6
    ep_end = 0.1

    # lr
    # agent.lr =

    moves_count = np.zeros(epochs)
    average_rewards = np.zeros(epochs)

    # number of epochs
    for epoch in range(epochs):
        print("epoch:", epoch)

        if simulation:
            rob = robobo.SimulationRobobo().connect(address='192.168.68.106', port=19997)
        else:
            rob = robobo.HardwareRobobo(camera=True).connect(address="10.15.3.238")

        # decrease epsilon over time
        r = np.max(((epochs - epoch) / epochs), 0)
        agent.epsilon = ((ep_init - ep_end) * r) + ep_end

        # start simulation
        time.sleep(0.5)
        rob.play_simulation()

        # collect performance values
        epoch_rewards = 0

        # number of moves
        for move in range(moves_limit):
            # print("move:", move)
            irs = np.array(rob.read_irs())
            irs = [irs[i] for i in [7, 5, 3]]
            current_state = get_current_state(simulation, states_cat,
                                              irs, close_side, close_center, very_close)
            print('current state', current_state)

            time.sleep(0.1)
            action = agent.choose_action(current_state)
            make_move(action, rob)
            time.sleep(0.1)

            new_irs = np.array(rob.read_irs())
            new_irs = [new_irs[i] for i in [7, 5, 3]]
            new_state = get_current_state(simulation, states_cat,
                                          new_irs, close_side, close_center, very_close=very_close)

            reward = agent.get_instant_reward(irs, new_irs, action)

            if stop(new_irs, collision):
                reward = agent.collision_penalty
                epoch_rewards += reward
                agent.update_q(current_state, action, new_state, reward)
                break

            epoch_rewards += reward
            agent.update_q(current_state, action, new_state, reward)

        moves_count[epoch] = move
        average_rewards[epoch] = epoch_rewards / move

        print(agent.Q)
        print(moves_count)

        # Stopping the simulation resets the environment
        if simulation:
            time.sleep(0.3)
            rob.stop_world()

        if epoch % 10 == 0:
            data = [moves_count, average_rewards]
            save_file(data, agent.lr, run)
            save_file(agent.Q, agent.lr, run, policy=True)


if __name__ == "__main__":
    main(run=1)
    main(run=2)
    main(run=3)
