#################################################################
# CountWordTotals.py
#################################################################
# Author: gametechmatch
# Course: Data Structures
# CH11 - Hash Tables
# Date: 3/19/2023
#################################################################
# This file counts the number of times different words appear in
# a file. Conjunctions are treated like unique words
##################### NOTE ########################################
# These files only run on Python3 since the Python code for file
# manipulation has changed since the prior version
##################################################################
from HashTable import *
from Hash import *

def main():
	# get file contents & remove non-word characters
	fileContentsAsString = getFileData()
	wordsInFile = removeExtraChars(fileContentsAsString)

	# figure out total number of words & set up hash
	# table based on total words
	totalWords = getTotalWords(wordsInFile)
	wordHashTable = HashTable(totalWords)

	# insert words into hash table & count their occurrences
	for word in wordsInFile.split():
		cells = wordHashTable.getTotalCellsInHashTable()
		uniqueCode = Hash.unique_encode_word(word) % cells
		wordHashTable.insert(uniqueCode, word)

	# print out the totals of each word
	print(wordHashTable.getStringOccupiedCells())

# This function gets the data from a text file
#################################################################
def getFileData():
	openedFile = open("theEgg.txt", mode='r', encoding="utf-8")
	fileContentsAsString = openedFile.read()
	openedFile.close()
	return fileContentsAsString

# This function removes non-word characters
#################################################################
def removeExtraChars(fileContentsAsString):

	wordsInFile = ""

	# Go through each word in string representation of file contents
	for word in fileContentsAsString.split():
		# Remove non-word characters
		strippedWord = word.strip(
			'(' + ')' + '<' + '>' + '[' + ']' + '{' + '}' + '-' +
			'_' + ',' + '.' + '?' + '!' + ':' + ';' + '"' + "'" +
			'…' + '“' + '”' + "’").lower()

		# update new string representation of words in file with
		# a space after each word
		wordsInFile += strippedWord + " "

	return wordsInFile

# This function finds the total number of words in the file
#################################################################
def getTotalWords(wordsInFile):
	count = 0
	for word in wordsInFile.split():
		count +=1
	return count

# execute main function
if __name__ == '__main__':
	main()
