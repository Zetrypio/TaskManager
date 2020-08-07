# -*- coding:utf-8 -*-
import datetime

from schedulable.groupe.Groupe import *
from schedulable.task.ITaskEditorDisplayableObject import *
from schedulable.task.Task import *

from util.util import *

from .dialog.modifierPeriodDialog import *
from .dialog.dupliquerPeriodDialog import *
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
        self.__primitivesSchedulables = []   # Liste des objets primitifs | natifs
        self.__instanciatedSchedulables = [] # Liste des objets instanciés

        self.uniqueID = self.setUniqueID() # Pour le calendrier des périodes sinon ça bug

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

        def chercheTask(id, p):
            """
            Fonction embarquée qui recherche la tache lié à l'id
            Pour l'instant seule les task ont un UUID
            @param id : <str> id de la tache qu'on cherche
            @param p  : <periode> celle qui contient la tache
            @return <task> recherché, None si non trouvé
            """
            for t in p.getPrimitivesSchedulables():
                if isinstance(t, Task) and id == t.getUniqueID():
                    return t

        ## On crée la période.
        p = Periode(periodManager,
                    data["nom"],
                    strToDate(data["debut"]),
                    strToDate(data["fin"]),
                    data["desc"],
                    data["color"])

        ## On crée ses schedulables standards
        for dataSchedulable in data["schedulables"]:
            # Si c'est un groupe :
            if "listTasks" in dataSchedulable:
                g = Groupe.load(dataSchedulable, p)
                p.addPrimitiveSchedulable(g)

            # Sinon c'est une tâche standard :
            else :
                t = Task.load(dataSchedulable, p)
                p.addPrimitiveSchedulable(t)

        ## Maintenant on passe au lien de dépendances :
        for s in data["schedulables"]:
            # S'il y a des dépendances :
            if "dependance" in s and s["dependance"] is not None:
                for dep in s["dependance"]:
                    chercheTask(s['id'], p).addDependance(chercheTask(dep, p))

        return p

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
        return self.periodManager.getApplication()

    def getColor(self):
        """
        Getter pour la couleur native d'affichage de l'objet.
        Par native, j'entend que ça ne prend pas en compte la couleur
        de sélection si jamais c'est sélectionné ou non.
        @return la couleur native d'affichage de l'objet.
        """
        return self.color

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

    def getPrimitivesSchedulables(self):
        """
        Getter pour la liste des objets planifiables primitifs, c'est-à-dire y compris ceux qui ne sont que dans le TaskEditor (dnd).
        @return une copie de la liste des schedulables primitifs.
        """
        return self.__primitivesSchedulables[:]

    def getInstanciatedSchedulables(self):
        """
        Getter pour la liste des schedulables
        @return une copie de la liste des schedulables instanciés.
        """
        return self.__instanciatedSchedulables[:]

    def getNom(self):
        """
        Getter pour le nom de la période
        @return le nom
        """
        return self.nom

    def getDescription(self):
        return self.desc

    def getUniqueID(self):
        """
        Getter pour l'unique Id
        @return l'uniqueID
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

    def setNom(self, nom):
        self.nom = nom

    def setDescription(self, description):
        self.desc = description

    def setColor(self, color):
        self.color = color

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
    def addInstanciatedSchedulable(self, schedulable):
        """
        Permet d'ajouter un objet planifiable à la liste des objets planifiables 
        @param schedulable: le schedulable à rajouter.
        """
        # Si c'est une période on va pas le rajouter....
        if not isinstance(schedulable, AbstractSchedulableObject):
            raise RuntimeError("Seul des objets planifiables peuvent aller dans la liste des objets planifiables instanciés.")
        self.__instanciatedSchedulables.append(schedulable)

        # FIXME : revoir pour être certain : OK il faut gérer la région, ailleurs.
        # On l'ajoute à tous le monde
        # Important pour les calendriers, car enfaite c'est un (schedulable OK)

        self.getApplication().getDonneeCalendrier().addSchedulable(schedulable)

    def addPrimitiveSchedulable(self, schedulable):
        """
        Méthode qui ajoute l'objet à une liste des schedulables à afficher dans le task editor
        @param schedulable : l'AbstractSchedulableObject à ajouter.
        """
        # Si c'est une période on va pas le rajouter....
        if not isinstance(schedulable, AbstractSchedulableObject):
            raise RuntimeError("Seul des objets planifiables peuvent aller dans la liste des objets planifiables primitifs.")
        self.__primitivesSchedulables.append(schedulable)

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

    def removeInstanciatedSchedulable(self, schedulable):
        """
        Permet de retirer un objet planifiable de la liste des schedulables instanciés.
        @param schedulable : AbstractSchedulableObject à enlever.
        """
        self.__instanciatedSchedulables.remove(schedulable)

        # TODO : revoir pour être certain :
        self.getApplication().getDonneeCalendrier().removeSchedulable(schedulable)

    def removePrimitiveSchedulable(self, schedulable):
        """
        Permet d'enlever un objet planifiable de la liste des schedulables primitifs.
        @param obj: L'objet à enlever.
        """
        self.__primitivesSchedulables.remove(schedulable)

    def resetInstanciatedSchedulables(self):
        """
        Permet de reset les schedulables instanciés.
        """
        self.__instanciatedSchedulables.clear()

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
            "schedulables"    : [schedulable.saveByDict() for schedulable in self.getPrimitivesSchedulables()]
            }
