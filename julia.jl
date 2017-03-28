using WAV
using PyPlot

y, fs = wavread("sample.wav")
plot(y, ".")
fy = fft(y)
plot(fy)
