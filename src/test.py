import pandas as pd


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

    # for index, row in train_df.iterrows():
    #
    #     if row["action_type"] == "search for poi":
    #         print(index, row["session_id"])
    #         # index = index + 1
    #         # while train_df[index]["action_type"] != "search for poi" and\
    #         #         row['session_id'] == train_df[index]["session_id"]:
    #         #     print(index, row["session_id"])
    #         #     index = index + 1
    # return True


path = 'C:/Users/Stachu/Desktop/sr/2019/data/train.csv'
train_csv = pd.read_csv(path, nrows=100000)

get_actions(train_csv)
