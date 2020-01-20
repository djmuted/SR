import numpy as np
import pandas as pd


def split(df, perc_train=80):
    # Get all session id
    session_ids = df.session_id.unique()
    sessions_length = len(session_ids)

    train_session_length = int(perc_train / 100 * sessions_length)
    train_last_session_id = session_ids[train_session_length]

    train_last_index = int(df[df.session_id == train_last_session_id][-1:].index[0])

    last_index = train_last_index + 1
    train = df[0:last_index]
    ground_truth = df[last_index:]

    train.to_csv("../data/train.csv")
    ground_truth.to_csv("../data/ground_truth.csv")

    last_steps = [x - 1 for x in np.array(ground_truth[ground_truth.step == 1].index)[1:]]
    test = ground_truth.copy()

    for step in last_steps:
        if ground_truth.loc[step]['action_type'] == 'clickout item':
            test['reference'][step] = np.nan

    test.to_csv("../data/test.csv")


data = pd.read_csv('../dataset/train.csv')

split(data)
