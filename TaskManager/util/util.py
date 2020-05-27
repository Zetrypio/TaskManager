import math

def mymap(n, a, b, x, y): # Fonction map classique
    """
    Permet de mapper n entre a et b, vers entre x et y.
    @param n: le nombre � mapper.
    @param a: le d�but du premier interval.
    @param b: la fin du premier interval.
    @param x: le d�but du deuxi�me interval.
    @param y: la fin du deuxi�me interval.
    @return n converti entre x et y depuix entre a et b.
    """
    return (n-a)/(b-a)*(y-x)+x

def posY(t, x1, y1, x2, y2):
    """
    Permet d'obtenir la position Y d'un sinus allant de X1 Y1 � X2 Y2.
    @param t: entre X1 et X2.
    @param x1: Position X de d�part de la courbe.
    @param y1: Position Y de d�part de la courbe.
    @param x2: Position X de fin de la courbe.
    @param y2: Position Y de fin de la courbe.
    @return la position Y du point en X dans cette courbe.
    """
    return mymap(math.cos(mymap(t, x1, x2, 0, math.pi)), 1, -1, y1, y2)

def err(e):
    """Return a nice string representation for error objects."""
    return "%s : %s" % (e.__class__.__name__, e)
