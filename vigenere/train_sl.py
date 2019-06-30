from DatasetManager import DatasetManager
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor


import numpy as np
import shutil
import os
from jungle import Jungle

jungle = Jungle()
shutil.rmtree('./Graph', ignore_errors=True)
shutil.rmtree('./checkpoints', ignore_errors=True)
if not os.path.exists("./checkpoints"):
    os.makedirs("./checkpoints")

dm = DatasetManager(max_len_word = 5)

words, encoded_words = dm.getSmallDataset()

x_train, x_test, y_train, y_test = train_test_split(encoded_words, words, test_size=0.2)

clf = KNeighborsRegressor(n_neighbors=100)

clf.fit(x_train, y_train)

res = clf.predict([x_test[0]])
decrypted_word_vec = list(res[0])
for j in range(0, len(decrypted_word_vec)):
	decrypted_word_vec[j] = int(round(decrypted_word_vec[j]))

res = clf.predict(x_test)

y_true = np.array(y_test)
y_pred = np.array(res)
acc = np.sum(np.not_equal(y_true, y_pred))/float(y_true.size)
print("Accuracy : "+str(acc))

word = "hi"
encrypted_word = jungle.encode(word)

words, enc_words = dm.readDataset(dataset_name="datasets/dataset.csv")

input_size = dm.getMaxLen(enc_words)
output_size = dm.getMaxLen(words)

input_dic = dm.getDic(enc_words)
output_dic = dm.getDic(words)

x_test = dm.wordToVec(encrypted_word, input_dic, input_size)
y_test = dm.wordToVec(word, output_dic, output_size)

print(dm.vecToWord(x_test, input_dic))
print(dm.vecToWord(y_test, output_dic))

print(x_test)
print(y_test)

res = clf.predict([x_test])
decrypted_word_vec = dm.roundResult(list(res[0]))
print(decrypted_word_vec)

print(dm.vecToWord(decrypted_word_vec, output_dic))


