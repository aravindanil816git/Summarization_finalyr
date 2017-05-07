import nltk
import networkx as nx
import numpy as np
import nltk

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer

import numpy
import math
import re
from operator import itemgetter
from nltk.tokenize.punkt import PunktSentenceTokenizer
from orderedset import OrderedSet

tfidf = {}
mytf={}
myidf={}
stopwords = []
sentence_tokenizer=[]
stopword_file = open("stopwords.txt", "r")
stopwords = [line.strip() for line in stopword_file]
idf_default = 1.5
    
document = """To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any 
other name. In his eyes she eclipses and predominates the whole of her sex. 
It was not that he felt any emotion akin to love for Irene Adler
"""
def get_tokens(str):
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())
    
def get_idf(term,sent_tokenizer):
    count=0  
    setter=set()
#    if term in stopwords:
#        return 0
    setter.add(term)
    for i in range(len(sentence_tokenizer)):
        tokens_idf = get_tokens(sentence_tokenizer[i])            
        tokens_set_idf = set(tokens_idf)
        if setter.intersection(tokens_set_idf):
            count=count+1
        
    return math.log(float((1 + len(sentence_tokenizer)) )/ (1 + count))

def normalised_tfid(mytf,myidf,max_tfid):
    for key,values in mytf.items():
        normalized=0.4+0.6*(values/max_tfid)
        mytf[key]=normalized
        tfidf[key]=(myidf[key]*mytf[key])


document = ' '.join(document.strip().split('\n'))
sentence_tokenizer =  nltk.sent_tokenize(document)
for i in range(len(sentence_tokenizer)):
    tokens = get_tokens(sentence_tokenizer[i])
    tokens_set = set(tokens)
    for word in tokens_set:
        mytf[word] = float(tokens.count(word)) / len(tokens)
        myidf[word] = get_idf(word,sentence_tokenizer)        
 #       tfidf[word] = mytf * myidf
normalised_tfid(mytf,myidf,max(mytf.values()))
"""for key,values in tfidf.items():
        normalized=0.4+0.6*(values/max(tfidf.values()))
        tfidf[key]=normalized/40 """

sci=tfidf.items()
out=list()
word_list=set(get_tokens(document))


for i in range(len(sentence_tokenizer)):
    tokens = get_tokens(sentence_tokenizer[i])
    tokens_set = set(tokens)
    new=list()
    for word in word_list:
        if word in tokens_set:
            new.append(tfidf[word])
        else:
            new.append(0)
    out.append(new)

matrix = numpy.matrix(out)
matrix=matrix*matrix.T
print matrix,tfidf
