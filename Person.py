import time

res = 0

class Person:

    def __init__(self, id, x, y, date, active=True):
        self.id = id
        self.x = x
        self.y = y
        self.date = date
        self.active = active

    def getId(self):
        return self.id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def updateCoords(self, newX, newY):
        self.x = newX
        self.y = newY

    def add2timer(self):
        if self.active:
            global res
            res = (time.time() % 60) - (self.date % 60)
            return int(res)
        else:
            return 0

    def stoptimer(self):
        self.active = False

    def getTest(self):
        if res >= 3:
            return True
        else:
            return False
