# -*- coding:utf-8 -*-

from .Point import *

class Rectangle:
    """
    Classe permettant de manipuler des rectangles.
    """
    def __init__(self, x1 = None, x2 = None, y1 = None, y2 = None, width = None, height = None):
        """
        Constructeur du rectangle.
        
        @attention: Vous devez utiliser exactement que 2 des 3 paramètres parmi x1, x2 et width. Sinon c'est une erreur.
        @attention: Vous devez utiliser exactement que 2 des 3 paramètres parmi y1, y2 et height. Sinon c'est une erreur.
        
        @param x1: Coordonnée X de la gauche du rectangle.
        @param y1: Coordonnée Y du haut du rectangle.
        @param x2: Coordonnée X de la droite du rectangle.
        @param y2: Coordonnée Y de la gauche du rectangle.
        @param width : Largeur du rectangle.
        @param height: Hauteur du rectangle.
        """
        # Vérification en X :
        if x1 is None :
            if x2 is None or width is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi x1, x2 et width.")
            self.__x1 = x2 - width
            self.__x2 = x2
        elif x2 is None :
            if x1 is None or width is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi x1, x2 et width.")
            self.__x1 = x1
            self.__x2 = x1 + width
        elif width is None :
            if x1 is None or x2 is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi x1, x2 et width.")
            self.__x1 = x1
            self.__x2 = x2
        else:
            raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi x1, x2 et width.")

        # Vérification en Y :
        if y1 is None :
            if y2 is None or height is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi y1, y2 et height.")
            self.__y1 = y2 - height
            self.__y2 = y2
        elif y2 is None :
            if y1 is None or height is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi y1, y2 et height.")
            self.__y1 = y1
            self.__y2 = y1 + height
        elif height is None :
            if y1 is None or y2 is None: raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi y1, y2 et height.")
            self.__y1 = y1
            self.__y2 = y2
        else:
            raise TypeError("Vous devez utiliser exactement que 2 des 3 paramètres parmi y1, y2 et height.")

    def getX1(self):
        """
        Getter pour X1
        @return x1
        """
        return self.__x1

    def getY1(self):
        """
        Getter pour Y1
        @return y1
        """
        return self.__y1

    def getX2(self):
        """
        Getter pour X2
        @return x2
        """
        return self.__x2

    def getY2(self):
        """
        Getter pour Y2
        @return y2
        """
        return self.__y2

    def getCenterX(self):
        """
        Getter pour le centre du rectangle en X.
        @return (x1 + x2) / 2
        """
        return (self.__x1 + self.__x2)/2

    def getCenterY(self):
        """
        Getter pour le centre du rectangle en Y.
        @return (y1 + y2) / 2
        """
        return (self.__y1 + self.__y2)/2

    def getCenterPoint(self):
        """
        Getter pour le point du centre du rectangle.
        @return util.geom.Point() correspondant au centre du rectangle.
        """
        return Point(self.getCenterX(), self.getCenterY())

    def getWidth(self):
        """
        Getter pour la largeur du rectangle.
        @return x2 - x1
        """
        return abs(self.__x2 - self.__x1)

    def getHeight(self):
        """
        Getter pour la hauteur du rectangle.
        @return y2 - y1.
        """
        return abs(self.__y2 - self.__y1)

    def moveby(self, amtX, amtY):
        """
        Permet de déplacer le rectangle d'une certaine quantitée,
        sans changer la largeur ni la hauteur.
        @param amtX: Quantitée de mouvement en X.
        @param amtY: Quantitée de mouvement en Y.
        """
        self.__x1 += amtX
        self.__y1 += amtY
        self.__x2 += amtX
        self.__y2 += amtY

    def setX1(self, x1):
        """
        Setter pour X1. Change la largeur car ne bouge pas x2.
        """
        self.__x1 = x1

    def setY1(self, y1):
        """
        Setter pour Y1. Change la hauteur car ne bouge pas y2.
        """
        self.__y1 = y1

    def setX2(self, x2):
        """
        Setter pour X2. Change la largeur car ne bouge pas x1.
        """
        self.__x2 = x2

    def setY2(self, y2):
        """
        Setter pour Y2. Change la hauteur car ne bouge pas y1.
        """
        self.__y2 = y2
