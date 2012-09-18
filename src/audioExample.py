#also look at the audioconfig in assets/audio to add more sounds.
import audio

t=audio.mySounds["trex"].play(-1) #loop
t.stop()
audio.mySounds["trex"].play(0) #loop
#audio.mySongs["chase"].play()

while(True):
    continue