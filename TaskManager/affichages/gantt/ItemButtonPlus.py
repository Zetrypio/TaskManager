# -*- coding:utf-8 -*-

from .AffichageGantt import *
from ..items.IDisplayableItem import *

class ItemButtonPlus(IDisplayableItem):
    def __init__(self, ganttObject, part):
        super().__init__()
        self.__ganttObj = ganttObject
        self.__part = part

    def redraw(self, canvas):
        """
        Permet de mettre à jour l'affichage.
        @param canvas: le Canvas sur lequel afficher cet objet.
        @override redraw in IDisplayableItem.
        """
        colonne = (self.__part.getJour() - self.__ganttObj.master.getJourDebut()).days

        s = min(24, int(self.__ganttObj.master.tailleColonne * (1-self.__ganttObj.master.facteurW)*0.5))
        r = s // 2

        x1 = int(self.__ganttObj.master.tailleColonne * colonne + self.__ganttObj.master.facteurW * self.__ganttObj.master.tailleColonne)
        y1 = int(AffichageGantt.TAILLE_BANDEAU_JOUR + self.__ganttObj.master.getPartPosition(self.__part)*AffichageGantt.TAILLE_LIGNE)

        x2 = int(self.__ganttObj.master.tailleColonne * (colonne+1))
        y2 = int(AffichageGantt.TAILLE_BANDEAU_JOUR + (self.__ganttObj.master.getPartPosition(self.__part)+1)*AffichageGantt.TAILLE_LIGNE)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="grey")
    
    def delete(self):
        """
        Permet de supprimer cet objet de l'affichage.
        @override delete in IDisplayableItem.
        """
        pass