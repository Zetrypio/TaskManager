# -*- coding:utf-8 -*-
import datetime

from task.ITaskEditorDisplayableObject import *

from .dialog.periodDialog import *
from .dialog.decalerPeriodDialog import *
from .dialog.scinderPeriodDialog import *

class Periode(ITaskEditorDisplayableObject):
    def __init__(self, periodManager, nom, debut, fin, desc, color = "white"):
        self.periodManager = periodManager
        self.nom = nom
        self.debut = debut + datetime.timedelta()
        self.fin = fin + datetime.timedelta()
        self.desc = desc
        self.color = color
        self.selected = False
        # Doit-on faire une liste des tâches contenues ? je pense pas, mais on pourras l'obtenir avec une méthode...

    def __str__(self):
        return "Periode: %s, from %s to %s"%(self.nom, self.debut or "Unknown", self.getFin() or "Unknown")

    def getColor(self):
        return self.color

    def getDebut(self):
        return self.debut + datetime.timedelta() # Faire une copie de la date
    def getDuree(self):
        return self.fin - self.debut
    def getFin(self):
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
            raise ValueError('Mauvaise valeure à changer : %s, seulement "duree" et "fin" sont possibles.'%change)
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
        return (self.getDebut() >= periode.getDebut() and self.getDebut() <= periode.getFin()) \
            or (periode.getDebut() >= self.getDebut() and periode.getDebut() <= self.getFin())

    def isSelected(self):
        return self.selected
    def setSelected(self, value):
        self.selected = value
    
    def isActuelle(self):
        return self.debut >= datetime.datetime.now().date() and self.debut <= datetime.datetime.now().date()

    def getHeader(self):
        return self.nom, self.isActuelle()
    def iterateDisplayContent(self):
        yield "Debut :", self.debut
        yield "Durée :", self.getDuree()
        yield "Fin :", self.fin
        yield "Description :", self.desc

    def getRMenuContent(self, taskEditor, rmenu):
         # Mise en place de simplicitées :
        retour = []
        add = lambda a, b=None: retour.append((a, b if b else {}))
        
        # Ajout des menus :
        add("command", {"label":"Supprimer %s"%self, "command": lambda: self.periodManager.supprimer(self)})
        return retour
    
    def getFilterStateWith(self, filter):
        # Si non autorisé par le filtre :
        if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
        or ("type" in filter and not "Période" in filter["type"]):
            return -1
        # Filtre prioritaire ?
        if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
            return 1
        # Sinon : autorisé par le filtre, mais pas prioritaire.
        return 0
