#!/usr/bin/env python
# -*- coding: utf-8 -*-
from keras.models import load_model
import numpy as np
from DatasetManager import DatasetManager
import hashlib
m = hashlib.md5()
dm = DatasetManager(max_len_word=5)

model_names = ['gs_jungle_0.h5']

models = []

for i in range(0, len(model_names)):
	models.append(load_model(model_names[i]))

word = "cove"
m.update(word)
encrypted_word = m.hexdigest()

words, enc_words = dm.readDataset(dataset_name="datasets/dataset_small.csv")

input_size = dm.getMaxLen(enc_words)
output_size = dm.getMaxLen(words)

input_dic = dm.getDic(enc_words)
output_dic = dm.getDic(words)

print(input_dic)
print(output_dic)

x_test = dm.wordToVec(encrypted_word, input_dic, input_size)
y_test = dm.wordToVec(word, output_dic, output_size)

print("Input word : "+dm.vecToWord(x_test, input_dic))
print("Output word : "+dm.vecToWord(y_test, output_dic))

print("Input vec : " + str(x_test))
print("Expected output vec : "+str(y_test))

decrypted_word_vecs = []
for i in range(0, len(models)):
	decrypted_word_vec = list(models[i].predict(np.array([x_test]))[0])
	decrypted_word_vec = dm.roundResult(decrypted_word_vec)
	#print(decrypted_word_vec)
	print("Result model"+str(i)+" : "+dm.vecToWord(decrypted_word_vec, output_dic))
	decrypted_word_vecs.append(decrypted_word_vec)

#Moyenne des trois models
decrypted_word_vec = []
for i in range(0, len(decrypted_word_vecs[0])):
	res = 0
	for j in range(0, len(decrypted_word_vecs)):
		res += decrypted_word_vecs[j][i]
	res = res/len(decrypted_word_vecs)
	decrypted_word_vec.append(res)

#Resultat final
decrypted_word_vec = dm.roundResult(decrypted_word_vec)
print("Final vec : "+str(decrypted_word_vec))
print("Resultat final : "+dm.vecToWord(decrypted_word_vec, output_dic))
