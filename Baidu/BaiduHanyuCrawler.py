import requests
import json
from bs4 import BeautifulSoup
import pickle


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
        resp = requests.get(url,allow_redirects=True)
        CACHE_DICTION[unique_ident] = str(resp.content,'utf-8','ignore')
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


antonyms={}
synonyms={}
#### get wiki data ####
def get_syn_ant_data(word):
    global antonyms
    global synonyms
    basepage_url = 'https://hanyu.baidu.com/s?wd='+word+'&device=pc&from=home'
    page_text = make_request_using_cache(basepage_url)
    print(basepage_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    syn_ant=page_soup.find('div',class_='tab-content syn_ant')
    if syn_ant!=None:
        syn=syn_ant.find('div',id='synonym')
        if syn!=None:
            # print(word,"同义词")
            # print(syn.find('div',class_='block').text.split())
            synonyms[word]=syn.find('div',class_='block').text.split()
        ant=syn_ant.find('div',id='antonym')
        if ant!=None:
            # print(word,"反义词")
            # print(ant.find('div',class_='block').text.split())
            antonyms[word]=ant.find('div',class_='block').text.split()

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
data=[]
#洗一洗
for each in rawdata:
     if len(each)>1:
          data.append(each)

all_words={}
for each in data:
    result=get_syn_ant_data(each)
    if result!=0:
        all_words[each]=result

savePickle(all_words,'Baidu/Baidu_all_words')
print("Yeah!Complete!")
print("反义词",len(antonyms))
print("同义词",len(synonyms))
savePickle(antonyms,'Baiduantonyms')
savePickle(synonyms,'Baidusynonyms')



