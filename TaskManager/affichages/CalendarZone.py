# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from toolbar.ToolBar import *
from toolbar.PeriodToolBar import *
from toolbar.dialog.decalageHeureDialog import *
from toolbar.dialog.gestionHeureCalendrierDialog import *
from toolbar.dialog.gestionJourDialog import *

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
            if   pos == "Avant":
                min = datetime.time(min.hour - nb)
                self.getDonneeCalendrier().setHeureDebut(min)
            elif pos == "Apres":
                max = datetime.time(max2.hour + nb, max2.minute)
                self.getDonneeCalendrier().setHeureFin(max)

    def ajouterJour(self):
        totalJour = self.getDonneeCalendrier().getLongueurPeriode().days-1
        nb, pos = askAjouterJour(totalJour)
        self.gestionJour(nb, pos)

    def gestionJour(self, nombreDeJour, position):
        """
        Fonction qui s'occupe d'ajouter ou de supprimer des jours
        En dehors de la fonction ajouterJour lié au bouton car on pourrait avoir à ajouter des jours autrement que par le bouton
        @param nombreDeJour : int relatif, permet d'ajouter ou retirer des jours
        @param position : string "Avant" / "Apres" pour savoir ou appliquer les changements
        """
        if nombreDeJour is not None and position is not None:
            periode = self.getDonneeCalendrier().getPeriodeActive()
            if   position == "Avant":
                self.getDonneeCalendrier().setPeriodeActiveDebut(periode.getDebut() - datetime.timedelta(days=nombreDeJour))
            elif position == "Apres":
                self.getDonneeCalendrier().setPeriodeActiveFin(periode.getFin() + datetime.timedelta(days=nombreDeJour))


    def selectionnerJour(self):
        pass
    def afficherMasquerJour(self):
        pass
    def deplacerIntervertir(self):
        self.getDonneeCalendrier().intervertir()

    def decalerJour(self):
        pass
    def decalerHeure(self): # TODO : gerer une tache de plusierus jours (peut-être)
        # Si la liste est vide on évite la question
        if len(self.getDonneeCalendrier().getSelectedTask()) == 0:
            return
        # S'il y a une tache de plus j'un jour on est mal
        for tache in self.getDonneeCalendrier().getSelectedTask():
            if tache.getDuree() > datetime.timedelta(days=1):
                showerror("Selection invalide", "Vous ne pouvez pas décaler en heure une tache de plus d'un jour.")

        # On détermine le nombre d'heure min et max
        first = None # Contient la tache qui finit    le plus tot  pour heure max
        last  = None # Contient la tache qui commence le plus tard pour heure min
        for tache in self.getDonneeCalendrier().getSelectedTask():
            if first is None or first.getFin() > tache.getFin():
                first = tache
            if last is None or last.getDebut() < tache.getDebut():
                last = tache

        heureRetirerMax = last.getDebut().hour - self.getDonneeCalendrier().getHeureDebut().hour
        heureAjoutMax = self.getDonneeCalendrier().getHeureFin().hour - first.getFin().hour + 1
        print(heureRetirerMax, heureAjoutMax)
        nb, pos = askDecalHeure(heureRetirerMax, heureAjoutMax)
        # Ajustement des heures
        for tache in self.getDonneeCalendrier().getSelectedTask():
            # Si tout va bien
            if  self.getDonneeCalendrier().getHeureDebut() <= (tache.getDebut()+datetime.timedelta(hours=nb)).time()\
            and self.getDonneeCalendrier().getHeureFin()   >= (tache.getFin()+datetime.timedelta(hours=nb)).time():
                print("ok")
                tache.setDebut(tache.getDebut()+datetime.timedelta(hours=nb))

            # Si on dépasse, on cadre selon les limites
            else:
                # Si on retire des heures au début
                if nb < 0:
                    # On peut pas mettre un
                    tache.setDebut(datetime.datetime.combine(tache.getDebut().date(), self.getDonneeCalendrier().getHeureDebut()))
                # Si on ajoute pour mettre à la fin
                else:
                    heureFin = self.getDonneeCalendrier().getHeureFin() # Time
                    time = datetime.datetime.combine(tache.getFin().date(), heureFin) - tache.getDuree() # datetime - timedelta
                    tache.setDebut(time)

        self.getDonneeCalendrier().updateAffichage()

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
    
