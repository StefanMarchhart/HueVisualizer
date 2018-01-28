import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import time
import requests
import random

def processWav(wavPeak):
    return str(int(((wavPeak+1000)/10000)*250))

def processFreq(freqPeak):
    return str(int((freqPeak/15000)*65535))

def randColor():
    return str(random.randint(0,65535))

def main():
    np.set_printoptions(suppress=True) # don't use scientific notation
    basePath = r"http://192.168.1.135/api/xREOsUlYetInkIHuxDldgzqJYLZySU6xDIaobRsx/lights"

    CHUNK = 4096 # number of data points to read at a time
    RATE = 44100 # time resolution of the recording device (Hz)

    p=pyaudio.PyAudio() # start the PyAudio class
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True, frames_per_buffer=CHUNK) #uses default input device


    for i in range(10):
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        # print(data)
        wavPeak=np.average(np.abs(data))*2
        # bars="#"*int(200*wavPeak/2**16)
        data = data * np.hanning(len(data)) # smooth the FFT by windowing data
        # print(data,"-Smoothed")
        fft = abs(np.fft.fft(data).real)
        fft = fft[:int(len(fft)/2)] # keep only first half
        print(fft," -fft")

        freq = np.fft.fftfreq(CHUNK,1/RATE)
        freq = freq[:int(len(freq)/2)] # keep only first half
        freqPeak = freq[np.where(fft==np.max(fft))[0][0]]+1
        # print("peak frequency: %05d Hz - Peak Wav: %05d %s" %(freqPeak, wavPeak, bars))
 

    # close the stream gracefully
    stream.stop_stream()
    stream.close()
    p.terminate()




if __name__ == '__main__':
    main()
