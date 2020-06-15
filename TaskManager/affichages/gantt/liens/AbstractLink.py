# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
import datetime

from ...items.IDisplayableItem import *
from util.util import *

class AbstractLink(IDisplayableItem):
    """
    Classe abstraite permettant de dessiner un lien depuis
    un AbstractItemContent[via DatetimeItemPart] vers un autre.
    """
    def __init__(self, affichageGantt, partA, partB):
        """
        Constructeur du AbstractLink.

        @param affichageGantt: Référence vers l'affichageGantt pour avoir
        des informations sur le positionnement des parts.
        @param partA: DatetimeItemPart qui correspond au moment du début de la flèche.
        @param partB: DatetimeItemPart qui correspond au moment de la fin de la flèche.
        """
        if self.__class__==AbstractLink:
            raise RuntimeError("Can't instantiate abstract class AbstractLink directly.")

        # Constructeur parent :
        super().__init__()

        # Attributs :
        self.__affichageGantt = affichageGantt
        self.__partA = partA
        self.__partB = partB
        self.__color = "black"
        self.__highlight = None
        self.__strokeWeight = 2
        self.__points = []
        self.__binding1 = None
        self.__binding2 = None

    def getPartA(self):
        """
        Getter pour le DatetimeItemPart A du début de la flèche du lien.
        """
        return self.__partA

    def getPartB(self):
        """
        Getter pour le DatetimeItemPart B de la fin de la flèche du lien.
        """
        return self.__partB

    def updateColor(self, canvas):
        """
        Permet de mettre à jour la couleur du lien.
        """
        color = self.__highlight if self.__highlight else self.getColor()
        sw = 3 if self.__highlight else self.getStrokeWeight()

        canvas.itemconfigure(self.getTag(),        fill=color, width = sw)
        canvas.itemconfigure(self.getTag()+"c", outline=color, width = sw)

    def setColor(self, color):
        """
        Setter pour la couleur.
        @param color: String avec un nom de couleur compatible avec les noms de couleurs tkinter.
        """
        self.__color = color

    def getColor(self):
        """
        Getter pour la couleur.
        @return la couleur.
        """
        return self.__color

    def highlight(self, color):
        """
        Permet de surligner ce lien d'une couleur donnée.
        @param color: la couleur à mettre.
        """
        self.__highlight = color

    def setStrokeWeight(self, strokeWeight):
        """
        Setter pour l'épaisseur du trait.
        @param strokeWeight: int correspondant à l'épaisseur du trait, en pixel.
        """
        self.__strokeWeight = strokeWeight

    def getStrokeWeight(self):
        """
        Getter pour l'épaisseur du trait.
        @return un int correspondant à l'épaisseur du trait en pixel.
        """
        return self.__strokeWeight

    def getTag(self):
        """
        Getter pour obtenir le tag qui est présent sur tout les éléments du trait.
        """
        return "link%s"%id(self)

    def _getAffichageGantt(self):
        """
        Getter pour l'affichage Gantt
        @return l'affichage Gantt.
        """
        return self.__affichageGantt

    def redraw(self, canvas):
        """
        Méthode pour dessiner la flèche.
        @param canvas: tkinter.Canvas() sur lequel dessiner la flèche du lien.
        """
        # On vide la liste des points de la courbe.
        self.__points = []
        
        ################################################################################################################################
        # Il y a 3 possibilités pour dessiner une flèche :                                                                             #
        # - Ou bien les 2 parts sont le même jour au quel cas on fait une flèche en forme de S en miroir ;                             #
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
            # Demi-cercle au début :
            r = rectA.getHeight() / 2 //2
            canvas.create_arc(rectA.getX1() - r,
                              rectA.getCenterY(),
                              rectA.getX1() + r,
                              rectA.getY2()-1,
                              start=-90, extent=180, style=ARC,
                              tag=(self.getTag(), self.getTag()+"c"))
            # Ligne horizontale vers la gauche à la suite de l'arc :
            canvas.create_line(rectA.getX1(),
                               rectA.getY2()-1,
                               rectB.getX2()-6, # -6 Pour la flèche
                               rectA.getY2()-1,
                               tag=self.getTag())
            # Premier quart de cercle :
            canvas.create_arc(rectB.getX2() - r-6, # -6 Pour la flèche
                              rectA.getY2()-1,
                              rectB.getX2() + r-6, # -6 Pour la flèche
                              rectA.getY2() + r*2,
                              start=90, extent=90, style=ARC,
                              tag=(self.getTag(), self.getTag()+"c"))
            # Ligne verticale vers le bas à la suite de l'arc :
            canvas.create_line(rectB.getX2() - r-6, # -6 Pour la flèche
                               rectA.getY2() + r,
                               rectB.getX2() - r-6, # -6 Pour la flèche
                               rectB.getCenterY() - r,
                               tag=self.getTag())
            # Deuxième arc de cercle qui fini :
            canvas.create_arc(rectB.getX2() - r-6, # -6 Pour la flèche
                              rectB.getCenterY() - r*2,
                              rectB.getX2() + r-6, # -6 Pour la flèche
                              rectB.getCenterY(),
                              start=180, extent=90, style=ARC,
                              tag=(self.getTag(), self.getTag()+"c"))
            # Petite ligne finale pour avoir le bout de la flèche :
            canvas.create_line(rectB.getX2()-6, # -6 Pour la flèche
                               rectB.getCenterY(),
                               rectB.getX2(),
                               rectB.getCenterY(),
                               arrow = LAST, tag=self.getTag())
            pass # TODO
        ####################
        # Deuxième Façon : #
        ####################
        elif self.__partA.getJour() + datetime.timedelta(days = 1) == self.__partB.getJour():
            x1 = rectA.getX1()
            x2 = rectB.getX2()
            y1 = rectA.getCenterY()
            y2 = rectB.getCenterY()
            self.__drawSinus(x1, y1, x2, y2) # Le -8 est ? pour que le bout de la flèche soit droite.
            self.__points.append([x2, y2])
            canvas.create_line(*self.__points, arrow = LAST, tag=self.getTag())
        #####################
        # Troisième façon : #
        #####################
        else:
            x1 = rectA.getX1()
            x2 = rectA.getX2()
            x3 = rectB.getX1()
            x4 = rectB.getX2()
            y1 = rectA.getCenterY()
            y2 = rectB.getY1() -1 # On bouge jusqu'à la hauteur de l'objet de destination
            y3 = rectB.getY1() -1 # Et on met -1 pour que ça passe bien ENTRE les autres objets.
            y4 = rectB.getCenterY()
            self.__drawSinus(x1, y1, x2,     y2)
            self.__drawSinus(x3, y3, x4 - 8, y4) # Le -8 est pour que le bout de la flèche soit droite.
            self.__points.append([x4, y4])
            canvas.create_line(*self.__points, arrow = LAST, tag=self.getTag())

        #############
        # Couleur : #
        #############
        self.updateColor(canvas)

        #############
        # Binding : #
        #############
        if self.__binding1 is None:
            self.__binding1 = canvas.tag_bind(self.getTag(), "<Button-1>", lambda e: self._onClic())
            self.__binding2 = canvas.tag_bind(self.getTag(), "<Control-Button-1>", lambda e: self._onControlClic())

    def _onBinding(self):
        """
        Méthode appelée quand un clic est fait sur ce lien.
        """
        raise NotImplementedError

    def _onControlClic(self):
        """
        Méthode appelée quand un contrôle+clic est fait sur ce lien.
        """
        raise NotImplementedError

    def __drawSinus(self, x1, y1, x2, y2):
        """
        Permet de mettre les points de la courbe suivant un (co)sinus commençant en x1, y1 et se terminant en x2, y2.
        @param x1: Début en X de la courbe.
        @param y1: Début en Y de la courbe.
        @param x2: Fin en X de la courbe.
        @param y2: Fin en Y de la courbe.
        """
        for x in range(int(x1), int(x2)):
            y = posY(x, x1, y1, x2, y2) # Fait un sinus, est défini dans util.util
            self.__points.append([x, y])
        self.__points.append([x2, y2])
        