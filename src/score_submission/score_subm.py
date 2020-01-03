from pathlib import Path

from src.score_submission import functions as f

current_directory = Path(__file__).absolute().parent
default_data_directory = current_directory.joinpath('..', '..', 'data')


def main(data_path, submission_file, ground_truth_file):
    # calculate path to files
    data_directory = Path(data_path) if data_path else default_data_directory
    gt_csv = data_directory.joinpath(ground_truth_file)
    subm_csv = data_directory.joinpath(submission_file)

    mrr = f.score_submissions(subm_csv, gt_csv, f.get_reciprocal_ranks)

    print(f'Mean reciprocal rank: {mrr}')


data_dir_path = '../../data'
submission_popular = 'submission_popular.csv'
ground_truth = 'ground_truth.csv'
if __name__ == '__main__':
    main(data_dir_path, submission_popular, ground_truth)
