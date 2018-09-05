import requests
import json
from bs4 import BeautifulSoup
import re
import pickle
import jieba

r1 = u'[a-zA-Z0-9’!"#$%&\'()（）*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

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

def get_pattern():
	lines=openFile('rawdata')
	patterns={}
	for line in lines:
		data=line.split()
		word_list=[data[0]]
		# word_list=data[1].split(',')
		patterns[data[0]]=word_list
	print(patterns)
	savePickle(patterns,'patterns')

get_pattern()
Baiduantonyms=loadPickle('Baiduantonyms')
Baidusynonyms=loadPickle('Baidusynonyms')
###########################################################
Cilinsynonyms=loadPickle('Cilinsynonyms')
COWantonyms=loadPickle('COWantonyms')
COWsynonyms=loadPickle('COWsynonyms')
OnlineCilinantonyms=loadPickle('OnlineCilinantonyms')
OnlineCilinsynonyms=loadPickle('OnlineCilinsynonyms')
###########################################################
Handianantonyms=loadPickle('Handianantonyms')
Handiansynonyms=loadPickle('Handiansynonyms')
othersynonyms=loadPickle('syns')
patterns=loadPickle('patterns')
# syns_list=loadPickle('syns_list')

def combine_list(list_a,list_b):
	c=[]
	for a in list_a:
		for b in list_b:
			a=re.sub(r1,'',a)
			b=re.sub(r1,'',b)
			c.append(a.strip()+b.strip())
	return c



def get_syn_list():
	global Baidusynonyms
	global Handiansynonyms
	global othersynonyms
	global Cilinsynonyms
	global COWsynonyms
	global OnlineCilinsynonyms
	######################找出其中pattern###################################
	syns_list={}
	lens=[]
	for p in patterns:
		################找出同义词对######################
		word_list=[]
		words=patterns[p]
		for w in words:
			syns=[w]
			if w in Baidusynonyms:
				syns+=Baidusynonyms[w]
				syns+=['百度汉语']
			if w in Handiansynonyms:
				syns+=Handiansynonyms[w]
				syns+=['汉典']
			if w in othersynonyms:
				syns+=othersynonyms[w]
				syns+=['其他相关词典']
			if w in Cilinsynonyms:
				for c in Cilinsynonyms[w]:
					syns+=Cilinsynonyms[w][c]
					syns+=['词林']
			if w in COWsynonyms:
				for c in COWsynonyms[w]:
					syns+=COWsynonyms[w][c]
					syns+=['COW']
			if w in OnlineCilinsynonyms:
				for c in OnlineCilinsynonyms[w]:
					syns+=OnlineCilinsynonyms[w][c]
					syns+=['Online词林']
			word_list.append(syns)
		##################两两组合########################
		combination=[]
		for i in range(len(word_list)):
			if i==0:
				combination=word_list[0]
			else:
				combination=combine_list(combination,word_list[i])
		syns_list[p]=combination
	# print(syns_list)
	return syns_list
	savePickle(syns_list,'syns_list')

def save_list(filename,word_list):
	###################保存一哈############################
	print('saving now...')
	f=open(filename+'.txt','w',encoding='utf-8')
	lines=[]
	n=0
	for s in word_list:
		n+=1
		for w in word_list[s]:
			line=s.strip()+"\t"+w.strip()+"\n"
			if line not in lines:
				lines.append(line)
		line="################################\n"
		lines.append(line)
		print("Complete"+str((n/len(word_list))*100)+"%!")
	f.writelines(lines)
	f.close()

# get_pattern()
# get_syn_list()
# save_syn_list()

def get_ant_list():
	global Baidusynonyms
	global Baiduantonyms
	global Handiansynonyms
	global Handianantonyms
	global othersynonyms
	global Cilinsynonyms
	global COWsynonyms
	global COWantonym
	global OnlineCilinantonyms
	global OnlineCilinsynonyms
	######################找出其中pattern###################################
	ants_list={}
	lens=[]
	for p in patterns:
		################找出同义词对######################
		word_ant_list=[]
		words=patterns[p]
		for w in words:
			ants=[]
			if w in Baiduantonyms:
				ants+=Baiduantonyms[w]
			if w in Handianantonyms:
				ants+=Handianantonyms[w]
			if w in COWantonyms:
				for c in COWantonyms[w]:
					ants+=COWantonyms[w][c]
			if w in OnlineCilinantonyms:
				for c in OnlineCilinantonyms[w]:
					ants+=OnlineCilinantonyms[w][c]
			word_ant_list.append(ants)
		# print(word_ant_list)
		################找出反义词对######################
		word_syn_list=[]
		words=patterns[p]
		for w in words:
			syns=[w]
			if w in Baidusynonyms:
				syns+=Baidusynonyms[w]
			if w in Handiansynonyms:
				syns+=Handiansynonyms[w]
			if w in othersynonyms:
				syns+=othersynonyms[w]
			if w in Cilinsynonyms:
				for c in Cilinsynonyms[w]:
					syns+=Cilinsynonyms[w][c]
			if w in COWsynonyms:
				for c in COWsynonyms[w]:
					syns+=COWsynonyms[w][c]
			if w in OnlineCilinsynonyms:
				for c in OnlineCilinsynonyms[w]:
					syns+=OnlineCilinsynonyms[w][c]
			word_syn_list.append(syns)
		##################两两组合########################
		combinations=[]
		for i in range(len(word_syn_list)):
			combination=[]
			for j in range(len(word_ant_list)):
				if len(word_ant_list[i])!=0:
					if j==0:
						if i==0:
							combination=word_ant_list[0]
						else:
							combination=word_syn_list[0]
					elif j==i:
						if len(word_ant_list[j])!=0:
							combination=combine_list(combination,word_ant_list[j])
					else:
						combination=combine_list(combination,word_syn_list[j])
			combinations+=combination
		ants_list[p]=combinations
	# print(syns_list)
	savePickle(ants_list,'ants_list')
	return ants_list

ants_list=get_ant_list()
save_list('ants_list',ants_list)
syns_list=get_syn_list()
save_list('syns_list',syns_list)
