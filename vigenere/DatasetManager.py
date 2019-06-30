
from vigenere import Vigenere
import random
import time

class DatasetManager:

	def __init__(self, max_len_word = 5):
		self.vig = Vigenere()
		self.max_len_output = max_len_word
		self.abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


	def randomword(self, length):
	   letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	   return ''.join(random.choice(letters) for i in range(length))

	def createDataset(self):
		print("#"*60)
		print("Creating dataset...")
		words_file = open("datasets/words.txt", "r")
		words = words_file.readlines()
		words = list(set(words))
		print("Got "+str(len(words))+" unique words")
		correct_words = []
		encoded_words = []
		keys = []
		for word in words:
			word = word.replace("\n", "").replace(" ", "").upper()
			is_valid = True
			for letter in word:
				if letter.upper() not in self.abc:
					is_valid = False
					break
			if is_valid and len(word) > 2:
				key = self.randomword(random.randint(2, len(word))).upper()
				print(key)
				encoded_word = self.vig.code_vigenere(word, key)
				print("word : "+word+", encoded_word : "+encoded_word+", key : "+key, ", same_length : "+str(len(word.replace("\n", "")) == len(encoded_word.replace("\n", ""))))
				if len(word.replace("\n", "")) == len(encoded_word.replace("\n", "")):
					correct_words.append(word)
					encoded_words.append(encoded_word)
					keys.append(key)
		print("Got "+str(len(encoded_words))+" unique encoded words")

		output_file = open("datasets/dataset.csv", "a+")
		output_file.seek(0)
		output_file.truncate()
		for i in range(0, len(encoded_words)):
			output_file.write(correct_words[i].replace("\n", "").upper() + ", " + encoded_words[i].replace("\n", "").upper() + ", " + keys[i].upper() + "\n")
		output_file.close()
		print("Dataset created !")

	def readDataset(self, dataset_name="datasets/dataset.csv"):

		file = open(dataset_name, "r")
		tup = file.readlines()

		words = []
		encoded_words = []
		keys = []

		for t in tup:
			t = t[:-1]
			t = t.replace(" ", "")
			t = t.split(',')
			if len(t[0]) == self.max_len_output:
				if len(t[0]) == len(t[1]):
					words.append(t[0].replace("\n", "").replace(" ", "").upper())
					encoded_words.append(t[1].replace("\n", "").replace(" ", "").upper())
					keys.append(t[2].replace("\n", "").replace(" ", "").upper())
			if len(encoded_words) >= 50000:
				break
		max_len = max(self.getMaxLen(words), self.getMaxLen(encoded_words))
		max_len_key = self.getMaxLen(keys)

		for i in range(0, len(words)):
			words[i] = words[i] + " "*(max_len-len(words[i]))

		for i in range(0, len(encoded_words)):
			encoded_words[i] = encoded_words[i] + " "*(max_len-len(encoded_words[i]))

		for i in range(0, len(keys)):
			keys[i] = keys[i] + " "*(max_len_key-len(keys[i]))

		return words, encoded_words, keys

	def getSmallDataset(self):
		words, enc_words, keys = self.readDataset("datasets/dataset_small.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for i in range(0, len(enc_words)):
			word = enc_words[i]
			y.append([len(keys[i])]+self.wordToVec(word, output_dic, output_size))

		return x, y

	def getDataset(self):
		words, enc_words, keys = self.readDataset("datasets/dataset.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for i in range(0, len(enc_words)):
			word = enc_words[i]
			y.append(self.wordToVec(word, output_dic, output_size))

		return x, y

	def getBigDataset(self):
		words, enc_words, keys = self.readDataset("datasets/dataset_big.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for i in range(0, len(enc_words)):
			word = enc_words[i]
			y.append([len(keys[i])]+self.wordToVec(word, output_dic, output_size))

		return x, y
	#TOOLS

	def wordToVec(self, word, dic, max_size):
		vec = []
		for l in word:
			vec.append(int((dic.index(l)+1))*100)
		for i in range(len(vec), max_size):
			vec.append(0)
		return vec

	def vecToWord(self, vec, dic):
		word = ""
		for nb in vec:

			if nb <= 0:
				word = word + " "
			else:
				word = word + dic[int(nb-1)/100]
		return word

	def getMaxLen(self, list_of_words):
		max_len = 0
		max_len_word = ""
		for word in list_of_words:
			if len(word) > max_len:
				max_len_word = word
				max_len = len(word)
		return max_len

	def getDic(self, list_of_words):
		chars = []
		for word in list_of_words:
			for letter in word:
				if letter not in chars:
					chars.append(letter)
		return chars

	def roundResult(self, vec):
		for j in range(0, len(vec)):
			vec[j] = int(round(vec[j]/100))*100
		return vec
