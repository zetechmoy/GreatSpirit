#Created by Theo Guidoux on 22/09/2018

class Vigenere():
	"""Tools for Vigenere."""
	def __init__(self):
		pass

	def getTable(self):
		table = {
		"A" : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
		"B" : "BCDEFGHIJKLMNOPQRSTUVWXYZB",
		"C" : "CDEFGHIJKLMNOPQRSTUVWXYZAB",
		"D" : "DEFGHIJKLMNOPQRSTUVWXYZABC",
		"E" : "EFGHIJKLMNOPQRSTUVWXYZABCD",
		"F" : "FGHIJKLMNOPQRSTUVWXYZABCDE",
		"G" : "GHIJKLMNOPQRSTUVWXYZABCDEF",
		"H" : "HIJKLMNOPQRSTUVWXYZABCDEFG",
		"I" : "IJKLMNOPQRSTUVWXYZABCDEFGH",
		"J" : "JKLMNOPQRSTUVWXYZABCDEFGHI",
		"K" : "KLMNOPQRSTUVWXYZABCDEFGHIJ",
		"L" : "LMNOPQRSTUVWXYZABCDEFGHIJK",
		"M" : "MNOPQRSTUVWXYZABCDEFGHIJKL",
		"N" : "NOPQRSTUVWXYZABCDEFGHIJKLM",
		"O" : "OPQRSTUVWXYZABCDEFGHIJKLMN",
		"P" : "PQRSTUVWXYZABCDEFGHIJKLMNO",
		"Q" : "QRSTUVWXYZABCDEFGHIJKLMNOP",
		"R" : "RSTUVWXYZABCDEFGHIJKLMNOPQ",
		"S" : "STUVWXYZABCDEFGHIJKLMNOPQR",
		"T" : "TUVWXYZABCDEFGHIJKLMNOPQRS",
		"U" : "UVWXYZABCDEFGHIJKLMNOPQRST",
		"V" : "VWXYZABCDEFGHIJKLMNOPQRSTU",
		"W" : "WXYZABCDEFGHIJKLMNOPQRSTUV",
		"X" : "XYZABCDEFGHIJKLMNOPQRSTUVW",
		"Y" : "YZABCDEFGHIJKLMNOPQRSTUVWX",
		"Z" : "ZABCDEFGHIJKLMNOPQRSTUVWXY",
		}
		return table


	def encrypt(self, plaintext, key):
		abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		plaintext = plaintext.replace(" ", "")
		plainkey = ""
		while len(plainkey) < len(plaintext):
			plainkey = plainkey + key

		table = self.getTable()
		output = ""
		for i in range(0, len(plaintext)):
			output = output + table[plaintext[i]][abc.index(plainkey[i])]
		return output

	def decrypt(self, ciphertext, key):
		abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		ciphertext = ciphertext.replace(" ", "")
		plainkey = ""
		while len(plainkey) < len(ciphertext):
			plainkey = plainkey + key

		table = self.getTable()
		output = ""

		for i in range(0, len(ciphertext)):
			output = output + abc[table[plainkey[i]].index(ciphertext[i])]
		return output


	def encrypt2(self, plaintext, key):
		key_length = len(key)
		print(key_length)
		key_as_int = [ord(i) for i in key]
		print(key_as_int)
		plaintext_int = [ord(i) for i in plaintext]
		print(plaintext_int)
		ciphertext = ''
		for i in range(len(plaintext_int)):
			value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
			ciphertext += chr(value + 65)
		return ciphertext


	def decrypt2(self, ciphertext, key):
		key_length = len(key)
		key_as_int = [ord(i) for i in key]
		ciphertext_int = [ord(i) for i in ciphertext]
		plaintext = ''
		for i in range(len(ciphertext_int)):
			value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
			plaintext += chr(value + 65)
		return plaintext
