# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from superclassCalendrier import *
from classCalendrier import *
from classGantt import *

class ZoneAffichage(Frame): # Contient les paramètre et les données
    def __init__(self, master = None, **kwargs):
        kwargs["bg"] = "gray"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers CalendarZone.
        
        # Affichage des paramètres
        self.zoneParametre = ParametreAffichage(self)
        self.zoneParametre.pack(side=TOP, fill=X)
        
        # Affichage des données
        self.donneeCalendrierFrame = DonneeCalendrier(self)
        self.donneeCalendrierFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
        
        self.donneeCalendrierFrame.updateAffichage()

    def getPanneauActif(self):
        """Renvoie le mode d'affichage de calendrier actif."""
        return self.donneeCalendrierFrame.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.donneeCalendrierFrame
        
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
            self.donneeCalendrierFrame.setJourDebut(0)
    
    def envoyerChangementJourDebut(self, valeur):
        self.donneeCalendrierFrame.setJourDebut(self.donneeCalendrierFrame.getJourDebut()+valeur)


class ParametreAffichage(Frame):
    def __init__(self, master = None, **kwargs):
        kwargs["bg"] = "yellow"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.
        self.boutonAvant = Button(self, text="<", command=lambda:master.envoyerChangementJourDebut(-1))
        self.boutonAvant.pack(side=LEFT, fill=Y)
        self.boutonApres = Button(self, text=">", command=lambda:master.envoyerChangementJourDebut(1))
        self.boutonApres.pack(side=RIGHT, fill=Y)             
        
        self.listeMode = Combobox(self, values=['1 jour', '2 jours', '5 jours', '1 semaine', 'Période'], state= "readonly")
        self.listeMode.set(self.listeMode.cget("values")[-1])
        self.listeMode.bind("<<ComboboxSelected>>",master.envoyerChangementNbJour) #passer par le maître et pas de parenthèse car on n'appelle pas la fonction, on la passe en paramètre
        self.listeMode.pack(side=TOP, fill=Y)
        
    
   
    
    

class DonneeCalendrier(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.

        # Ceci est un panneau à onglet.
        self.panneau = Notebook(self)

        # Création du contenu des différents onglets.
        self.listPanneau = []
        self.listPanneau.append(AffichageCalendrier(self.panneau)) #liste de tout les panneaux pour appliquer un changement à tous
        self.listPanneau.append(AffichageGantt(self.panneau))

        # Ajout des onglets au panneau
        self.panneau.add(self.listPanneau[0], text="Calendrier", padding=1) # padding optionnel
        self.panneau.add(self.listPanneau[1], text="Gantt", padding=1)

        # Placement du panneau :
        self.panneau.pack(expand = YES, fill = BOTH)

    
    def setHeureDebut(self, heure):
        """Setter pour l'heure du début"""
        super().setHeureDebut(heure)
        for panneau in self.listPanneau:
            panneau.setHeureDebut(heure)

    def setHeurefin(self, heure):
        """Setter pour l'heure de la fin."""
        super().setHeurefin(heure)
        for panneau in self.listPanneau:
            panneau.setHeurefin(heure)

    def setJourDebut(self, jour):
        """Setter pour le jour du début."""
        super().setJourDebut(jour)
        for panneau in self.listPanneau:
            panneau.setJourDebut(jour)

    def setNbJour(self, jour):
        """Setter pour le nombre de jour."""
        super().setNbJour(jour)
        for panneau in self.listPanneau:
            panneau.setNbJour(jour)

    def getPanneauActif(self):
        """Getter pour le panneau actif."""
        # self.panneau.select() renvoie l'id du panneau actif
        # self.panneau.index() renvoie l'index d'un panneau selon son id
        # on peut donc utiliser notre liste avec cet index.
        return self.listPanneau[self.panneau.index(self.panneau.select())]
    
    def getToutLesPanneaux(self):
        """Renvoie une copie de la liste de tout les panneaux."""
        return self.listPanneau[:]
        
    
    def updateAffichage(self):
        # Faire un parcour des panneaux pour pouvoir effectuer les changements
        # sur TOUTES les disposition de calendriers (gantt, calendrier classique etc)
        #for panneau in self.listPanneau:
        #    panneau.updateAffichage()
        
        if self.getJourDebut() == 0:
            self.master.zoneParametre.boutonAvant.configure(state=DISABLED) # Désactive le bouton quand on est au début de la période
        else:
            self.master.zoneParametre.boutonAvant.configure(state=NORMAL)
        if self.getJourDebut()+self.getNbJour() > self.getLongueurPeriode():
            self.setJourDebut(self.getLongueurPeriode() - self.getNbJour())
        elif self.getJourDebut()+self.getNbJour()== self.getLongueurPeriode():
            self.master.zoneParametre.boutonApres.configure(state=DISABLED)
        else:
            self.master.zoneParametre.boutonApres.configure(state=NORMAL)

    def addTask(self, tache, region = None):
        '''Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas.'''
        tache = SuperCalendrier.addTask(self, tache, region) # region est géré dans la variante parent : on ne s'en occupe plus ici.

        ####################
        # Ajout graphique. #
        ####################
        for panneau in self.listPanneau:
            tache = panneau.addTask(tache, region)

        return tache # on revoie la tache avec son début et sa duree. TRÈS IMPORTANT.



if __name__=='__main__':
    import Application
    Application.main()
