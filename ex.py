#!/usr/bin/kivy
import kivy
kivy.require('1.7.2')

from random import random
from random import choice
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in

Window.size = (1000,768)

r1c2=random()
Builder.load_string("""
<Highest>:
    BoxLayout:
        cols: 3
        canvas:
            Color:
                rgb: (0.93, 0.93, 0.93)

        TextInput:
            id: lt0
            hint_text: 'Enter Text to be summarized'
            foreground_color: (0.059, 1, 1,1)
            background_color: (0.22, 0.204, 0.298,1)

        Button:
            text: 'Summarize'
            height: 15
            on_press: root.step(lt0.text)
        
        Label:
            text: root.r1c2
            text_size: self.size
            halign: 'left'
            valign: 'top'

""")

class Highest(Screen):
    r1c2 = StringProperty(str(2))

    def step(self,a):
        f=open("C:\Users\ARAVIND ANIL\Desktop\my_file.txt","w+")
        f.write(a)
        f.close()
        self.summer("C:\Users\ARAVIND ANIL\Desktop\my_file.txt")
        with open("summari.txt") as f:
            content=f.read()
            self.r1c2 = str(content)

    def summer(self,fname):
        parser = PlaintextParser.from_file(fname, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences
        f=open("C:\Users\ARAVIND ANIL\Desktop\summari.txt","w+")
        for sentence in summary:
            f.write(str(sentence))
        f.close()

# Create the screen manager
sm = ScreenManager()
sm.add_widget(Highest(name='Highest'))

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()