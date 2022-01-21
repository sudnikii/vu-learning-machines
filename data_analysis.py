import pandas as pd
import json
import numpy as np
import plotly as plt


def save_file(data, lr, run, policy=False):
    if policy:
        a_file = open('policy_{}_{}.json'.format(run, 10*lr), "w")
        json.dump(data, a_file)
        a_file.close()
    else:
        data = list(zip(data[0], data[1]))
        df = pd.DataFrame(data,
                          columns=['moves_count', 'average_rewards'])
        df.to_csv('eval_{}_{}.csv'.format(run, 10*lr))


def open_file(file_dir):
    if '.json' in file_dir:
        f = open(file_dir)
        policy = json.load(f)
        return policy
    else:
        df = pd.read_csv(file_dir)
        return df


def plot():
    pass


def get_number_of_collisions(df, start_epoch):
    number = df['moves_count'][start_epoch:].value_counts()['99']

    return number


def transform_policy(policy):
    policy_t = {}
    for state in policy:
        policy_t[state] = max(policy[state], key=policy[state].get)

    return policy_t




