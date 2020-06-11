# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime

from ..AbstractSchedulableObject import *

from .dialog.datetimeDialog import *
from .TaskInDnd import *

from affichages.items.DatetimeItemPart import *
from affichages.items.content.DisplayableTask import *

class Task(AbstractSchedulableObject):
    """Classe définissant une tâche."""
    def __init__(self, nom, periode, desc="", color="white",
                 debut=None, duree=None, rep=-1, nbrep = 0, parent = None):
        """
        @param nom : nom de la tâche.
        @param periode: Période de la tâche, peut être None.
        @param desc : description.
        @param color: couleur avec un nom compatible avec les noms de couleurs tkinter.
        @param debut : datetime. du début.
        @param duree : datetime.
        @param rep : répétition.
        @param nbrep : nombre de répétitions.
        """
        # Constructeur parent :
        super().__init__(nom, periode, desc, color)
        
        # Informations temporelles :
        self.__debut = (debut + datetime.timedelta()) if debut is not None else None # Faire une copie
        self.__duree = (duree + datetime.timedelta()) if duree is not None else None
        
        # Informations des répétitions :
        self.__rep   = rep    # répétition
        self.__nbrep = nbrep  # nombre de répétitions
        
        # Parent : Garde-t-on cela ?
        self.__parent = parent

        # Liste des dependancies pour les liens
        self.__dependances = []
        self.__dependantes = []

        self.updateStatut()

        if self.isContainer():
            # Attribut présent que quand on est un conteneur : est-ce une bonne idée ?
            self.__subtasks = []

    def __str__(self):
        """Return a nice string representation of this object."""
        return "Task: %s, from %s to %s, %s"%(self.getNom(), self.getDebut() or "Unknown", self.getFin() or "Unknown", self.getStatut())

    "" # Marque pour repli de code

    #######################################################
    # Méthode de l'interface ITaskEditorDisplayableObject #
    # implémentée par la superclasse de cette classe :    #
    #######################################################
    def getHeader(self):
        return self.getNom(), self._statut

    def iterateDisplayContent(self, displayDependances = True, displayDependantes = True):
        # Note : on yield par paires.
        if not self.isContainer():
            yield "Début :",           self.getDebut()
            yield "Durée :",           self.getDuree()
            yield "Fin :",             self.getFin()
            yield "Nombre rep :",      self.__nbrep
            yield "Temps entre rep :", self.__rep
            if displayDependances:
                a = {
                    "displayDependances": True,
                    "displayDependantes": False
                }
                yield "Dépendances :", len(self.__dependances)
                yield a
                yield from self.__dependances
            if displayDependantes:
                a = {
                    "displayDependances": False,
                    "displayDependantes": True
                }
                yield "Dépendantes :", len(self.__dependantes)
                yield a
                yield from self.__dependantes
        if self.__parent is None: # Ne pas répéter les descriptions identiques dans les sous-tâches.
            yield "Description :", self.getDescription()
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
        if not self.isContainer() and self.__parent is None:
            add("command", {"label":"Transformer en une tâche déplaçable", "command":lambda: self.transformToDnd(taskEditor, rmenu)})
            add("separator")
        # Dans tout les cas :
        add("command", {"label":"Supprimer %s"%self, "command": lambda: self.delete(taskEditor.getApplication())})
        return retour

    ""
    ########################################
    # Définition des méthodes abstraites : #
    # de la superclasse.                   #
    ########################################
    def delete(self, app):
        """Permet de supprimer définitivement cette tâche."""
        # TODO : Suppression des calendriers.
        if self.parent is None:
            app.getTaskEditor().supprimer(self)
        else:
            self.parent.removeSubTask(self)
            
            app.getTaskEditor().redessiner()

    def copy(self):
        """
        Permet d'obtenir une copie de la tâche
        @return une copie de la tâche.
        """
        t = Task(self.getNom(), self.getPeriode(), self.getDescription(), self.getColor(),
                 self.getDebut(), self.getDuree(), self.__rep, self.__nbrep, self.getParent())
        # Doit-on copier les dépendances et le statut ?
        t.__dependances = self.__dependances[:]
        t.updateStatut()
        # On retourne la copie :
        return t

    def updateStatut(self):
        """Permet de mettre à jour le statut de la tâche."""
        if self.getDebut() == None:
            self._statut = "Inconnu"
        
        # XXX : What's this ?
#        elif (self.getPeriode().getDateStatut() is not None and self.getDebut() < self.getPeriode().getDateStatut()):
#                self.statut = "Fait"
        else:
            self._statut = "À faire"

        if self.__nbrep != 0:
            self._statut = "Répétition"

        #self._statut = "Inconnu" if self.getDebut() == None else "À faire" if self.__nbrep == 0 else "Répétition"

    def createDisplayableInstance(self, frame, part):
        # Ici, on s'en fiche de la part.
        return DisplayableTask(frame, self)

    def getRawRepartition(self, displayedCalendar):
        return self.getRepartition(displayedCalendar)

    def getRepartition(self, displayedCalendar):
        if self.getDebut().date() == self.getFin().date():
            yield DatetimeItemPart(self.getDebut().date(),
                                   self.getDebut().time(),
                                   self.getFin().time(),
                                   self)
        else:
            debutJour = datetime.time(0, 0, 0)
            finJour   = datetime.time(23, 59, 59)

            date = self.getDebut().date()
            heure1 = self.getDebut().time()
            heure2 = finJour

            while date < self.getFin().date():
                yield DatetimeItemPart(date, heure1, heure2, self)
                heure1 = debutJour
                date += datetime.timedelta(days = 1)

            heure2 = self.getFin().time()

            yield DatetimeItemPart(date, heure1, heure2, self)

    ""
    ##############
    # Container: #
    ##############
    def isContainer(self):
        """Permet de savoir si cette tâche est une tâche conteneur."""
        self.updateStatut()
        if self._statut == "Inconnu" and not hasattr(self, "subtasks"):
            self.subtasks = []
        return self._statut == "Inconnu"

    def addSubTask(self, task):
        """Il est impératif de gérer la suppression de la tâche dans TaskEditor depuis l'extérieur."""
        if not self.isContainer():
            raise ValueError("Impossible de rajouter une tâche dans une tâche non conteneur.")
        if task.isContainer():
            raise ValueError("Impossible de rajouter une tâche conteneur dans une autre tâche conteneur")
        if task.__parent is not None:
            raise ValueError("Impossible de rajouter une tâche dans un conteneur, sachant qu'elle est déjà présente dans un autre conteneur")
        self.subtasks.append(task)
        task.__parent = self    # Possible, au vu que ce sont des objets de même type.

    def removeSubTask(self, task):
        if not self.isContainer():
            raise ValueError("Impossible d'enlever une tâche d'une tâche non conteneur.")
        if task.__parent != self:
            raise ValueError("Impossible d'enlever une tâche d'un conteneur où cette tâche n'est pas présente.")
        self.subtasks.remove(task)
    
    def getSubTasks(self):
        if not self.isContainer():
            raise ValueError("Impossible d'obtenir les sous-tâches d'une tâche non conteneur.")
        return self.subtasks
    
    def getParent(self):
        """Retourne la tâche conteneur qui contient cette tâche (si ce conteneur existe)."""
        return self.__parent

    ""
    #################
    # Dépendances : #
    #################
    def addDependance(self, task):
        """
        Permet d'ajouter une dépendance à cette tâche,
        c'est-à-dire que notre tâche (self) dépendra de
        cette nouvelle task.
        @param task: la tâche dont celle-ci va dépendre.
        """
        self.__dependances.append(task)
        task.__dependantes.append(self)

    def removeDependance(self, task):
        """
        Permet d'enlever une dépendance à cette tâche,
        c'est-à-dire que notre tâche (self) dépendra de
        cette nouvelle task.
        @param task: la tâche dont celle-ci dépendait.
        """
        self.__dependances.remove(task)
        task.__dependantes.remove(self)

    def getDependances(self):
        """
        Permet d'obtenir une copie de la liste des tâches
        dont dépend cette tâche.
        @return: une copie de cette liste.
        """
        return self.__dependances[:]

    def getDependantes(self):
        """
        Permet d'obtenir une copie de la liste des tâches
        dépendant de cette tâche.
        @return une copie de la liste des tâches dépendantes.
        """
        return self.__dependantes[:]

    ""
    ###########################
    # Méthode "temporelles" : #
    ###########################

    def getDebut(self):
        """
        Getter pour le début de la tâche.
        @return un datetime.datetime() correspondant au début de cette tâche si elle en a un.
        @return None si cette tâche n'a pas de début.
        """
        return self.__debut + datetime.timedelta() if self.__debut is not None else None # Faire une copie et vérifier les trucs

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
            self.__debut = debut + datetime.timedelta() # Faire une copie de la date
            self.__duree = fin - self.getFin()
        elif change == "fin":
            self.__debut = debut + datetime.timedelta() # Faire une copie de la date
        else:
            raise ValueError('Mauvaise valeur à changer : %s, seulement "duree" et "fin" sont possibles.'%change)

    def getDuree(self):
        """
        Getter pour la Durée de la tâche.
        @return un datetime.timedelta() correspondant à la durée de la tâche.
        """
        return self.__duree + datetime.timedelta() # Faire une copie

    def getFin(self):
        """
        Getter pour la fin de la tâche.
        @return un datetime.datetime() correspondant à la fin de la tâche si il existe.
        @return None si la tâche n'as pas de début (en vrai c'est qu'elle n'as pas de fin).
        """
        return (self.__debut + self.__duree) if self.__debut is not None else None

    ""
    ####################
    # Autre méthodes : #
    ####################

    def transformToDnd(self, taskEditor, rmenu):
        """
        Permet de transformer cette tâche en une tâche déplaçable,
        c'est-à-dire une tâche conteneur. En vrai, ce sera une
        nouvelle tâche, avec comme contenu cette tâche ici présente.
        
        @param taskEditor: Référence vers le TaskEditor pour pouvoir
        faire les opérations.
        @param rmenu: référence vers le RMenu de cet tâche en tant
        qu'item du TaskEditor. Nécessaire pour l'opération.
        """
        # On supprime le RMenu pour le recréer après
        # dans le TaskEditor via notre méthode getRMenuContent()
        # car il va être différent.
        rmenu.destroy()
        del rmenu
        
        # On s'enlève du TaskEditor, mais on ne se supprime pas
        # attention. On va juste se réajouter ailleurs...
        taskEditor.supprimer(self)
        
        # On crée une tâche qui nous ressemble, mais dont le début
        # n'est pas présent. Et pour cause : c'est ce qui fait que
        # ça devient une tâche conteneur. On peut alors s'y ajouter.
        newTask = self.copy()
        newTask.__debut = None
        newTask.updateStatut()
        newTask.addSubTask(self)
        
        # Le fait de rajouter cette nouvelle tâche va nous rajouter
        # indirectement. Je vous avais bien dit qu'on ne se supprimait pas !
        taskEditor.ajouter(newTask)

#    def getFilterStateWith(self, filter):
#        # Si non autorisé par le filtre :
#        if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
#        or ("type" in filter and not "Tâche" in filter["type"]): # TODO : Ajouter tâches indépendantes.
#            return -1
#        # Filtre prioritaire ?
#        if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
#            return 1
#        # Sinon : autorisé par le filtre, mais pas prioritaire.
#        return 0

    def getGroupes(self):
        """
        Retourne une liste ? de groupe auxquelles appartient la tache.
        """
        listeGroupe = []
        for groupe in self.getPeriode().getGroupeManager().getGroupes():
            if tache in groupe.getListTasks():
                listeGroupe.append(groupe)
        return listeGroupes

#    def reverseStateValide(self):
#        self.__statutValideManuel = not self.__statutValideManuel
#        self.updateStatut()
