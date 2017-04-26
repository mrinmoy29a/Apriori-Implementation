'''
Apriori Algorithm implementation

The program reads datasets from a .csv file and output the association rules.

Currently supports only integer type data
'''

from itertools import permutations

def generateData(filepath):
	'''
	This function stores the data in data-structures by reading a given file
	'''
	f = open(filepath, 'rU')
	itemSet = set()
	dataSet = []
	
	for line in f:
		line = line.strip()
		data = frozenset(line.split(' '))
		dataSet.append([int(i) for i in data])
		for d in data:
			itemSet.add(frozenset([int(d)]))
	return itemSet, dataSet

def getsupport(dataSet, items):
	'''
	returns the the support of given items over dataSet
	'''
	items = frozenset(items)
	dataSetSize = len(dataSet)
	occurenceOfItems = 0
	
	for d in dataSet:
		d = frozenset(d)
		if items.issubset(d):
			occurenceOfItems += 1
		
	return float(occurenceOfItems)/dataSetSize


def generateMinimumSupportedItemset(dataSet, itemSet, minSupport, supportValues):
	'''
	Generates itemsets with minimum support value
	'''
	supportedItems = set()
	for item in itemSet:
		sv = getsupport(dataSet, item)
		if sv >= minSupport:
			supportedItems.add(frozenset(item))
			supportValues[frozenset(item)] = sv
	return supportedItems

def generateAssociationRules(supportValues, dataSet, allSupportedItems, minConfidence):
	'''
	Generate association rules from supported items.
	All the rules are greater than equal to minimum confidence value.
	'''
	
	assocRules = []
	for item in allSupportedItems:
		itemperm = permutations(item, len(item))
		for permutedItem in itemperm:
			for i in xrange(1, len(item)):
				conf = supportValues[item]/supportValues[frozenset(permutedItem[0:i])]
				if conf >= minConfidence:
					assocRule = str(list(item - frozenset(permutedItem[0:i]))) + ' -> ' + str(permutedItem[0:i])
					supcon = (supportValues[item], conf)
					assocRules.append((assocRule, supcon))
					print assocRule + '----SUPPORT: '+str(supportValues[item])+'----CONFIDENCE: '+str(conf)
	
	return assocRules
	
	
	
def AprioriAlgorithm(filepath, minSupport, minConfidence):
	'''
	Apriori Algorithm
	
	The function extracts data from filepath and runs the apriori algorithm over it.
	The minimum support value is given as minSupport.
	The minimum confidence value is given as minConfidence.
	'''
	
	itemSet, dataSet = 	generateData(filepath)
	
	currentItems = itemSet
	allcombinations = set(itemSet)
	setSize = 1
	allSupportedItems = []
	
	supportValues = {} # Item --> Support
	
	print 'processing itemset'
	while True:
		# Current value of subset size
		print 'k = ' + str(setSize
		currentItems = generateMinimumSupportedItemset(dataSet, allcombinations, minSupport, supportValues)
		allSupportedItems.extend(currentItems)
		if len(currentItems)==0:
                        break
		setSize += 1
		
		# From a given set generates another set whose elements have length+1
		allcombinations = set(i.union(j) for i in currentItems for j in currentItems if len(i.union(j))==setSize)
	
	assocRules = generateAssociationRules(supportValues, dataSet, allSupportedItems, minConfidence)
	#print assocRules                    


filepath = raw_input('Enter filepath: ')
minSupport = float(raw_input('Enter minimum support: '))
minConfidence = float(raw_input('Enter minimum confidence: '))
AprioriAlgorithm(filepath, minSupport, minConfidence)
