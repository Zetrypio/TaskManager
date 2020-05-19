# -*- coding:utf-8 -*-

from .classique.AffichageCalendrier import *
from .gantt.AffichageGantt import *
from .periode.AffichageCalendrierPeriode import *

from .AbstractDisplayedCalendar import *

class DonneeCalendrier(AbstractDisplayedCalendar):
    def __init__(self, master = None, **kwargs):
        AbstractDisplayedCalendar.__init__(self, master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.

        # Ceci est un panneau à onglet.
        self.panneau = Notebook(self)

        # Création du contenu des différents onglets.
        self.listPanneau = []
        self.listPanneau.append(AffichageCalendrier(self.panneau)) #liste de tout les panneaux pour appliquer un changement à tous
        self.listPanneau.append(AffichageGantt(self.panneau))
        self.listPanneau.append(AffichageCalendrierPeriode(self.panneau))

        # Ajout des onglets au panneau
        self.panneau.add(self.listPanneau[0], text="Calendrier", padding=1) # padding optionnel
        self.panneau.add(self.listPanneau[1], text="Gantt", padding=1)
        self.panneau.add(self.listPanneau[2], text="Gérer les périodes", padding = 1)
        
        # Ajout d'un binding sur le panneau pour savoir quand on en change :
        self.panneau.bind("<<NotebookTabChanged>>", self.panneauChange)

        # Placement du panneau :
        self.panneau.pack(expand = YES, fill = BOTH)

        self.jourSelectionnes = set()

    def clearJourSelectionnes(self):
        self.jourSelectionnes.clear()

    def addJourSelectionnes(self, jour):
        self.jourSelectionnes.add(jour)

    def intervertir(self):
        if len(self.jourSelectionnes) != 2 :
            showerror("Selection invalide", "Il vous faut exactement deux jours sélectionnés pour executer cette action.")
            return

        lesJours = list(self.jourSelectionnes)
        jour1 = lesJours[0]
        jour2 = lesJours[1]
        if jour1 > jour2:
            jour2, jour1 = jour1, jour2

        tacheJour1 = set()
        tacheJour2 = set()

        # Seulement les taches sélectionnés au cas où il y en a qu'on veux pas switch
        for tache in self.getSelectedTask():
            if   tache.getDebut().date() <= jour1 and tache.getFin().date() >= jour1:
                tacheJour1.add(tache)
            elif tache.getDebut().date() <= jour2 and tache.getFin().date() >= jour2:
                tacheJour2.add(tache)

        diff = datetime.datetime.combine(jour2, datetime.time()) - datetime.datetime.combine(jour1, datetime.time())
        # On applique les changements
        for tache in tacheJour1-tacheJour2:
            tache.setDebut(tache.getDebut()+diff)
        for tache in tacheJour2-tacheJour1:
            tache.setDebut(tache.getDebut()-diff)

        for p in self.getToutLesPanneaux():
            p.onIntervertir()
        self.updateAffichage()

    def getParametreAffichage(self):
        return self.master.getParametreAffichage()

    def getApplication(self):
        return self.master.getApplication()

    def getZoneAffichage(self):
        return self.master

    def panneauChange(self, e):
        p = self.getPanneauActif()
        p.doConfiguration(self.master.getParametreAffichage())

    def mouseClicked(self, event):
        self.getPanneauActif().mouseClicked(event)

    def escapePressed(self, event):
        """ On annule ce qu'on fait sur tous les panneux """
        for panneau in self.listPanneau:
            panneau.escapePressed(event)
    
    def setHeureDebut(self, heure):
        """Setter pour l'heure du début"""
        for panneau in self.listPanneau:
            panneau.setHeureDebut(heure)
        super().setHeureDebut(heure)

    def setHeureFin(self, heure):
        """Setter pour l'heure de la fin."""
        for panneau in self.listPanneau:
            panneau.setHeureFin(heure)
        super().setHeureFin(heure)

    def setJourDebut(self, jour):
        """Setter pour le jour du début."""
        for panneau in self.listPanneau:
            panneau.setJourDebut(jour)
        super().setJourDebut(jour)

    def setJourFin(self, jour):
        """Setter pour le jour de fin."""
        for panneau in self.listPanneau:
            panneau.setJourFin(jour)
        super().setJourFin(jour)

    def setDureeJour(self, jour):
        """Setter pour le nombre de jour."""
        for panneau in self.listPanneau:
            panneau.setDureeJour(jour)
        super().setDureeJour(jour)

    def setNbJour(self, jour):
        """Setter pour le nombre de jour."""
        for panneau in self.listPanneau:
            panneau.setNbJour(jour)
        super().setNbJour(jour)

    def setPeriodeActiveDebut(self, jour):
        """Setter pour le jour du début de la période active."""

        ### Option utile ou pas ?, à voir dans le préférences ?, faire ça seulement si on est au début ? ##

        # Si le nouveau jour de début de la période est avant, il faut changer le nouveau jour de début
        #if jour < self.getJourDebut():
        duree = self.getJourFin() - jour + datetime.timedelta(days=1)
        self.setJourDebut(jour)
        self.setDureeJour(duree)


        self.getPeriodeActive().setDebut(jour)

    def setPeriodeActiveFin(self, jour):
        """Setter pour le jour de fin de la période active."""
        self.getPeriodeActive().setFin(jour)
        # Si le nouveau jour de fin de la période est avant, il faut changer le nouveau jour de fin
        if jour < self.getJourFin():
            self.setJourFin(jour)
    def getPanneauActif(self):
        """Getter pour le panneau actif."""
        # self.panneau.select() renvoie l'id du panneau actif
        # self.panneau.index() renvoie l'index d'un panneau selon son id
        # on peut donc utiliser notre liste avec cet index.
        return self.listPanneau[self.panneau.index(self.panneau.select())]
    
    def getToutLesPanneaux(self):
        """Renvoie une copie de la liste de tout les panneaux."""
        return self.listPanneau[:]

    def updateTaskColor(self):
        for p in self.getToutLesPanneaux():
            p.updateTaskColor()

    def updateAffichage(self):
        # Faire un parcour des panneaux pour pouvoir effectuer les changements
        # sur TOUTES les disposition de calendriers (gantt, calendrier classique etc)
        for panneau in self.listPanneau:
            panneau.updateAffichage()
        
        if self.getJourDebut() == self.getDebutPeriode():
            self.master.zoneParametre.boutonBienAvant.configure(state=DISABLED)
            self.master.zoneParametre.boutonAvant.configure(state=DISABLED) # Désactive le bouton quand on est au début de la période
        else:
            self.master.zoneParametre.boutonBienAvant.configure(state=NORMAL)
            self.master.zoneParametre.boutonAvant.configure(state=NORMAL)

        if self.getFinPeriode() is None or self.getJourFin() is None:
            self.master.zoneParametre.boutonBienApres.configure(state=DISABLED)
            self.master.zoneParametre.boutonApres.configure(state=DISABLED)
        elif self.getJourFin() > self.getFinPeriode():
            duree = self.getDureeJour()
            self.setJourFin(self.getFinPeriode())
            self.setJourDebut(self.getFinPeriode() - duree)
        elif self.getJourFin()== self.getFinPeriode():
            self.master.zoneParametre.boutonBienApres.configure(state=DISABLED)            
            self.master.zoneParametre.boutonApres.configure(state=DISABLED)
        else:
            self.master.zoneParametre.boutonBienApres.configure(state=NORMAL)
            self.master.zoneParametre.boutonApres.configure(state=NORMAL)

    def addTask(self, tache, region = None):
        '''Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas.'''
        tache = super().addTask(tache, region) # region est géré dans la variante parent : on ne s'en occupe plus ici.

        ####################
        # Ajout graphique. #
        ####################
        for panneau in self.listPanneau:
            tache = panneau.addTask(tache, region)

        return tache # on revoie la tache avec son début et sa duree. TRÈS IMPORTANT.

