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
        """
        Constructeur de l'affichage d'un groupe.
        @param master: master du tkinter.Frame() que cet objet est.
        @param schedulable: le groupe à gérer.
        @param part: la partie d'affichage géré par cet objet.
        @param **kwargs: les options d'affichage du tkinter.Frame() que cet objet est.
        """
        # S'assurer que c'est bien un groupe :
        if not isinstance(schedulable, Groupe):
            raise TypeError("Expected Group, but got %s for schedulable %s"%(schedulable.__class__.__name__, schedulable))

        super().__init__(master, schedulable, bg = schedulable.getColor(), **kwargs)
        
        # Création des widgets :
        if self.getApplication().getData().testDataExist("General", "Thème", "couleur adaptative") \
            and self.getApplication().getData().getOneValue("General", "Thème", "couleur adaptative") == "True":
            self.__texte = Text(self, wrap = "word", bg = self.__getDisplayColor(), fg=self._schedulable.getTextColor(), width=0, height=0)
        else :
            self.__texte = Text(self, wrap = "word", bg = self.__getDisplayColor(), width=0, height=0)
        self.__scrollbar = Scrollbar(self, orient = VERTICAL, command = self.__texte.yview)
        self.__texte.configure(yscrollcommand = self.__scrollbar.set)

        # Config des Tags :
        self.__texte.tag_config("titre", font="Arial 12 bold") 
        self.__texte.tag_config("corps", font="Arial 10")

        # Texte : 
        self.__texte.insert(INSERT, self._schedulable.getNom())
        self.__texte.insert(INSERT, "\n")
        self.__texte.insert(INSERT, self._schedulable.getDescription())

        self.__taskFrame = []

        # Ajout des tâches à l'intérieur :
        for t in self._schedulable.getListTasks() :
            self.__texte.insert(INSERT, "\n")
            f = Frame(self.__texte)
            tache = t.createDisplayableInstance(f, part)
            tache.pack_propagate(True)
            tache.pack(expand = YES, fill = BOTH)
            tache.configSize(width = 10, height = 2)
            tache.bindTo("<Button-1>",         lambda e, task=tache: self.__onTaskSelected(task, False))
            tache.bindTo("<Control-Button-1>", lambda e, task=tache: self.__onTaskSelected(task, True))
            self.__taskFrame.append(tache)
            self.__texte.window_create(INSERT, window = f)#, stretch = 1)
        # TODO : filtrer selon la part.
        
        # Ajout des tags
        self.__texte.tag_add("titre", "0.0", "1.0")#%int(len(task.getNom())))
        self.__texte.tag_add("corps", "1.0", END)#, %int(len(task.getDescription())))

        # Finalisation :
        self.__texte.config(state = "disabled") # Pour ne pas changer le texte dedans
        
        # Placement :
        self.__texte.pack(fill=BOTH, expand = YES, side = LEFT)# On l'affiche une fois qu'il est tout beau.
        self.__scrollbar.pack(fill = Y, side = RIGHT)
        self.pack_propagate(False)

        # La selection des tâches
        #self.__texte.bind("<Button-1>", self._clique)
        #self.__texte.bind("<Control-Button-1>", self.multiSelection)

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def __getDisplayColor(self):
        """
        Getter pour savoir la véritable couleur d'affichage,
        suivant que le groupe soit sélectionné ou non.
        """
        return self.getApplication().getData().getPalette()["selected"] if self._schedulable.isSelected() else self._schedulable.getColor()

    def needButtonPlus(self, affichageGantt):
        return False

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def updateColor(self):
        """
        Permet de mettre à jour la couleur de l'objet, suivant sa sélection etc.
        """
        self.__texte.config(bg=self.__getDisplayColor())
        for t in self.__taskFrame:
            t.updateColor()

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def bindTo(self, binding, command, add=None):
        self.bind(binding, command, add)
        self.__texte.bind(binding, command, add)
        # TODO : Ajouter les sous-tâches ?

    def __onTaskSelected(self, task, control):
        """
        Méthode de callback de quand on clic sur l'une des tâches du groupe,
        éventuellement avec la touche contrôle en plus, pour faire la sélection des tâches du groupe.
        @param task: L'objet d'affichage représentant de la tâche qui reçoit le clic.
        @param control: Permet de savoir si il y a la touche contrôle avec le clic.
        """
        print("Task selection: task =", task.getSchedulable(), "| control =", control)
        if not control:
            self.getDonneeCalendrier().deselectEverything()
            self._schedulable.setSelected(False)
        task.getSchedulable().setSelected(True)
        self._schedulable.setSelected(True)
        self.updateColor()
        

from schedulable.groupe.Groupe import *
