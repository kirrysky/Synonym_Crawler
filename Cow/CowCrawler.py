import re
import pickle

def openFile(filename):
     originalfile=open(filename+'.txt',encoding='utf-8')
     originitems=[]
     for line in originalfile.readlines():
          originitems.append(line[:-1])
     originalfile.close()
     return originitems

def savePickle(dictfile,filename):
	print("saving....")
	f=open(filename+".pickle",'wb')
	pickle.dump(dictfile,f)
	f.close()

def loadPickle(filename):
	print("loading....")
	f=open(filename+".pickle",'rb')
	dictfile=pickle.load(f)
	f.close()
	return dictfile

rawdata=openFile('rawdata')
wordWithSense=openFile('COW/WordWithSense')
data=[]
#洗一洗
for each in rawdata:
     if each!="":
          data.append(each)
word2sense={}
sense2word={}
for each in wordWithSense:
     line=each.split()
     if line[1] in data:
          if line[1] not in word2sense:
               word2sense[line[1]]=[line[4]]
          else:
               word2sense[line[1]].append(line[4])
     if line[4] not in sense2word:
          sense2word[line[4]]=[line[1]]
     else:
          sense2word[line[4]].append(line[1])
savePickle(word2sense,'COW/word2sense')
savePickle(sense2word,'COW/sense2word')
SynsetWithRel=openFile('COW/SynsetWithRel')
antsrel={}
for each in SynsetWithRel:
	line=each.split()
	if line[3]=='ants':
		if line[0] not in antsrel:
		    antsrel[line[0]]=[line[2]]
		else:
		    antsrel[line[0]].append(line[2])
savePickle(antsrel,'COW/antsrel')
word2sense=loadPickle('COW/word2sense')
sense2word=loadPickle('COW/sense2word')
n=0
antonym={}
for each in word2sense:
	if len(each)>1:
		n+=1
		antonym[each]={}
		for dic in word2sense[each]:
			if dic in antsrel:
				for ants in antsrel[dic]:
					if ants in sense2word:
						antonym[each][ants]=[]
						for word in sense2word[ants]:
							if '+的' in word:
								word=word[:-2]
							if word not in antonym[each]:
								antonym[each][ants].append(word)
antonym1={}
for each in antonym:
	checker=False
	for ants in antonym[each]:
		if ants[-1]=='v' or ants[-1]=='n' or ants[-1]=='a':
			checker=True
	if len(antonym[each])!=0 and checker:
		antonym1[each]={'v':[],'n':[],'a':[]}
		for ants in antonym[each]:
			if ants[-1]=='v' or ants[-1]=='n' or ants[-1]=='a':
				antonym1[each][ants[-1]]+=antonym[each][ants]
for each in antonym1:
	for cx in antonym1[each]:
		words=[]
		for word in antonym1[each][cx]:
			if word not in words:
				words.append(word)
		print(words)
		antonym1[each][cx]=words
print(antonym1)
print(len(antonym1))
f=open('Antonym.txt','w')
f.write("一共有"+str(len(antonym1))+"个反义词!\n")
f.write("--------------------------------------\n")
for each in antonym1:
	f.write(each+"\n")
	n=0
	for a in antonym1[each]:
		if len(antonym1[each][a])!=0:
			f.write(a+":")
			for word in antonym1[each][a]:
				f.write(word+" ")
			f.write("\n")
	f.write("========================\n")
f.close()
savePickle(antonym1,'COWantonyms')
n=0
synonyms={}
for each in word2sense:
	add_name=False
	for dic in word2sense[each]:
		if dic[-1]=="n" or dic[-1]=="v":
			add_name=True
	if len(each)>1 and add_name:
		n+=1
		synonyms[each]={'v':[],'n':[]}
		for dic in word2sense[each]:
			if dic[-1]=="n" or dic[-1]=="v":
				for word in sense2word[dic]:
					if word!=each:
						synonyms[each][dic[-1]].append(word)
				for word in sense2word[dic]:
					pass
synonyms1={}
n=0
f=open("COWSynonym.txt",'w')
for each in synonyms:
	if synonyms[each]!={'v':[],'n':[]}:
		n+=1
		synonyms1[each]=synonyms[each]
		f.write(each+":\n")
		for cx in synonyms1[each]:
			if len(synonyms1[each][cx])==0:
				pass
			else:
				f.write(cx+":")
				for word in synonyms1[each][cx]:
					f.write(word+" ")
				f.write("\n")
		f.write("===============================\n")
savePickle(synonyms1,'COWsynonyms')
f.close()
print(n)
