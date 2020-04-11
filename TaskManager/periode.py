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
        self.periodes.append(Periode("A", datetime.date(2020, 4,  6), datetime.date(2020, 4, 18), "Période A", "#3782F4"))
        self.periodes.append(Periode("B", datetime.date(2020, 4, 19), datetime.date(2020, 4, 23), "Période B", "#F637C2"))
        self.periodes.append(Periode("C", datetime.date(2020, 4, 16), datetime.date(2020, 4, 20), "Période C", "#F4D523"))
        self.periodes.append(Periode("D", datetime.date(2020, 4, 20), datetime.date(2020, 4, 26), "Période D", "#12F763"))
    def getPeriodes(self):
        return self.periodes
    def ajouter(self, periode):
        self.periodes.append(periode)
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().updateAffichage()

if __name__=='__main__':
    import Application
    Application.main()
