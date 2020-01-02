import numpy as np
import pandas as pd


def split(df, perc_train=80):
    # Get all session id
    session_ids = df.session_id.unique()
    sessions_length = len(session_ids)
    train_session_length = int(perc_train / 100 * sessions_length)
    train_last_session_id = session_ids[train_session_length]
    train_last_index = int(df[df.session_id == train_last_session_id][-1:].index[0])

    train = df[:train_last_index + 1]
    ground_truth = df[train_last_index + 1:]

    last_step = [x - 1 for x in np.array(ground_truth[ground_truth.step == 1].index)[1:]]

    test = ground_truth.copy()

    for step in last_step:
        print(step)
        if test.loc[step].action_type == 'clickout item':
            test.loc[step].reference = np.nan

    train.to_csv("train.csv")
    test.to_csv("test.csv")
    ground_truth.to_csv("ground_truth.csv")


data = pd.read_csv('../dataset/test.csv', nrows=100000)
split(data)