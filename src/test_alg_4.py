# from src.baseline_algorithm import rec_popular as r
# from src.score_submission import score_subm as s
#
# data_dir_path = '../data'
# submission_popular = 'submission_popular.csv'
# ground_truth = 'ground_truth.csv'
# result_path = 'result.txt'
# for i in range(0, 10):
#     for j in range(0, 10):
#         r.main(data_dir_path, i, j)
#         result = s.main(data_dir_path, submission_popular, ground_truth)
#
#         text = "Result for popular=" + str(i) + " and action=" + str(j) + " is " + str(result) + "\n"
#         f = open(result_path, "a")
#         f.write(text)
#         f.close()
