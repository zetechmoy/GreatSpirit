from DatasetManager import DatasetManager
from sklearn.model_selection import train_test_split
from keras.utils import plot_model
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Flatten
from keras.layers import Embedding
from keras import metrics
from keras.callbacks import ModelCheckpoint
from keras import optimizers
from keras import callbacks
from keras import regularizers

import numpy as np
import shutil
import os

shutil.rmtree('./Graph', ignore_errors=True)
shutil.rmtree('./checkpoints', ignore_errors=True)
if not os.path.exists("./checkpoints"):
    os.makedirs("./checkpoints")

dm = DatasetManager()

words, encoded_words = dm.getSmallDataset()

x_train, x_test, y_train, y_test = train_test_split(encoded_words, words, test_size=0.2)

print(x_train[0])
print(y_train[0])

#x_train = [x_train]
#y_train = [y_train]

print("Input shape : "+str((len(x_train),len(x_train[0]))))
print("Output shape : "+str((len(y_train),len(y_train[0]))))
# create model
model = Sequential()
model.add(Embedding(len(x_train), 8))
model.add(LSTM(8, dropout=0.1, recurrent_dropout=0.1, activation="relu"))
#model.add(Dense(len(x_train[0]), activation='relu'))
#model.add(Dropout(0.1))
model.add(Dense(int(len(x_train[0])), activation='relu', kernel_regularizer=regularizers.l2(0.001)))
#model.add(Dropout(0.05))
#model.add(Dense(int(len(x_train[0])*4), activation='relu', kernel_regularizer=regularizers.l2(0.001)))

#model.add(Dense(int(len(x_train[0])*4), activation='relu', kernel_regularizer=regularizers.l2(0.001)))

model.add(Dense(len(y_train[0]), activation='relu'))
plot_model(model, to_file='model.png')

# Compile model
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# checkpoint
tbCallBack = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

esCallBack = callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=20, verbose=1, mode='auto')

filepath="checkpoints/weights-improvement-{epoch:02d}-{acc:.2f}.h5"
checkpointCallBack = ModelCheckpoint(filepath, monitor='acc', verbose=1, save_best_only=True, mode='max')

callbacks_list = [checkpointCallBack, esCallBack, tbCallBack]
# Fit the model
print("Fitting ...")
history = model.fit(np.array(x_train), np.array(y_train), epochs=1000, batch_size=64*4, callbacks=callbacks_list)

plot_model(model, to_file='model.png')

# evaluate the model
scores = model.evaluate(np.array(x_test), np.array(y_test))
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

model.save("pyhack_jungle.h5")
