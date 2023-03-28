#################################################################
# HashTable.py
#################################################################
# Source Title: HashTable_OpenAddressing.py
# Source Type: Book
# Source Title: Data Structures & Algorithms in Python
# Source Authors: John Canning, Alan Broder, & Robert Lafore
#################################################################
# Additional Methods: .getStringOccupiedCells()
#################################################################
# Author of additional methods: gametechmatch
# Course: Data Structures
# CH11 - Hash Tables
# Date: 3/19/2023
#################################################################
# Implement a hash table using open addressing
# To experiment with different types of open addressing,
# users provide both a hashing function and a probe generator
#################################################################
from Hash import *

# A hash table using open addressing
#################################################################
class HashTable(object):

   # This constructor initializes a hash table
   #################################################################
   def __init__(self, size=7, maxLoadFactor=0.5):
      self.__table = [None] * size # Allocate spaces for empty hash table
      self.__nItems = 0     # Track the count of items in the table
      self.__hash = Hash.simpleHash    # Store given hash function, probe
      self.__probe = Hash.doubleHashProbe  # sequence generator, and max load factor
      self.__maxLoadFactor = maxLoadFactor

   # This method returns the number of cells that have items in the
   # hash table
   #################################################################
   def __len__(self):
      return self.__nItems

   # This method returns the total number of cells in the hash table
   #################################################################
   def getTotalCellsInHashTable(self):
      return len(self.__table)

   # This method uses the hashing function to get the default cell index
   #################################################################
   def getDefaultCellIndex(self, key):
      return self.__hash(key) % self.getTotalCellsInHashTable()

   # This method gets the value associated with a key in the hash
   # table, if it is present
   #################################################################
   def findValueInHTable(self, key):
      # Look for cell index matching key. If index not found, item
      # at i is empty or it has another key, return None, else
      # return item value
      i = self.__findHashTableIndex(key)

      return (None if (i is None) or self.__table[i] is None or
              self.__table[i][0] != key else self.__table[i][1])

   # Unique value for deletions
   __Deleted = (None, 'Deletion marker')

   # This method finds the hash table index for a key using open
   # addressing probes. It will find deleted cells if asked
   #################################################################
   def __findHashTableIndex(self, key, deletedOK=False):
      for i in self.__probe(self.getDefaultCellIndex(key), key, self.getTotalCellsInHashTable()):

         # If we find an empty cell or a deleted cell when one is
         # sought or the 1st of tuple matches key
         if (self.__table[i] is None or
             (self.__table[i] is HashTable.__Deleted and
              deletedOK) or self.__table[i][0] == key):

            # then return index
            return i

      # If probe ends, the key was not found
      return None

   # This method inserts or updates the value associated with a given key
   #################################################################
   def insert(self, key, value, count=1):

      # Look for cell index matching key or an empty or deleted cell
      i = self.__findHashTableIndex(key, deletedOK=True)

      # If the probe sequence fails, then the hash table is full
      if i is None:
         raise Exception('Hash table probe sequence failed on insert')

      # If we found an empty cell, or a deleted cell
      if (self.__table[i] is None or self.__table[i] is HashTable.__Deleted):

         # Then insert the new item there as a key-value pair and
         # increment the item count
         self.__table[i] = (key, value, count)
         self.__nItems += 1

         # When load factor exceeds limit, grow table
         if self.getLoadFactor() > self.__maxLoadFactor:
            self.__growTable()

         # Return flag to indicate item inserted
         return True

      # If first of tuple matches key, and value doesn't,
      # then update item
      if self.__table[i][0] == key and self.__table[i][1] != value:
         self.__table[i] = (key, value, count)

         # Return flag to indicate update
         return False

      # If tuple matches key, but value is same, only increase
      # count for that word
      if self.__table[i][0] == key and self.__table[i][1] == value:

         # make a temporary list to update the count variable
         # since current index in table is a tuple which cannot
         # be changed
         tempList = list(self.__table[i])
         tempList[2] += 1
         listToTuple = tuple(tempList)
         self.__table[i] = listToTuple

         return False

   # This method gets the load factor for the hash table
   #################################################################
   def getLoadFactor(self):
      return self.__nItems / len(self.__table)

   # This method increases the table's total cells to accommodate
   # additional items
   #################################################################
   def __growTable(self):

      # Save old table
      oldTable = self.__table

      # Make new table at least 2 times bigger and a prime number of
      # cells
      size = len(oldTable) * 2 + 1
      while not Hash.isPrime(size):

         # Only consider odd sizes
         size += 2

      # Allocate new table
      self.__table = [None] * size

      # Note that it is empty
      self.__nItems = 0

      # Loop through old cells and insert non-deleted items by re-hashing
      for i in range(len(oldTable)):
         if (oldTable[i] and oldTable[i] is not HashTable.__Deleted):
            # Call with (key, value, count) tuple
            self.insert(*oldTable[i])

   # This method deletes an item identified by its key from the hash
   # table and raises an exception if not ignoring missing keys
   #################################################################
   def delete(self, key, ignoreMissing=False):

      # Look for cell index matching key
      i = self.__findHashTableIndex(key)

      # If the probe sequence fails or cell i is empty or it's not the item to delete
      # Then item was not found.
      if (i is None or self.__table[i] is None or self.__table[i][0] != key):

         # Ignore it if so directed
         if ignoreMissing:
            return

         # Otherwise raise an exception
         raise Exception('Cannot delete key {} not found in hash table'.format(key))

      # Mark table cell deleted
      self.__table[i] = HashTable.__Deleted

      # Reduce count of items
      self.__nItems -= 1

   # This method traverses the key, value pairs in table
   #################################################################
   def traverse(self):

      # Loop through all cells
      for i in range(len(self.__table)):

         # For those that contain undeleted items, yield them to
         # the caller
         if (self.__table[i] and self.__table[i] is not HashTable.__Deleted):
            yield self.__table[i]

   # This method returns a string representation of the hash table
   #################################################################
   def __str__(self):
      N = len(self.__table)
      out = '<HashTable of {} items'.format(self.__nItems)
      show = 40    # Number of cells to show at either end

      # First cells up to show - 1
      for i in range(min(show, N)):
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += '{}: {}'.format(*self.__table[i])
      if N > 2 * show:
         out += '\n  ...'

      # Last cells up to N - 1
      for i in range(max(N - show, show), N):
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += '{}: {}'.format(*self.__table[i])
      out += ' >'
      return out

   # This method returns a string representation of the hash table
   #################################################################
   def getStringHash(self):
      N = len(self.__table)
      out = '<HashTable of {} items'.format(self.__nItems)
      show = 40  # Number of cells to show at either end

      # First cells up to show - 1
      for i in range(min(show, N)):
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += '{}: {}'.format(*self.__table[i])
      if N > 2 * show:
         out += '\n  ...'

      # Last cells up to N - 1
      for i in range(max(N - show, show), N):
         out += '\n  {:4d}-'.format(i)
         if self.__table[i]:
            out += '{}: {}'.format(*self.__table[i])
      out += ' >'
      return out

   # This method returns a string representation of the hash table
   # cells that contain items
   #################################################################
   def getStringOccupiedCells(self):
      # figure out total number of cells & print header
      N = len(self.__table)
      out = '<HashTable of {} unique words'.format(self.__nItems)
      out += '\nWORD\t\tTOTAL OCCURRENCES'

      # Shows cells
      for i in range(N):
         if self.__table[i] is not None and self.__table[i] is not HashTable.__Deleted:
            out += '\n'
            if self.__table[i]:
               out += 'Word: {}'.format(self.__table[i][1]) + '______count: {}'.format(self.__table[i][2])

      return out

   # This method shows the keys of all table cells as a string
   #################################################################
   def tableString(self):

      # Empty cells are spaces, deleted cells are the null otherwise
      # use the string of the key
      return '[{}]'.format(','.join(' ' if cell is None else
         'ø' if cell is HashTable.__Deleted else
         repr(cell[0])
         for cell in self.__table))

   # This method peeks at the contents of cell i
   #################################################################
   def peek(self, i):
      return self.__table[i]
