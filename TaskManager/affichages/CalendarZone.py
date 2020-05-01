# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from toolbar.ToolBar import *
from toolbar.PeriodToolBar import *
from toolbar.dialog.gestionHeureCalendrierDialog import *

from .ZoneAffichage import *

class CalendarZone(Frame):
    def __init__(self, master = None, periodeManager = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers l'Application.
        
        self.__isBarrePeriode = False
        # Barre du haut
        self.outilBar = ToolBar(self) # frame avec tous les boutons outils
        self.outilBar.pack(side=TOP, fill=X, expand=NO)
        
        # Barre du haut pour les périodes
        self.outilBarPeriode = PeriodToolBar(self, periodeManager) # frame avec tous les boutons outils
        
        # Zone calendrier
        self.zoneDynamicCalendarFrame = ZoneAffichage(self) # frame avec la zone d'affichage des paramètre et la zone avec les données
        self.zoneDynamicCalendarFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    def getApplication(self):
        return self.master
    def setBarreOutilPeriode(self, value):
        self.__isBarrePeriode = value
        if value:
            self.outilBarPeriode.pack(side=TOP, fill=X, expand=NO)
            self.outilBar.pack_forget()
        else:
            self.outilBarPeriode.pack_forget()
            self.outilBar.pack(side=TOP, fill=X, expand=NO)
    def getBarreOutilActive(self):
        if self.__isBarrePeriode:
            return self.outilBarPeriode
        else:
            return self.outilBar

    def ajouterHeure(self):
        min = self.getDonneeCalendrier().getHeureDebut()
        max = datetime.timedelta(hours=23) - datetime.timedelta(hours=self.getDonneeCalendrier().getHeureFin().hour)
        max2 = self.getDonneeCalendrier().getHeureFin()
        nbHeure = max2.hour - min.hour
        nb, pos = askAjouterHeure(min, max, nbHeure)
        if nb is not None and pos is not None:
            if pos == "Avant":
                min = datetime.time(min.hour - nb)
                self.getDonneeCalendrier().setHeureDebut(min)
            elif pos == "Apres":
                max = datetime.time(max2.hour + nb, max2.minute)
                self.getDonneeCalendrier().setHeureFin(max)

    def ajouterJour(self):
        pass

    def selectionnerJour(self):
        pass
    def afficherMasquerJour(self):
        pass
    def deplacerIntervertir(self):
        self.getDonneeCalendrier().intervertir()

    def decalerJour(self):
        pass
    def decalerHeure(self):
        pass

    def grouper(self):
        pass
    def degrouper(self):
        pass

    def avancementRetard(self):
        pass
    def avancementJourFini(self):
        pass
    def avancementNormal(self):
        pass

    def getPanneauActif(self):
        return self.zoneDynamicCalendarFrame.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.zoneDynamicCalendarFrame.getDonneeCalendrier()
    
    # Pour la barre d'outil des périodes :
    def voirTacheDansVue(self):
        pass
    def supprimerTache(self):
        pass
    
