# enemies
import interactions, animatedobject, animationstate, character, random

class Enemies:
    tigletNeedleObjOrange = None
    tigletNeedleObjBlue = None
    tigletNeedleObjPink = None
    tigletNeedleObjRed = None
    beefyObj = None
    donkeyObj = None

    def __init__(self, game):
        self.enemies = []
        if Enemies.donkeyObj == None:
            Enemies.donkeyObj = animatedobject.createAnimatedObject('../assets/eeyore','object.ini')
            Enemies.donkeyObj.tag = 'eeyore'

        if Enemies.tigletNeedleObjOrange == None:
            Enemies.tigletNeedleObjOrange = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/orange/', 'object.ini')
            Enemies.tigletNeedleObjOrange.tag = 'tiglet'

        if Enemies.tigletNeedleObjBlue == None:
            Enemies.tigletNeedleObjBlue = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/blue/', 'object.ini')
            Enemies.tigletNeedleObjBlue.tag = 'tiglet'

        if Enemies.tigletNeedleObjPink == None:
            Enemies.tigletNeedleObjPink = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/pink/', 'object.ini')
            Enemies.tigletNeedleObjPink.tag = 'tiglet'

        if Enemies.tigletNeedleObjRed == None:
            Enemies.tigletNeedleObjRed = animatedobject.createAnimatedObject('../assets/enemies/tigglette (needle)/red/', 'object.ini')
            Enemies.tigletNeedleObjRed.tag = 'tiglet'

        if Enemies.beefyObj == None:
            Enemies.beefyObj = animatedobject.createAnimatedObject('../assets/enemies/beefy/', 'object.ini')
            Enemies.beefyObj.tag = 'beefy'

        #Enemies.tigletScissorObj = animatedobject.createAnimatedObject('../assets/enemies/tigglette\ \(scissors\)/red/', 'object.ini')
        self.game = game
        self.donkeyHP = 5
        self.donkeyAmmo = 5
        self.tigletHP = 3
        self.tigletAmmo = 0
        self.beefyHP = 20
        self.beefyAmmo = 10

    def spawnDonkey(self, x = 250, y = 250):
        temp = character.Enemy(Enemies.donkeyObj, self.game, self.donkeyHP, self.donkeyAmmo)
        temp.setPos(x, y)
        temp.setAnimation('stopped')
        temp.setDirection(0)
        temp.move.moveSpeed = [0, 0]
        temp.direction = [0, 0]
        temp.setPos(x, y)

        self.enemies.append(temp)

    def spawnTiglet(self, x = 250, y = 250):
        color = random.randint(0, 3)
        enemyobj = Enemies.tigletNeedleObjOrange
        if color == 0: enemyobj = Enemies.tigletNeedleObjOrange
        elif color == 0: enemyobj = Enemies.tigletNeedleObjBlue
        elif color == 0: enemyobj = Enemies.tigletNeedleObjPink
        elif color == 0: enemyobj = Enemies.tigletNeedleObjRed
        temp = character.Enemy(enemyobj, self.game, self.tigletHP, self.tigletAmmo)
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
