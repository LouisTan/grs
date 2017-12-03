#!/usr/bin/env python
from classes import *
from const import *
import sys

def extractData(fileName):
	lines, words = [], []

    #Removes the lines breaks
	with open(fileName, "r") as file:
		lines = file.readlines()
		lines = [x.strip() for x in lines]
        #if (debug):
        #    print("\nEnumeration of the lines list:\n")
        #    orderedLines = list(enumerate(lines))
        #    for line in orderedLines: 
        #        print(line)
        #    print('\n')
    
    #Separates the lines in a list of words
	for line in lines:
		words.append(line.split(' '))
        if (debug):
            print("\nEnumeration of the words list:\n")
            orderedWords = list(enumerate(words))
            for word in orderedWords: 
                print(word)
            print('\n')
	
	return lines, words 


def populateReceipt(lines):

    print("\nHeader verification\n")
    print(PAHead0+("\t\t\t\tYes" if str(lines[0]) == PAHead0 else "\t\t\t\tNo"))    #merchant
    print(PAHead1+("\t\t\tYes" if str(lines[1]) == PAHead1 else "\t\t\tNo"))        #address1
    print(PAHead2+("\t\tYes" if str(lines[2]) == PAHead2 else "\t\tNo"))            #address2
    print(PAHead3+("\t\t\tYes" if str(lines[3]) == PAHead3 else "\t\t\tNo"))        #tel
    print(PAHead4+("\t\t\tYes" if str(lines[4]) == PAHead4 else "\t\t\tNo"))        #fax

    print("\nFooter verification\n")
    
    def searchFoot(PAfoot):
        foundFoot = False
        index = -1
        for line in lines:
                if line == PAfoot:
                    foundFoot = True
                    index = lines.index(line)
        return foundFoot, index 
    
    print(PAFoot0+("\t\t\t\tYes" if searchFoot(PAFoot0)[0] else "\t\t\t\tNo"))      #Vente nette
    print(PAFoot1+("\t\t\t\tYes" if searchFoot(PAFoot1)[0] else "\t\t\t\tNo"))      #Vente totale
    print(PAFoot2+("\t\t\tYes" if searchFoot(PAFoot2)[0] else "\t\t\tNo"))          #Arrondi
    print(PAFoot3+("\t\t\t\tYes" if searchFoot(PAFoot3)[0] else "\t\t\t\tNo"))     #Sous-total
    print(PAFoot4+("\t\t\t\tYes" if searchFoot(PAFoot4)[0] else "\t\t\t\tNo"))     #Comptant
    print(PAFoot5+("\t\t\t\t\tYes" if searchFoot(PAFoot5)[0] else "\t\t\t\t\tNo"))  #Remise

    indValue = -9
    if (searchFoot(PAFoot5)[0]):
        indValue = searchFoot(PAFoot5[1])+1:
    else:
        indValue = searchFoot(PAFoot4[1])+1:

    """TODO
    indPayment = -11
    if (searchFoot(PAFoot5)[0]):
        indValue = searchFoot(PAFoot5[1])+1:
    else:
        indValue = searchFoot(PAFoot4[1])+1:
    """


    if (debug):
        print("\nHere is your receipt :\n") 
        Receipt.printReceipt()

    return Receipt(
        str(lines[0]),          #merchant
        "client",               #client
        lines[5][1],            #date
        lines[5][2],            #time
        lines[5][0],            #cashNo
        lines[5][3],            #cashier
        "items",                #items
        lines[indValue][0],     #value
        lines[indPayment][0])   #payment


def removeNoise(lines):
    cleanLines = []
    
    #TODO: Cuts above and under the useful information
    for i in range(7, len(lines) - 18):
        cleanLines.append(lines[i].split(' '))

    #Removes unique numerical values
    for x in cleanLines:
        if x[0].isdigit():
            if (debug):
                print("Removing numerical value " + str(x))
            cleanLines.remove(x)

    #Removes unique alphabetical values
    for x in cleanLines:
        for y in x:
            if len(y) < 2 and not y.isdigit():
                if (debug):
                    print("Removing small value " + str(y) + " from " + str(x))
                x.remove(y)

    return cleanLines

def collectItems(cleanLines):
    groceryList = []

    #Checks the first character of a line and decides if it should be added to
    # the groceryList
    for x in cleanLines:
        for y in x:
            #If the first letter is alphabetical, keep on adding letters until
            # the item name is fully added
            if y.isalpha():
                groceryList[cleanLines.index(x)][0] += y + ' ';
            #The first occurence of the '$' tells the program to add it to the
            # most recent item added
            if y[0] is '$':
                groceryList[cleanLines.index(x)][1] = y.replace('%', '')

    #Removes all the empty pairs of the groceryList
    for x in groceryList:
        if not x[0]:
            if not x[1]:
                if (debug):
                    print("Removing :" + str(x) + ". Both values are missing.")
                groceryList.remove(x)


    temp = ['', '']
    for x in groceryList:
        if x[0]:
            if not x[1]:
                temp[0] = x[0]

        if not x[0]:
            if x[1]:
                temp[1] = x[1]

        if temp[0]:
            if temp[1]:
                groceryList.append(temp)
                temp = ['', '']

    for x in groceryList:
        if not x[0]:
            if (debug):
                print("Removing :" + str(x) + ". Missing the first value.")
            groceryList.remove(x)

    for x in groceryList:
        if not x[1]:
            if (debug):
                print("Removing :" + str(x) + ". Missing the second value.")
            groceryList.remove(x)

    return groceryList

def verifyAmount(receipt, groceryList):
    sumOfItems = 0.0
    for x in groceryList:
        sumOfItems += float(x[1].replace('$', ''))

    diff = float(receipt.value.replace('$', '')) - sumOfItems
    if (diff > 0.04):
        print("\nThe amount is not exact! " + str(round(diff, 2)))
        return False

    print("\nThe amount is exact ~" + str(round(diff, 2)))

    return True


   

