#!/usr/bin/env python
from classes import *
from utils import *

def main(argv=None):
	fileName = "resources/SUPERMARCHE PA.txt"

	if (debug):
		print("\n\n****************************************\n* The program is starting\n****************************************")

	"""
	The function extractData return the following variables:
	- lines: contains all lines of the receipt
	- words contains all the words of the receipt

	"""
	lines, words = extractData(fileName)

	"""
	The Receipt object contains the following attributes:
	 - merchant
	 - client 
	 - date
	 - time
	 - cashNo
	 - cashier
	 - items
	 - value
	 - payment
	"""
	Receipt = populateReceipt(lines)

	if (debug):
		print("\nHere is your receipt :\n") 
		Receipt.printReceipt()
	
	"""
	The function removeNoise removes single characters from the 
	lines list and returns a cleaned version, cleanLines
	"""
	if (debug):
		print ("\nDEBUG :\n")
	cleanLines = removeNoise(lines)

	"""
	The function collectItems
	"""
	groceryList = collectItems(cleanLines)

	for x in groceryList:
		Receipt.items.append(Item(x[0], x[1]))

	if (debug):
		print("\n\nThis is a list of your items :\n")
		for x in Receipt.items:
			x.printItem()

	verifyAmount(Receipt, groceryList)

	if (debug):
		print("\n\n****************************************\n* The program has finished\n****************************************\n")

		


if __name__ == "__main__":
    main()
