# enemies
import interactions, animatedobject, animationstate, character, random

class Enemies:
    tigletNeedleObjOrange = None
    tigletNeedleObjBlue = None
    tigletNeedleObjPink = None
    tigletNeedleObjRed = None
    beefyObj = None

    def __init__(self, game):
        self.enemies = []
        if Enemies.tigletNeedleObjOrange == None:
            Enemies.tigletNeedleObjOrange = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/orange/', 'object.ini')
            Enemies.tigletNeedleObjOrange.setTag('tiglet')

        #if Enemies.tigletNeedleObjBlue == None:
        #    Enemies.tigletNeedleObjBlue = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/blue/', 'object.ini')
        #    Enemies.tigletNeedleObjBlue.setTag('tiglet')

        #if Enemies.tigletNeedleObjPink == None:
        #    Enemies.tigletNeedleObjPink = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/pink/', 'object.ini')
        #    Enemies.tigletNeedleObjPink.setTag('tiglet')

        #if Enemies.tigletNeedleObjRed == None:
        #    Enemies.tigletNeedleObjRed = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/red/', 'object.ini')
        #    Enemies.tigletNeedleObjRed.setTag('tiglet')

        if Enemies.beefyObj == None:
            Enemies.beefyObj = animatedobject.createAnimatedObject('../assets/enemies/beefy/', 'object.ini')
            Enemies.tigletNeedleObjRed.setTag('beefy')

        #Enemies.tigletScissorObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette\ \(scissors\)/red/', 'object.ini')
        self.game = game
        self.tigletHP = 3
        self.tigletAmmo = 0

    def spawnTiglet(self, x = 100, y = 100):
        #color = random.randint(0, 3)
        #color = random.randint(0, 1)
        enemyobj = Enemies.tigletNeedleObjOrange
        #if color == 0: enemyobj = Enemies.tigletNeedleObjOrange
        #elif color == 0: enemyobj = Enemies.tigletNeedleObjBlue
        #elif color == 0: enemyobj = Enemies.tigletNeedleObjPink
        #elif color == 0: enemyobj = Enemies.tigletNeedleObjRed
        temp = character.Enemy(enemyobj, self.game, self.tigletHP, self.tigletAmmo)
        #temp.setPos(random.randint(1, 500),random.randint(1, 500))
        temp.setPos(x, y)
        temp.setAnimation('stopped')
        temp.setDirection(0)
        
        self.enemies.append(temp)

    def spawnBeefy(self, x = 250, y = 250):
        temp = character.Enemy(Enemies.beefyObj, self.game, self.beefyHP, self.beefyAmmo)
        temp.setPos(x, y)
        temp.setAnimation('stopped')
        temp.setDirection(0)

        self.enemies.append(temp)
    
    def remove(self, tiglet):
        if tiglet in self.enemies:
            self.enemies.remove(tiglet)
            tiglet.visualDelete(tiglet.game.tilemap.surface, tiglet.game._screen)
