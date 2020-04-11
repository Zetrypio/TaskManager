# -*- coding:utf-8 -*-
import datetime

class Periode:
    def __init__(self, nom, debut, fin, desc, color = "white"):
        self.nom = nom
        self.debut = debut
        self.fin = fin
        self.desc = desc
        self.color = color
        # Doit-on faire une liste des tâches contenus ?
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

if __name__=='__main__':
    import Application
    Application.main()
