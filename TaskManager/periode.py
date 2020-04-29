# -*- coding:utf-8 -*-
import datetime
from tkinter.messagebox import *
from periodDialog import *
from decalerPeriodDialog import *
from scinderPeriodDialog import *

class Periode:
    def __init__(self, nom, debut, fin, desc, color = "white"):
        self.nom = nom
        self.debut = debut
        self.fin = fin
        self.desc = desc
        self.color = color
        self.selected = False
        # Doit-on faire une liste des tâches contenus ? je pense pas, mais on pourras l'obtenir avec une méthode...?
    def getDebut(self):
        return self.debut + datetime.timedelta() # Faire une copie de la date
    def getDuree(self):
        return self.fin - self.debut
    def getFin(self):
        return self.fin + datetime.timedelta() # Faire une copie de la date
    def getColor(self):
        return self.color
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
        
    def intersectWith(self, periode):
        return (self.debut >= periode.debut and self.debut <= periode.fin) \
            or (periode.debut >= self.debut and periode.debut <= self.fin)
    def isSelected(self):
        return self.selected
    def setSelected(self, value):
        self.selected = value


class PeriodManager:
    """Gestionnaire des périodes."""
    def __init__(self, app):
        self.app = app
        self.periodes = []
        self.taskEditor = None
    
    def setTaskEditor(self, taskEditor):
        self.taskEditor = taskEditor

    def getPeriodes(self):
        return self.periodes
    def ajouter(self, periode):
        self.periodes.append(periode)
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().updateAffichage()
    
    def getPeriodesSelectionnees(self):
        return [periode for periode in self.periodes if periode.isSelected()]

    # Fonctions de la barre d'outil :
    def deplacerPeriode(self):
        """Permet de déplacer la ou les périodes sélectionnées."""
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) == 1:
             askPeriode(self, self.taskEditor, from_ = periodes[0], duplicate = False)
        else:
            duree = askDureeJours()
            if duree is not None:
                for p in periodes:
                    p.setDebut(p.getDebut() + duree, change = "fin")
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().updateAffichage()

    def dupliquerPeriode(self):
        """Permet de duppliquer la période sélectionnée."""
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) != 1:
            showerror("Erreur de sélection", "Vous ne pouvez effectuer cette tâche qu'avec exactement une seule période sélectionnée.")
            return
        askPeriode(self, self.taskEditor, from_ = periodes[0], duplicate = True)
        
    def supprimerPeriode(self):
        """Permet de supprimer les périodes sélectionnées."""
        periodes = self.getPeriodesSelectionnees()
        for periode in reversed(periodes):
            self.periodes.remove(periode)
        self.app.getDonneeCalendrier().updateAffichage()
    
    def scinderPeriode(self):
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) != 1:
            showerror("Erreur de sélection", "Vous ne pouvez effectuer cette tâche qu'avec exactement une seule période sélectionnée.")
            return
        try:
            print(askScinderPeriode(self, self.taskEditor, periode = periodes[0]))
        except ValueError:
            return
        else:
            pass
    def fusionnerPeriodes(self):
        pass
    
    def lierTachePeriode(self):
        pass

if __name__=='__main__':
    import Application
    Application.main()
