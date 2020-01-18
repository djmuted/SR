from pathlib import Path

import pandas as pd
import numpy as np

from src.baseline_algorithm import functions as f

current_directory = Path(__file__).absolute().parent
default_data_directory = current_directory.joinpath('..', '..', 'data')


# def create_score(df_actions, df_popular, popular_ratio, action_ratio):
#     df_popular = df_popular * [1, 1, popular_ratio]
#     df_actions = df_actions * [1, 1, action_ratio]
#
#     concat = pd.concat([df_popular, df_actions], ignore_index=True)
#
#     concat.sort_values(by=['reference'])
#     concat = concat.groupby('reference').sum().reset_index()
#     concat.drop(columns=['Unnamed: 0'])
#     return concat
#
#
# def get_actions(train_df):
#     df = pd.DataFrame(columns=['reference', 'n_clicks'])
#
#     x = 0
#     index = 0
#     while x < len(train_df):
#         session_id = str(train_df.loc[[x]]['session_id'][x])
#         x = x + 1
#
#         intesting = []
#         while x < len(train_df) - 1 and str(train_df.loc[[x]]['session_id'][x]) == session_id:
#             ref = str(train_df.loc[[x]]['reference'][x])
#             if ref not in intesting and ref.isnumeric():
#                 intesting.append(ref)
#             x = x + 1
#
#         for i in intesting:
#             df.loc[index] = [i, 1]
#             index = index + 1
#
#     df.sort_values(by=['reference'])
#     df = df.groupby('reference').sum().reset_index()
#     df.to_csv('Score.csv')
#     return df


def main(data_path):
    data_directory = Path(data_path) if data_path else default_data_directory
    train_csv = data_directory.joinpath('train.csv')
    test_csv = data_directory.joinpath('test.csv')
    subm_csv = data_directory.joinpath('submission_popular.csv')

    print(f"Reading {train_csv} ...")
    df_train = pd.read_csv(train_csv)
    print(f"Reading {test_csv} ...")
    df_test = pd.read_csv(test_csv)

    print("Get popular items...")
    # df_popular = pd.read_csv("Popular.csv")
    df_popular = f.get_popularity(df_train)
    df_popular.to_csv("Popular.csv")

    # print("Get actions...")
    # df_actions = pd.read_csv("Score.csv")
    # df_actions = get_actions(df_train)
    # df_popular.to_csv("Score.csv.csv")

    # print("Get score...")
    # concat = create_score(df_actions, df_popular, popular_ratio, action_ratio)
    # concat.to_csv("Concat.csv")
    # concat_reading = pd.read_csv('Concat.csv')

    print("Identify target rows...")
    df_target = f.get_submission_target(df_test)

    print("Get recommendations...")
    df_expl = f.explode(df_target, "impressions")
    df_out = f.calc_recommendation(df_expl, df_popular)

    print(f"Writing {subm_csv}...")
    df_out.to_csv(subm_csv, index=False)

    print("Finished calculating recommendations.")


data_dir_path = '../../data'
if __name__ == '__main__':
    # main(data_dir_path, 0, 1)
    main(data_dir_path)
