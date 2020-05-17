# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime

from .dialog.datetimeDialog import *
from .TaskInDnd import *
from .ITaskEditorDisplayableObject import *

class Task(ITaskEditorDisplayableObject):
    """Classe définissant une tâche."""
    def __init__(self, nom, debut, duree, rep=-1, nbrep = 0, desc="", color="white", periode = None, parent = None):
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
        self.parent = parent
        self.dependances = []
        self.dependantes = []

        self.__statutValideManuel = False # Variable pour savoir si on a validé la tache manuellement pour continuer d'utiliser updateStatut()
        self.updateStatut()


        # Doit-on l'afficher ?
        self.visible = True

        # Attribut de selection
        self.selected = False

        if self.isContainer():
            self.subtasks = []

    def __str__(self):
        return "Task: %s, from %s to %s, %s"%(self.nom, self.debut or "Unknown", self.getFin() or "Unknown", self.statut)

    def inverseSelection(self):
        self.selected = not self.selected
    def setSelected(self, value):
        if not isinstance(value, bool): raise TypeError("Exptected a boolean")
        self.selected = value
    def isSelected(self):
        return self.selected

    def getDisplayColor(self):
        return self.getNativeColor() if not self.isSelected() else "#0078FF"
    def getNativeColor(self):
        return self.color
    def getColor(self):
        return self.getNativeColor()

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
        if task.parent is not None:
            raise ValueError("Impossible de rajouter une tâche dans un conteneur, sachant qu'elle est déjà présente dans un autre conteneur")
        self.subtasks.append(task)
        task.parent = self
    
    def removeSubTask(self, task):
        if not self.isContainer():
            raise ValueError("Impossible d'enlever une tâche d'une tâche non conteneur.")
        if task.parent != self:
            raise ValueError("Impossible d'enlever une tâche d'un conteneur où cette tâche n'est pas présente.")
        self.subtasks.remove(task)
    
    def getSubTasks(self):
        if not self.isContainer():
            raise ValueError("Impossible d'obtenir les sous-tâches d'une tâche non conteneur.")
        return self.subtasks
    
    def getParent(self):
        """Retourne la tâche conteneur qui contient cette tâche (si ce conteneur existe)."""
        return self.parent

    def getHeader(self):
        return self.nom, self.statut
    def iterateDisplayContent(self, displayDependances = True, displayDependantes = True):
        # Note : on yield par paires.
        if not self.isContainer():
            yield "Début :",           self.getDebut()
            yield "Durée :",           self.getDuree()
            yield "Fin :",             self.getFin()
            yield "Nombre rep :",      self.nbrep
            yield "Temps entre rep :", self.rep
            if displayDependances:
                a = {
                    "displayDependances": True,
                    "displayDependantes": False
                }
                yield "Dépendances :", len(self.dependances)
                yield a
                yield from self.dependances
            if displayDependantes:
                a = {
                    "displayDependances": False,
                    "displayDependantes": True
                }
                yield "Dépendantes :", len(self.dependantes)
                yield a
                yield from self.dependantes
        if self.parent is None: # Ne pas répéter les descriptions identiques dans les sous-tâches.
            yield "Description :", self.desc
        if self.isContainer():
            a = {
                "displayDependances": displayDependances,
                "displayDependantes": displayDependantes
            }
            yield "Instances :", len(self.getSubTasks())
            yield a
            yield from self.getSubTasks()
    
    def getRMenuContent(self, taskEditor, rmenu):
        # Mise en place de simplicitées :
        retour = []
        add = lambda a, b=None: retour.append((a, b if b else {}))
        
        # Ajout des menus :
        # Si c'est un conteneur :
        if not self.isContainer() and self.parent is None:
            add("command", {"label":"Transformer en une tâche déplaçable", "command":lambda: self.transformToDnd(taskEditor, rmenu)})
            add("separator")
        # Dans tout les cas :
        add("command", {"label":"Supprimer %s"%self, "command": lambda: self.supprimer(taskEditor)})
        return retour
    
    def supprimer(self, taskEditor):
        if self.parent is None:
            taskEditor.supprimer(self)
        else:
            self.parent.removeSubTask(self)
            taskEditor.redessiner()

    def transformToDnd(self, taskEditor, rmenu):
        rmenu.destroy()
        del rmenu
        taskEditor.supprimer(self)
        newTask = self.copy()
        newTask.debut = None
        newTask.updateStatut()
        newTask.addSubTask(self)
        taskEditor.ajouter(newTask)

    def getFilterStateWith(self, filter):
        # Si non autorisé par le filtre :
        if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
        or ("type" in filter and not "Tâche" in filter["type"]): # TODO : Ajouter tâches indépendantes.
            return -1
        # Filtre prioritaire ?
        if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
            return 1
        # Sinon : autorisé par le filtre, mais pas prioritaire.
        return 0

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
        if self.debut == None:
            self.statut = "Inconnu"
        elif (self.getPeriode().getDateStatut() is not None and self.getDebut() < self.getPeriode().getDateStatut()) or self.__statutValideManuel:
                self.statut = "Fait"
        else:
            self.statut = "À faire"

        if self.nbrep != 0:
            self.statut = "Répétition"

        #self.statut = "Inconnu" if self.debut == None else "À faire" if self.nbrep == 0 else "Répétition"

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

    def getGroupes(self):
        """ Retourne une liste de groupe auxquelles appartient la tache et None s'il n'y a pas de groupe """
        listeGroupe = []
        for groupe in self.getPeriode().getGroupeManager().getGroupes():
            for tache in groupe.getListTasks():
                if tache == self:
                    listeGroupe.append(groupe)
        return listeGroupe if listeGroupe else None

    def getVisible(self):
        return self.visible
    def setVisible(self, valeur):
        self.visible = valeur

    def reverseStateValide(self):
        self.__statutValideManuel = not self.__statutValideManuel
        print(self.__statutValideManuel)
        self.updateStatut()
