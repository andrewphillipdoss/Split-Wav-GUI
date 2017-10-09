from find_silence import *

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
import subprocess

pad_bank = 0
number_files = len(os.listdir(output_dir))

def play(audio_file_path):
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])

def play_sample(self):
    for btn in xrange(0,16):
        if self.text == str(btn+1):
            #print str(btn+1)
            output_filepath = "{}_{:03d}.wav".format(
                os.path.join(output_dir, output_filename_prefix),
                (pad_bank * 16) + (btn + 1)
            )
            play(output_filepath)
            print(output_filepath)
        else:
            pass

def split_wav(self):
    os.system("python gui.py '/Users/andrewdoss/Desktop/test_rendering/ObamaSpeech.wav' -o '/Users/andrewdoss/Desktop/test_rendering/test' -t 1e-5")

def next_pad_bank(self):
    global pad_bank
    if pad_bank < (number_files / 16):
        pad_bank += 1
    else:
        pad_bank = -1
    print pad_bank

def previous_pad_bank(self):
    global pad_bank
    if pad_bank > 0:
        pad_bank -= 1
    else:
        pad_bank = (number_files / 16) - 1
    print pad_bank

class MyApp(App):
    def build(self):
        return main_layout

main_layout = GridLayout(cols=1,rows=2)
control_layout = GridLayout(cols=3,rows=1)
button_layout = GridLayout(cols=4,rows=5)

pad_buttons = []
for btn in xrange(0,16):
    print btn
    pad_buttons.append(Button(text=str(btn+1)))
    pad_buttons[btn].bind(on_press=play_sample)
    button_layout.add_widget(pad_buttons[btn])

button_split_wav = Button(text="Split Wav at Silences")
button_next_pad_bank = Button(text="Next Pad Bank")
button_previous_pad_bank = Button(text="Previous Pad Bank")
button_split_wav.bind(on_press=split_wav)
button_next_pad_bank.bind(on_press=next_pad_bank)
button_previous_pad_bank.bind(on_press=previous_pad_bank)
control_layout.add_widget(button_split_wav)
control_layout.add_widget(button_previous_pad_bank)
control_layout.add_widget(button_next_pad_bank)

main_layout.add_widget(control_layout)
main_layout.add_widget(button_layout)

if __name__ == '__main__':
    MyApp().run()
