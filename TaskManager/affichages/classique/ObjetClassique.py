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
        self.__listeCadre = []
        self.__widget = []

    def redraw(self, frame):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                # On crée le cadre
                f = Frame(frame, bg=self._schedulable.getColor())

                # Ce "widget" est une instance d'une sous-classe de AbstractItemContent :
                widget = self._schedulable.createDisplayableInstance(f, part)
                widget.pack(expand = YES, fill = BOTH)
                # C'est pour ça que l'on fait cette méthode-ci pour le bind.
                # Cela permet de s'assurer que tout les sous-widgets seront binds aussi :
                widget.bindTo("<Button-1>", lambda e: self.__onSelect())
                widget.bindTo("<Control-Button-1>", lambda e: self.__onMultiSelect())

                # On le place :
                rect = self.master.getPartRectangle(part)
                ligne       = int(rect.getY1())
                lignespan   = int(rect.getHeight())
                colonne     = int(rect.getX1())
                colonnespan = int(rect.getWidth())

                f.grid(row = ligne, rowspan = lignespan, column = colonne, columnspan = colonnespan, sticky="nsew")

                # On le mémorise :
                self.__listeCadre.append(f)
                self.__widget.append(widget)

    def __onSelect(self):
        """
        Permet d'informer à l'affichage gantt que l'on a appuyé sur cet objet.
        Utile pour la création des liens par exemple, ou la sélection des tâches etc.
        """
        self.master.clicSurObjet(self)

    def __onMultiSelect(self):
        """
        Permet d'inverser l'état de sélection de l'objet schedulable.
        """
        self._schedulable.inverseSelection()
        self.master.getDonneeCalendrier().updateColor()

    def updateColor(self, frame):
        for w in self.__widget:
            w.updateColor()

    def delete(self):
        for f in self.__listeCadre:
            try:
                f.destroy()
            except:
                pass
        self.__listeCadre = []
        self.__widget = []
