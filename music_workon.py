#!/usr/bin/python

import stft
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

fs, audio = wav.read('sample.wav')
specgram = stft.spectrogram(audio)
plt.specgram(audio[0], Fs=fs)
plt.show()
#output = stft.ispectrogram(specgram)
#wav.write('output.wav', fs, output)
