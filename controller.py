#!/usr/bin/env python3
from __future__ import print_function

import time
import numpy as np

import robobo
import cv2
import sys
import signal
import prey
import random

from data_analysis import *
from send_commands import make_move, get_current_state


def terminate_program(signal_number, frame):
    print("Ctrl-C received, terminating program")
    sys.exit(1)


def main():
    signal.signal(signal.SIGINT, terminate_program)

    simulation = True
    states_cat = 'VCF'  # CF or VCF

    # get policy
    policy = open_file('data/policy_1_5.json')
    policy = transform_policy(policy)

    # change very_close to None if using CF
    very_close = 0.12
    close_side = 0.15
    close_center = 0.18

    actions = ['L', 'SL', 'C', 'R', 'SR']

    moves_limit = 100

    if simulation:
        rob = robobo.SimulationRobobo().connect(address='192.168.68.106', port=19997)
    else:
        rob = robobo.HardwareRobobo(camera=True).connect(address="10.15.3.238")

    for move in range(moves_limit):
        irs = np.array(rob.read_irs())
        irs = [irs[i] for i in [7, 5, 3]]

        state = get_current_state(simulation, states_cat,
                                  irs, close_side, close_center, very_close=very_close)
        print(state)

        time.sleep(0.1)

        if state == 'FFF':
            if random.uniform(0, 1) < 0.2:
                action = random.choice(actions)
            else:
                action = 'C'
        else:
            action = policy[state]

        make_move(action, rob)
        time.sleep(0.1)

    rob.stop_world()
    time.sleep(0.3)


if __name__ == "__main__":
    main()
