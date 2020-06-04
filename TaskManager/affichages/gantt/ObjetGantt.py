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

        self.__activePlus = None

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
                    # On fait dans tout les cas un frame pour ne pas prendre de risque de positionnement :
                    f = Frame(canvas, bg=self._schedulable.getColor())

                    # Ce "widget" est une instance d'une sous-classe de AbstractItemContent :
                    widget = self._schedulable.createDisplayableInstance(f, part)
                    widget.pack(expand = YES, fill = BOTH)
                    # C'est pour ça que l'on fait cette méthode-ci pour le bind.
                    # Cela permet de s'assurer que tout les sous-widgets seront binds aussi :
                    widget.bindTo("<Button-1>", self.clic)

                    # On crée le plus qui correspond à cet objet.
                    plus = ItemButtonPlus(self, part)

                    # On mémorise tout cet ensemble.
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

    def beginLigneVerte(self, plus):
        self.__activePlus = plus
        self.master.beginLigneVerte(self)

    def clic(self, event):
        self.master.clicSurObjet(self)

    def getXPlus(self):
        return self.__activePlus.getX()

    def getYPlus(self):
        return self.__activePlus.getY()

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
