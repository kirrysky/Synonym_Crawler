import requests
import json
from bs4 import BeautifulSoup
import pickle
import re


# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}


def openFile(filename):
     originalfile=open(filename+'.txt',encoding='utf-8')
     originitems=[]
     for line in originalfile.readlines():
          originitems.append(line[:-1])
     originalfile.close()
     return originitems

def make_request_using_cache(url):
    unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = str(resp.content,'utf-8')
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#### get wiki data ####
def get_card_data(word):
    basepage_url = 'http://www.cilin.org/jyc/w_'+word+'.html'
    page_text = make_request_using_cache(basepage_url)
    print(basepage_url)
    #print(basepage_url+str(i)+'&offset='+str((i-1)*30)+'#gotoList')
    page_soup = BeautifulSoup(page_text, 'html.parser')
    page_div=page_soup.find('div',class_='col-md-8')
    word_dict={}
    if page_div:
        words=page_div.find_all('p',class_='aboutwords')
        n=0
        for word in words:
            n+=1
            word_dict[n]={}
            word=str(word)
            jyc=re.search(r"<b>近义词</b><br/>汉语:.+",word)
            if jyc:
                    jyc=jyc.group(0)
                    jyc=jyc.split('<br/>')[1]
                    jycs=BeautifulSoup(jyc, 'html.parser').text[3:].split(',')
                    word_dict[n]['近义词']=jycs
            fyc=re.search(r"<b>反义词</b><br/>汉语:.+",word)
            if fyc:
                    fyc=fyc.group(0)
                    fyc=fyc.split('<br/>')[1]
                    fycs=BeautifulSoup(fyc, 'html.parser').text[3:].split(',')
                    word_dict[n]['反义词']=fycs
            return word_dict
    else:
        return 0

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



# #### Write out file here #####
rawdata=openFile('rawdata')
data=[]
#洗一洗
for each in rawdata:
     if len(each)>1:
          data.append(each)

all_words={}
for each in data:
    result=get_card_data(each)
    if result!=0:
        all_words[each]=result

savePickle(all_words,'OnlineCilin/all_words')
print("Yeah!Complete!")

all_words=loadPickle('OnlineCilin/all_words')
antonyms={}
for each in all_words:
    if len(all_words[each])>0:
        for sense in all_words[each]:
            if '反义词' in all_words[each][sense]:
                if each not in antonyms:
                    antonyms[each]={}
                    if sense not in antonyms[each]:
                        antonyms[each][sense]=all_words[each][sense]['反义词']
savePickle(antonyms,'OnlineCilinantonyms')
print("反义词：",len(antonyms))
synonyms={}
for each in all_words:
    if len(all_words[each])>0:
        for sense in all_words[each]:
            if '近义词' in all_words[each][sense]:
                if each not in synonyms:
                    synonyms[each]={}
                    if sense not in synonyms[each]:
                        synonyms[each][sense]=all_words[each][sense]['近义词']
savePickle(synonyms,'OnlineCilinsynonyms')
print("近义词：",len(synonyms))




f=open('OnlineCilinSyn.txt','w')
f.write("一共有"+str(len(synonyms))+"个同义词!\n")
f.write("--------------------------------------\n")
for each in synonyms:
	f.write(each+"\n")
	n=0
	for a in synonyms[each]:
		if len(synonyms[each][a])!=0:
			f.write(str(a)+":")
			for word in synonyms[each][a]:
				f.write(word+" ")
			f.write("\n")
	f.write("========================\n")
f.close()
f=open('OnlineCilinAnts.txt','w')
f.write("一共有"+str(len(antonyms))+"个反义词!\n")
f.write("--------------------------------------\n")
for each in antonyms:
	f.write(each+"\n")
	n=0
	for a in antonyms[each]:
		if len(antonyms[each][a])!=0:
			f.write(str(a)+":")
			for word in antonyms[each][a]:
				f.write(word+" ")
			f.write("\n")
	f.write("========================\n")
f.close()
