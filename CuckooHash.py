import math
class CuckooHash:
	
	def __init__(self,size=1000):
		self.len=size#length of tables
		self.hashtable=[[None for _ in range(self.len)] for _ in range(3)]
		#self.hashtable=[[None,None,None],[None,None,None],[None,None,None]]
		self.stash=CuckooHash(self.len//10) if self.len>=10 else None#stash to store elements that create infinite loops
		self.population=0#to store number of elements in all tables combined

	def stringHashFunction(self,str):
		p1=37#a prime number
		sum1,sum2,sum3=37,5381,0#assigning initial values to hashvalues
		for i in range(len(str)-1,-1,-1):
			sum1 = (sum1+ord(str[i]))*p1#calculated using Horner's rule
			sum2 = ((sum2 << 5) + sum2) + ord(str[i]) #djb2 algorithm
			sum3 = ord(str[i]) + (sum3 << 6) + (sum3 << 16) - sum3#sdbm algorithm
		sum1=sum1%self.len#using compression maps
		sum2=sum2%self.len
		sum3=sum3%self.len
		return (sum1,sum2,sum3)#return a tuple consisting of hashvalues

	def integerHashFunction(self,key): 
		#MAD function
		A = ((5**(1/2))-1)/2 #Conjugate of Golden Ratio
		b = 29 #random prime number
		ans1 = math.floor(A*key + b) % self.len
		#Combination of Mid-squared method and Random Generator
		key = key**2
		l = 10 ** (len(str(key))//2 + 2)
		key = key % l #Removing the front of the unwanted digits
		l = 3 if key>999 else len(str(key))
		key=int(str(key)[0:l]) #getting the final middle 3 digits of the squared key
		random.seed(key) #seeding the random generator with the middle 3 digits
		ans2 = math.floor(random.random()*self.len)
		#Basic Multiplication method
		A = ((5**(1/2))-1)/2 #Conjugate of Golden Ratio
		ans3 = math.floor(self.len * ((key*A) % 1))
		return (ans1,ans2,ans3)

	def insert(self,data,count=0,i=0):
		if(isinstance(data[0],int)):
			hashvalues=self.integerHashFunction(data[0])
			'''the return value of integer 
			hash function is assigned to hashvalues variable'''
		else:
			hashvalues=self.stringHashFunction(data[0])
			'''the return value of string
			hash function is assigned to hashvalues variable'''
		if self.stash is not None and (count>math.floor(math.log(self.len))):
			self.stash.insert(data)				
			return
			'''Here we are checking if number of function calls exceeds the
			log of table size. If it does,it indicates an infinite loop and we push into the stash'''
		if(self.hashtable[i][hashvalues[i]]==None):
			self.hashtable[i][hashvalues[i]]=data
			'''if the slot to which key is hashed is empty,then we
			simply insert the data''' 
		else:
			temp=self.hashtable[i][hashvalues[i]]
			self.hashtable[i][hashvalues[i]]=data
			self.insert(temp,count+1,(i+1)%3)
			'''if the slot to which the key is hashed is filled,then we pop 
			the previous element ,insert the new element and rehash the previous key
			to alternate location in the next table''' 
			self.population += 1
		if self.population>=(self.len*0.9*3):
			self.rehash()

	def delete(self,key):
		if self.lookup(key):
			if isinstance(key,int):
				hashvalues = self.integerHashFunction(key)
				'''the return value of integer 
				hash function is assigned to hashvalues variable'''
			else:
				hashvalues = self.stringHashFunction(key)
				'''the return value of string
				hash function is assigned to hashvalues variable'''
			if self.hashtable[0][hashvalues[0]][0]==key:
				self.hashtable[0][hashvalues[0]]=None
			elif self.hashtable[1][hashvalues[1]][0]==key:
				self.hashtable[1][hashvalues[1]]=None
			elif self.hashtable[2][hashvalues[2]][0]==key:
				self.hashtable[2][hashvalues[2]]=None
			elif self.stash is not None and self.stash.population>0:
				self.stash.delete(key)

	def lookup(self,key):
		if(isinstance(key,int)):
			hashvalues=self.integerHashFunction(key)
		else:
			hashvalues=self.stringHashFunction(key)
		if self.hashtable[0][hashvalues[0]] is not None and self.hashtable[0][hashvalues[0]][0]==key:
			return True
		elif self.hashtable[1][hashvalues[1]] is not None and self.hashtable[1][hashvalues[1]][0]==key:
			return True			
		elif self.hashtable[2][hashvalues[2]] is not None and self.hashtable[2][hashvalues[2]][0]==key:
			return True			
		elif self.stash is not None and self.stash.population>0:
			return self.stash.lookup(key)
		return False

	def getElements(self,elements=[]):
		for i in self.hashtable:
			for j in i:
				if j is not None:
					elements.append(j)
		if self.stash is not None and self.stash.population>0:
			elements = self.stash.getElements(elements)
		return elements

	def rehash(self):
		elements = self.getElements()
		LEN = 2*self.len
		self.hashtable[0] = [None] * LEN
		self.hashtable[1] = [None] * LEN
		self.hashtable[2] = [None] * LEN
		self.len=LEN
		self.population=0
		self.stash=CuckooHash(LEN//10) if LEN>10 else None
		for i in elements:
			self.insert(i)

	def print(self):
		for i in range(3):
			print("Table ",i)
			for j in range(self.len):
				if self.hashtable[i][j] is not None:
					print(*self.hashtable[i][j])
		print("--------------------------------------------------------")
		if self.stash is not None and self.stash.population>0:
			print("Stash:")
			self.stash.print()


	def update(self,sign,key,val):
		if(isinstance(key,int)):
			hashvalues=self.integerHashFunction(key)
		else:
			hashvalues=self.stringHashFunction(key)
		if sign=='+':
			if self.hashtable[0][hashvalues[0]][0]==key:
				self.hashtable[0][hashvalues[0]][1] += val
			elif self.hashtable[1][hashvalues[1]][0]==key:
				self.hashtable[1][hashvalues[1]][1] += val
			elif self.hashtable[2][hashvalues[2]][0]==key:
				self.hashtable[2][hashvalues[2]][1] += val
			elif self.stash.population>0:
				self.stash.update(sign,key,val)
		else:
			if self.hashtable[0][hashvalues[0]][0]==key:
				if self.hashtable[0][hashvalues[0]][1]>=val:
					self.hashtable[0][hashvalues[0]][1] -= val
				else:
					print("invalid",key,val,">",self.hashtable[0][hashvalues[0]][1])
			elif self.hashtable[1][hashvalues[1]][0]==key:
				if self.hashtable[1][hashvalues[1]][1]>=val:
					self.hashtable[1][hashvalues[1]][1] -= val
				else:
					print("invalid",key,val,">",self.hashtable[1][hashvalues[1]][1])
			elif self.hashtable[2][hashvalues[2]][0]==key:
				if self.hashtable[2][hashvalues[2]][1]>=val:
					self.hashtable[2][hashvalues[2]][1] -= val
				else:
					print("invalid",key,val,">",self.hashtable[2][hashvalues[2]][1])
			elif self.stash.population>0:
				self.stash.update(sign,key,val)


def main():
	ht = CuckooHash()
	ht.insert(["ably"])
	ht.insert(["abl"])
	#ht.print()
	ht.insert(["bat"])
	#print("\n\n\n\n")
	ht.print()
	#print(ht.len)
	#ht.print()


if __name__=='__main__':
	main()