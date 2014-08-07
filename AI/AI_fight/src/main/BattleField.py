__author__ = 'jeong-yonghan'
__package__ = 'AI_fight'

class BattleField(object):

    def __init__(self, xaxis, yaxis):
        self.xaxis = xaxis+1
        self.yaxis = yaxis+1

    def field(self):
        myfield = []
        for x in range(1,self.xaxis):
            for y in range(1,self.xaxis):
                myfield.append([x,y])
        return myfield


    def myship(self, size, dir, startlocs):
        self.size=  size
        self.dir = dir
        self.startlocs = startlocs
        ship = []

        if self.startlocs[0] + self.size <= self.xaxis \
            and self.startlocs[1] + self.size <= self.yaxis:
            if self.dir == "up":
                for y in range(self.size):
                    ship.append([self.startlocs[0],self.startlocs[1]+y])
            elif self.dir == "side":
                for x in range(self.size):
                    ship.append([self.startlocs[0]+ x,self.startlocs[1]])
            return ship

        else:
            print "ship size over "


