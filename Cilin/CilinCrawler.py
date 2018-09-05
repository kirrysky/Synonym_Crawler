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
smalldict8=openFile('Cilin/smalldict-dict-8')
smalldict5=openFile('Cilin/smalldict-dict-5')
smalldict4=openFile('Cilin/smalldict-dict-4')
smalldict2=openFile('Cilin/smalldict-dict-2')
data=[]
#洗一洗
for each in rawdata:
     if each!="":
          data.append(each)

pickedword={}
n=0
for each in data:
     for dic in smalldict8:
          if len(dic.split(" "))==2:
               n+=1
               if each==dic.split(" ")[1]:
                    if each not in pickedword:
                         pickedword[each]={}
                         pickedword[each][dic.split(" ")[0]]=[]
                    else:
                         pickedword[each][dic.split(" ")[0]]=[]
savePickle(pickedword,'Cilin/pickedword')
pickedword=loadPickle('Cilin/pickedword')
for each in pickedword:
     for code in pickedword[each]:
          for dic in smalldict8:
               if len(dic.split(" "))==2:
                    if code in dic and dic.split(" ")[1]:
                         pickedword[each][code].append(dic.split(" ")[1])
savePickle(pickedword,'Cilin/pickedword2')

smalldict=loadPickle('Cilin/smalldict')
smalldict2=loadPickle('Cilin/smalldict2')
smalldict4=loadPickle('Cilin/smalldict4')
smalldict5=loadPickle('Cilin/smalldict5')
pickedword=loadPickle('Cilin/pickedword2')
print(len(pickedword))
f=open("Cilinsynonyms.txt",'w')
n=0
synonyms={}
for each in pickedword:
     add_synonyms=False
     for code in pickedword[each]:
          if code[-1]=="=":
               add_synonyms=True
     if len(each)>1 and add_synonyms:
          n+=1
          f.write(each+":\n")
          synonyms[each]={}
          for dic in pickedword[each]:
               if dic[-1]=='=':
                    synonyms[each][dic]=[]
                    f.write(dic+" ")
                    for word in pickedword[each][dic]:
                         f.write(word+" ")
                         synonyms[each][dic].append(word)
                    f.write("\n")
          f.write("====================\n")
print("所有词:",n)
f.write("total:"+str(n))
savePickle(synonyms,"Cilinsynonyms")
f.close()
