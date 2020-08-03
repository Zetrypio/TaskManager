# -*- coding:utf-8 -*-
import datetime

from schedulable.groupe.GroupeManager import *
from schedulable.task.ITaskEditorDisplayableObject import *
from schedulable.task.Task import *
from schedulable.task.dialog.askDureeTache import *

from util.util import *

from .dialog.dupliquerPeriodDialog import *
from .dialog.modifierPeriodDialog import *
from .dialog.decalerPeriodDialog import *
from .dialog.scinderPeriodDialog import *

class Periode(ITaskEditorDisplayableObject):
    """
    Classe représentant une période.
    """
    def __init__(self, periodManager, nom, debut, fin, desc, color = "white"):
        """
        Constructeur de la période.
        @param periodManager: Gestionnaire de période.
        @param nom: Nom de la période.
        @param debut: datetime.date() de début de la période.
        @param fin: datetime.date() de fin de la période.
        @param desc: Description de la période.
        @param color = "white": Couleur d'affichage de la période.
        """
        self.periodManager = periodManager
        self.nom = nom
        self.debut = debut + datetime.timedelta()
        self.fin = fin + datetime.timedelta()
        self.desc = desc
        self.color = color
        self.selected = False

        # Listes :
        self.listSchedulables = []
        self.listAllThingsInPeriod = [] # Liste faite pour le taskEditor et l'enregistrement

        # datetime avant lequel tout est fait
        self.dateStatut = None

        # Création d'un groupe manager de la période
        self.groupeManager = GroupeManager(self.periodManager.getApplication(), self)

        self.uniqueID = self.setUniqueID()# Pour le calendrier des périodes sinon ça bug

    def __str__(self):
        """Return a nice string representation for Period objects."""
        return "Période: %s, de %s à %s"%(self.nom, self.debut or "Unknown", self.getFin() or "Unknown")

    "" # Marque pour le repli de code
    ##############################
    # Constructeur alternatifs : #
    ##############################
    ""
    @staticmethod
    def load(data, periodManager):
        return Periode(periodManager,
                       data["nom"],
                       strToDate(data["debut"]),
                       strToDate(data["fin"]),
                       data["desc"],
                       data["color"])

    ""
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'Application
        @return l'application
        """
        return self.getGroupeManager().getApplication()

    def getColor(self):
        """
        Getter pour la couleur native d'affichage de l'objet.
        Par native, j'entend que ça ne prend pas en compte la couleur
        de sélection si jamais c'est sélectionné ou non.
        @return la couleur native d'affichage de l'objet.
        """
        return self.color

    def getDateStatut(self):
        """
        Getter de la datetime clé
        @deprecated: On va complètement changer ce système.
        """
        return self.dateStatut

    def getDebut(self):
        """
        Getter pour le début de la période.
        @return datetime.date() correspondant au début de la période.
        """
        return self.debut + datetime.timedelta() # Faire une copie de la date

    def getDuree(self):
        """
        Permet d'obtenir la durée de la période.
        @return datetime.timedelta() correspondant à la durée de la période.
        """
        return self.fin - self.debut

    def getFilterStateWith(self, filter):
        """
        Permet de savoir l'état de filtrage de cet objet selon le filtre donné
        lors de l'affichage de cet objet dans le Treeview() du TaskEditor().
        @param filter: Dictionnaire du filtre.
        @return -1 si l'élément n'est pas filtré, 1 si il est prioritaire, et 0 sinon.
        @specified by getFilterStateWith(filter) in ITaskEditorDisplayableObject().
        """
        # Si non autorisé par le filtre :
        if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
        or ("type" in filter and not "Période" in filter["type"]):
            return -1
        # Filtre prioritaire ?
        if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
            return 1
        # Sinon : autorisé par le filtre, mais pas prioritaire.
        return 0

    def getFin(self):
        """
        Getter pour la fin de la période.
        @return datetime.date() correspondant à la fin de la période.
        """
        return self.fin + datetime.timedelta() # Faire une copie de la date

    def getGroupeManager(self):
        """
        Getter pour le gestionnaire de groupe de cette période.
        @return le GroupManager de cette période.
        """
        return self.groupeManager

    def getHeader(self):
        """
        Permet de donner la ligne d'entête de cet objet dans l'affichage du Treeview() du TaskEditor().
        @return le nom suivi de :
         - "En cours" si la période est actuelle (voire #isActuelle()) ;
         - "Prochainement" si la période n'est pas encore commencée ;
         - "Finie" si la période est déjà finie.
        @specified by getHeader() in ITaskEditorDisplayableObject().
        """
        return self.nom, "En cours" if self.isActuelle()\
                    else "Prochainement" if self.debut > datetime.datetime.now().date()\
                    else "Finie"

    def getListAllThingsInPeriod(self):
        """
        Getter pour la liste des choses (task, taches contenantes, groupes) pour le taskEditor et l'enregistrement
        @return la liste de self.listAllThingsInPeriod car on s'occupe de faire des tries dans TaskEditor
        """
        return self.listAllThingsInPeriod

    def getListSchedulables(self):
        """
        Getter pour la liste des schedulables
        @return un copy de self.listSchedulables
        """
        return self.listSchedulables[:]

    def getNom(self):
        """
        Getter pour le nom de la période
        @return le nom
        """
        return self.nom

    def getUniqueID(self):
        """
        Getter pour l'unique Id
        @reutrn l'uniqueID
        """
        return self.uniqueID

    def intersectWith(self, other):
        """
        Permet de savoir si cette période s'intersectionne avec une autre.
        @param other: la période dont on teste l'intersection avec celle-ci.
        @return True si les 2 périodes s'intersectionnent, False sinon.
        """
        return not (self.getFin() < other.getDebut() or self.getDebut() > other.getFin())

    def isActuelle(self):
        """
        Permet de savoir si la période est actuellement en cours,
        c'est à dire que le Maintenant est entre le début et la fin de cette période.
        @return True si la période est actuellement en cours, False sinon.
        """
        return self.debut >= datetime.datetime.now().date() and self.debut <= datetime.datetime.now().date()

    def isSelected(self):
        """
        Getter pour savoir si la période est sélectionnée dans l'affichage de calendrier des périodes.
        @return True si la période est sélectionnée dans l'affichage de calendrier des périodes, False sinon.
        """
        return self.selected

    ""
    #############
    # Setters : #
    #############
    ""
    def setDateStatut(self, datetime):
        """
        Setter du datetime de limite de statut.
        @deprecated: On va complètement changer ce système.
        """
        self.dateStatut = datetime

    def setDebut(self, debut, change = "duree"):
        """
        Permet de mettre le début de la période.
        @param debut: Le datetime.date du début de la période.
        @param change: Si "duree": change la durée mais pas la fin,
                       Si "fin": change la fin mais pas la durée.
                       Sinon : raise ValueError
        """
        if change == "duree":
            self.debut = debut + datetime.timedelta() # Faire une copie de la date
        elif change == "fin":
            duree = self.getDuree()
            self.debut = debut + datetime.timedelta() # Faire une copie de la date
            self.fin = self.debut + duree
        else:
            raise ValueError('Mauvaise valeur à changer : %s, seulement "duree" et "fin" sont possibles.'%change)

    def setFin(self, fin, change = "duree"):
        """
        Permet de mettre la fin de la période.
        @param debut: Le datetime.date de la fin de la période.
        @param change: Si "duree": change la durée mais pas la début,
                       Si "debut": change le début mais pas la durée.
                       Sinon : raise ValueError
        """
        if change == "duree":
            self.fin = fin + datetime.timedelta() # Faire une copie de la date.
        elif change == "debut":
            duree = self.getDuree()
            self.fin = fin + datetime.timedelta() # Faire une copie de la date
            self.debut = fin - duree
        else:
            raise ValueError('Mauvaise valeur à changer : %s, seulement "duree" et "debut" sont possibles.'%change)

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
        # Ajout des menus :
        rmenu.add_command(label="Supprimer %s"%self, command=lambda: self.periodManager.supprimer(self))
        return True

    def setSelected(self, value):
        """
        Setter pour indiquer si la période est sélectionnée dans l'affichage de calendrier des périodes.
        @param value: True si la période doit être sélectionnée, False sinon.
        """
        if not isinstance(value, bool): raise TypeError("Expected a boolean")
        self.selected = value

    def setUniqueID(self):
        """
        Permet d'ajouter un uniqueID à une période et de le mettre dans la liste
        qui vérifie s'il est bien unique
        @raise AttributeError si toute les possibilités ont été faites
        """
        id = str(self.__init__)[-12:-2]
        i = 0 # Stopper si on fait trop de boucles
        while id in self.getApplication().listKey:
            l = list(id)
            r = random.shuffle(l)
            id = ''.join(r)
            i+=1
            if i == 30:
                id += "htcfjgvkkjgyftcgvhbh"

            if i == 100:
                raise AttributeError

        self.getApplication().listKey.append(id)
        return id

    ""
    ######################
    # Méthodes liées aux #
    #    schedulables    #
    ######################
    ""
    def addSchedulable(self, schedulable, region = None):
        """
      - Permet d'ajouter un schedulable sur le panneau d'affichage.

      - Méthode à redéfinir dans les sous-classes, en appelant
        la variante parent (celle de SuperCalendrier), car celle-ci
        s'occuppe de mettre le schedulable dans la liste et de demander la durée
        à l'utilisateur quand celle-ci n'est pas définie (càd: elle est de 0).

      - Cependant, la suite doit être redéfinie dans les sous-classes pour gérer
        l'affichage de la tâche.

      - Et le plus important : la méthode doit renvoyer le schedulable avec sa durée prédéfinie.

      - Dans les sous-classes, ça donne :
        def addTask(self, schedulable, region = None):
            '''Permet d'ajouter une schedulable, region correspond au début de la tâche si celle-ci n'en a pas.'''
            if (schedulable := SuperCalendrier.addTask(self, schedulable, region)) == None: # region est géré dans la variante parent : on ne s'en occupe plus ici.
                return

            ####################
            # Ajout graphique. #
            ####################
            ... # Note : on utilisera très probablement une liste, non ?
            ... # et peut-être une classe particulière, défini dans le même fichier ?
            ... # Quand je dis une liste, c'est une liste différente de self.listeTask,
                # car celle-ci existe déjà, mais qui contiendrait les cadres/panneaux des classes
                # que l'on va créer pour cette représentation. Cependant, on pourrais dire, si
                # c'est possible, que cette classe pourrait être utilisée pour plusieurs dispositions
                # si celles-ci sont similaires. Mais chaque disposition pourra aussi avoir sa classe
                # d'affichage d'une tâche custom.

        @param schedulable: le schedulable à rajouter
        @param region: datetime.datetime() correspondant au début du schedulable si celui-ci n'en a pas (notamment le cas via Drag&Drop)
        @return le schedulable, potentiellement changé.
        @deprecated: va être renommé en addSchedulable()
        """
        ## Traitement du schedulable

        # Si le schedulable viens d'une tache de ListTaskUnplanified
        # À mettre avant de traiter le schdeulable
        """
        inListUnplanified = False
        if schedulable in self.getListTaskUnplanified():
            inListUnplanified = True
        """

        if region and schedulable.getDebut() is None:
            # Important pour ne pas altérer l'originelle :
            # Cela permet de pouvoir Drag&Drop une même tâche
            # plusieurs fois.
            schedulable = schedulable.copy()
            schedulable.setDebut(region)

        if isinstance(schedulable, Task) and schedulable.getDuree() <= datetime.timedelta():
            schedulable.setDuree(askDureeTache(self.getApplication(), self.getDuree() + datetime.timedelta(days = 1)))
            if not schedulable.getDuree():
                return None
        if schedulable is None :
            return

        ## On le rentre dans la liste
        self.listSchedulables.append(schedulable)

        # On l'ajoute à tous le monde
        # Important pour les calendriers, car enfaite c'est un (schedulable OK)
        self.getApplication().getDonneeCalendrier().addSchedulable(schedulable)
        return schedulable # Pour le dnd  "trouverPositionTache"

    def addItemInListAllThingsInPeriod(self, task):
        """
        Méthode qui ajoute l'objet à une liste des schedulables à afficher dans le task editor
        (pas complet manque les périodes, géré par le TaskEditor)
        @param task : <task>
        """

        # Si c'est une période on va pas le rajouter....
        if isinstance(task, Periode):
            return
        self.listAllThingsInPeriod.append(task)


    def iterateDisplayContent(self):
        """
        Permet de donner les lignes de contenu de cet objet dans l'affichage du Treeview() du TaskEditor().
        @yield "Début :" suivi de la date de début.
        @yield "Durée :" suivi de la durée.
        @yield "Fin :" suivi de la date de fin.
        @yield "Description :" suivi de la description.
        @specified by iterateDisplayContent() in ITaskEditorDisplayableObject().
        """
        yield "Début :", self.debut
        yield "Durée :", self.getDuree()
        yield "Fin :", self.fin
        yield "Description :", self.desc

    def removeItemInListAllThingsInPeriod(self, task):
        """
        Méthode qui retire l'objet à une liste des schedulables à afficher dans le task editor
        (pas complet manque les périodes, géré par le TaskEditor)
        @param task : <task>
        """
        self.listAllThingsInPeriod.remove(task)

    def removeSchedulable(self, schedulable):
        """
        Permet d'enlever un objet du calendrier.
        @param obj: L'objet à enlever.
        """
        if schedulable in self.getListSchedulables():
            self.listSchedulables.remove(schedulable)
        self.getApplication().getDonneeCalendrier().removeSchedulable(schedulable)

    ""
    ####################################
    # Méthodes pour l'enregistrement : #
    ####################################
    ""
    def saveByDict(self):
        """
        Méthode qui enregistre ce qu'elle peut de la période

        @save nom   : <str> contient le nom de la période
        @save debut : <date> du début de la période
        @save fin   : <date> fin de la période
        @save desc  : <str> contient la description de la période
        @save color : <str> contient la couleur de la période
        @save group : <task> contient les tack du groupe

        @return dico <dict> contient les couples clé-valeur ci-dessus
        """
        return {
            "nom"             : self.getNom(),
            "debut"           : dateToStr(self.getDebut()),
            "fin"             : dateToStr(self.getFin()),
            "desc"            : self.desc,
            "color"           : self.getColor(),
            "schedulables"    : [schedulable.saveByDict() for schedulable in self.getListAllThingsInPeriod()]
            }
