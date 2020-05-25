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
        return self.getNom(), self._statut
    
    def iterateDisplayContent(self):
        yield "Tâches", len(self.__listTasks)
        yield {}
        yield from sorted(self.__listTasks, key=lambda t:t.getDebut())
    
    def getRMenuContent(self, taskEditor, rmenu):
        pass # TODO
    
#    def getFilterStateWith(self):
#        pass # TODO
    
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

    def createDisplayableInstance(self, frame, part):
        return DisplayableGroup(frame, self, part)

    def getRepartition(self, displayedCalendar):
        previous = None
        for task in sorted(self.__listTasks, key=lambda t: t.getDebut()):
            for part in task.getRepartition():
                if previous is None:
                    previous = part
                elif self.__canPartsBeOne(previous, part):
                    previous = DatetimeItemParts(previous.getJour(),
                                                 previous.getHeureDebut(),
                                                 part    .getHeureFin())
                else:
                    yield previous
            yield part

    def __canPartsBeOne(self):
        """
        Permet de savoir si 2 DatetimeItemParts peuvent être une seule,
        connaissant le fait que si il y quelque chose entre les 2, ça ne
        peut pas se fusionner.
        """
        # TODO
        return False
                    

    ""
    ####################
    # Autre méthodes : #
    ####################

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
