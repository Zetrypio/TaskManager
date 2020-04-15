import math

def mymap(n, a, b, x, y): # Fonction map classique
            return (n-a)/(b-a)*(y-x)+x

def posY(t, x1, y1, x2, y2):
            return mymap(math.cos(mymap(t, x1, x2, 0, math.pi)), 1, -1, y1, y2)

