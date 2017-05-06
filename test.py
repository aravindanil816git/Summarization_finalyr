import nltk
import networkx as nx
import numpy as np
import nltk

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer

import math
import re
from operator import itemgetter
from nltk.tokenize.punkt import PunktSentenceTokenizer


tfidf = {}
stopwords = []
sentence_tokenizer=[]
stopword_file = open("stopwords.txt", "r")
stopwords = [line.strip() for line in stopword_file]
idf_default = 1.5
    
document = """To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name. In his eyes she eclipses and predominates the whole of her sex. It was not that he felt any emotion akin to love for Irene Adler
"""
def get_tokens(str):
        return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", str.lower())
    
def get_idf(term,sent_tokenizer):
    count=0  
    if term in stopwords:
        return 0
    setter=set()
    setter.add(term)
    for i in range(len(sentence_tokenizer)):
        tokens_idf = get_tokens(sentence_tokenizer[i])            
        tokens_set_idf = set(tokens_idf)
        if not setter.intersection(tokens_set_idf):
                continue
        count=count+1
        
    return math.log(float(1 + len(sentence_tokenizer)) /
                        (1 + count))


document = ' '.join(document.strip().split('\n'))
sentence_tokenizer =  nltk.sent_tokenize(document)
for i in range(len(sentence_tokenizer)):
    tokens = get_tokens(sentence_tokenizer[i])
    tokens_set = set(tokens)
    for word in tokens_set:
        mytf = float(tokens.count(word)) / len(tokens)
        myidf = get_idf(word,sentence_tokenizer)
        tfidf[word] = mytf * myidf
sci=sorted(tfidf.items(), key=itemgetter(1), reverse=True)
print sci

