'''
Apriori Algorithm for frequent pattern mining
The program reads datasets from a .dat file and output the association rules.
Currently supports only numerically represented data
'''

try:
	from itertools import combinations
	import sys
except:
	print "module inclusion error"

# dataSet is a list that stores every transaction
dataSet = []

# itemSet is a frozenset that keeps track of list of items in the given dataset
itemSet = set()

# candidates is a python dictionary or hash table that stores the candidate itemsets of size k
# candidates[i] = Set of all k length patterns
candidates = {}

# associations is a list that stores all association rules
associations = []

def generateData(filepath):
	
	# This function stores the data in data-structures by reading a given file
	
	f = open(filepath, 'rU')
	splitter = ' '
	if filepath.split('.')[-1] == 'csv':
		splitter = ','
	
	global itemSet
	
	for line in f:
		line = line.strip()
		data = line.split(' ')
		dataSet.append(sorted(data))
		for d in data:
			itemSet.add(d)
		
	
	itemSet = set(sorted(itemSet))
		
def apriori_gen(k, Ck, Ck_p):
	
	print "Generating ", k, " candidate set"
	
	if k == 1:
		for item in itemSet:
			Ck.append([item])
		return
	
	
	cklen = len(Ck_p)
	
	for i in xrange(cklen):
		for j in xrange(i+1, cklen):
			
			if Ck_p[i][:-1] == Ck_p[j][:-1]:
				Ck.append( Ck_p[i] + [ Ck_p[j][-1] ] )

def supportof(pat):
	
	pat = frozenset(pat)
	frequency = 0
	
	for d in dataSet:
		ds = frozenset(d)
		if pat.issubset(ds):
			frequency += 1
	
	return frequency

def generateAssociateRule(pat, suppat, minconf, NTd):
	
	# Generate all Association Rules from a given pattern pat
	
	allCombi = sum([map(list, combinations(pat, i)) for i in range(len(pat) + 1)], [])
	setSize = len(allCombi)-2
	
	for i in xrange(setSize, setSize/2, -1):
		conf = float(suppat)/candidates[ frozenset(allCombi[i]) ]
		if conf >= minconf:
			associations.append((conf, str(allCombi[i]), str(allCombi[setSize-i+1]), float(suppat)/NTd) )

def apriori(minsup, minconf):
	k = 1
	
	# NTd is total number of transactions
	NTd = len(dataSet)
	
	# Adjust the value of minsup
	minsup *= NTd
	
	Ck_p = []
	
	while True:
		
		# Candidates list
		Ck = []
		apriori_gen(k, Ck, Ck_p)
		Ck_p = []
	
		if len(Ck)==0:
			break

		for c in Ck:
			supc = supportof(c)
			if supc >= minsup:
				generateAssociateRule(c, supc, minconf, NTd)
				candidates[frozenset(c)] = supc
				Ck_p.append(sorted(c))
			
		k += 1
		del Ck

def main(argv):
	global associations
	
	if len(argv)<3:
		print "You must enter the arguments manually."
		filepath = raw_input("Enter data file path: ")
		minsup = float(raw_input("Enter minimum support: "))
		minconf = float(raw_input("Enter minimum confidence: "))
	else:
		filepath = argv[0]
		minsup = float(argv[1])
		minconf = float(argv[2])
	
	print filepath
	generateData(filepath)
	apriori(minsup, minconf)
	
	
	associations.sort(reverse=True)
	print "\n-------------------ASSOCIATION RULES-------------------\n"
	for rule in associations:
		conf, left, right, sup = rule
		print left + "--->" + right + " --------- conf:", conf, ' sup:', sup, '\n'

if __name__ == "__main__":
	main(sys.argv[1:])
