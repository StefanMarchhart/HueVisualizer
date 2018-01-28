## Inspiration
I bought the Hue lights a couple months ago, and didn't really do anything of interest with them until now. I wanted to take advantage of Brickhack to finally do something cool with them! 
## What it does
It loads an audio stream from either my mic, or my computers internal audio recording, and categorizes the music by wavelength before sending it to the bulbs
## How I built it
Honestly, it was just a ton of trial and error before I stumbled upon something that seemed usable
## Challenges I ran into
I spent an absurdly long amount of time trying to get a c-wrapped-in-python audio processing library working. It was fully featured, but after blowing more than an hour on it, I gave up, and decided to use the raw audio input and a little bit of math, and build the functionality I needed myself
## Accomplishments that I'm proud of
I'm honestly just proud I got it working. There was a serious dryspell in the middle of the night, and I was absoulutely elated when I finally got it working! The biggest limitations were the processing and the bandwidth limitation of the bulbs. I'm happy to have worked around them.
## What I learned
The basics of how audio visualization works! I feel like I have a stronger understanding of sound and music as well from this project
## What's next for HueVisualizer
A couple of things!
* Working on a more robust visualization (i.e. Responding to frequency)
* Working to decrease latency
* Better handling of rogue sounds (someone slamming a door or shouting)
* Audio passthrough to cast-audio
