# -*- coding:utf-8 -*-
from affichages.items.DatetimeItemPart import *

from ..AbstractSchedulableObject import *
from ..task.Task import *
from .dialog.askEditGroupe import askEditGroupe

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
        self.__listTasks = set(listTasks) # Un set supprime toujours les doublons.

    "" # Marque pour repli de code

    def __str__(self):
        """Return a nice string representation for Groupe()s objects."""
        return "Groupe %s, contenant %s tâches."%(self.getNom(), len(self.__listTasks))

    ""
    ###############################
    # Constructeurs alternatifs : #
    ###############################
    ""
    @staticmethod
    def load(data, periode, mapChangementUID):
        """
        Constructeur alternatif des groupes, via lecture d'un json.
        Normalement la lecture d'un json donné via la méthode saveByDict()
        doit redonner une copie complète et profonde de ce groupe.
        @param data: le json à lire.
        @param periode: la période du groupe.
        @param mapChangementUID: map des changements d'ID pour garder une trace
        @return le groupe.
        """
        # Création de l'instance :
        g = Groupe(data["nom"], periode, data["desc"], data["color"])

        # Ajout des sous-tâches :
        for t in data["listTasks"]:
            g.addTask(Task.load(t, periode, mapChangementUID))

        # Indication de correction de l'UID
        mapChangementUID[int(d["id"])] = g.getUniqueID()

        return g

    ""
    ################################
    # Méthode de l'interface       #
    # ITaskEditorDisplayableObject #
    ################################
    ""
    def getDebut(self):
        """
        Le début de ce groupe, à savoir le début de la tâche qui commence le plus tôt.
        @return datetime.datetime() du début de ce groupe.
        """
        return min(self.__listTasks, key=lambda  t:t.getDebut()).getDebut()

    def getFin(self):
        """
        La fin de ce groupe, à savoir la fin de la tâche qui termine le plus tard.
        @return datetime.datetime() de la fin de ce groupe.
        """
        return max(self.__listTasks, key=lambda  t:t.getFin()).getFin()

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
    
    def setAllDone(self, value):
        """
        Permet de valider le groupe, en validant toutes les tâches contenues dans le groupe.
        @param value: True si il faut valider le groupe, False sinon, selon Task#setDone().
        """
        for t in self.getListTasks():
            t.setDone(value)

    def setDone(self, value):
        """
        Permet de valider le groupe, en validant toutes les tâches contenues dans le groupe.
        @param value: True si il faut valider le groupe, False sinon, selon Task#setDone()
        @return changed : <list Task> liste des taches qui n'étaient pas faites avant (pour l'undo-redo)
        """
        changed = []
        for t in self.getSelectedTask():
            if t.isDone() != value: # vérifie on doit changer son état sinon pas besoin
                changed.extend(t.setDone(value))
        return changed

    #def getFilterStateWith(self):
        #"""
        #Permet de savoir l'état de filtrage de cet objet selon le filtre donné
        #lors de l'affichage de cet objet dans le Treeview() du TaskEditor().
        #@param filter: Dictionnaire du filtre.
        #@return -1 si l'élément n'est pas filtré, 1 si il est prioritaire, et 0 sinon.
        #@specified by getFilterStateWith(filter) in ITaskEditorDisplayableObject().
        #"""
        #pass # TODO

    def setRMenuContent(self, taskEditor, rmenu):
        """
        Permet de rajouter les commandes au RMenu() de cet objet si il est présent.
        Si cet objet n'a pas besoin de RMenu() dans le TaskEditor(), il faut simplement
        que cette méthode retourne False
        @param taskEditor : permet de faire des interactions avec le TaskEditor().
        @param rmenu : le RMenu() sur lequel rajouter les commandes et tout et tout.
        @return True car le RMenu() existe.
        @specified by getRMenuContent() in ITaskEditorDisplayableObject().
        """
        rmenu.add_command(label = "Éditer %s"%self.getNom(), command = lambda : askEditGroupe(self))
        rmenu.add_command(label = "Supprimer %s"%self, command = lambda : self.delete())
        return True

    ""
    #######################################
    # Méthode abstraite de la superclasse #
    # AbstractSchedulableObject           #
    #######################################
    ""
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

    def createDisplayableInstance(self, frame, part):
        """
        Permet de créer une instance de la version affichable d'un groupe.
        @param frame: master du tkinter.Frame() qu'est l'objet créé par cette méthode.
        @param part: DatetimeItemPart() nécessaire pour savoir quelle partie du groupe à afficher.
        """
        return DisplayableGroup(frame, self, part)

    def copy(self):
        """
        Permet de copier ce groupe.
        TODO
        """
        pass # TODO

    def delete(self):
        """
        Permet de supprimer définitivement ce groupe et ses tâches
        """
        # On commence par supprimer toutes les tâches
        for tache in self.getListTasks():
            tache.delete()
        # Et on se supprime
        self.getPeriode().removeInstanciatedSchedulable(self) if self in self.getPeriode().getInstanciatedSchedulables() else None
        self.getPeriode().removePrimitiveSchedulable(self) if self in self.getPeriode().getPrimitivesSchedulables() else None
        self.getApplication().getTaskEditor().redessiner()

    def getRawRepartition(self, displayedCalendar):
        """
        @see AbstractSchedulableObject#getRawRepartition(displayedCalendar)
        @override AbstractSchedulableObject#getRawRepartition(displayedCalendar)
        """
        if self.isVisible():
            for task in self.__listTasks:
                yield from task.getRepartition(displayedCalendar)

    def getRepartition(self, displayedCalendar):
        """
        @see AbstractSchedulableObject#getRepartition(displayedCalendar)
        @override AbstractSchedulableObject#getRepartition(displayedCalendar)
        """
        if self.isVisible():
            parts = []
            for task in self.__listTasks:
                parts += task.getRepartition(displayedCalendar)
            parts.sort(key = lambda p: p.getDebut())
            i = 0
            while i < len(parts)-1:
                if self.__canPartsBeOne(displayedCalendar, parts[i], parts[i+1]):
                    parts[i:i+2] = [DatetimeItemPart(parts[i+0].getJour(),
                                                     min(parts[i+0].getHeureDebut(), parts[i+1].getHeureDebut()),
                                                     max(parts[i+0].getHeureFin(),   parts[i+1].getHeureFin()),
                                                     self)]
                    i-=1
                i += 1
            yield from parts

    def instantiate(self):
        """
        Permet de se rajouter aux objets instanciés de la période.
        """
        self.getPeriode().addInstanciatedSchedulable(self)

    def setSelected(self, selected, andInside=False):
        """
        Permet de sélectionner ou désélectionner cet objet.
        Si andInside est sur True, affecte aussi les sous-tâches.
        @param selected: True si l'objet doit être sélectionné, False sinon.
        @param andInside: True si on affecte aussi les sous-tâches.
        @override setSelected(value) in AbstractSchedulableObject.
        """
        super().setSelected(selected, andInside)
        if andInside:
            for t in self.__listTasks:
                t.setSelected(selected, andInside)

    def updateStatut(self):
        """
        Permet de mettre à jour le statut de ce groupe.
        """
        self._statut = "Fait" if not any(not t.isDone() for t in self.__listTasks)\
                  else "En cours" if any(t.isDone() for t in self.__listTasks)\
                  else "En retard" if any(t.getStatut()=="En retard" for t in self.__listTasks)\
                  else "À Faire"

    ""
    ####################
    # Autre méthodes : #
    ####################
    ""
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
        if partA.getFin() > partB.getDebut():
            return True
        for part in displayedCalendar.getPartsOfDay(partA.getJour()):
            if part.getSchedulable() is not self and part.getSchedulable() not in self.__listTasks:
                if part.intersectWith(partA) or part.intersectWith(partB):
                    return False
                if part.getDebut() > partA.getFin() and part.getFin() < partB.getDebut():
                    return False
        return True           

    def addTask(self, task):
        """
        Permet d'ajouter une tâche à la liste du groupe.
        @param task: la tâche à ajouter à la liste.
        """
        self.__listTasks.add(task)
        task.setGroupe(self)

    def getListTasks(self):
        """
        Getter des tâches du groupe.
        @return une copie de la liste des tâches de ce groupe.
        """
        return self.__listTasks.copy()

    def getSelectedTask(self):
        """
        Permet de d'obtenir les sous-tâches qui sont sélectionnées dans le groupe.
        @return un générateur avec les sous-tâches qui sont sélectionnées dans le groupe.
        """
        return (t for t in self.__listTasks if t.isSelected())

    def removeTask(self, task, testDelete = True):
        """
        Permet de retirer une tâche de la liste du groupe.
        @param task: la tâche à enlever de la liste.
        @param testDelete : <bool> Doit-on vérifier si on veux supprimer le groupe
        """
        self.__listTasks.remove(task)
        task.removeGroupe()
        if testDelete and self.getListTasks() == set():
            self.delete()

    def setPeriode(self, periode):
        """
        Setter pour la période de ce groupe.
        @param periode: la Période à mettre.
        @override setPeriode(periode) in AbstractSchedulableObject.
        """
        super().setPeriode(periode)

    ""
    #######################################
    # Méthodes liées à l'enregistrement : #
    #######################################
    ""
    def saveByDict(self, saveID = True):
        """
        Méthode qui sauvegarde les attributs présent dans la classe "Groupe" (ici)
        @param saveID : <bool> True on enregistre l'UID actuel
        @save listTasks : <list Task> contient les taches du groupe
        @return dico <dict> contient les couples clé-valeur ci-dessus
        """
        dico = {}
        dico = super().saveByDict(saveID)
        dico["listTasks"] = [task.saveByDict(saveID = saveID) for task in self.getListTasks()]
        return dico

# L'import est à la fin pour éviter les soucis circulaires d'imports (un vrai cauchemar).
from affichages.items.content.DisplayableGroup import *
