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
    def getJoutDebut(self):
        """Override, car en fait ça fonctionne avec un mois."""
    

    def updateAffichage(self):
        pass

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