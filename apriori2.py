'''
Apriori Algorithm for frequent pattern mining
The program reads datasets from a .csv or .dat file and output the association rules.
Currently supports only numerically represented data
'''

try:
	from itertools import combinations
except:
	print "module inclusion error"

# dataSet is a list that stores every transaction
dataSet = []

# tempdata is used for transaction reduction
tempdata = []

# itemSet is a frozenset that keeps track of list of items in the given dataset
itemSet = set()

# candidates is a python dictionary or hash table that stores the candidate itemsets of size k
# candidates[i] = Set of all k length patterns
candidates = {}

def generateData(filepath):
	
	# This function stores the data in data-structures by reading a given file
	
	f = open(filepath, 'rU')
	global itemSet
	
	for line in f:
		line = line.strip()
		data = line.split(' ')
		dataSet.append(sorted(data))
		for d in data:
			itemSet.add(d)
		
	
	itemSet = set(sorted(itemSet))
		
def apriori_gen(k, Ck):
	
	print "Generating ", k, " candidate set"
	
	if k == 1:
		for item in itemSet:
			Ck.append([item])
		return
	
	
	cklen = len(candidates[k-1])
	
	for i in xrange(cklen):
		for j in xrange(i+1, cklen):
			
			if candidates[k-1][i][:-1] == candidates[k-1][j][:-1]:
				Ck.append( candidates[k-1][i] + [ candidates[k-1][j][-1] ] )

def supportof(pat):
	
	pat = frozenset(pat)
	frequency = 0
	
	for d in dataSet:
		ds = frozenset(d)
		if pat.issubset(ds):
			frequency += 1
			if d not in tempdata:
				tempdata.append(d)
	
	return frequency

def apriori(minsup):
	
	global dataSet
	
	k = 1
	
	# NTd is total number of transactions
	NTd = len(dataSet)
	
	
	while True:
		
		# Candidates list
		Ck = []
		apriori_gen(k, Ck)
		
		if len(Ck)==0:
			break
		
		candidates[k] = []

		for c in Ck:
			if supportof(c) >= minsup*NTd:	
				candidates[k].append(sorted(c))
		
		print candidates[k]
		k += 1
		dataSet = tempdata[:]
		del tempdata[:]
		del Ck
	
generateData("chess.dat")
apriori(0.95)
