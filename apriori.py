'''
Apriori Algorithm implementation

The program reads datasets from a .csv file and output the association rules.
'''

from itertools import chain, combinations
import decimal

decimal.getcontext().prec = 6

def generateData(filepath):
	f = open(filepath, 'rU')
	itemSet = set()
	dataSet = []
	
	for line in f:
		line = line.strip()
		data = frozenset(line.split(' '))
		dataSet.append(list(data))
		for d in data:
			itemSet.add(d)
			
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


def generateMinimumSupportedItemset(dataSet, itemSet, minSupport):
	
	supportedItems = set()
	for item in itemSet:
		print getsupport(dataSet, item), item
		if getsupport(dataSet, item) >= minSupport:
			supportedItems.add(item)
	
	return supportedItems
	
def AprioriAlgorithm(filepath, minSupport, minConfidence):
	'''
	Apriori Algorithm
	
	The function extracts data from filepath and runs the apriori algorithm over it.
	The minimum support value is given as minSupport.
	The minimum confidence value is given as minConfidence.
	'''
	
	itemSet, dataSet = 	generateData(filepath)
	
	currentItems = itemSet
	print currentItems
	setSize = 1
	allSupportedItems = []
	
	print 'processing itemset'
	while len(currentItems):
			
		allcombinations = chain(*combinations(currentItems, setSize))
		currentItems = generateMinimumSupportedItemset(dataSet, allcombinations, minSupport)
		allSupportedItems.extend(currentItems)
		print currentItems
		
		setSize += 1
	
	#print allSupportedItems


filepath = raw_input('Enter filepath: ')
minSupport = float(raw_input('Enter minimum support: '))
AprioriAlgorithm(filepath, minSupport, 0)

		
	

