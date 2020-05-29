# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..items.AbstractMultiFrameItem import *

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

    def redraw(self, canvas):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                # On crée le cadre
                f = Frame(canvas, bg=self._schedulable.getColor())
                
                self._schedulable.createDisplayableInstance(f, part).pack(expand = YES, fill = BOTH)
                
                # On le place :
                # TODO
                colonne = (self._schedulable.getDebut().date() - self.master.getJourDebut()).days
                if colonne >= 0 and colonne < self.master.getNbJour():
                    print(self.schedulable)

                # On le mémorise :
                self._listeCadre.append(f)
    
    def delete(self):
        for f in self._listeCadre:
            try:
                f.destroy()
            except:
                pass
        self._listeCadre = []
