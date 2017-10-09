from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from find_silence import *
from settings import *
import subprocess

def load_from_filechooser(self, filechooser, touch=None):
    global input_filename
    submitted_file = str(self.selection)
    input_filename = submitted_file[3:len(submitted_file)-2]
    print input_filename

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
    global pad_bank
    global number_files
    pad_bank = 0
    print "SPLITTING WAV"
    find_silence(silence_threshold, input_filename)
    number_files = len(os.listdir(output_dir))
    print "WAV SPLIT"

def next_pad_bank(self):
    global pad_bank
    if pad_bank < (number_files / 16):
        pad_bank += 1
    else:
        pad_bank = 0
    print pad_bank

def previous_pad_bank(self):
    global pad_bank
    if pad_bank > 0:
        pad_bank -= 1
    else:
        pad_bank = (number_files / 16)
    print pad_bank

def move_slider(instance,value):
    print file_chooser.path
    label_silence_threshold.text = str(value)

class MyApp(App):
    def build(self):
        return main_layout

main_layout = GridLayout(cols=2,rows=1)
sampler_layout = GridLayout(rows=3)
control_layout = GridLayout(cols=3,rows=2)
slider_layout = GridLayout(cols=1,rows=3)
button_layout = GridLayout(cols=4,rows=5)

pad_buttons = []
for btn in xrange(0,16):
    print btn
    pad_buttons.append(Button(text=str(btn+1)))
    pad_buttons[btn].bind(on_press=play_sample)
    button_layout.add_widget(pad_buttons[btn])

file_chooser = FileChooserListView(filers="*.wav")
slider_silence_threshold = Slider(value_track=True, min=1e-6, max=1e-4, value=1e-5)
label_silence_threshold = Label()
silence_threshold = slider_silence_threshold.value
button_split_wav = Button(text="Split Wav at Silences")
button_next_pad_bank = Button(text="Next Pad Bank")
button_previous_pad_bank = Button(text="Previous Pad Bank")
file_chooser.bind(on_submit=load_from_filechooser)
button_split_wav.bind(on_press=split_wav)
button_next_pad_bank.bind(on_press=next_pad_bank)
button_previous_pad_bank.bind(on_press=previous_pad_bank)
slider_silence_threshold.bind(value=move_slider)
control_layout.add_widget(button_split_wav)
control_layout.add_widget(button_previous_pad_bank)
control_layout.add_widget(button_next_pad_bank)

slider_layout.add_widget(slider_silence_threshold)
slider_layout.add_widget(label_silence_threshold)

main_layout.add_widget(file_chooser)
main_layout.add_widget(sampler_layout)
sampler_layout.add_widget(control_layout)
sampler_layout.add_widget(slider_layout)
sampler_layout.add_widget(button_layout)
