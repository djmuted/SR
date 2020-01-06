from pathlib import Path

import pandas as pd
import numpy as np

from src.baseline_algorithm import functions as f

current_directory = Path(__file__).absolute().parent
default_data_directory = current_directory.joinpath('..', '..', 'data')


def get_actions(train_df):
    df = pd.DataFrame(columns=['Reference', 'Score'])

    x = 0
    index = 0
    while x < len(train_df):
        session_id = str(train_df.loc[[x]]['session_id'][x])
        x = x + 1

        intesting = []
        while x < len(train_df) - 1 and str(train_df.loc[[x]]['session_id'][x]) == session_id:
            ref = str(train_df.loc[[x]]['reference'][x])
            if ref not in intesting and ref.isnumeric():
                intesting.append(ref)
            x = x + 1

        for i in intesting:
            df.loc[index] = [i, 1]
            index = index + 1

    df.sort_values(by=['Reference'])
    df = df.groupby('Reference').sum()
    df.to_csv('Score.csv')
    return df


def main(data_path):
    data_directory = Path(data_path) if data_path else default_data_directory
    train_csv = data_directory.joinpath('train.csv')
    test_csv = data_directory.joinpath('test.csv')
    subm_csv = data_directory.joinpath('submission_popular.csv')

    print(f"Reading {train_csv} ...")
    df_train = pd.read_csv(train_csv, nrows=10000)
    print(f"Reading {test_csv} ...")
    df_test = pd.read_csv(test_csv, nrows = 10000)

    print("Get popular items...")
    df_popular = pd.read_csv("Popular.csv")
    # df_popular = f.get_popularity(df_train)
    # df_popular.to_csv("Popular.csv")

    print("Get actions...")
    # df_popular = pd.read_csv("Actions.csv")
    df_actions = get_actions(df_train)
    df_popular.to_csv("Acions.csv")

    print("Identify target rows...")
    df_target = f.get_submission_target(df_test)

    print("Get recommendations...")
    df_expl = f.explode(df_target, "impressions")
    df_out = f.calc_recommendation(df_expl, df_popular, df_actions)

    print(f"Writing {subm_csv}...")
    df_out.to_csv(subm_csv, index=False)

    print("Finished calculating recommendations.")


data_dir_path = '../../data'
if __name__ == '__main__':
    main(data_dir_path)
