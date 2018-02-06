# Split-Wav-GUI

A just-for-fun sampler that can choose and split a wav file by silences. 

Usage Instructions:

Clone the repo, and install the dependencies from 'requirements.txt'

In terminal, run 'start.py'

A GUI should pop up.

You can use the file chooser to select a .wav file. The software only supports .wav
To select a file, double click it in the file chooser. 
The file path will be printed to the console if it is properly selected.

You can adjust the sensitivity of the .wav spliter with the slider.

Then, to split the file by its silences, click the 'Split Wav at Silences' button.
The console will print 'SPLITTING WAV' when it begins and 'WAV SPLIT' when it finishes.
Make sure to select a file before you click this button, or the software will crash.

Once the wav is split, the parts audio in between silences will be distributed across the soundboard.
You can click on any of the buttons of the soundboard, and they should each play a clip of the audio.
If there are more than 16 clips, you can move to the next pad bank with the 'Next Pad Bank' button.
Move backwards with 'Previous Pad Bank'




