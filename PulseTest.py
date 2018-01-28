import pyaudio
import numpy as np
from datetime import datetime as dt
import time, random, requests

rateLimiting=False

def randColor():
    return str(random.randint(0,65535))


def pulseAll():
    rateLimiting=True
    print("PULSE")
    for light in lightArray:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"on":true, "transition_time":1, "bri":'+brightness+',"sat":254,"hue":'+randColor()+' }'
        requests.put(path,data=dataString)
        # time.sleep(1)
    time.sleep(.15)
    for light in lightArray:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"on":false, "transition_time":1, "bri":'+brightness+',"sat":254}'
        requests.put(path,data=dataString)
    rateLimiting=False


peakdelta=3000
brightness="100"

CHUNK = 2**11
RATE = 44100

basePath = r"http://192.168.1.135/api/xREOsUlYetInkIHuxDldgzqJYLZySU6xDIaobRsx/"
lightArray=[6,1,3,2,4]

p=pyaudio.PyAudio()
stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
              frames_per_buffer=CHUNK)

oldoldpeak=0
oldpeak=0
peak=0
while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    if (oldpeak+peakdelta ) < peak or (oldoldpeak+peakdelta ) < peak:
        if not rateLimiting:
            pulseAll()
        else:
            print("RATELIMITED")
    
    bars="#"*int(200*peak/2**16)
    print(" %05d %s"%(peak,bars))
    oldoldpeak=oldpeak
    oldpeak=peak
    

stream.stop_stream()
stream.close()
p.terminate()