# -*- coding:utf-8 -*-

from ..AbstractSchedulableObject import *

class Groupe(AbstractSchedulableObject):
    def __init__(self, nom, periode, desc, color, *listTasks):
        """
        Constructeur d'un groupe.
        Il est possible de rajouter ou d'enlever des tâches après coup
        avec les méthodes addTask() et removeTask().
        @param nom: Nom du groupe.
        @param periode: Période du groupe.
        @param desc: Description du groupe.
        @param color: Couleur du groupe pour l'affichage.
        @param *listTasks: liste des tâches à inclure automatiquement dans le groupe.
        """
        super().__init__(nom, periode, desc, color)
        
        # Attributs :
        self.__groupeManager = periode.getGroupeManager()
        self.__listTasks = set(listTasks) # Un set supprime toujours les doublons.

    "" # Marque pour repli de code

    ################################
    # Méthode de l'interface       #
    # ITaskEditorDisplayableObject #
    ################################
    def getHeader(self):
        pass # TODO
    
    def iterateDisplayContent(self):
        pass # TODO
    
    def getRMenuContent(self, taskEditor, rmenu):
        pass # TODO
    
    def getFilterStateWith(self):
        pass # TODO
    
    ""
    #######################################
    # Méthode abstraite de la superclasse #
    # AbstractSchedulableObject           #
    #######################################
    def delete(self, app):
        pass # TODO

    def copy(self):
        pass # TODO

    def updateStatut(self):
        pass # TODO
    
    ""
    ####################
    # Autre méthodes : #
    #####################

    def getGroupeManager(self):
        """
        Getter pour le groupe Manager.
        @return le GroupeManager de ce groupe.
        """
        return self.groupeManager

    def setGroupeManager(self, groupeManager):
        """ Setter du groupe Manager """
        self.groupeManager = groupeManager
        self.setPeriode(groupeManager.getPeriode())

    def setPeriode(self, periode):
        """
        Setter pour la période de ce groupe.
        @param periode: la Période à mettre.
        @override setPeriode(periode) in AbstractSchedulableObject.
        """
        super().setPeriode(periode)
        self.__groupeManager = periode.getGroupeManager()

    def getListTasks(self):
        """ Getter des taches du groupe. """
        return self.listTasks[:]

    def addTask(self, task):
        """ Ajoute une task à la liste du groupe """
        self.listTasks.add(task)

    def removeTask(self, task):
        """ Retire une tache de la liste du groupe """
        self.listTasks.remove(task)

