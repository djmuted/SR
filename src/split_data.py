import pandas as pd
import numpy as np


def prepare_train_session_last_index(df, rate):
    session_ids = df.session_id.unique()

    train_sessions_num = int(rate * len(session_ids))
    train_end_session_id = session_ids[train_sessions_num]

    # index[0] - fetch id of element
    return int(df[df.session_id == train_end_session_id][-1:].index[0])


def prepare_last_step_indexes(ground_truth):
    first_step_indexes = (np.array(ground_truth[ground_truth.step == 1].index))
    return [x - 1 for x in first_step_indexes[1:]]


def create_test_dataset_and_labels(ground_truth):
    last_step_indexes = prepare_last_step_indexes(ground_truth)

    test = ground_truth.copy()
    labels = test[(test.index.isin(last_step_indexes)) & (test.action_type == CLICK_OUT_ITEM)][REFERENCE]

    test.loc[test.index.isin(last_step_indexes) & (test.action_type == CLICK_OUT_ITEM),
             REFERENCE] = np.nan

    return test, labels


def ground_truth_sub(ground_truth):
    ground_truth_submission = pd.DataFrame(columns=['reference', 'impressions', 'prices'])
    last_step_indexes = prepare_last_step_indexes(ground_truth)

    counter = 0
    for index, row in ground_truth.iterrows():
        if index in last_step_indexes and row['action_type'] == 'clickout item':
            print(row['reference'],  row['impressions'],  row['prices'])
            ground_truth_submission.loc[counter] = [row['reference'], row['impressions'], row['prices']]
            counter = counter + 1

    return ground_truth_submission


def split_dataset(df, rate):
    train_session_last_index = prepare_train_session_last_index(df, rate)

    train = df[:train_session_last_index + 1]

    ground_truth = df[train_session_last_index + 1:]
    test, label = create_test_dataset_and_labels(ground_truth)

    ground_truth_submission = ground_truth_sub(ground_truth)

    return train, test, ground_truth, label, ground_truth_submission


CLICK_OUT_ITEM = 'clickout item'
REFERENCE = 'reference'

if __name__ == '__main__':
    core_dataset = pd.read_csv('../dataset/test.csv', nrows=10000)
    train_df, test_df, ground_truth_df, label_df, ground_truth_submission = split_dataset(core_dataset, 0.8)

    # train_df.to_csv('../data/train.csv')
    # ground_truth_df.to_csv('../data/ground_truth.csv')
    # test_df.to_csv('../data/test.csv')
    # label_df.to_csv('../data/label.csv')
    ground_truth_submission.to_csv('../data/ground_truth_submission.csv')
