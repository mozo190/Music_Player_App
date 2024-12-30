import os
import random

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (400, 500)


class MusicPlayerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = None

    def playAudio(self, instance=None):
        if self.sound:
            self.sound.stop()  # Stop the current audio

        self.play_btn.disabled = True
        self.stop_btn.disabled = False

        self.song_title = random.choice(self.song_list)
        self.sound = SoundLoader.load(os.path.join(self.music_dir, self.song_title))

        if self.sound:
            self.song_label.text = self.song_title[:-4]
            self.album_image.source = 'assets/img/king_arthur.jpg'
            self.sound.play()
        else:
            self.song_label.text = 'Error: File not found'

    def stopAudio(self, instance):
        if self.sound:
            self.sound.stop()  # Stop the audio
        self.play_btn.disabled = False
        self.stop_btn.disabled = True

    def pauseAudio(self, instance):
        if self.sound:
            self.sound.seek(self.sound.get_pos())  # Pause the audio

    def build(self):
        layout = MDRelativeLayout(md_bg_color=(1, 1, 1, 1))

        # Music list from the directory
        self.music_dir = 'F:\zene'

        self.song_list = [x for x in os.listdir(self.music_dir) if x.endswith('.mp3')]

        if not self.song_list:
            raise ValueError('No music files found in the directory')

        self.song_label = Label(text='=== Playing music ===', pos_hint={'center_x': 0.5, 'center_y': 0.96},
                                size_hint=(1, 1), font_size=18, color=(0, 0, 0, 1))

        self.album_image = Image(source='assets/img/king_arthur.jpg', pos_hint={'center_x': 0.5, 'center_y': 0.55},
                                 size_hint=(1, 0.70))

        # Labels for the app
        self.play_btn = MDIconButton(icon='assets/img/play.png', pos_hint={'center_x': 0.3, 'center_y': 0.1},
                                     icon_size=75, on_press=self.playAudio)

        self.pause_btn = MDIconButton(icon='assets/img/pause.png', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                      icon_size=75, on_press=self.pauseAudio)

        self.stop_btn = MDIconButton(icon='assets/img/stop.png', pos_hint={'center_x': 0.7, 'center_y': 0.1},
                                     icon_size=75, on_press=self.stopAudio, disabled=True)

        # Widgets for the app
        layout.add_widget(self.play_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.pause_btn)
        layout.add_widget(self.song_label)
        layout.add_widget(self.album_image)

        Clock.schedule_once(self.playAudio)

        return layout


if __name__ == '__main__':
    MusicPlayerApp().run()
