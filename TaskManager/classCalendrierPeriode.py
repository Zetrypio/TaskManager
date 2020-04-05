# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
import time
from superclassCalendrier import *
from periode import *


class AffichageCalendrierPeriode(SuperCalendrier):
    """Classe permettant la vision des périodes dans un mois."""
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
        self.annee = time.localtime().tm_year
        self.mois = time.localtime().tm_mon
        
        self.can = Canvas(self, width = 1, height = 1)
        self.can.pack(expand = YES, fill = BOTH)
        self.can.bind("<Configure>", lambda e: self.updateAffichage())
    
    def setJourDebut(self, jour):
        """Override, car en fait ca fonctionne avec un mois."""
        self.mois = jour.month
        self.annee = jour.year
    def getJourDebut(self):
        """Override, car en fait ça fonctionne avec un mois."""
        return datetime.datetime(self.annee, self.mois, 1)
    

    def updateAffichage(self):
        self.can.delete(ALL)
        hh = 20
        w = self.can.winfo_width()
        h = self.can.winfo_height()
        self.can.create_rectangle(0, 0, w, hh, fill = "light grey")
        for i, j in enumerate(JOUR):
            self.can.create_text(int(i*w/7+w/14), int(hh/2), width = w, text = j)
            self.can.create_line(int(i*w/7), hh+1, int(i*w/7), h, fill = "light grey")
        for i in range(5):
            self.can.create_line(0, hh+(h-hh)/5*(i+1), w, hh+(h-hh)/5*(i+1))
        jour = self.getJourDebut()
        semaine = 1
        while jour.month == self.mois:
            self.can.create_text(int(jour.isoweekday()-1)*w/7+5, semaine*(h-hh)/5+hh, anchor = "sw", text = jour.day)
            if jour.isoweekday()%7 == 0:
                semaine += 1
            jour += datetime.timedelta(days = 1)

    def doConfiguration(self, paramAffichage):
        """
        Méthode pour éventuellement changer la barre d'outil
        secondaire quand ce panneau est actif.
        
        Ce widget difère pour afficher "1 Mois" dans la liste (et désactive la liste)
        """
        paramAffichage.setStateListe(DISABLED)
        paramAffichage.setModeListe("1 Mois")


if __name__=='__main__':
    import Application
    Application.main()