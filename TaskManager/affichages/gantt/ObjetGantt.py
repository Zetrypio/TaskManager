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
        @param master: AffichageGantt.
        @param schedulable: objet dont on fait l'affichage.
        """
        super().__init__(master, schedulable)
        
        self.__parts = []

        self.__activePlus = None

    def __del__(self):
        for p in self.__parts:
            p[1].destroy()
        self.__parts = []

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

                    # Si cette part à besoin d'un plus :
                    if widget.needButtonPlus(self.master):
                        # On crée le plus qui correspond à cet objet.
                        plus = ItemButtonPlus(self, part)

                        # On mémorise tout cet ensemble.
                        self.__parts.append((part, f, widget, plus))
                    else:
                        # Sinon pas de plus
                        self.__parts.append((part, f, widget))
#                # Si le plus à disparu :
#                elif not self.__getWidgetForPart(part).needButtonPlus(self.master) and self.__getPlusForPart() is not None:
#                    
#                    pass

                f = self.__getFrameForPart(part)
                rect = self.master.getPartRectangle(part)
                x = rect.getX1()+1
                y = rect.getY1()+1
                width = rect.getWidth() * self.master.facteurW
                height = rect.getHeight() - 4
                canvas.create_window(x, y, width=width, height=height, window = f, anchor="nw")

        # Suppression des parties qui ne sont plus visibles :
        for p in reversed(self.__parts):
            if not self.getVisiblePart(p[0]):
                p[1].destroy()
                self.__parts.remove(p)
            elif len(p) > 3:
                p[3].redraw(canvas)

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
