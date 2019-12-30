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
    labels = test[(test.index.isin(last_step_indexes))
                  & (test.action_type == CLICK_OUT_ITEM)][REFERENCE]

    test.loc[test.index.isin(last_step_indexes) & (test.action_type == CLICK_OUT_ITEM),
             REFERENCE] = np.nan

    return test, labels


def split_dataset(df, rate):
    train_session_last_index = prepare_train_session_last_index(df, rate)

    train = df[:train_session_last_index + 1]
    ground_truth = df[train_session_last_index + 1:]
    test, label = create_test_dataset_and_labels(ground_truth)

    return train, test, ground_truth, label


CLICK_OUT_ITEM = 'clickout item'
REFERENCE = 'reference'

if __name__ == '__main__':
    core_dataset = pd.read_csv('../dataset/test.csv')
    train_df, test_df, ground_truth_df, label_df = split_dataset(core_dataset, 0.8)
    train_df.to_csv('../data/train.csv')
    ground_truth_df.to_csv('../data/ground_truth.csv')
    test_df.to_csv('../data/test.csv')
    label_df.to_csv('../data/label.csv')
