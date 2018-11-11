from CuckooHash import CuckooHash
#import sys
def AutoCorrect(word):
	word=word+"\n"
	filename=input("enter name of the file")
	dic=CuckooHash(100)
	file_obj=open(filename,"r")
	for w in file_obj:
		dic.insert([w])
	dic.print()	
	print(dic.len)
	result=dic.lookup(word)
	if not(result):
		possible_words=list()
		alphabets=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		for i in range(len(word)-2,-1,-1):
			#print("i is now",i)
			for letter in alphabets:
				new_word=list(word)
				new_word[i]=letter
				new_word=''.join(new_word)
				#print(new_word)
				isvalid=dic.lookup(new_word)
				if (isvalid):
					possible_words.append(new_word)

				new_word2=list(word)
				#print(new_word2)
				new_word2.append('')
				for j in range(len(word)-1,i,-1):
					new_word2[j+1]=new_word2[j]
				new_word2[i+1]=letter
				new_word3=list(new_word2)
				if i==0:
					new_word3[i+1]=new_word3[i]
					new_word3[i]=letter
					#print(new_word3)
					new_word3=''.join(new_word3)
					isvalid=dic.lookup(new_word3)
					if (isvalid):
						possible_words.append(new_word3)
				new_word2=''.join(new_word2)
				#print(new_word2)
				isvalid=dic.lookup(new_word2)
				if isvalid:
					possible_words.append(new_word2)

			new_word4=list(word)
			for j in range(i,len(word)-1):
				new_word4[j]=new_word4[j+1]
			temp=new_word4.pop()
			new_word4=''.join(new_word4)	
			isvalid=dic.lookup(new_word4)
			if isvalid:
				possible_words.append(new_word4)

		return possible_words
	else:
		#print("word exists")
		return None	
		

def main():
	word=input("enter a word to search : ")
	result=AutoCorrect(word)
	#if result!=None:
		#print("the possible words are :",result)
if __name__=='__main__':
	#sys.setrecursionlimit(30000)
	main()		