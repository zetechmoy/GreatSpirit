# -*- coding: utf-8 -*-
'''An implementation of sequence to sequence learning for performing addition

Input: "535+61"
Output: "596"
Padding is handled by using a repeated sentinel character (space)

Input may optionally be reversed, shown to increase performance in many tasks in:
"Learning to Execute"
http://arxiv.org/abs/1410.4615
and
"Sequence to Sequence Learning with Neural Networks"
http://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf
Theoretically it introduces shorter term dependencies between source and target.

Two digits reversed:
+ One layer LSTM (128 HN), 5k training examples = 99% train/test accuracy in 55 epochs

Three digits reversed:
+ One layer LSTM (128 HN), 50k training examples = 99% train/test accuracy in 100 epochs

Four digits reversed:
+ One layer LSTM (128 HN), 400k training examples = 99% train/test accuracy in 20 epochs

Five digits reversed:
+ One layer LSTM (128 HN), 550k training examples = 99% train/test accuracy in 30 epochs
'''  # noqa
from __future__ import print_function
from keras.models import Sequential
from keras import layers
import numpy as np
from six.moves import range
from DatasetManager import DatasetManager
from sklearn.model_selection import train_test_split
from keras import regularizers
from keras import callbacks
from keras.callbacks import ModelCheckpoint
import shutil
import os

class CharacterTable(object):
    """Given a set of characters:
    + Encode them to a one hot integer representation
    + Decode the one hot integer representation to their character output
    + Decode a vector of probabilities to their character output
    """
    def __init__(self, chars):
        """Initialize character table.

        # Arguments
            chars: Characters that can appear in the input.
        """
        self.chars = sorted(set(chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

    def encode(self, C, num_rows):
        """One hot encode given string C.

        # Arguments
            num_rows: Number of rows in the returned one hot encoding. This is
                used to keep the # of rows for each data the same.
        """
        x = np.zeros((num_rows, len(self.chars)))
        for i, c in enumerate(C):
            #print((i, c))
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, x, calc_argmax=True):
        if calc_argmax:
            x = x.argmax(axis=-1)
        return ''.join(self.indices_char[x] for x in x)


class colors:
    ok = '\033[92m'
    fail = '\033[91m'
    close = '\033[0m'

if __name__ == "__main__":


	shutil.rmtree('./Graph', ignore_errors=True)
	shutil.rmtree('./checkpoints', ignore_errors=True)
	if not os.path.exists("./checkpoints"):
	    os.makedirs("./checkpoints")

	file = open("stats.csv", "a+")
	file.seek(0)
	file.truncate()
	file.close()

	dm = DatasetManager(max_len_word = 10)

	expected, questions = dm.readDataset("datasets/dataset.csv")
	#x_train, x_test, y_train, y_test = train_test_split(questions, expected, test_size=0.001)

	x_train = questions
	y_train = expected
	# Parameters for the model and dataset.
	TRAINING_SIZE = len(x_train)
	# Maximum length of input is 'int + int' (e.g., '345+678'). Maximum length of
	MAXLEN = dm.getMaxLen(questions)
	REVERSE = False
	print("TRAINING_SIZE = "+str(TRAINING_SIZE))
	print("MAXLEN = "+str(MAXLEN))
	print("REVERSE = "+str(REVERSE))

	# All the numbers, plus sign and space for padding.
	chars = dm.getDic(x_train)
	chars = chars + [c for c in dm.getDic(y_train) if c not in chars]
	print(chars)
	ctable = CharacterTable(chars)
	print(ctable.encode("hello", MAXLEN))

	print('Total training sample :', len(x_train))

	print(type(x_train[0]))
	print(x_train[0])
	print(type(y_train[0]))
	print(y_train[0])

	print('Vectorization...')

	x = np.zeros((len(x_train), MAXLEN, len(chars)), dtype=np.bool)
	y = np.zeros((len(questions), MAXLEN, len(chars)), dtype=np.bool)

	for i, sentence in enumerate(x_train):
	    x[i] = ctable.encode(sentence, MAXLEN)
	for i, sentence in enumerate(y_train):
	    y[i] = ctable.encode(sentence, MAXLEN)

	# Shuffle (x, y) in unison as the later parts of x will almost all be larger
	# digits.
	indices = np.arange(len(y))
	np.random.shuffle(indices)
	x = x[indices]
	y = y[indices]

	# Explicitly set apart 10% for validation data that we never train over.
	split_at = len(x) - len(x) // 10
	(x_train, x_val) = x[:split_at], x[split_at:]
	(y_train, y_val) = y[:split_at], y[split_at:]

	#print(type(x_train[0]))
	#print(x_train[0])
	#print(y_train[0])

	print('Training Data:')
	print(x_train.shape)
	print(y_train.shape)

	print('Validation Data:')
	print(x_val.shape)
	print(y_val.shape)

	# Try replacing GRU, or SimpleRNN.
	RNN = layers.LSTM
	HIDDEN_SIZE = 128
	BATCH_SIZE = 128
	LAYERS = 1

	print('Build model...')
	print((MAXLEN, len(chars)))
	model = Sequential()
	# "Encode" the input sequence using an RNN, producing an output of HIDDEN_SIZE.
	# Note: In a situation where your input sequences have a variable length,
	# use input_shape=(None, num_feature).
	model.add(RNN(HIDDEN_SIZE, input_shape=(MAXLEN, len(chars))))
	# As the decoder RNN's input, repeatedly provide with the last hidden state of
	# RNN for each time step. Repeat 'DIGITS + 1' times as that's the maximum
	# length of output, e.g., when DIGITS=3, max output is 999+999=1998.
	model.add(layers.RepeatVector(MAXLEN))
	# The decoder RNN could be multiple layers stacked or a single layer.
	for _ in range(LAYERS):
	    # By setting return_sequences to True, return not only the last output but
	    # all the outputs so far in the form of (num_samples, timesteps,
	    # output_dim). This is necessary as TimeDistributed in the below expects
	    # the first dimension to be the timesteps.
	    model.add(RNN(HIDDEN_SIZE, return_sequences=True, kernel_regularizer=regularizers.l2(0.001)))

	# Apply a dense layer to the every temporal slice of an input. For each of step
	# of the output sequence, decide which character should be chosen.
	model.add(layers.TimeDistributed(layers.Dense(len(chars))))
	model.add(layers.Activation('softmax'))
	model.compile(loss='categorical_crossentropy',
	              optimizer='adam',
	              metrics=['accuracy'])

	tbCallBack = callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

	esCallBack = callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=5, verbose=1, mode='auto')

	filepath="checkpoints/weights-improvement-{epoch:02d}-{acc:.2f}.h5"

	checkpointCallBack = ModelCheckpoint(filepath, monitor='acc', verbose=1, save_best_only=True, mode='max')

	callbacks_list = [checkpointCallBack, esCallBack, tbCallBack]

	model.summary()

	# Train the model each generation and show predictions against the validation
	# dataset.
	for iteration in range(1, 60):
	    print()
	    print('-' * 50)
	    print('Iteration', iteration)
	    model.fit(x_train, y_train,
	              batch_size=BATCH_SIZE,
	              epochs=1,
	              validation_data=(x_val, y_val),
	              callbacks=callbacks_list)
	    # Select 10 samples from the validation set at random so we can visualize
	    # errors.
	    for i in range(10):
	        ind = np.random.randint(0, len(x_val))
	        rowx, rowy = x_val[np.array([ind])], y_val[np.array([ind])]
	        preds = model.predict_classes(rowx, verbose=0)
	        q = ctable.decode(rowx[0])
	        #print(rowx[0])
	        correct = ctable.decode(rowy[0])
	        #print(rowy[0])
	        #print(preds[0])
	        guess = ctable.decode(preds[0], calc_argmax=False)
	        print('Q', q[::-1] if REVERSE else q, end=' ')
	        print('T', correct, end=' ')
	        if correct == guess:
	            print(colors.ok + '☑' + colors.close, end=' ')
	        else:
	            print(colors.fail + '☒' + colors.close, end=' ')
	        print(guess)
	        file = open("stats.csv", "a+")
	        file.write(str(i)+"########################################################\n")
	        file.write('Q' + q[::-1] if REVERSE else q + 'T' + correct + " => " + guess + "\n")
	        file.close()
	        #model.save("checkpoints/vig_lstm_"+str(iteration)+".h5")
	model.save("jungle_lstm.h5")
