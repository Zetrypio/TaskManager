# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime

from .TaskInDnd import *
from .dialog.datetimeDialog import *

class Task:
    """Classe définissant une tâche."""
    def __init__(self, nom, debut, duree, rep=-1, nbrep = 0, desc="", color="white", periode = None):
        """
        @param nom : nom de la tâche.
        @param debut : datetime. du début.
        @param duree : datetime.
        @param rep : répétition.
        @param nbrep : nombre de répétitions.
        @param desc : description.
        @param color: couleur avec un nom compatible avec les noms de couleurs tkinter.
        """
        self.nom = nom
        self.debut = debut
        self.duree = duree
        self.rep = rep      # répétition
        self.nbrep = nbrep  # nombre de répétitions
        self.desc = desc    # descirption
        self.color = color
        self.periode = periode
        self.dependances = []
        self.dependantes = []
        self.updateStatut()

        # Doit-on l'afficher ?
        self.visible = True

        # Attribut de selection
        self.selected = False

        if self.isContainer():
            self.subtasks = []

    def __str__(self):
        return "Task %s: from %s to %s, %s"%(self.nom, self.debut or "Unknown", self.getFin() or "Unknown", self.statut)

    def inverseSelection(self):
        self.selected = not self.selected
    def setSelected(self, value):
        self.selected = value
    def isSelected(self):
        return self.selected

    def getDisplayColor(self):
        return self.getNativeColor() if not self.isSelected() else "#0078FF"
    def getNativeColor(self):
        return self.color

    def isContainer(self):
        self.updateStatut()
        if self.statut == "Inconnu" and not hasattr(self, "subtasks"):
            self.subtasks = []
        return self.statut == "Inconnu"
    def addSubTask(self, task):
        """Il est impératif de gérer la suppresion de la tâche dans TaskEditor depuis l'extérieur."""
        if not self.isContainer():
            raise ValueError("Impossible de rajouter une tâche dans une tâche non conteneur.")
        if task.isContainer():
            raise ValueError("Impossible de rajouter une tâche conteneur dans une autre tâche conteneur")
        self.subtasks.append(task)
    def getSubTasks(self):
        if not self.isContainer():
            raise ValueError("Impossible d'obtenir les sous-tâches d'une tâche non conteneur.")
        return self.subtasks

    def addDependance(self, task):
        self.dependances.append(task)
        task.dependantes.append(self)
    def removeDependance(self, task):
        self.dependances.remove(task)
        task.dependantes.remove(self)
    def getDependances(self):
        return self.dependances[:]
    def getDependantes(self):
        return self.dependantes[:]
    def getPeriode(self):
        return self.periode
    def setPeriode(self, periode):
        self.periode = periode

    def copy(self):
        t = Task(self.nom, self.getDebut(), self.getDuree(), self.rep, self.nbrep, self.desc, self.color)
        # Doit-on copier les dépendances et le statut ?
        t.dependances = self.dependances[:]
        t.statut = self.statut
        # On retourne la copie :
        return t

    def updateStatut(self):
        """Permet de mettre à jour le statut de la tâche."""
        self.statut = "Inconnu" if self.debut == None else "À faire" if self.nbrep == 0 else "Répétition"

    def getDebut(self):
        return self.debut + datetime.timedelta() if self.debut is not None else None # Faire une copie et vérifier les trucs
    def setDebut(self, debut, change = "fin"):
        """
        Permet de mettre le début de la période.
        @param debut: Le datetime.date du début de la période.
        @param change: Si "duree": change la durée mais pas la fin,
                       Si "fin": change la fin mais pas la durée.
                       Sinon : raise ValueError
        """
        if change == "duree":
            fin = self.getFin()
            self.debut = debut + datetime.timedelta() # Faire une copie de la date
            self.duree = fin - self.getFin()
        elif change == "fin":
            self.debut = debut + datetime.timedelta() # Faire une copie de la date
        else:
            raise ValueError('Mauvaise valeure à changer : %s, seulement "duree" et "fin" sont possibles.'%change)
    def getDuree(self):
        return self.duree + datetime.timedelta() # Faire une copie
    def getFin(self):
        return (self.debut + self.duree) if self.debut is not None else None

    def getVisible(self):
        return self.visible
    def setVisible(self, valeur):
        self.visible = valeur
