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
                temps0 = 1 + self.master.getHeureDebut().hour * 60 + self.master.getHeureDebut().minute
                temps1 = 1 + part.getHeureDebut()       .hour * 60 + part.getHeureDebut()       .minute
                temps2 = 1 + part.getHeureFin()         .hour * 60 + part.getHeureFin()         .minute

                ligne1 = 1 + temps1 - temps0
                ligne2 = 1 + temps2 - temps0

                lignespan = ligne2 - ligne1

                colonne = self.getPartPosition(part)
                colonnespan = self.getPartSpan(part)

                f.grid(row = ligne1, rowspan = lignespan, column = colonne, columnspan = colonnespan, sticky="nsew")

                # On le mémorise :
                self._listeCadre.append(f)
    
    def delete(self):
        for f in self._listeCadre:
            try:
                f.destroy()
            except:
                pass
        self._listeCadre = []
