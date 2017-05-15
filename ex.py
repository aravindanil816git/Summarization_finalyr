#!/usr/bin/kivy
import kivy
import codecs
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.factory import Factory
from Tkinter import Tk
from tkFileDialog import askopenfilename

import networkx as nx
import numpy as np
import subprocess

from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer


from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer 

Window.size = (800,500)

Builder.load_file('myui.ky')


class Myui(TabbedPanel):
    finaltxt = StringProperty(str(""))

    def upload(self):
        Tk().withdraw()
        filename = askopenfilename()
        subprocess.call(['pdftotext', filename, 'pdf2text.txt'])
        self.summarize('pdf2text.txt')

    def step(self,a):
        f=codecs.open("my_file.txt",mode='w+',encoding='utf-8')
        f.write(a)
        f.close()
        self.summarize('my_file.txt')

    def summarize(self,txtfile):
        self.textrank(txtfile)
        with open("summari.txt") as f:
            content=f.read()
            self.finaltxt = str(content)

    def textrank(self,fname):
        f=open(fname,"r")
        document=f.read()
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.tokenize(document)
    
        bow_matrix = CountVectorizer().fit_transform(sentences)
        normalized = TfidfTransformer().fit_transform(bow_matrix)
    
        similarity_graph = normalized * normalized.T
    
        nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
        scores = nx.pagerank(nx_graph)
        summary =  sorted(((scores[i],s) for i,s in enumerate(sentences)),reverse=True)
        f=open("summari.txt","w+")
        for i in range(5) :
            sentence=summary[i][1]
            f.write(str(sentence)+'\n \n')
        f.close()

"""def summer(self,fname):
        parser = PlaintextParser.from_file(fname, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences
        f=open("summari.txt","w+")
        for sentence in summary:
            f.write(str(sentence)+'\n \n')
        f.close() """




# Create the screen manager
#sm = ScreenManager()
"""sm.add_widget(Myui(name='Myui'))"""

class TestApp(App):

    def build(self):
        return Myui()

if __name__ == '__main__':
    TestApp().run()


