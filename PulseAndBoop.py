import pyaudio
import numpy as np
import datetime
import time, random, requests

def randColor():
    return str(random.randint(0,65535))


def pulseAll():
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

def pulseEnds():
    
    path = basePath+"lights/"+str(lightArray[0])+"/state"
    dataString = '{"on":true, "transition_time":1, "bri":'+str(brightness)+',"sat":254,"hue":'+randColor()+' }'
    requests.put(path,data=dataString)
    # time.sleep(1)
    time.sleep(.15)
    path = basePath+"lights/"+str(lightArray[0])+"/state"
    dataString = '{"transition_time":1, "bri":'+str(low_bright)+',"sat":254}'
    requests.put(path,data=dataString)

    path = basePath+"lights/"+str(lightArray[-1])+"/state"
    dataString = '{"on":true, "transition_time":1, "bri":'+str(brightness)+',"sat":254,"hue":'+randColor()+' }'
    requests.put(path,data=dataString)
    # time.sleep(1)
    time.sleep(.15)
    path = basePath+"lights/"+str(lightArray[-1])+"/state"
    dataString = '{"transition_time":1, "bri":'+str(low_bright)+',"sat":254}'
    requests.put(path,data=dataString)



def pulseRandom(num=1):
    lights=[]
    for i in range(0,num+1):
        lights.append(lightArray[random.randint(0,len(lightArray)-1)])

    for light in lights:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"on":true, "transition_time":1, "bri":'+str(brightness)+',"sat":254,"hue":'+randColor()+' }'
        requests.put(path,data=dataString)
    
    time.sleep(.15)
    for light in lights:
        path = basePath+"lights/"+str(light)+"/state"
        dataString = '{"transition_time":1, "bri":'+str(low_bright)+',"sat":254}'
        requests.put(path,data=dataString)


def pulseOne():
    light=lightArray[random.randint(0,len(lightArray)-1)]
    path = basePath+"lights/"+str(light)+"/state"
    dataString = '{"on":true, "transition_time":1, "bri":'+str(brightness)+',"sat":254,"hue":'+randColor()+' }'
    requests.put(path,data=dataString)
    
    time.sleep(.15)
    path = basePath+"lights/"+str(light)+"/state"
    dataString = '{"transition_time":1, "bri":'+str(low_bright)+',"sat":254}'
    requests.put(path,data=dataString)


min_peak_threshold=3000
brightness=200
low_bright=50
chill_threshold=.25

CHUNK = 2**11
RATE = 44100
max_peak=0
max_peak_time=datetime.datetime.now()


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
max_buffer_counter=0
while True:
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    peak=np.average(np.abs(data))*2
    
    if (peak >= max_peak) or ((datetime.datetime.now() - max_peak_time) > datetime.timedelta(seconds=30)):
        if max_buffer_counter>2:
            max_peak = peak
            max_peak_time = datetime.datetime.now()
            min_peak_threshold= max_peak/10
            max_buffer_counter=0
            print("                                                     NEWMAX")
        else:
            max_buffer_counter+=1
    currentTrigger = datetime.datetime.now()
        
    if (oldpeak+ min_peak_threshold*5 ) < peak or (oldoldpeak+min_peak_threshold*5 ) < peak:
        if ((currentTrigger - lastTriggered) > datetime.timedelta(seconds=chill_threshold)):
            lastTriggered=currentTrigger
            pulseAll()
            # pulseRandom()
            print("50%+")
        else:
            print("Chill")

    elif (oldpeak+ min_peak_threshold*3 ) < peak or (oldoldpeak+min_peak_threshold*3 ) < peak:
        if ((currentTrigger - lastTriggered) > datetime.timedelta(seconds=chill_threshold)):
            lastTriggered=currentTrigger
            # pulseRandom(2)
            pulseEnds()
            print("30%+")
        else:
            print("Chill")

    elif (oldpeak+ min_peak_threshold ) < peak or (oldoldpeak+min_peak_threshold ) < peak:
        if ((currentTrigger - lastTriggered) > datetime.timedelta(seconds=chill_threshold)):
            lastTriggered=currentTrigger
            # pulseAll()
            # pulseRandom()
            pulseOne()
            print("10%+")
        else:
            print("Chill")

    else:
        print("0%")

    bars="#"*int(200*peak/2**16)
    print("MAX:%05d %05d %s"%(max_peak,peak,bars))

    oldoldpeak=oldpeak
    oldpeak=peak
    time.sleep(.1)

stream.stop_stream()
stream.close()
p.terminate()