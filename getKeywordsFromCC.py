# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 13:49:29 2016

@author: bambangs
"""
#!/bin/python

#import requests
import urllib2
from bs4 import BeautifulSoup
#from FrequencySummarizer import FrequencySummarizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest


import argparse
parser = argparse.ArgumentParser(description='video id and most frequent words')
parser.add_argument("--vid", help="video ID", default="zZiM-8TTkmM")
parser.add_argument("--max_results", help="Max results", default=25)
args = parser.parse_args()

#print args
vid = args.vid
max_results = int(args.max_results)

base_url="http://video.google.com/timedtext?lang=en&v="
#vid="zZiM-8TTkmM"
#vid="m1_iriasROc"

url=base_url+vid
try:
    page = urllib2.urlopen(url).read().decode('utf8')
except:
    # if unable to download the URL, return title = None, article = None
    page = None
    
soup = BeautifulSoup(page,"lxml")

token="transcript"
caption = ""
if soup.find_all(token) is not None:
    # Search the page for whatever token demarcates the transcript
    # usually '<transcript></transcript>'
    caption = ''.join(map(lambda p: p.text, soup.find_all(token)))
    # mush together all the text in the <transcript></transcript> tags
    soup2 = BeautifulSoup(caption,"lxml")
    # create a soup of the text within the <transcript> tags
    if soup2.find_all('text')!=[]:
        # now mush together the contents of what is in <text> </text> tags
        # within the <transcript>
        caption = ''.join(map(lambda p: p.text, soup2.find_all('text')))

        # create a soup of the text within the <text> tags
        soup3 = BeautifulSoup(caption,"lxml")    
        if soup3.find_all('i')!=[]:
            # now mush together the contents of what is in <i> </i> tags
            # within the <text>
            caption = ''.join(map(lambda p: p.text, soup3.find_all('i'))) 
            
# somehow these single quote was encoded in unicode
#caption=caption.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\n"," ")
caption=caption.replace(u"\u2018", "'").replace(u"\u2019", "'")            
            
# use a stemmer to remove the different from of verbs
from nltk.stem.lancaster import LancasterStemmer
st=LancasterStemmer()
caption=st.stem(caption)

## now create a set of customStopWords
customStopWords=set(stopwords.words("english")+list(punctuation))

# i still don't know how to remove these
customStopWords.update(['we', 'us','you','he','she','can','will','may','would','wow'])


sentences = sent_tokenize(caption)
# split the text into sentences
word_sent = [word_tokenize(s.lower()) for s in sentences]

freq = defaultdict(int)
max_cut = 0.95
min_cut = 0.1
for sentence in word_sent:
    for word in sentence:
        if len(word) > 1: # you don't want to get a single word
            if word not in customStopWords:
                freq[word] += 1

m = float(max(freq.values()))
for word in freq.keys():
    freq[word] = freq[word]/m
    if freq[word] >= max_cut or freq[word] <= min_cut:
        del freq[word]
        
print nlargest(max_results,freq)        