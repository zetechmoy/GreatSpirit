from DatasetManager import DatasetManager

dm = DatasetManager(max_len_word = 6)

expected, questions, keys = dm.readDataset("datasets/dataset.csv")

print(expected)