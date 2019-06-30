
import argparse

#Created by zeTechMoy on 08/08/2018
#This is a little implementation of jungle cipher

class Jungle:

	def __init__(self):
		self.vowels = "aeiouy"
		self.consonants = "zrtpqsdfghjklmwxcvbn"
		self.voy_numbers = "123456"

	def encode(self, str_to_encode):
		"""Return the jungle encoded string
			str_to_decode : string to be encoded
		"""
		str_to_encode = str_to_encode.lower()
		encoded_str = ""
		for letter in str_to_encode:
			if letter in self.vowels:
				index = str(self.vowels.index(letter)+1)
				encoded_str = encoded_str + index
			elif letter in self.consonants:
				encoded_str = encoded_str + letter + "a"
			else:
				encoded_str = encoded_str + letter
		return encoded_str

	def decode(self, str_to_decode):
		"""Return the jungle decoded string
			str_to_decode : string to be decoded
		"""
		str_to_decode = str_to_decode.lower()
		decoded_str = ""
		for letter in str_to_decode:
			if letter == "a":
				#do nothing
				continue
			elif letter in self.voy_numbers:
				decoded_str = decoded_str + self.vowels[int(letter)-1]
			else:
				decoded_str = decoded_str + letter
		return decoded_str

if __name__ == "__main__":
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0', help="Show program's version number and exit.")
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message')
	parser.add_argument("-e", "--encode", type=str, help='Encode string')
	parser.add_argument("-d", "--decode", type=str, help='Decode string')

	args = parser.parse_args()

	jungle = Jungle()

	if args.encode != None:
		print(jungle.encode(args.encode))

	if args.decode != None:
		print(jungle.decode(args.decode))
