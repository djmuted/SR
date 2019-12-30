import numpy as np
import pandas as pd


def read_into_df(file):
    """Read csv file into data frame."""
    df = (
        pd.read_csv(file)
            .set_index(['user_id', 'session_id', 'timestamp', 'step'])
    )

    return df


def generate_rranks_range(start, end):
    """Generate reciprocal ranks for a given list length."""

    return 1.0 / (np.arange(start, end) + 1)


def convert_string_to_list(df, col, new_col):
    """Convert column from string to list format."""
    fxn = lambda arr_string: [int(item) for item in str(arr_string).split(" ")]

    mask = ~(df[col].isnull())

    df[new_col] = df[col]
    df.loc[mask, new_col] = df[mask][col].map(fxn)

    return df


def get_reciprocal_ranks(ps):
    """Calculate reciprocal ranks for recommendations."""
    mask = ps.reference == np.array(ps.item_recommendations)

    if mask.sum() == 1:
        rranks = generate_rranks_range(0, len(ps.item_recommendations))
        return np.array(rranks)[mask].min()
    else:
        return 0.0


def read_sub(sub_path):
    full_df_gt = pd.read_csv(sub_path)

    content = pd.DataFrame(columns=['item_recommendations'])

    for index, row in full_df_gt.iterrows():
        content.loc[index] = [row['item_recommendations']]

    return content

def score_submissions(subm_csv, gt_csv, objective_function):
    print(f"Reading ground truth data {gt_csv} ...")
    df_gt = pd.read_csv(gt_csv)

    print(f"Reading submission data {subm_csv} ...")
    df_subm = read_sub(subm_csv)


    join = df_gt.join(df_subm, how='inner')
    # join.reference = join.reference.astype(int)
    join = convert_string_to_list(
        join, 'item_recommendations', 'item_recommendations'
    )


    join['score'] = join.apply(objective_function, axis=1)

    mrr = join.score.mean()
    return mrr
