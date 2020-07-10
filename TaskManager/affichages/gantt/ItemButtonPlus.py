# -*- coding:utf-8 -*-

from util.geom.Point import *

from .AffichageGantt import *
from ..items.IDisplayableItem import *

class ItemButtonPlus(IDisplayableItem):
    """
    Classe correspondant au plus parfois affiché à côté d'un objet gantt.
    """
    def __init__(self, ganttObject, part):
        """
        Constructeur de l'objet Plus (+).

        @param ganttObject: référence à l'objet gantt (et donc indirectement au schedulable ou
        à l'affichage gantt) qui correspond à l'objet qui rajoute ce plus.
        @param part: Référence vers la DatetimeItemPart qui permettra de positionner correctement
        ce plus à côté de l'AbstractItemContent qui est relié à cette partie de l'ObjetGantt.
        """
        # Constructeur parent :
        super().__init__()

        # Attributs :
        self.__ganttObj = ganttObject
        self.__part = part
        self.__x = self.__y = 0

    def redraw(self, canvas):
        """
        Permet de mettre à jour l'affichage.
        @param canvas: le Canvas sur lequel afficher cet objet.
        @override redraw in IDisplayableItem.
        """
        # Zone de l'objet :
        rect = self.__ganttObj.master.getPartRectangle(self.__part)

        # On extrait la zone du plus :
        rect.setX1(rect.getX1() + rect.getWidth()*self.__ganttObj.master.facteurW)

        # Taille du plus (diamètre et rayon) :
        d = int(min(rect.getWidth()/2, rect.getHeight()/2))
        r = d // 2

        # Position du centre du plus :
        self.__x = cx = int(rect.getCenterX())
        self.__y = cy = int(rect.getCenterY())

        # Création du rond :
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="light grey", tag = ("plus", "plus%s"%(id(self.__ganttObj.getSchedulable()))))

        # Taille de la ligne 60% du rayon :
        s = int(r * 0.6)

        # Complément du x2 et y2 permettant de faire que le plus est
        # toujours une taille impaire, pour que son dessin soit centré :
        completion = 1-s%2
        
        # Création de la ligne :
        canvas.create_line(cx-s, cy, cx+s+completion, cy, tag = ("plus", "plus%s"%(id(self.__ganttObj.getSchedulable()))))
        canvas.create_line(cx, cy-s, cx, cy+s+completion, tag = ("plus", "plus%s"%(id(self.__ganttObj.getSchedulable()))))

        # Bindings :
        canvas.tag_bind("plus%s"%(id(self.__ganttObj.getSchedulable())), "<Button-1>",
            lambda e: canvas.after(10,
                lambda :self.__ganttObj.beginLinkingLine(Point(self.__x, self.__y))))

    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        Étant donné que tout est déjà effacé dans AffichageGantt
        lors du redessinage, rien a été mis ici.
        @override delete() in IDisplayableItem.
        """
        pass

    def getSchedulable(self):
        return self.__ganttObj.getSchedulable()

    def getX(self):
        """
        Getter pour le centre X du plus.
        Il est calculé lors de l'appel à la méthode redraw().
        @return la position X du centre du plus.
        """
        return self.__x

    def getY(self):
        """
        Getter pour le centre Y du plus.
        Il est calculé lors de l'appel à la méthode redraw().
        @return la position Y du centre du plus.
        """
        return self.__y

