# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..items.AbstractMultiFrameItem import *
from .AffichageGantt import *

class ObjetGantt(AbstractMultiFrameItem):
    """
    Classe représentant un contenu dans
    l'affichage calendrier classique.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur d'un objet classique.
        """
        super().__init__(master, schedulable)
        
        self.__parts = []

    def redraw(self, canvas):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                
                if not self.__isPartPresent(part):
                    f = Frame(canvas, bg=self._schedulable.getColor())
                    self._schedulable.createDisplayableInstance(f, part).pack(expand = YES, fill = BOTH)
                    self.__parts.append((part, f))

                f = self.__getFrameForPart(part)
                colonne = (self._schedulable.getDebut().date() - self.master.getJourDebut()).days
                x = int(self.master.tailleColonne * colonne)
                y = int(AffichageGantt.TAILLE_BANDEAU_JOUR)
                width = int(self.master.tailleColonne * self.master.facteurW)
                height = int(AffichageGantt.TAILLE_LIGNE)
                print(x, y, width, height)
                canvas.create_window(x, y, width=width, height=height, window = f, anchor="nw")

    def __isPartPresent(self, part):
        for p in self.__parts:
            if p[0] == part:
                return True
        return False

    def __getFrameForPart(self, part):
        for p in self.__parts:
            if p[0] == part:
                return p[1]

    def delete(self):
        # TODO
        for f in self._listeCadre:
            try:
                f.destroy()
            except:
                pass
        self._listeCadre = []
