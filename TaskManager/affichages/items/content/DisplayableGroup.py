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

        ## Création des widgets :
        # Texte :
        self.__texte = Text(self, wrap = "word", bg = self.__getDisplayColor(), width=0, height=0)
        if self.getApplication().getData().testDataExist("General", "Thème", "couleur adaptative") \
        and self.getApplication().getData().getOneValue("General", "Thème", "couleur adaptative") == "True":
            self.__texte.configure(fg=adaptTextColor(self.__getDisplayColor()), width=0, height=0)

        # Scrollbar
        self.__scrollbar = Scrollbar(self, orient = VERTICAL, command = self.__texte.yview)
        self.__texte.configure(yscrollcommand = self.__scrollbar.set)

        # Texte écrit: 
        self.__texte.insert(INSERT, self._schedulable.getNom() + "\n" + self._schedulable.getDescription())

        # Liste des parts des tâches à afficher :
        self.__taskFrame = []
        parts = []
        for t in self._schedulable.getListTasks():
            parts += t.getRepartition(None)
        parts.sort(key=lambda p: p.getDebut())

        # Ajout des tâches à l'intérieur :
        # TODO fixed ? : filtrer selon la position (si 2 tâches ont 1 heure de décalage, que ça ce voie sur Classique).
        for p in parts :
            if part.getDebut() <= p.getDebut() and p.getFin() <= part.getFin():
                self.__ajouterTask(p, part)

        # Config des Tags :
        self.__texte.tag_config("titre", font="Arial 12 bold") 
        self.__texte.tag_config("corps", font="Arial 10")

        # Ajout des tags
        self.__texte.tag_add("titre", "0.0", "1.0") # Première ligne = titre
        self.__texte.tag_add("corps", "1.0", END)   # le reste = description

        # Finalisation :
        self.__texte.config(state = DISABLED) # Pour ne pas changer le texte dedans

        # Placement (à la fin) :
        self.__texte.pack(fill=BOTH, expand = YES, side = LEFT)
        self.__scrollbar.pack(fill = Y, side = RIGHT)
        self.pack_propagate(False)

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
        """
        Un groupe ne permet pas d'avoir un bouton + pour faire des liens.
        @return false car pas de bouton +
        """
        return False

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def updateColor(self):
        """
        Permet de mettre à jour la couleur de l'objet ainsi que ses sous-tâches, suivant la sélection etc.
        """
        self.__texte.config(bg=self.__getDisplayColor(), fg=adaptTextColor(self.__getDisplayColor()))
        for t in self.__taskFrame:
            t.updateColor()

    def __ajouterTask(self, p, part):
        self.__texte.insert(INSERT, "\n")                               # nouvelle ligne pour un bon positionnement
        f = Frame(self.__texte)                                         # cadre de la tâche
        tache = p.getSchedulable().createDisplayableInstance(f, part)   # affichage de la tâche
        tache.pack_propagate(True)
        tache.pack(expand = YES, fill = BOTH)
        tache.configSize(width = 10, height = 2)
        self.__texte.window_create(INSERT, window = f)#, stretch = 1)
        self.__taskFrame.append(tache)                                  # on la mémorise

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def bindTo(self, binding, command, add=None):
        """
        Permet de binder tout les widgets contenus dans celui-ci.
        @param binding: même doc que pour les binds de tkinter
        @param command: fonction qui va prendre cet objet ou la tâche cliquée en paramètre.
        @param add: même doc que pour les binds de tkinter.
        @see tkinter.Misc#bind(binding, command, add) pour la documentation du binding.
        """
        self        .bind(binding, lambda e: command(self), add)
        self.__texte.bind(binding, lambda e: command(self), add)
        for task in self.__taskFrame:
            task.bindTo(binding, lambda e, tache=task: command(tache), add)

    def onClic(self, control=False):
        taskEditor = self.getApplication().getTaskEditor()
        # Quand il y a la touche contrôle, cela ne concerne que le groupe, pas ses sous-tâches.
        if control:
            # et la nouvelle valeur est une inversion de l'ancienne.
            value = not self._schedulable.isSelected()
        else:
            # Alors qu'un clic est toujours une activation,
            value = True
        # On met à jour la valeur :
        self._schedulable.setSelected(value)
        taskEditor.selectLineTreeview(self._schedulable, value)
        if value:
            # On sélectionne aussi toutes les sous-tâches.
            for t in self.__taskFrame:
                t.getSchedulable().setSelected(True)
                taskEditor.selectLineTreeview(t.getSchedulable(), True)

from schedulable.groupe.Groupe import *
