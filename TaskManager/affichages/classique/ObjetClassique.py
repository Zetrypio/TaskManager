# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..items.AbstractMultiFrameItem import *

class ObjetClassique(AbstractMultiFrameItem):
    """
    Classe représentant un contenu dans
    l'affichage calendrier classique.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur d'un objet classique.
        @param master: AffichageClassique.
        @param schedulable: Objet à afficher.
        """
        super().__init__(master, schedulable)

    def redraw(self, frame):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                # On crée le cadre
                f = Frame(frame, bg=self._schedulable.getColor())

                self._schedulable.createDisplayableInstance(f, part).pack(expand = YES, fill = BOTH)

                # On le place :
                rect = self.master.getPartRectangle(part)
                ligne       = int(rect.getY1())
                lignespan   = int(rect.getHeight())
                colonne     = int(rect.getX1())
                colonnespan = int(rect.getWidth())

                f.grid(row = ligne, rowspan = lignespan, column = colonne, columnspan = colonnespan, sticky="nsew")

                # On le mémorise :
                self._listeCadre.append(f)

    def delete(self):
        for f in self._listeCadre:
            try:
                f.destroy()
            except:
                pass
        self._listeCadre = []
