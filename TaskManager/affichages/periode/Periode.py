# -*- coding:utf-8 -*-
import datetime

from schedulable.groupe.GroupeManager import *
from schedulable.task.ITaskEditorDisplayableObject import *

from .dialog.periodDialog import *
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

        # datetime avant lequel tout est fait
        self.dateStatut = None

        # Création d'un groupe manager de la période
        self.groupeManager = GroupeManager(self.periodManager.getApplication(), self)
        # Doit-on faire une liste des tâches contenues ? je pense pas, mais on pourra l'obtenir avec une méthode...

    def __str__(self):
        """Return a nice string representation for Period objects."""
        return "Période: %s, de %s à %s"%(self.nom, self.debut or "Unknown", self.getFin() or "Unknown")

    def getColor(self):
        """
        Getter pour la couleur native d'affichage de l'objet.
        Par native, j'entend que ça ne prend pas en compte la couleur
        de sélection si jamais c'est sélectionné ou non.
        @return la couleur native d'affichage de l'objet.
        """
        return self.color

    def getNom(self):
        return self.nom

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

    def getFin(self):
        """
        Getter pour la fin de la période.
        @return datetime.date() correspondant à la fin de la période.
        """
        return self.fin + datetime.timedelta() # Faire une copie de la date

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
        
    def intersectWith(self, periode):
        """
        Permet de savoir si cette période s'intersectionne avec une autre.
        @param periode: la période dont on teste l'intersection avec celle-ci.
        @return True si les 2 périodes s'intersectionnent, False sinon.
        """
        return not (self.getFin() < task.getDebut() or self.getDebut() > task.getFin())

    def getGroupeManager(self):
        """
        Getter pour le gestionnaire de groupe de cette période.
        @return le GroupManager de cette période.
        """
        return self.groupeManager

    def isSelected(self):
        """
        Getter pour savoir si la période est sélectionnée dans l'affichage de calendrier des périodes.
        @return True si la période est sélectionnée dans l'affichage de calendrier des périodes, False sinon.
        """
        return self.selected

    def setSelected(self, value):
        """
        Setter pour indiquer si la période est sélectionnée dans l'affichage de calendrier des périodes.
        @param value: True si la période doit être sélectionnée, False sinon.
        """
        if not isinstance(value, bool): raise TypeError("Expected a boolean")
        self.selected = value
    
    def setDateStatut(self, datetime):
        """
        Setter du datetime de limite de statut.
        @deprecated: On va complètement changer ce système.
        """
        self.dateStatut = datetime

    def isActuelle(self):
        """
        Permet de savoir si la période est actuellement en cours,
        c'est à dire que le Maintenant est entre le début et la fin de cette période.
        @return True si la période est actuellement en cours, False sinon.
        """
        return self.debut >= datetime.datetime.now().date() and self.debut <= datetime.datetime.now().date()

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

    def getRMenuContent(self, taskEditor, rmenu):
        """
        Permet de donner le contenu du RMemnu() de la ligne de cette objet dans le Treeview() du TaskEditor().
        @param taskEditor: le TaskEditor()
        @param rmenu: l'instance du RMenu() dont on ajoute du contenu.
        @return la liste des commandes nécessaire.
        @specified by getRMenuContent() in ITaskEditorDisplayableObject().
        """
         # Mise en place de simplicitées :
        retour = []
        add = lambda a, b=None: retour.append((a, b if b else {}))
        
        # Ajout des menus :
        add("command", {"label":"Supprimer %s"%self, "command": lambda: self.periodManager.supprimer(self)})
        return retour
    
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
