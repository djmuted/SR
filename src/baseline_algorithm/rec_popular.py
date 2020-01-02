from pathlib import Path

import pandas as pd

from src.baseline_algorithm import functions as f

current_directory = Path(__file__).absolute().parent
default_data_directory = current_directory.joinpath('..', '..', 'data')


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
    df_popular = f.get_popularity(df_train)

    print("Identify target rows...")
    df_target = f.get_submission_target(df_test)

    print("Get recommendations...")
    df_expl = f.explode(df_target, "impressions")
    df_out = f.calc_recommendation(df_expl, df_popular)

    print(f"Writing {subm_csv}...")
    df_out.to_csv(subm_csv, index=False)

    print("Finished calculating recommendations.")


data_dir_path = '../../part_data'
if __name__ == '__main__':
    main(data_dir_path)
