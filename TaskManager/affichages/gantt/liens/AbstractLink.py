# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
import datetime

from ...items.IDisplayableItem import *

class AbstractLink(IDisplayableItem):
    """
    Classe abstraite permettant de dessiner un lien depuis
    un DatetimeItemPart|AbstractItemContent vers un autre.
    """
    def __init__(self, affichageGantt, partA, partB):
        """
        Constructeur du AbstractLink.

        @param affichageGantt: Référence vers l'affichageGantt pour avoir
        des informations sur le positionnement des parts.
        @param partA: DatetimeItemPart qui correspond au moment du début de la flèche.
        @param partB: DatetimeItemPart qui correspond au moment de la fin de la flèche.
        """
        # Constructeur parent :
        super().__init__()

        # Attributs :
        self.__can = can
        self.__affichageGantt = affichageGantt
        self.__partA = partA
        self.__partB = partB
        self.__color = "black"

    def redraw(self, canvas):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        # TODO : Dessiner correctement les liens selon le visibilitée partielle !
        
        ################################################################################################################################
        # Il y a 3 possibilitées pour dessiner une flèche :                                                                            #
        # - Ou bien les 2 parts sont le même jour au quel cas on fait une flèche en forme de S en mirroir ;                            #
        # - Ou bien les 2 parts sont 2 jours consécutifs au quel cas on fait simplement un sinus du début vers la fin ;                #
        # - Ou bien dans les autres cas, on fait un premier sinus pour se décaler, puis une ligne droite, puis un sinus pour terminer. #
        ################################################################################################################################
        rectA = self.__affichageGantt.getPartRectangle(self.__partA)
        rectB = self.__affichageGantt.getPartRectangle(self.__partB)
        
        # Le rectangle A prend la partie juste à droite de l'objet :
        rectA.setX1(rectA.getX1() + rectA.getWidth()*self.__affichageGantt.facteurW)
        
        # Le rectangle B prend la partie juste à droite de la colonne juste à gauche de l'objet :
        width = rectB.getWidth()
        rectB.setX1(rectB.getX1() + rectB.getWidth()*self.__affichageGantt.facteurW)
        rectB.moveby(-width, 0)
        
        
        ####################
        # Première façon : #
        ####################
        if self.__partA.getJour() == self.__partB.getJour():
            pass
        ####################
        # Deuxième Façon : #
        ####################
        elif self.__partA.getJour() + datetime.timedelta(days = 1) == self.__partB.getJour():
            x1 = rectA.getX1()
            x2 = rectB.getX2()
            y1 = rectA.getCenterY()
            y2 = rectB.getCenterY()
            self.__drawSinus(x1, y1, x2, y2, orient = HORIZONTAL)
            self.__can.create_line(*self.__points, width = self.__strokeWeight, fill = self.__color)
        #####################
        # Troisième façon : #
        #####################
        else:
            x1 = rectA.getX1()
            x2 = rectA.getX2()
            x3 = rectB.getX1()
            x4 = rectB.getX2()
            y1 = rectA.getCenterY()
            y2 = rectB.getY1() # On bouge jusqu'à la hauteur de l'objet de destination
            y3 = rectB.getY1()
            y4 = rectB.getCenterY()
            self.__drawSinus(x1, y1, x2, y2, orient = HORIZONTAL)
            self.__drawSinus(x3, y3, x4, y4, orient = HORIZONTAL)
            self.__can.create_line(*self.__points, width = self.__strokeWeight, fill = self.__color)
        