
from jungle import Jungle

class DatasetManager:

	def __init__(self, max_len_word = 7):
		self.jungle = Jungle()
		self.max_len_output = max_len_word

	def createDataset(self):
		print("#"*60)
		print("Creating dataset...")
		words_file = open("datasets/words.txt", "r")
		words = words_file.readlines()
		words = list(set(words))
		print("Got "+str(len(words))+" unique words")
		encoded_words = []
		valid_words = []
		abc = "abcdefghijklmnopqrstuvwxyz"
		for word in words:
			word = word.replace("\n", "")
			valid = True
			for l in word:
				if l.lower() not in abc:
					valid = False
			if valid == True:
				encoded_words.append(self.jungle.encode(word))
				valid_words.append(word)
		print("Got "+str(len(encoded_words))+" unique encoded words")

		output_file = open("datasets/dataset.csv", "a+")
		output_file.seek(0)
		output_file.truncate()
		for i in range(0, len(encoded_words)):
			output_file.write(valid_words[i].lower() + ", " + encoded_words[i].lower() + "\n")
		output_file.close()
		print("Dataset created !")

	def readDataset(self, dataset_name="datasets/dataset.csv"):

		file = open(dataset_name, "r")
		tup = file.readlines()

		words = []
		encoded_words = []

		for t in tup:
			t = t[:-1]
			t = t.split(', ')
			if len(t[0]) <= self.max_len_output:
				words.append(t[0])
				encoded_words.append(t[1])

		max_len = max(self.getMaxLen(words), self.getMaxLen(encoded_words))

		for i in range(0, len(words)):
			words[i] = words[i] + " "*(max_len-len(words[i]))

		for i in range(0, len(encoded_words)):
			encoded_words[i] = encoded_words[i] + " "*(max_len-len(encoded_words[i]))

		return words, encoded_words

	def getSmallDataset(self):
		words, enc_words = self.readDataset("datasets/dataset_small.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for word in enc_words:
			y.append(self.wordToVec(word, output_dic, output_size))

		return x, y

	def getDataset(self):
		words, enc_words = self.readDataset("datasets/dataset.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for word in enc_words:
			y.append(self.wordToVec(word, output_dic, output_size))

		return x, y

	def getBigDataset(self):
		words, enc_words = self.readDataset("datasets/dataset_big.csv")

		input_size = self.getMaxLen(words)
		output_size = self.getMaxLen(enc_words)

		input_dic = self.getDic(words)
		output_dic = self.getDic(enc_words)

		x = []
		y = []
		for word in words:
			x.append(self.wordToVec(word, input_dic, input_size))

		for word in enc_words:
			y.append(self.wordToVec(word, output_dic, output_size))

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
				return word
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
