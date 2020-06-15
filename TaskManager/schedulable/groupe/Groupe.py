# -*- coding:utf-8 -*-

from affichages.items.DatetimeItemPart import *

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

    def __str__(self):
        """Return a nice string representation for Groupe()s objects."""
        return "Groupe %s, contient %s tâches."%(self.getNom(), len(self.__listTasks))

    ################################
    # Méthode de l'interface       #
    # ITaskEditorDisplayableObject #
    ################################
    def getHeader(self):
        """
        Permet de donner la ligne d'entête de cet objet dans l'affichage du Treeview() du TaskEditor().
        @return Le nom suivi du statut
        @specified by getHeader() in ITaskEditorDisplayableObject().
        """
        return self.getNom(), self._statut
    
    def iterateDisplayContent(self):
        """
        Permet de donner les lignes de contenu de cet objet dans l'affichage du Treeview() du TaskEditor().
        @yield Tâches suivi du nombre de tâches
        @yield from les tâches.
        @specified by iterateDisplayContent() in ITaskEditorDisplayableObject().
        """
        yield "Tâches", len(self.__listTasks)
        yield {}
        yield from sorted(self.__listTasks, key=lambda t:t.getDebut())
    
    def getRMenuContent(self, taskEditor, rmenu):
        """
        Permet de donner le contenu du RMemnu() de la ligne de cette objet dans le Treeview() du TaskEditor().
        @param taskEditor: le TaskEditor()
        @param rmenu: l'instance du RMenu() dont on ajoute du contenu.
        @return la liste des commandes nécessaire.
        @specified by getRMenuContent() in ITaskEditorDisplayableObject().
        """
        pass # TODO
    
    def getDebut(self):
        """
        Le début de ce groupe, à savoir le début de la tâche qui commence le plus tôt.
        @return datetime.datetime() du début de ce groupe.
        """
        return min(self.__listTasks, key=lambda  t:t.getDebut()).getDebut()
    
#    def getFilterStateWith(self):
#        """
#        Permet de savoir l'état de filtrage de cet objet selon le filtre donné
#        lors de l'affichage de cet objet dans le Treeview() du TaskEditor().
#        @param filter: Dictionnaire du filtre.
#        @return -1 si l'élément n'est pas filtré, 1 si il est prioritaire, et 0 sinon.
#        @specified by getFilterStateWith(filter) in ITaskEditorDisplayableObject().
#        """
#        pass # TODO
    
    ""
    #######################################
    # Méthode abstraite de la superclasse #
    # AbstractSchedulableObject           #
    #######################################
    def delete(self, app):
        """
        Permet de supprimer ce groupe.
        TODO
        """
        pass # TODO

    def copy(self):
        """
        Permet de copier ce groupe.
        TODO
        """
        pass # TODO

    def updateStatut(self):
        """
        Permet de mettre à jour le statut de ce groupe.
        TODO
        """
        pass # TODO

    def createDisplayableInstance(self, frame, part):
        """
        Permet de créer une instance de la version affichable d'un groupe.
        @param frame: master du tkinter.Frame() qu'est l'objet créé par cette méthode.
        @param part: DatetimeItemPart() nécessaire pour savoir quelle partie du groupe à afficher.
        """
        return DisplayableGroup(frame, self, part)

    def acceptLink(self):
        """
        Permet de savoir si l'objet peut être à l'origine d'un lien, sans se soucier
        de la destination pour le moment encore inconnu.
        @return True si l'objet est en capacité de faire des liens, False sinon.
        """
        return False

    def acceptLinkTo(self, schedulable):
        """
        Permet de savoir si un lien est possible entre cet objet et l'objet reçu, peut importe le sens.
        @param schedulable: l'autre objet dont on doit faire le lien avec cet objet.
        """
        return False

    def getRawRerpartition(self, displayedCalendar):
        """
        @see AbstractSchedulableObject#getRawRerpartition(displayedCalendar)
        @override AbstractSchedulableObject#getRawRerpartition(displayedCalendar)
        """
        for task in self.__listTasks:
            yield from task.getRepartition(displayedCalendar)

    def getRepartition(self, displayedCalendar):
        """
        @see AbstractSchedulableObject#getRerpartition(displayedCalendar)
        @override AbstractSchedulableObject#getRerpartition(displayedCalendar)
        """
        parts = []
        for task in self.__listTasks:
            parts += task.getRepartition(displayedCalendar)
        parts.sort(key = lambda p: p.getDebut())
        i = 0
        while i < len(parts)-1:
            if self.__canPartsBeOne(displayedCalendar, parts[i], parts[i+1]):
                parts[i:i+2] = [DatetimeItemPart(parts[i+0].getJour(),
                                                 parts[i+0].getHeureDebut(),
                                                 parts[i+1].getHeureFin(),
                                                 self)]
                i-=1
            i += 1
        yield from parts

    ""
    ####################
    # Autre méthodes : #
    ####################

    def __canPartsBeOne(self, displayedCalendar, partA, partB):
        """
        Permet de savoir si 2 DatetimeItemParts peuvent être une seule,
        connaissant le fait que si il y quelque chose entre les 2, ça ne
        peut pas se fusionner.
        @param displayedCalendar: Permet d'avoir des informations pour savoir
        la liste des parts déjà présentes.
        @param partA: la première part à fusionner avec la deuxième.
        @param partB: la deuxième part à fusionner avec la première.
        @return True si les parts peuvent se fusionner, False sinon.
        """
        if partA.getJour() != partB.getJour():
            return False
        if partA.getDebut() > partB.getDebut():
            partA, partB = partB, partA
        for part in displayedCalendar.getPartsOfDay(partA.getJour()):
            if part.getSchedulable() is not self and part.getSchedulable() not in self.__listTasks:
                if part.intersectWith(partA) or part.intersectWith(partB):
                    return False
                if part.getDebut() > partA.getFin() and part.getFin() < partB.getDebut():
                    return False
        return True           

    def getGroupeManager(self):
        """
        Getter pour le groupe Manager.
        @return le GroupeManager de ce groupe.
        """
        return self.groupeManager

    def setGroupeManager(self, groupeManager):
        """
        Setter du groupe Manager.
        @param groupeManager: le GroupeManager à mettre.
        """
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
        """
        Getter des tâches du groupe.
        @return une copie de la liste des tâches de ce groupe.
        """
        return self.listTasks[:]

    def addTask(self, task):
        """
        Permet d'ajouter une tâche à la liste du groupe.
        @param task: la tâche à ajouter à la liste.
        """
        self.listTasks.add(task)

    def removeTask(self, task):
        """
        Permet de retirer une tâche de la liste du groupe.
        @param task: la tâche à enlever de la liste.
        """
        self.listTasks.remove(task)

# L'import est à la fin pour éviter les soucis circulaires d'imports (un vrai cauchemar).
from affichages.items.content.DisplayableGroup import *
