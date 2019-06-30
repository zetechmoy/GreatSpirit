#!/usr/bin/env python
# -*- coding: utf-8 -*-
from keras.models import load_model
import numpy as np
from DatasetManager import DatasetManager
from jungle import Jungle
from train_lstm import CharacterTable

jungle = Jungle()

model = load_model('jungle_lstm.h5')

word = "jetaimedilu"
encrypted_word = jungle.encode(word)

dm = DatasetManager(max_len_word = 10)

expected, questions = dm.readDataset("datasets/dataset.csv")

x_train = questions
y_train = expected

MAXLEN = dm.getMaxLen(questions)
print("MAXLEN = "+str(MAXLEN))
word = word + " "*(MAXLEN-len(word))

# All the numbers, plus sign and space for padding.
chars = dm.getDic(x_train)
chars = chars + [c for c in dm.getDic(y_train) if c not in chars]
#print(chars)
ctable = CharacterTable(chars)
#print(ctable.encode("hello", MAXLEN))

x_test = ctable.encode(encrypted_word, MAXLEN)
y_test = ctable.encode(word, MAXLEN)

#print("Input word : "+encrypted_word)
#print("Output word : "+word)

#print("Input vec : " + str(x_test))
#print("Expected output vec : "+str(y_test))

preds = model.predict_classes(np.array([x_test]), verbose=0)
q = ctable.decode(x_test)
correct = ctable.decode(y_test)
guess = ctable.decode(preds[0], calc_argmax=False)
print(preds[0])
print("encrypted_word : "+encrypted_word)
print("word : "+word)
print("AI RESULT : "+guess)
