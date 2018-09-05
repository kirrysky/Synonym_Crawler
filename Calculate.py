import requests
import json
from bs4 import BeautifulSoup
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

Baiduantonyms=loadPickle('Baiduantonyms')
Baidusynonyms=loadPickle('Baidusynonyms')
Cilinsynonyms=loadPickle('Cilinsynonyms')
COWantonyms=loadPickle('COWantonym')
COWsynonyms=loadPickle('COWsynonyms')
OnlineCilinantonyms=loadPickle('OnlineCilinantonyms')
OnlineCilinsynonyms=loadPickle('OnlineCilinsynonyms')
Handianantonyms=loadPickle('Handianantonyms')
Handiansynonyms=loadPickle('Handiansynonyms')
othersynonyms=loadPickle('syns')
#### Write out file here #####
rawdata=openFile('rawdata')
data=[]
#洗一洗
for each in rawdata:
     if len(each)>1:
          data.append(each)

synword=[]
antword=[]
otherword=[]

for each in data:
    if (each in othersynonyms) or (each in Handiansynonyms) or (each in OnlineCilinsynonyms) or (each in COWsynonyms) or (each in Cilinsynonyms) or (each in Baidusynonyms):
        synword.append(each)
    if (each in Handianantonyms) or (each in OnlineCilinantonyms) or (each in COWantonyms) or (each in Baiduantonyms):
        antword.append(each)

print("百度汉语同义词：",len(Baidusynonyms))
print("百度汉语反义词：",len(Baiduantonyms))
print("汉典同义词：",len(Handiansynonyms))
print("汉典反义词：",len(Handianantonyms))
print("Online词林同义词：",len(OnlineCilinsynonyms))
print("Online词林反义词：",len(OnlineCilinantonyms))
print("COW同义词：",len(COWsynonyms))
print("COW反义词：",len(COWantonyms))
print("cilin同义词：",len(Cilinsynonyms))
print("某同义词词典同义词：",len(othersynonyms))
print("总同义词：",len(synword))
print("总反义词：",len(antword))


