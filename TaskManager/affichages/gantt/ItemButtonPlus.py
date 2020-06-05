# -*- coding:utf-8 -*-

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
        # Colonne du plus :
        colonne = (self.__part.getJour() - self.__ganttObj.master.getJourDebut()).days

        # Taille du plus :
        d = min(24, int(self.__ganttObj.master.tailleColonne * (1-self.__ganttObj.master.facteurW)*0.5))
        r = d // 2

        # Bordure de la zone possible ou mettre le plus en X et en Y, en minimum et en maximum :
        x1 = int(self.__ganttObj.master.tailleColonne * colonne + self.__ganttObj.master.facteurW * self.__ganttObj.master.tailleColonne)
        y1 = int(AffichageGantt.TAILLE_BANDEAU_JOUR + self.__ganttObj.master.getPartPosition(self.__part)*AffichageGantt.TAILLE_LIGNE)

        x2 = int(self.__ganttObj.master.tailleColonne * (colonne+1))
        y2 = int(AffichageGantt.TAILLE_BANDEAU_JOUR + (self.__ganttObj.master.getPartPosition(self.__part)+1)*AffichageGantt.TAILLE_LIGNE)

        # Position du centre du plus :
        self.__x = cx = (x1 + x2) // 2
        self.__y = cy = (y1 + y2) // 2

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
        canvas.tag_bind("plus%s"%(id(self.__ganttObj.getSchedulable())), "<Button-1>", lambda e: canvas.after(10, lambda :self.__ganttObj.beginLigneVerte(self)))

    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        Etant donné que tout est déjà effacé dans AffichageGantt
        lors du redessinage, rien a été mis ici.
        @override delete() in IDisplayableItem.
        """
        pass

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

