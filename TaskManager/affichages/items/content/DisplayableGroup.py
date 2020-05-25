# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractItemContent import *

class DisplayableGroup(AbstractItemContent):
    """
    Permet d'afficher un groupe.
    """
    def __init__(self, master, schedulable, part, **kwargs):
        # S'assurer que c'est bien un groupe :
        if not isinstance(schedulable, Groupe):
            raise TypeError("Excpected Group, but got %s for %s"%(schedulable.__class__.__name__, schedulable))

        super().__init__(master, schedulable, **kwargs)
        
        # Création des widgets :
        self.__texte = Text(self, wrap = "word", bg = self.__getDisplayColor(), width=0, height=0)

        # Config des Tags :
        self.__texte.tag_config("titre", font="Arial 12 bold") 
        self.__texte.tag_config("corps", font="Arial 10")

        # Texte : 
        self.__texte.insert(INSERT, self._schedulable.getNom())
        self.__texte.insert(INSERT, "\n")
        self.__texte.insert(INSERT, self._schedulable.getDescription())
        
        # Ajout des tags
        self.__texte.tag_add("titre", "0.0", "1.0")#%int(len(task.getNom())))
        self.__texte.tag_add("corps", "1.0", END)#, %int(len(task.getDescription())))

        # Finalisation et placements :
        self.__texte.config(state = "disabled") # Pour ne pas changer le texte dedans
        self.__texte.pack(fill=BOTH, expand=YES)# On l'affiche une fois qu'il est tout beau.
        self.pack_propagate(False)
        
        # Ajout des tâches à l'intérieur :
        # TODO
        # Et filtrer selon la part.

#        # La selection des taches
#        self.__texte.bind("<Button-1>", self._clique)
#        self.__texte.bind("<Control-Button-1>", self.multiSelection)
    
    def __getDisplayColor(self):
        return "#0078FF" if self._schedulable.isSelected() else self._schedulable.getColor()

from schedulable.groupe.Groupe import *