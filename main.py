# -*- coding: utf-8 -*-
"""

@author: Alex
"""

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.graphics import Color
from kivy.uix.settings import Settings
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty, NumericProperty

from json import dumps, loads
#from random import choice

kivy.require('1.4.0')
Config.set('kivy','window_icon','images/logo.ico')

class MenuScreen(Screen):
    pass

class QuizScreen(Screen):
    question = StringProperty()
    answer1, answer2, answer3 = StringProperty(), StringProperty(), StringProperty()
    color1, color2, color3 = ListProperty([1, 1, 1, 1]), ListProperty([1, 1, 1, 1]), ListProperty([1, 1, 1, 1])
    questions_list = ListProperty([])
    n, success = NumericProperty(), NumericProperty()
    
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self._get_questions()
        self.start_quiz()
        
    def _get_questions(self):
        with open('questions.json','r') as f:
            self.questions_list = loads(f.read())
            
    def _load_question(self, q):
        self.question = q["question"]
        self.answer1 = q["answer1"]
        self.answer2 = q["answer2"]
        self.answer3 = q["answer3"]
        self.correct = q["correct"]      
        
    def _clean_buttons(self):
        self.color1[:2] = [1, 1]
        self.color2[:2] = [1, 1]
        self.color3[:2] = [1, 1]
        
    def _enable_buttons(self):
        self.ids.first.disabled = False
        self.ids.second.disabled = False
        self.ids.third.disabled = False
        
    def _disable_buttons(self):
        self.ids.first.disabled = True
        self.ids.second.disabled = True
        self.ids.third.disabled = True
        
    def start_quiz(self):
        self.n = 0
        self._load_question(self.questions_list[self.n])
    
    def next_question(self):
        self.n += 1
        self._clean_buttons()
        self._enable_buttons()
        self._load_question(self.questions_list[self.n])
        if self.n >= len(self.questions_list) - 1:
            self.ids.next.disabled = True
        
    def check_result(self, n):
        answers = [self.answer1, self.answer2, self.answer3]
        colors = [self.color1, self.color2, self.color3]
        self._disable_buttons()
        if answers[n-1] == self.correct:
            colors[n-1][1] = 255
            self.success += 1
        else:
            colors[n-1][0] = 255
        
            
class EndScreen(Screen):
    points = NumericProperty()
    question_number = NumericProperty()
    message = StringProperty()

    def set_score(self, **kwargs):
        self.points = kwargs["points"]
        self.question_number = kwargs["n"] + 1
        self.message = "Resultado: {0}/{1}".format(self.points, self.question_number)

class ScreenManagement(ScreenManager):
    pass


class AECRQuizApp(App):

    def build(self):
        self.settings_cls = Settings
        with open("aecrquiz.kv", encoding='utf8') as f: 
            return Builder.load_string(f.read()) 
        
    def build_config(self, config):
        config.setdefaults("main", {"music": False, "font_size": 12, 
                                    "back_color": "black", "name": "Username"})
    
    def build_settings(self, settings):
        settings.add_json_panel("Settings", self.config, 'settings.json')
        
    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)
        if key == 'color':
            {"black": Color(1,1,1,1), "red": Color(1,0,0,1), "green": Color(0,1,0,1), "blue": Color(0,0,1,1), "white": Color(0,0,0,1)}
    
if __name__ == '__main__':
    AECRQuizApp().run()