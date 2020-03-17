# # Import Package
# from cryptography.fernet import Fernet
#
# # Generate a Key and Instantiate a Fernet Instance
# key = Fernet.generate_key()
# f = Fernet(key)
# print(key)
#
# # Define our message
# plaintext = b"encryption is very useful"
#
# # Encrypt
# ciphertext = f.encrypt(plaintext)
# print(ciphertext)
#
# # Decrypt
# decryptedtext = f.decrypt(ciphertext)
# print(decryptedtext)

# ###############################################################################
# ###############################################################################
#
# # Load the NIST list of 10,000 most commonly used passwords
# with open('nist_10000.txt', newline='') as bad_passwords:
#     nist_bad = bad_passwords.read().split('\n')
# print(nist_bad[1:10])
#
# # The following data is a normalized simplified user table
# # Imagine this information was stolen or leaked
# leaked_users_table = {
#     'jamie': {
#         'username': 'jamie',
#         'role': 'subscriber',
#         'md5': '203ad5ffa1d7c650ad681fdff3965cd2'
#     },
#     'amanda': {
#         'username': 'amanda',
#         'role': 'administrator',
#         'md5': '315eb115d98fcbad39ffc5edebd669c9'
#     },
#     'chiaki': {
#         'username': 'chiaki',
#         'role': 'subscriber',
#         'md5': '941c76b34f8687e46af0d94c167d1403'
#     },
#     'viraj': {
#         'username': 'viraj',
#         'role': 'employee',
#         'md5': '319f4d26e3c536b5dd871bb2c52e3178'
#     },
# }
#
# # import the hashlib
# import hashlib
# # example hash
# word = 'blueberry'
# hashlib.md5(word.encode()).hexdigest()
#
# # RAINBOW TABLE SOLUTION
# rainbow_table = {}
# for word in nist_bad:
#     hashed_word = hashlib.md5(word.encode()).hexdigest()
#     rainbow_table[hashed_word] = word
#
# # Use the Rainbow table to determine the plain text password
# for user in leaked_users_table.keys():
#     try:
#         print(user + ":\t" + rainbow_table[leaked_users_table[user]['md5']])
#     except KeyError:
#         print(user + ":\t" + '******* hash not found in rainbow table')

#################################################################
#################################################################
# SALTED HASHING
# Import the Python Library
import bcrypt
password = b"studyhard"

# Hash a password for the first time, with a certain number of rounds
salt = bcrypt.gensalt(14)
#hashed = bcrypt.hashpw(password, salt)
hashed = b'$2b$14$EFOxm3q8UWH8ZzK1h.WTZeRcPyr8/X0vRfuL3/e9z7AKIMnocurBG'
print(salt)
print(hashed)

# Check a plain text string against the salted, hashed digest
for sin_pass in [b'securepassword', b'udacity', b'learningisfun']:
    print(bcrypt.checkpw(sin_pass, hashed))
