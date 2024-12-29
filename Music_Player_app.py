import os
import random

from kivy.core.window import Window
from kivymd.app import MDApp

from kivy.core.audio import SoundLoader
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.button import Button

Window.size = (500, 300)

class MusicPlayerApp(MDApp):
    def build(self):

        layout = MDRelativeLayout(md_bg_color=(0, 0, 0, 1))

        return layout

if __name__ == '__main__':
    MusicPlayerApp().run()