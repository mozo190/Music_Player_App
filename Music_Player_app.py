import os
import random

from kivy.core.window import Window
from kivymd.app import MDApp

from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.button import Button

Window.size = (500, 300)

class MusicPlayerApp(MDApp):

    def build(self):

        layout = MDRelativeLayout(md_bg_color=(1, 1, 1, 1))

        self.music_dir = 'F:\zene'
        self.music_files = os.listdir(self.music_dir)
        self.music_file = random.choice(self.music_files)

        # Labels for the app
        self.play_btn = MDIconButton(icon='assets/img/play.png', pos_hint={'center_x': 0.4, 'center_y': 0.2},
                                     icon_size=75)

        self.stop_btn = MDIconButton(icon='assets/img/stop.png', pos_hint={'center_x': 0.7, 'center_y': 0.2},
                                     icon_size=75)

        self.pause_btn = MDIconButton(icon='assets/img/pause.png', pos_hint={'center_x': 0.55, 'center_y': 0.2},
                                     icon_size=75)

        # Widgets for the app
        layout.add_widget(self.play_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.pause_btn)

        return layout

if __name__ == '__main__':
    MusicPlayerApp().run()