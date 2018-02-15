# -*- coding: utf-8 -*-
"""

@author: Alex
"""

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.settings import Settings
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty

from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

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
    q_time = NumericProperty(10)
    font_size = NumericProperty()
    
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self._get_questions()
        
    def _get_questions(self):
        with open('questions.json','r') as f:
            self.questions_list = loads(f.read())
           
    def start_time(self):
        self.q_time = 10
        Clock.schedule_interval(self._minus_one, 1)
        
    def _minus_one(self, dt):
        if self.q_time > 0:
            self.q_time -= 1
        else:
            self.stop_time()
        
    def stop_time(self):
        Clock.unschedule(self._minus_one)
        self._disable_buttons()
    
    def _load_question(self, q):
        self.question = q["question"]
        self.answer1 = q["answer1"]
        self.answer2 = q["answer2"]
        self.answer3 = q["answer3"]
        self.correct = q["correct"]      
        self.start_time()
        
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
        self.stop_time()
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

class AudioManagement():
    def load_audio(self, filename = "sound/back_sound.mp3", loop = True, volume = 0.5):
        self.sound = SoundLoader.load(filename)
        self.sound.loop = loop
        self.sound.volume = volume
        return self.sound
                
class FontManagement():
    def load_font_size(self):
        app = App.get_running_app()
        self.font_size = float(app.config.get('main', 'font_size'))
        app.manager.ids.qs.font_size = self.font_size

class AECRQuizApp(App):
    sound = ObjectProperty(None, allownone = True)
    manager = ObjectProperty(None)

    def build(self):
        with open("aecrquiz.kv", encoding='utf8') as f: 
            self.manager = Builder.load_string(f.read()) 
            
        self.settings_cls = Settings
        self.use_kivy_settings = False
        self.check_audio()
        self.check_font()
        
        return self.manager
        
    def build_config(self, config):
        config.setdefaults("main", {"music": True, "font_size": 15, 
                                    "back_color": "blue", "name": "Username"})
    
    def build_settings(self, settings):
        settings.add_json_panel("Settings", self.config, 'settings.json')
        
    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)
        if key == 'back_color':
            self.check_color(value)            
        elif key == 'music':
            self.check_audio()
        elif key == 'font_size':
            self.check_font(value)
                    
    def check_audio(self):
        if self.config.get('main', 'music') == '1':
            self.sound = AudioManagement().load_audio()
            self.sound.play()
        else:
            if self.sound:
                self.sound.stop()
                self.sound.unload()
                self.sound = None
                
    def check_color(self, color):
        op = {"black": get_color_from_hex("#000000"), 
              "red": get_color_from_hex("#da2d37"), 
              "green": get_color_from_hex("##70b790"), 
              "blue": get_color_from_hex("#1c1c3d"), 
              "white": get_color_from_hex("##f0f8ff")}
        Window.clearcolor = op[color]
        
    def check_font(self, font_size = None):
        if font_size is None:
            FontManagement().load_font_size()
        else:
            if int(font_size) < 31:
                self.manager.ids.qs.font_size = float(font_size)

    
if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex("#1c1c3d")
    AECRQuizApp().run()