from DatasetManager import DatasetManager
import hashlib
m = hashlib.md5()

dm = DatasetManager()

dm.createDataset("datasets/words.txt", "datasets/dataset.csv")
dm.createDataset("datasets/words_big.txt", "datasets/dataset_big.csv")
dm.createDataset("datasets/words_small.txt", "datasets/dataset_small.csv")