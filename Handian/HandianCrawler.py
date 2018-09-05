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
        CACHE_DICTION[unique_ident] = str(resp.content,'utf-8')
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#### get wiki data ####
antonyms={}
synonyms={}
def get_card_data(word):
    global antonyms
    global synonyms
    basepage_url = 'http://www.zdic.net/search/?q='+word
    print(basepage_url)
    page_text = make_request_using_cache(basepage_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    infobox=page_soup.find('div',class_='notice')
    if infobox!=None:
        tyc_fyc=infobox.find_all('span',class_='dicty')
        if len(tyc_fyc)!=0:
            for each in tyc_fyc:
                imgsrc=each.find('img')['src']
                if 'tyc' in imgsrc:
                    print(word,'同义词：')
                    print(each.text.split())
                    synonyms[word]=each.text.split()
                else:
                    print(word,'反义词：')
                    print(each.text.split())
                    antonyms[word]=each.text.split()

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

print("反义词",len(antonyms))
print("同义词",len(synonyms))
savePickle(antonyms,'Handianantonyms')
savePickle(synonyms,'Handiansynonyms')
# print("Yeah!Complete!")



