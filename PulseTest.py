import pyaudio
import numpy as np
import datetime
import time, random, requests

def randColor():
    return str(random.randint(0,65535))


def pulseAll():
    print("PULSE")
    for light in lightArray:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"on":true, "transition_time":1, "bri":'+str(brightness)+',"sat":254,"hue":'+randColor()+' }'
        requests.put(path,data=dataString)
        # time.sleep(1)
    time.sleep(.15)
    for light in lightArray:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"transition_time":1, "bri":'+str(brightness-100)+',"sat":254}'
        requests.put(path,data=dataString)


peakdelta=3000
brightness=150

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
lastTriggered = datetime.datetime.now()
time.sleep(.5)
while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    currentTrigger = datetime.datetime.now()
        
    if (oldpeak+peakdelta ) < peak or (oldoldpeak+peakdelta ) < peak:
        if ((currentTrigger - lastTriggered) > datetime.timedelta(seconds=.5)):
            lastTriggered=currentTrigger
            pulseAll()
        else:
            print("Chill")

    bars="#"*int(200*peak/2**16)
    print(" %05d %s"%(peak,bars))
    


    oldoldpeak=oldpeak
    oldpeak=peak
    

stream.stop_stream()
stream.close()
p.terminate()