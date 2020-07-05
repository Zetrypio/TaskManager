# -*- coding:utf-8 -*-
import math
import datetime

def mymap(n, a, b, x, y): # Fonction map classique
    """
    Permet de mapper n entre a et b, vers entre x et y.
    @param n: le nombre à mapper.
    @param a: le début du premier interval.
    @param b: la fin du premier interval.
    @param x: le début du deuxième interval.
    @param y: la fin du deuxième interval.
    @return n converti entre x et y depuis entre a et b.
    """
    return (n-a)/(b-a)*(y-x)+x

def posY(t, x1, y1, x2, y2):
    """
    Permet d'obtenir la position Y d'une interpolation sinusoïdale horizontale allant de X1 Y1 à X2 Y2.
    @param t: entre X1 et X2.
    @param x1: Position X de départ de la courbe.
    @param y1: Position Y de départ de la courbe.
    @param x2: Position X de fin de la courbe.
    @param y2: Position Y de fin de la courbe.
    @return la position Y du point en X dans cette courbe.
    """
    return mymap(math.cos(mymap(t, x1, x2, 0, math.pi)), 1, -1, y1, y2)

def err(e):
    """Return a nice string representation for error objects."""
    return "%s : %s" % (e.__class__.__name__, e)

def ppcm(a, b):
    """Renvoie le plus petit commun multiple (ppcm) des 2 nombres a et b."""
    return (a*b)//math.gcd(a,b)

def rangeDate(jourA, jourB, last = True):
    """
    Permet de faire un générateur renvoyant des jours
    d'un début vers une fin.
    @bug: Essai de correction cependant (en test), mais : Il semblerait que cela ne fonctionne pas correctement.
    @param jourA: début du générateur, sera yield.
    @param jourB: fin du générateur, sera yield si et
    seulement si last est sur True (défaut).
    @param last = True: True si on doit inclure le jour de fin.
    """
    if jourA is not None and jourB is not None:
        jour = jourA + datetime.timedelta()
        while jour < jourB:
            yield jour
            jour += datetime.timedelta(days = 1)
        if last:
            yield jourB
