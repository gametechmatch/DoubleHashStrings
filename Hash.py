#################################################################
# Hash.py
#################################################################
# Source Title: HashTable_OpenAddressing.py & Hashing.py
# Source Type: Book
# Source Title: Data Structures & Algorithms in Python
# Source Authors: John Canning, Alan Broder, & Robert Lafore
#################################################################
# Student: gametechmatch
# Course: Data Structures
# CH11 - Hash Tables
# Date: 3/19/2023
#################################################################
# Hash static methods to support the HashTable.py file
#################################################################

class Hash:
	# This method encodes letters a through z as 1 thru 26
	#################################################################
	@staticmethod
	def encode_letter(letter):

		# Treat uppercase as lower case
		letter = letter.lower()
		if 'a' <= letter and letter <= 'z':
			return ord(letter) - ord('a') + 1

		# Spaces and everything else are 0
		return 0

	# This method encodes a word uniquely (abbreviated)
	#################################################################
	@staticmethod
	def unique_encode_word(word):
		return sum(Hash.encode_letter(word[i]) * 27 ** (len(word) - 1 - i)
				   for i in range(len(word)))

	# This method is a generator used to determine the probe interval
	# from a secondary hash of the key
	#################################################################
	@staticmethod
	def doubleHashProbe(start, key, size):

		# Yield the first cell index
		yield start % size

		# Get the step size for this key
		step = Hash.getHashStepSize(key, size)

		# Loop over all remaining cells using step from second hash of key
		for i in range(1, size):
			yield (start + i * step) % size

	# This method determines the step size for a given key
	#################################################################
	@staticmethod
	def getHashStepSize(key, size):

		# Find the largest prime below array size
		prime = Hash.getLargestPrimeBelowN(size)

		# Step size is based on second hash and is in range [1, prime]
		return prime - (Hash.simpleHash(key) % prime)

	# This method finds the largest prime below n
	#################################################################
	@staticmethod
	def getLargestPrimeBelowN(n):

		# Start with an odd number below n while n is bigger than 3 or
		# is not prime, go to next odd number
		n -= 1 if n % 2 == 0 else 2
		while (3 < n and not Hash.isPrime(n)):
			n -= 2

		# Return prime number or 3
		return n

	# This method determines if an integer is prime. If N is small
	# or even then it is not prime.
	#################################################################
	@staticmethod
	def isPrime(N):
		if N < 2 or (N > 2 and N % 2 == 0):
			return False

		# The upper bound of possible factors is the square root of N
		top = int(pow(N, 0.5) + 1)

		# Start factor testing at 3
		factor = 3

		# While there are more factors to check, test if factor divides
		# N evenly. If so, then N is not prime otherwise check next odd
		# factor
		while factor < top:
			if N % factor == 0:
				return False
			factor += 2

		# No factors found, so N is prime
		return True


	# This method executes a simple hashing function
	#################################################################
	@staticmethod
	def simpleHash(key):
		# Integers hash to themselves
		if isinstance(key, int):
			return key

		# Strings are hashed by letters. Multiply the code for each
		# letter by 256 to the power of its position in the string
		elif isinstance(key, str):
			return sum(256 ** i * ord(key[i])
					   for i in range(len(key)))

		# For sequences, multiply the simpleHash of each element by
		# 256 to the power of its position in the sequence
		elif isinstance(key, (list, tuple)):
			return sum(256 ** i * Hash.simpleHash(key[i])
					   for i in range(len(key)))

		# Otherwise it's an unknown type
		raise Exception('Unable to hash key of type ' + str(type(key)))
