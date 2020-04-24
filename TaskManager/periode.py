# -*- coding:utf-8 -*-
import datetime

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
        return self.debut
    def getDuree(self):
        return self.fin - self.debut
    def getFin(self):
        return self.fin
    def getColor(self):
        return self.color
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
        pass
    def dupliquerPeriode(self):
        pass
    def supprimerPeriode(self):
        periodes = self.getPeriodesSelectionnees()
        for periode in reversed(periodes):
            self.periodes.remove(periode)
        self.app.getDonneeCalendrier().updateAffichage()
    
    def scinderPeriode(self):
        pass
    def fusionnerPeriodes(self):
        pass
    
    def lierTachePeriode(self):
        pass

if __name__=='__main__':
    import Application
    Application.main()
