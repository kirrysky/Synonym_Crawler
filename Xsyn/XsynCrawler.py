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
        print(resp.history)
        CACHE_DICTION[unique_ident] = str(resp.content,'utf-8')
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#### get wiki data ####
def get_card_data(word):
    basepage_url = 'http://www.fantizi5.com/jinyici/jyc'+str(word)+'.html'
    page_text = make_request_using_cache(basepage_url)  
    print(basepage_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    namediv=page_soup.find('input',id='kw')
    if namediv is not None:
        name=namediv['value']
        print(name)
    jyclist=page_soup.find('li',style='font-size:14px')
    if jyclist is not None:
        jyclist=jyclist.text.split('、')
        print(jyclist)
        return name,jyclist
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



#### Write out file here #####

worddict={}
for i in range(14202):
    result=get_card_data(i)
    if result!=0:
        worddict[result[0]]=result[1]
savePickle(worddict,'Xsyn/worddict')
rawdata=openFile('rawdata')
data=[]
#洗一洗
for each in rawdata:
     if len(each)>1:
          data.append(each)

syns={}
for each in data:
    if each in worddict:
        result=worddict[each]
        syns[each]=result

savePickle(syns,'syns')
print("同义词：",len(syns))


