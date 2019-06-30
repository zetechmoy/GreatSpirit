#Created by Theo Guidoux on 22/09/2018

from vigenere import Vigenere
import time

vig = Vigenere()

str_to_encode = "MICHIGANTECHNOLOGICALUNIVERSITY"
key = "HOUBHBE"

print("String is : "+str_to_encode)
print("Key is : "+key)

#First type
encoded_str = vig.encrypt(str_to_encode, key)
decrypted_str = vig.decrypt(encoded_str, key)

print("encoded_str : "+encoded_str)
print("decrypted_str : "+decrypted_str)

#Second type
encoded_str = vig.encrypt2(str_to_encode, key)
decrypted_str = vig.decrypt2(encoded_str, key)

print("encoded_str : "+encoded_str)
print("decrypted_str : "+decrypted_str)
