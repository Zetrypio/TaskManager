# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from .AbstractItemContent import *

from util.util import adaptTextColor

class DisplayableTask(AbstractItemContent):
    """
    Permet d'afficher une tâche.
    """
    def __init__(self, master, schedulable, part, **kwargs):
        super().__init__(master, schedulable, **kwargs)
        """
        Constructeur de l'affichage d'une tâche.
        @param master: master du tkinter.Frame() que cet objet est.
        @param schedulable: la tâche à gérer.
        @param part: la partie d'affichage géré par cet objet.
        @param **kwargs: les options d'affichage du tkinter.Frame() que cet objet est.
        """
        # S'assurer que c'est bien une tâche :
        if not isinstance(schedulable, Task):
            raise TypeError("Expected Task, but got %s for schedulable %s"%(schedulable.__class__.__name__, schedulable))

        super().__init__(master, schedulable, bg = schedulable.getColor(), **kwargs)

        ## Création des widgets :
        # Texte :
        self.__texte = Text(self, wrap="word", bg=self.__getDisplayColor(), width=0, height=0)
        if self.getApplication().getData().testDataExist("General", "Thème", "couleur adaptative") \
        and self.getApplication().getData().getOneValue("General", "Thème", "couleur adaptative") == "True":
            self.__texte.configure(fg=adaptTextColor(self.__getDisplayColor()), width=0, height=0)

        # Texte écrit :
        self.__texte.insert(INSERT, self._schedulable.getNom())
        self.__texte.insert(INSERT, "\n")
        self.__texte.insert(INSERT, self._schedulable.getDescription())

        # Config des Tags :
        self.__texte.tag_config("titre", font="Arial 12 bold")
        self.__texte.tag_config("corps", font="Arial 10")

        # Ajout des tags
        self.__texte.tag_add("titre", "0.0", "1.0")
        self.__texte.tag_add("corps", "1.0", END)

        # Finalisation et placements :
        self.__texte.config(state="disabled")    # Pour ne pas changer le texte dedans.
        self.__texte.pack(fill=BOTH, expand=YES) # On l'affiche une fois qu'il est tout beau.
        self.pack_propagate(False)

        # Autre attributs :
        self.__part = part

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def __getDisplayColor(self):
        """
        Getter pour savoir la véritable couleur d'affichage,
        suivant que la tâche soit sélectionnée ou non.
        """
        return self.getApplication().getData().getPalette()["selected"] if self._schedulable.isSelected() else self._schedulable.getColor()

    def needButtonPlus(self, affichageGantt):
        return (affichageGantt.getVisiblePart(self._schedulable.getLastPart(affichageGantt)) == self.__part
            and len(self._schedulable.getDependantes()) == 0)

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def configSize(self, width, height):
        """
        Permet de contrôler la taille de l'objet (pour les groupes).
        """
        self.__texte.config(width = width, height = height)

    def updateColor(self):
        """
        Permet de mettre à jour la couleur de l'objet, suivant sa sélection etc.
        """
        self.__texte.config(bg=self.__getDisplayColor(), fg=adaptTextColor(self.__getDisplayColor()))

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def bindTo(self, binding, command, add=None):
        """
        Permet de binder tout les widgets contenus dans celui-ci.
        @param binding: même doc que pour les binds de tkinter
        @param command: fonction qui va prendre cet objet en paramètre.
        @param add: même doc que pour les binds de tkinter.
        @see tkinter.Misc#bind(binding, command, add) pour la documentation du binding.
        """
        self.bind(binding, lambda e: command(self), add)
        self.__texte.bind(binding, lambda e: command(self), add)

    def onClic(self, control=False):
        if control:
            value = not self._schedulable.isSelected()
        else:
            value = True
        self._schedulable.setSelected(value)
        self.getApplication().getTaskEditor().selectLineTreeview(self._schedulable, value)

from schedulable.task.Task import Task
