def flush(hand):
	suit = hand[0][1]
	for i in xrange(1,5):
		if hand[i][1] != suit: return 0
	return 1
	
def straight(hand):
	low = hand[0][0]
	for i in xrange(1,5):
		if hand[i][0] != low+i: return 0
	return 1
	

def evalhand(hand):
	strength = []
	for i in xrange(0,5):
		strength.append( hand[i][0] )
	
	#straight flush
	if flush(hand) and straight(hand):
		strength.append(8)
		strength.reverse()
		return strength
		
	#4-of
	if strength[0]==strength[3] or strength[1]==strength[4]:
		strength.append(strength[3])
		strength.append(7)
		strength.reverse()
		return strength
		
	#full house
	if strength[0]==strength[1] and strength[3]==strength[4]:
		if strength[1]==strength[2] or strength[2]==strength[3]:
			strength.append(strength[2])
			strength.append(6)
			strength.reverse()
			return strength
	
	#flush
	if flush(hand):
		strength.append(5)
		strength.reverse()
		return strength
		
	#straight
	if straight(hand):
		strength.append(4)
		strength.reverse()
		return strength
		
	#3-of
	if strength.count(strength[0]) == 3 or strength.count(strength[1]) == 3 or strength.count(strength[2]) == 3 :
		strength.append(strength[2])
		strength.append(3)
		strength.reverse()
		return strength
		
	tmp = []
	#two pairs, one pair, highcard  
	paircards = 0
	for val in strength:
		if strength.count(val) == 2:
			paircards += 1
			tmp.append(val)
	tmp.sort()
	if paircards == 4:
		strength.append(tmp)
		strength.append(2)
	elif paircards == 2:
		strength.append(tmp)
		strength.append(1)
	else: strength.append(0)
	
	strength.reverse()
	return strength
		
def cmphands(hand1, hand2):
	hand1 = evalhand(hand1)
	hand2 = evalhand(hand2)
	for i in xrange(len(hand1)):
		if hand1[i]>hand2[i]: return 1
		if hand1[i]<hand2[i]: return 0
	return 9
	
#opens data
input = open('e54.txt', 'r')

#reads line and parses into two hands
hands = input.readline()
wins = 0
while hands!='':
	hands = hands.rstrip()
	hands = hands.split(' ')

	hand1 = []
	hand2 = []

	for i in xrange(10):
		temp = []
	
		if hands[i][0] == 'T': temp.append(10)
		elif hands[i][0] == 'J': temp.append(11)
		elif hands[i][0] == 'Q': temp.append(12)
		elif hands[i][0] == 'K': temp.append(13)
		elif hands[i][0] == 'A': temp.append(14)
		else: temp.append( int(hands[i][0]))
	
		if hands[i][1] == 'S': temp.append(0)
		elif hands[i][1] == 'C': temp.append(1)
		elif hands[i][1] == 'H': temp.append(2)
		elif hands[i][1] == 'D': temp.append(3)
	
	
		if (i>4): hand2.append(temp)
		else: hand1.append(temp)
	
	hand1 = sorted(hand1)
	hand2 = sorted(hand2)
	
	if cmphands(hand1,hand2) == 1: wins += 1
	print hands, cmphands(hand1,hand2)
	
	
	hands = input.readline()
	
print wins