# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from .DonneeCalendrier import *
from .ParametreAffichage import *

class ZoneAffichage(Frame):
    """
    Classe qui contient les paramètres et les données.
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de ZoneAffichage.
        @param master: master du tkinter.Frame() que cet objet est.
        @param **kwargs : configurations graphiques du tkinter.Frame() que cet objet est.
        """
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers CalendarZone.
        
        # Affichage des paramètres
        self.zoneParametre = ParametreAffichage(self)
        self.zoneParametre.pack(side=TOP, fill=X)

        # Affichage des données
        self.donneeCalendrierFrame = DonneeCalendrier(self)
        self.donneeCalendrierFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.donneeCalendrierFrame.updateAffichage()

        # Création de la liste qui contient les durées
        self.getData().readFile("duree")
        self.__listeValue = []
        for duree in self.getData().sections():
            self.__listeValue.append([self.getData()[duree]["nom"], self.getData()[duree]["Duree en jour"]])

        self.__listeValue.remove(['Période', '-1'])



    def getApplication(self):
        """
        Getter pour l'application.
        @return l'Application.
        """
        return self.master.getApplication()

    def getData(self):
        """
        Getter pour data.
        @return Data.
        """
        return self.getApplication().getData()

    def getPanneauActif(self):
        """
        Renvoie le mode d'affichage de calendrier actif.
        @return le calendrier actif.
        """
        return self.getDonneeCalendrier().getPanneauActif()
    
    def getDonneeCalendrier(self):
        """
        Getter pour le DonneeCalendrier.
        @return le DonneeCalendrier.
        """
        return self.donneeCalendrierFrame
    
    def getParametreAffichage(self):
        """
        Getter pour le ParametreAffichage.
        @return le ParametreAffichage.
        """
        return self.zoneParametre
        
    def envoyerChangementNbJour(self, event):
        """
        Méthode callback du combobox qui gère le nombre de jours à afficher.
        @param event: l'événement, doit contenir le combobox dans l'attritbut widget.
        """
        valeur = event.widget.get()
        for duree in self.__listeValue:
            print(valeur, duree[0], valeur == duree[0])
            if valeur == duree[0]:
                self.getDonneeCalendrier().setNbJour(int(duree[1]))
                break # Important sinon on essaye les autre et on affiche la periode parce que la condition n'est pas vérifié
        else: # Si c'est une période
            self.getDonneeCalendrier().setDureeJour(self.getDonneeCalendrier().getLongueurPeriode())
            self.getDonneeCalendrier().setJourDebut(self.getDonneeCalendrier().getDebutPeriode())

    def envoyerChangementJourDebut(self, valeur):
        """
        Permet d'envoyer les informations de changement de jours, suivant le bouton
        sur lequel on a appuyé.
        @param valeur: "f" pour aller à la fin, "d" pour aller au début,
        +1 ou -1 pour augmenter ou diminuer de 1 jour.
        """
        duree = self.getDonneeCalendrier().getDureeJour()
        if valeur == "d": # Si on appuie sur remettre au début
            self.getDonneeCalendrier().setJourDebut(self.getDonneeCalendrier().getDebutPeriode())
        elif valeur == "f": # Si on appuie sur mettre à la fin
            self.getDonneeCalendrier().setJourDebut(self.getDonneeCalendrier().getFinPeriode()-self.getDonneeCalendrier().getDureeJour()+datetime.timedelta(days=1))
        else:
            self.getDonneeCalendrier().setJourDebut(self.getDonneeCalendrier().getJourDebut()+datetime.timedelta(days = valeur))
            #self.getDonneeCalendrier().setJourFin(self.getDonneeCalendrier().getJourFin()+datetime.timedelta(days = valeur))

        self.getDonneeCalendrier().setDureeJour(duree)
    

