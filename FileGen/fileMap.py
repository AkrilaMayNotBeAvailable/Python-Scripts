import random

'''
1. Generates a random platform level between a, b, c, d, e and append a list as first element
2. Generates a random value between 1, 2, 3. This will be the number of platforms on that column (doesn't need to append, but should be considerated)
3. Based on 2, generates X (where X is the value generated in 2) platforms on that level (append in a list as element)
4. After 3, print a underscore to repesent next column. Repeat 1, 2, 3, 4 until list size equals to 100
'''

def GenerateSequence(size):
	# Output List
	finalSequence = []
	newColumn = '_'
	
	curColumn = []
	
	# First choosen value
	firstValue = ['a', 'b', 'c', 'd', 'e']
	prev = random.choice(firstValue)
	finalSequence.append(prev)
	curColumn.append(prev)
	
	
	# Rest values
	for i in range(0, size):
		# Defines a random amount of platforms on each column between 1 and 4
		platforms = random.randint(1, 3)
		
		# Defines column levels for each platform
		for column in range(0, platforms):
			match prev:
				case 'a':
					next = 'b'
				case 'b':
					next = random.choice(['a', 'c'])
				case 'c':
					next = random.choice(['a', 'b', 'd'])
				case 'd':
					next = random.choice(['a', 'b', 'c', 'e'])
				case 'e':
					next = random.choice(['a', 'b', 'c', 'd'])
					
			prev = next
			
			# Remove element if it is inside the column already
			if prev in curColumn:
				curColumn.pop()
			else:
				curColumn.append(prev)
				finalSequence.append(''.join(curColumn))
				print(curColumn)
				
					
		# Next column
		finalSequence.append(newColumn)
		curColumn.clear()
	
	# Returns output as String
	return ''.join(finalSequence)

#=======================================
# Main():
#=======================================
sizeSequence = 40

for i in range(1, 6):
	generatedSequence = GenerateSequence(sizeSequence)
	with open(f'map_{i}.txt', 'w') as file:
		file.write(generatedSequence)
