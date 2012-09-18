# enemies
import interactions, animatedobject, animationstate, character, random

class Enemies:
    tigletNeedleObj = None

    def __init__(self, game):
        self.enemies = []
        if Enemies.tigletNeedleObj == None:
            Enemies.tigletNeedleObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/blue/', 'object.ini')
            Enemies.tigletNeedleObj.setTag('tiglet')
        #Enemies.tigletScissorObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette\ \(scissors\)/red/', 'object.ini')
        self.game = game
        self.tigletHP = 3
        self.tigletAmmo = 0

    def spawnTiglet(self, x = random.randint(1,500), y = random.randint(1,500)):
        temp = character.Enemy(Enemies.tigletNeedleObj, self.game, self.tigletHP, self.tigletAmmo)
        #temp.setPos(random.randint(1, 500),random.randint(1, 500))
        temp.setPos(x, y)
        temp.setAnimation('stopped')
        temp.setDirection(0)
        
        self.enemies.append(temp)
