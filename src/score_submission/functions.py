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


# TODO: Zapytać marcina co on na to, i co z ta jebana referencja
def get_reciprocal_ranks(ps):
    """Calculate reciprocal ranks for recommendations."""
    # mask = ps.impressions.split('|') == np.array(ps.item_recommendations)

    # TODO: Możliwe klikniecia
    impressions = ps.impressions.split('|')
    # len(ps.impressions.split('|')) = 25

    # TODO: Proponowane klikniecia
    item_reco = np.array(ps.item_recommendations)
    # len(np.array(ps.item_recommendations)) = 25

    # mask = np.arange(len(impressions))
    to_find = impressions[0]

    result = 0
    for i in range(result, len(item_reco)):
        if to_find == str(item_reco[i]):
            result = i
            continue

    print(i)
    # TODO: Lista przetrzymujaca true false, true jesli w ktorejs propozycji znalazl ta wlasnie szukana
    # Reference to jest szukana pozycja nie wiem jak to znalezc pokombinowac z item_metadata
    # mask = ps.reference == np.array(ps.item_recommendations)

    if result == 0:
        return 0.0
    else:
        return 1.0 / result


def score_submissions(subm_csv, gt_csv, objective_function):
    """Score submissions with given objective function."""

    print(f"Reading ground truth data {gt_csv} ...")
    print(gt_csv)
    df_gt = read_into_df(gt_csv)
    # TODO: df_gt.shape = (757695,9)

    print(f"Reading submission data {subm_csv} ...")
    df_subm = read_into_df(subm_csv)
    # TODO: df_subm.shape = (50567,1)

    # ITEM METADATA
    meta_data = pd.read_csv('../../part_data/item_metadata.csv')

    # create dataframe containing the ground truth to target rows
    cols = ['reference', 'impressions', 'prices']
    df_key = df_gt.loc[:, cols]
    # TODO: df_key.shape = (757695,9). Part of gt

    # append key to submission file
    df_subm_with_key = df_key.join(df_subm, how='inner')
    # TODO: df_subm_with_key.shape = (50567, 1)

    # TODO: How to change this references?
    # df_subm_with_key.reference = df_subm_with_key.reference.astype(int)
    df_subm_with_key = convert_string_to_list(
        df_subm_with_key, 'item_recommendations', 'item_recommendations'
    )

    # score each row
    df_subm_with_key['score'] = df_subm_with_key.apply(objective_function, axis=1)
    mrr = df_subm_with_key.score.mean()

    return mrr
