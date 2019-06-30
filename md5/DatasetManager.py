import hashlib

class DatasetManager:

	def __init__(self, max_len_word = 7):
		self.max_len_output = max_len_word

	def createDataset(self, words_file_path, output_file_path):
		print("#"*60)
		print("Creating dataset...")
		words_file = open(words_file_path, "r")
		words = words_file.readlines()
		words = list(set(words))
		print("Got "+str(len(words))+" unique words")
		encoded_words = []
		for word in words:
			m = hashlib.md5()
			m.update(word)
			encoded_words.append(m.hexdigest())
		print("Got "+str(len(encoded_words))+" unique encoded words")

		output_file = open(output_file_path, "a+")
		output_file.seek(0)
		output_file.truncate()
		for i in range(0, len(encoded_words)):
			output_file.write(words[i].lower().replace(" ", "").replace("\n", "") + ", " + encoded_words[i].lower().replace(" ", "").replace("\n", "") + "\n")
		output_file.close()
		print("Dataset created !")

	def readDataset(self, dataset_name="datasets/dataset.csv"):

		file = open(dataset_name, "r")
		tup = file.readlines()

		words = []
		encoded_words = []

		for t in tup:
			t = t.split(', ')
			if len(t[0]) <= self.max_len_output:
				words.append(t[0].replace(" ", "").replace("\n", ""))
				encoded_words.append(t[1].replace(" ", "").replace("\n", ""))

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