def sieve(mx):
	isprime = []
	for i in xrange(mx): isprime.append([])
	isprime[0] = []
	isprime[1] = []
	
	
	for i in xrange(2, mx):
		if isprime[i] == []:
			j = 1
			while i*j < mx:
				isprime[i*j].append(i)
				j += 1
	
	return isprime

def prod(lst): return reduce(lambda x,y: x*y, lst, 1)
	
def fill(lst, mx):
	for i in xrange(2,mx):
		p = prod(lst[i])
		if p != i: lst[i] += lst[i/p]
	return lst

def div(lst):
	d = 1
	n = sorted(lst)
	
	val = n[0]
	cnt = 1
	
	for num in n[1:]:
		if num != val:
			d *= (cnt+1)
			val = num
			cnt = 1
		else: cnt += 1
	d *= (cnt+1)
	
	return d
	
mx = 10**7+2

lst = sieve(mx)
lst = fill(lst,mx)

tot = 0

pdiv = 2

for i in xrange(3, mx-1):
	cdiv = div(lst[i])
	if pdiv == cdiv:
		tot += 1
	pdiv = cdiv

print tot