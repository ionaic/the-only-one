import ConfigParser, os, pygame, string

config = ConfigParser.ConfigParser()
config.read("../assets/audio/audioconfig.ini")

mySounds={}
mySongs={}
pygame.init()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound


for sound in config.items('sounds'):
    fullname = os.path.join('../assets/audio/sfx', sound[1])
    try:
        mySounds[sound[0]] = load_sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message

for song in config.items('music'):
    fullname = os.path.join('../assets/audio/music', song[1])
    try:
        mySongs[song[0]] = load_sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message