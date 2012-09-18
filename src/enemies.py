# enemies
import interactions, animatedobject, animationstate, character, random

class Enemies:
    def __init__(self, game):
        Enemies.enemies = []
        Enemies.tigletNeedleObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/blue/', 'object.ini')
        Enemies.tigletNeedleObj.setTag('tiglet')
        #Enemies.tigletScissorObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette\ \(scissors\)/red/', 'object.ini')
        Enemies.game = game
        self.tigletHP = 3
        self.tigletAmmo = 0

    def spawnTiglet(self):
        temp = character.Character(Enemies.tigletNeedleObj, self.game, self.tigletHP, self.tigletAmmo)
        temp.setPos(random.randint(1, 500),random.randint(1, 500))
        temp.setAnimation('stopped')
        temp.setDirection(0)
        
        Enemies.enemies.append(temp)
