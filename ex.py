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


from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer 

Window.size = (800,500)

Builder.load_file('myui.ky')


class Myui(TabbedPanel):
    finaltxt = StringProperty(str(""))

    def step(self,a):
        f=codecs.open("C:\Users\ARAVIND ANIL\Desktop\my_file.txt",mode='w+',encoding='utf-8')
        f.write(a)
        f.close()
        self.summer("C:\Users\ARAVIND ANIL\Desktop\my_file.txt")
        with open("summari.txt") as f:
            content=f.read()
            self.finaltxt = str(content)

    def summer(self,fname):
        parser = PlaintextParser.from_file(fname, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences
        f=open("C:\Users\ARAVIND ANIL\Desktop\summari.txt","w+")
        for sentence in summary:
            f.write(str(sentence)+'\n \n')
        f.close()

# Create the screen manager
#sm = ScreenManager()
"""sm.add_widget(Myui(name='Myui'))"""

class TestApp(App):

    def build(self):
        return Myui()

if __name__ == '__main__':
    TestApp().run()