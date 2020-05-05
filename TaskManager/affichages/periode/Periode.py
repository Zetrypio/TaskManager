# -*- coding:utf-8 -*-
import datetime

from .dialog.periodDialog import *
from .dialog.decalerPeriodDialog import *
from .dialog.scinderPeriodDialog import *

class Periode:
    def __init__(self, nom, debut, fin, desc, color = "white"):
        self.nom = nom
        self.debut = debut + datetime.timedelta()
        self.fin = fin + datetime.timedelta()
        self.desc = desc
        self.color = color
        self.selected = False
        # Doit-on faire une liste des tâches contenues ? je pense pas, mais on pourras l'obtenir avec une méthode...

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
            self.fin += self.getDuree()
            self.debut = debut + datetime.timedelta() # Faire une copie de la date
        else:
            raise ValueError('Mauvaise valeure à changer : %s, seulement "duree" et "fin" sont possibles.'%change)
    def setFin(self, fin):
        self.fin = fin + datetime.timedelta() # Faire une copie de la date.
        
    def intersectWith(self, periode):
        return (self.debut >= periode.debut and self.debut <= periode.fin) \
            or (periode.debut >= self.debut and periode.debut <= self.fin)

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
