# enemies
import interactions, animatedobject, animationstate, character, random

class Enemies:
    tigletNeedleObj = None

    def __init__(self, game):
        self.enemies = []
        if Enemies.tigletNeedleObj == None:
            Enemies.tigletNeedleObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/orange/', 'object.ini')
            Enemies.tigletNeedleObj.setTag('tiglet')
        #Enemies.tigletScissorObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette\ \(scissors\)/red/', 'object.ini')
        self.game = game
        self.tigletHP = 3
        self.tigletAmmo = 0

    def spawnTiglet(self, x = 100, y = 100):
        temp = character.Enemy(Enemies.tigletNeedleObj, self.game, self.tigletHP, self.tigletAmmo)
        #temp.setPos(random.randint(1, 500),random.randint(1, 500))
        temp.setPos(x, y)
        temp.setAnimation('stopped')
        temp.setDirection(0)
        
        self.enemies.append(temp)
    
    def remove(self, tiglet):
        if tiglet in self.enemies:
            self.enemies.remove(tiglet)
            tiglet.visualDelete(tiglet.game.tilemap.surface, tiglet.game._screen)
    #    if tiglet in self.tilemap.enemies:
    #        self.game.tilemap.enemies.remove(tiglet)
    #        tiglet.visualDelete(tiglet.game.tilemap.surface, tiglet.game._screen)
