import os
import random

from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp

from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.button import Button

Window.size = (400, 500)

class MusicPlayerApp(MDApp):
    def playAudio(self, instance):
        self.song_title = self.song_list[random.randint(0, self.song_count - 1)]
        self.sound = SoundLoader.load(self.music_dir + '/' + self.song_title)
        self.song_label.text = self.song_title[:-4]
        self.album_image.source = 'assets/img/king_arthur.jpg'
        self.sound.play()

    def stopAudio(self, instance):
        self.sound.stop()

    def pauseAudio(self, instance):
        self.sound.stop()


    def build(self):

        layout = MDRelativeLayout(md_bg_color=(1, 1, 1, 1))

        # Music list from the directory
        self.music_dir = 'F:\zene'
        self.music_files = os.listdir(self.music_dir)
        self.music_file = random.choice(self.music_files)
        print(self.music_files)
        self.song_list = [x for x in self.music_files if x.endswith('.mp3')]
        print(self.song_list)

        self.song_count = len(self.song_list)
        print(self.song_count)

        self.song_label = Label(text='self.music_file', pos_hint={'center_x': 0.5, 'center_y': 0.96},
                                size_hint=(1, 1), font_size=18, color=(0, 0, 0, 1))

        self.album_image = Image(source='assets/img/king_arthur.jpg', pos_hint={'center_x': 0.5, 'center_y': 0.55},
                                    size_hint=(1, 0.70))

        # Labels for the app
        self.play_btn = MDIconButton(icon='assets/img/play.png', pos_hint={'center_x': 0.3, 'center_y': 0.1},
                                     icon_size=75, on_press=self.playAudio)

        self.pause_btn = MDIconButton(icon='assets/img/pause.png', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                     icon_size=75)

        self.stop_btn = MDIconButton(icon='assets/img/stop.png', pos_hint={'center_x': 0.7, 'center_y': 0.1},
                                     icon_size=75, on_press=self.stopAudio)


        # Widgets for the app
        layout.add_widget(self.play_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.pause_btn)
        layout.add_widget(self.song_label)
        layout.add_widget(self.album_image)

        # Clock.schedule_once(self.playAudio)

        return layout

if __name__ == '__main__':
    MusicPlayerApp().run()