from DatasetManager import DatasetManager
from sklearn.model_selection import train_test_split
from keras.utils import plot_model
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers import Reshape
from keras import metrics
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras import callbacks
from keras import regularizers
from keras.optimizers import Adam

import numpy as np
import shutil
import os

shutil.rmtree('./Graph', ignore_errors=True)
shutil.rmtree('./checkpoints', ignore_errors=True)
if not os.path.exists("./checkpoints"):
    os.makedirs("./checkpoints")

dm = DatasetManager(max_len_word = 5)

words, encoded_words = dm.getSmallDataset()

x_train, x_test, y_train, y_test = train_test_split(encoded_words, words, test_size=0.2)

def getModel(x_train, y_train, loss='mean_absolute_error', optimizer='adam'):
	nb_of_node = int((len(x_train[0]) + len(y_train[0]))/2)

	print("Input shape : "+str((len(x_train),len(x_train[0]))))
	print("Output shape : "+str((len(y_train),len(y_train[0]))))
	print("nb_of_node : "+str(nb_of_node))
	# create model
	model = Sequential()
	#model.add(LSTM(64, return_sequences=True, input_shape=(len(x_train[0]),len(x_train[0][1]))))
	model.add(Dense(len(x_train[0]), input_dim=len(x_train[0]), activation='relu'))
	model.add(Dense(nb_of_node*30, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
	model.add(Dropout(0.1))
	model.add(Dense(nb_of_node*20, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
	#model.add(Dropout(0.1))
	model.add(Dense(nb_of_node*10, activation='relu', kernel_regularizer=regularizers.l2(0.001)))
	#model.add(Dropout(0.1))
	model.add(Dense(nb_of_node, activation='relu', kernel_regularizer=regularizers.l2(0.001)))


	model.add(Dense(len(y_train[0]), activation='relu'))

	# Compile model
	model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
	return model

opt = Adam(lr=0.0005, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model1 = getModel(x_train, y_train, loss="mean_absolute_error", optimizer=opt)
model2 = getModel(x_train, y_train, loss="mean_squared_error", optimizer=opt)
model3 = getModel(x_train, y_train, loss="logcosh", optimizer=opt)

# checkpoint
tbCallBack = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

esCallBack = callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=5, verbose=1, mode='auto')

filepath="checkpoints/weights-improvement-{epoch:02d}-{acc:.2f}.h5"
checkpointCallBack = ModelCheckpoint(filepath, monitor='acc', verbose=1, save_best_only=True, mode='max')

callbacks_list = [checkpointCallBack, esCallBack, tbCallBack]

models = [model1, model2, model3]
models = [model1]

for i in range(0, len(models)):
	# Fit the model
	print("Fitting model"+str(i)+"...")
	model = models[i]
	model.fit(np.array(x_train), np.array(y_train), epochs=5000, batch_size=64, callbacks=callbacks_list)

	scores = model.evaluate(np.array(x_test), np.array(y_test))
	print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

	model.save("gs_jungle_"+str(i)+".h5")

