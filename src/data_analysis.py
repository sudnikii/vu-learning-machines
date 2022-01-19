import pandas as pd
import json


def save_file(data, epsilon, lr, run, policy=False):
    if policy:
        a_file = open("policy_{}_{}_{}.csv'.format(run, epsilon, lr).json", "w")
        json.dump(data, a_file)
        a_file.close()
    else:
        data = list(zip(data[0], data[1]))
        df = pd.DataFrame(data,
                          columns=['moves_count', 'average_rewards'])
        df.to_csv('eval_{}_{}_{}.csv'.format(run, epsilon, lr))
