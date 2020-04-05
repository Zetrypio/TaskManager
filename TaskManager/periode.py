# -*- coding:utf-8 -*-
import datetime

class Periode:
    def __init__(self, debut, fin, color = "white"):
        self.debut = debut
        self.fin = fin
        self.color = color
        # Doit-on faire une liste des tâches contenus ?
    def getDebut(self):
        return self.debut
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
        # Période de test étant donné qu'on a pas
        # de moyen d'en rajouter dynamiquement pour le moment :
        self.periodes = []
        self.periodes.append(Periode(datetime.datetime(2020, 4, 6), datetime.datetime(2020, 4, 18), "#3782F4"))
        self.periodes.append(Periode(datetime.datetime(2020, 4, 19), datetime.datetime(2020, 4, 23), "#F637C2"))
        self.periodes.append(Periode(datetime.datetime(2020, 4, 16), datetime.datetime(2020, 4, 20), "#F4D523"))
        self.periodes.append(Periode(datetime.datetime(2020, 4, 20), datetime.datetime(2020, 4, 26), "#12F763"))
    def getPeriodes(self):
        return self.periodes

if __name__=='__main__':
    import Application
    Application.main()
