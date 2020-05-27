# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractItemContent import *

class DisplayableTask(AbstractItemContent):
    """
    Permet d'afficher une tâche.
    """
    def __init__(self, master, schedulable, **kwargs):
        super().__init__(master, schedulable, **kwargs)
        """
        Constructeur de l'affichage d'une tâche.
        @param master: master du tkinter.Frame que cet objet est.
        @param schedulable: la tâche à gérer.
        @param **kwargs: les options d'affichage du tkinter.Frame que cet objet est.
        """
        
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
        self.__texte.tag_add("titre", "0.0", "1.0")
        self.__texte.tag_add("corps", "1.0", END)

        # Finalisation et placements :
        self.__texte.config(state = "disabled")  # Pour ne pas changer le texte dedans.
        self.__texte.pack(fill=BOTH, expand=YES) # On l'affiche une fois qu'il est tout beau.
        self.pack_propagate(False)

#        # La selection des taches
#        self.__texte.bind("<Button-1>", self._clique)
#        self.__texte.bind("<Control-Button-1>", self.multiSelection)
    
    def __getDisplayColor(self):
        """
        Getter pour savoir la véritable couleur d'affichage,
        suivant que la tâche soit sélectionnée ou non.
        """
        return "#0078FF" if self._schedulable.isSelected() else self._schedulable.getColor()
