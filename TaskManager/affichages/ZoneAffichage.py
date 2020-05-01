# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from .DonneeCalendrier import *
from .ParametreAffichage import *

class ZoneAffichage(Frame): # Contient les paramètre et les données
    def __init__(self, master = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers CalendarZone.
        
        # Affichage des paramètres
        self.zoneParametre = ParametreAffichage(self)
        self.zoneParametre.pack(side=TOP, fill=X)
        
        # Affichage des données
        self.donneeCalendrierFrame = DonneeCalendrier(self)
        self.donneeCalendrierFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        
        self.donneeCalendrierFrame.updateAffichage()

    def getApplication(self):
        return self.master.getApplication()

    def getPanneauActif(self):
        """Renvoie le mode d'affichage de calendrier actif."""
        return self.donneeCalendrierFrame.getPanneauActif()
    
    def getDonneeCalendrier(self):
        return self.donneeCalendrierFrame
    
    def getParametreAffichage(self):
        return self.zoneParametre
        
    def envoyerChangementNbJour(self, event):
        """
        Méthode callback du combobox qui gère
        le nombre de jours à afficher.
        """
        valeur = event.widget.get()
        if valeur == '1 jour':
            self.donneeCalendrierFrame.setNbJour(1)
        elif valeur == '2 jours':
            self.donneeCalendrierFrame.setNbJour(2)
        elif valeur == '5 jours':
            self.donneeCalendrierFrame.setNbJour(5)
        elif valeur == '1 semaine':
            self.donneeCalendrierFrame.setNbJour(7)
        else: # Si c'est une période
            self.donneeCalendrierFrame.setNbJour(self.donneeCalendrierFrame.getLongueurPeriode())
            self.donneeCalendrierFrame.setJourDebut(self.donneeCalendrierFrame.getDebutPeriode())
    
    def envoyerChangementJourDebut(self, valeur):
        if valeur == "d": # Si on appui sur remetre au début
            self.donneeCalendrierFrame.setJourDebut(self.donneeCalendrierFrame.getDebutPeriode())
        elif valeur == "f": # Si on appuie sur mettre à la fin
            self.donneeCalendrierFrame.setJourDebut(self.donneeCalendrierFrame.getJourDebut()+
                                                    datetime.timedelta(days =
                                                                       self.donneeCalendrierFrame.getLongueurPeriode()
                                                                       -self.donneeCalendrierFrame.getNbJour()))
        else:
            self.donneeCalendrierFrame.setJourDebut(self.donneeCalendrierFrame.getJourDebut()+datetime.timedelta(days = valeur))

    

