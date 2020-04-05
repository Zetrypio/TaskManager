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
        self.__listeHauteur = {}
        
        self.can = Canvas(self, width = 1, height = 1, bd = 0)
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
        self.__listeHauteur = {}
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
            self.can.create_text(int(jour.weekday())*w/7+5, semaine*(h-hh)/5+hh, anchor = "sw", text = jour.day)
            if jour.isoweekday()%7 == 0:
                semaine += 1
            jour += datetime.timedelta(days = 1)
        
        ############################
        # Affichage des périodes : #
        ############################
        
        for p in self.getApplication().getPeriodManager().getPeriodes():
            jour = p.getDebut()
            semaine = self.getSemaineOf(jour)
            jourDebutSemaine = jour
            isFirst = 2
            while jour < p.getFin():
                jour += datetime.timedelta(days = 1)
                if jour.weekday()%7 == 0:
                    self.can.create_rectangle(int(jourDebutSemaine.weekday())*w/7 + isFirst,
                                              semaine*(h-hh)/5+hh+self.getPeriodeYPosition(p),
                                              w,
                                              semaine*(h-hh)/5+hh+self.getPeriodeYPosition(p)+self.getPeriodHeight(),
                                              fill = p.getColor())
                    isFirst = 0
                    semaine += 1
                    jourDebutSemaine = jour
            self.can.create_rectangle(int(jourDebutSemaine.weekday())*w/7 + isFirst,
                                      semaine*(h-hh)/5+self.getPeriodeYPosition(p)+hh,
                                      int(jour.weekday()+1)*w/7 -3,
                                      semaine*(h-hh)/5+self.getPeriodeYPosition(p)+hh+self.getPeriodHeight(),
                                      fill = p.getColor())
    def getPeriodeYPosition(self, p):
        if p in self.__listeHauteur:
            return self.__listeHauteur[p]*self.getPeriodHeight()
        bannedHeight = []
        for per, haut in self.__listeHauteur.items():
            if per.intersectWith(p):
                bannedHeight.append(haut)
        for i in range(len(self.__listeHauteur)+2):
            if i not in bannedHeight:
                self.__listeHauteur[p] = i
                return self.__listeHauteur[p]*self.getPeriodHeight()
            
            
    
    def getPeriodHeight(self):
        return 10
    
    def getSemaineOf(self, jour):
        """Renvoie le numéro de la ligne de la semaine correspondant au jour demmandé."""
        return (jour.day + self.getJourDebut().weekday()-1) // 7
            

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
