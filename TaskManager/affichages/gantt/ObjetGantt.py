# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..items.AbstractMultiFrameItem import *
from .AffichageGantt import *
from .ItemButtonPlus import *

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
        self.__plus = []

    def __del__(self):
        for p in self.__parts:
            p[1].destroy()
        for p in self.__plus:
            p.delete()
        self.__parts = []
        self.__plus = []

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
                    plus = ItemButtonPlus(self, part)
                    self.__parts.append((part, f, plus))

                f = self.__getFrameForPart(part)
                colonne = (part.getJour() - self.master.getJourDebut()).days
                x = 2+int(self.master.tailleColonne * colonne)
                y = 1+int(AffichageGantt.TAILLE_BANDEAU_JOUR + self.getPartPosition(part)*AffichageGantt.TAILLE_LIGNE)
                width = int(self.master.tailleColonne * self.master.facteurW)
                height = int(AffichageGantt.HAUTEUR_TACHE)
                print(x, y, width, height)
                canvas.create_window(x, y, width=width, height=height, window = f, anchor="nw")
        
        # Suppression des parties qui ne sont plus visibles :
        for p in reversed(self.__parts):
            if not self.getVisiblePart(p[0]):
                p[1].destroy()
                self.__parts.remove(p)
            else:
                p[2].redraw(canvas)

        # Bindings :
        canvas.tag_bind("plus%s"%(id(self._schedulable)), "<Button-1>", lambda e:print(self._schedulable))

    def __isPartPresent(self, part):
        for p in self.__parts:
            if p[0] == part:
                return True
        return False

    def __getFrameForPart(self, part):
        for p in self.__parts:
            if p[0] == part:
                return p[1]

    def delete(self):pass
