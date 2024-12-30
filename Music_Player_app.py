import os
import random
import time

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout

Window.size = (400, 500)


class MusicPlayerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volume_Slider = None
        self.total_time_label = None
        self.current_time_label = None
        self.stop_btn = None
        self.pause_btn = None
        self.play_btn = None
        self.progress_bar = None
        self.album_image = None
        self.song_label = None
        self.song_list = None
        self.music_dir = None
        self.timeEvent = None
        self.progressbar_position = None
        self.progressbar_event = None
        self.song_title = None
        self.sound = None
        self.paused_pos = 0
        self.is_paused = False  # Check if the audio is paused

    def playAudio(self, instance=None):
        if self.is_paused and self.sound:
            self.sound.seek(self.paused_pos)
            self.sound.play()
            self.is_paused = False

            # Continue the progress bar event
            self.progressbar_event = Clock.schedule_interval(self.updateProgressBar, 0.1)
            self.timeEvent = Clock.schedule_interval(self.setTimeLabels, 1)

        else:
            # If the audio is not paused, play the audio
            if self.sound:
                self.sound.stop()

            self.song_title = random.choice(self.song_list)
            file_path = os.path.join(self.music_dir, self.song_title)
            self.sound = SoundLoader.load(file_path)

            if self.sound:
                if not self.sound.length:
                    self.sound.length = 1 # Set the length to 1 if the length is None

                self.song_label.text = self.song_title[:-4]
                self.album_image.source = 'assets/img/king_arthur.jpg'
                self.progress_bar.value = 0

                self.progressbar_event = Clock.schedule_interval(self.updateProgressBar, 0.1)
                self.timeEvent = Clock.schedule_interval(self.setTimeLabels, 1)

                self.sound.volume = self.volume_Slider.value / 100
                self.sound.play()
            else:
                self.song_label.text = 'Error: File not found'

        self.play_btn.disabled = True
        self.pause_btn.disabled = False
        self.stop_btn.disabled = False

    def stopAudio(self, instance):
        if self.sound:
            self.sound.stop()  # Stop the audio
            self.timeEvent.cancel()

            self.sound.unload()  # Unload the audio
            self.progress_bar.value = 0
            self.current_time_label.text = '00:00'
            self.total_time_label.text = '00:00'
            if self.progressbar_event:  # Stop the progress bar event
                self.progressbar_event.cancel()

        self.is_paused = False
        self.paused_pos = 0
        self.play_btn.disabled = False
        self.pause_btn.disabled = True
        self.stop_btn.disabled = True

    def pauseAudio(self, instance):
        if self.sound and self.sound.state == 'play':
            self.paused_pos = self.sound.get_pos()  # Save the paused position
            if self.progressbar_event:  # Stop the progress bar event
                self.progressbar_event.cancel()
            self.sound.stop()  # Stop the audio
            self.is_paused = True
            self.pause_btn.disabled = True  # Disable the pause button
            self.play_btn.disabled = False

    def updateProgressBar(self, dt):
        if self.sound and self.sound.state == 'play':
            current_pos = self.sound.get_pos()
            if current_pos is not None and self.sound.length:
                self.progress_bar.value = (current_pos / self.sound.length) * 100
            elif current_pos is None:
                self.progress_bar.value = 100  # Set the progress bar value to 100 when the audio is finished
                self.progressbar_event.cancel()

    def setTimeLabels(self, instance):
        if self.sound and self.sound.state == 'play':
            current_time = self.sound.get_pos()
            if current_time is not None and self.sound.length:
                self.current_time_label.text = time.strftime('%M:%S', time.gmtime(current_time))
                self.total_time_label.text = time.strftime('%M:%S', time.gmtime(self.sound.length))
            else:
                self.current_time_label.text = '00:00'
                self.total_time_label.text = '00:00'

    def on_volume(self, instance, value):
        if self.sound:
            self.sound.volume = value / 100

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

        self.progress_bar = ProgressBar(max=100, value=0, pos_hint={'center_x': 0.5, 'center_y': 0.17},
                                        size_hint=(0.8, 0.75))

        # Buttons for the app
        self.play_btn = MDIconButton(icon='assets/img/play.png', pos_hint={'center_x': 0.3, 'center_y': 0.1},
                                     icon_size=75, on_press=self.playAudio)

        self.pause_btn = MDIconButton(icon='assets/img/pause.png', pos_hint={'center_x': 0.5, 'center_y': 0.1},
                                      icon_size=75, on_press=self.pauseAudio)

        self.stop_btn = MDIconButton(icon='assets/img/stop.png', pos_hint={'center_x': 0.7, 'center_y': 0.1},
                                     icon_size=75, on_press=self.stopAudio, disabled=True)

        self.current_time_label = Label(text='00:00', pos_hint={'center_x': 0.1, 'center_y': 0.1},
                                        size_hint=(1, 1), font_size=18, color=(0, 0, 0, 1))

        self.total_time_label = Label(text='00:00', pos_hint={'center_x': 0.9, 'center_y': 0.1},
                                      size_hint=(1, 1), font_size=18, color=(0, 0, 0, 1))

        self.volume_Slider = Slider(orientation='vertical', min=0, max=100, value=30, step=1, size_hint=(0.05, 0.5),
                                    pos_hint={'center_x': 0.95, 'center_y': 0.5})
        self.volume_Slider.bind(value=self.on_volume)

        # Widgets for the app
        layout.add_widget(self.play_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.pause_btn)
        layout.add_widget(self.song_label)
        layout.add_widget(self.album_image)
        layout.add_widget(self.progress_bar)
        layout.add_widget(self.current_time_label)
        layout.add_widget(self.total_time_label)
        layout.add_widget(self.volume_Slider)

        Clock.schedule_once(self.playAudio)

        return layout


if __name__ == '__main__':
    MusicPlayerApp().run()
