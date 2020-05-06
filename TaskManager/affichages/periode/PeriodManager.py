# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror

from util.widgets.Dialog import *

from .dialog.periodDialog import *
from .dialog.scinderPeriodDialog import *
from .Periode import *

class PeriodManager:
    """Gestionnaire des périodes."""
    def __init__(self, app):
        self.app = app
        self.periodes = []
        self.taskEditor = None
        self.activePeriode = None
    
    def setTaskEditor(self, taskEditor):
        self.taskEditor = taskEditor

    def getPeriodes(self):
        return self.periodes
    def ajouter(self, periode):
        for p in self.periodes:
            if p.nom == periode.nom:
                nom = periode.nom
                print("nom av.", nom)
                a = -1
                while nom[a] in "0123456789":
                    a-=1
                if nom[-1] in "0123456789":
                    a+=1
                    nom = nom[:a] + str(int(nom[a])+1)
                else:
                    nom = nom + " 2"
                print("nom ap.", nom)
                periode.nom = nom
        self.periodes.append(periode)
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().getPanneauActif().updateAffichage()
        self.app.getTaskEditor().ajouter(periode)
        if self.activePeriode is None:
            self.setActivePeriode(periode)

    def setActivePeriode(self, periode):
        if not isinstance(periode, Periode):
            raise ValueError("La période ne peut pas être %s")
        self.activePeriode = periode
        self.app.getDonneeCalendrier().setJourDebut(periode.getDebut())
        self.app.getDonneeCalendrier().setJourFin(periode.getFin())
    
    def getActivePeriode(self):
        return self.activePeriode
    
    def getPeriodesSelectionnees(self):
        return [periode for periode in self.periodes if periode.isSelected()]

    # Fonctions de la barre d'outil :
    def deplacerPeriode(self):
        """Permet de déplacer la ou les périodes sélectionnées."""
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) == 0:
            return showerror("Erreur de sélection", "Vous devez avoir au moins une période sélectionnée pour effectuer cette action.")
        elif len(periodes) == 1:
             askPeriode(self, self.taskEditor, from_ = periodes[0], duplicate = False)
        else:
            duree = askDureeJours()
            if duree is not None:
                for p in periodes:
                    p.setDebut(p.getDebut() + duree, change = "fin")
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().updateAffichage()
        self.app.getTaskEditor().redessiner()

    def dupliquerPeriode(self):
        """Permet de duppliquer la période sélectionnée."""
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) != 1:
            showerror("Erreur de sélection", "Vous ne pouvez effectuer cette action qu'avec exactement une seule période sélectionnée.")
            return
        askPeriode(self, self.taskEditor, from_ = periodes[0], duplicate = True)
        
    def supprimerPeriode(self):
        """Permet de supprimer les périodes sélectionnées."""
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) == 0:
            return showerror("Erreur de sélection", "Vous devez avoir au moins une période sélectionnée pour effectuer cette action.")
        for periode in reversed(periodes):
            self.periodes.remove(periode)
            self.app.getTaskEditor().supprimer(periode)
        self.app.getDonneeCalendrier().updateAffichage()
    
    def scinderPeriode(self):
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) != 1:
            showerror("Erreur de sélection", "Vous ne pouvez effectuer cette action qu'avec exactement une seule période sélectionnée.")
            return
        periode = periodes[0]
        try:
            dateScindage = askScinderPeriode(self, self.taskEditor, periode = periode)
            if dateScindage is None:
                return
        except ValueError:
            return
        else:
            prevFin = periode.getFin()
            periode.setFin(dateScindage - datetime.timedelta(days = 1))
            newPeriode = Periode(periode.nom, dateScindage, prevFin, periode.desc, periode.getColor())
            # TODO : changer les périodes des tâches concernées.
            self.ajouter(newPeriode)
    def fusionnerPeriodes(self):
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) < 2:
            return showerror("Erreur de sélection", "Vous devez avoir au moins 2 périodes sélectionnées pour pouvoir effectuer cette action.")
        # Vérification des trous entre les périodes pour affichage de confirmation eventuelle :
        lesPeriodesListees = [periodes[0]]
        onEnAAjoute = True
        while onEnAAjoute:
            onEnAAjoute = False
            for p1 in periodes:
                if p1 not in lesPeriodesListees:
                    for p2 in reversed(lesPeriodesListees):
                        if p1.intersectWith(p2):
                            lesPeriodesListees.append(p1)
                            onEnAAjoute = True
        trou = False
        for p1 in periodes:
            if p1 not in lesPeriodesListees:
                trou = True
                break
        if trou:
            if not askyesnowarning("Êtes-vous sûr ?", "Il y a un ou plusieurs jours au milieu de la nouvelle période à créer qui ne sont dans aucunes de vos périodes sélectionnées.\n"
            "Voulez-vous tout de même fusionner les périodes, sachant qu'un espace de jours n'étant pas présent auparavant va être ajouter dans votre nouvelle période ?"):
                return
        # Fuuusioonnnnnn !!!!! :
       
        # TODO : changer les périodes des tâches concernées.
        nom = "Fusion de " + ", ".join(p.nom for p in periodes) + "."
        debut = min(periodes, key=lambda p: p.getDebut()).getDebut()
        fin   = max(periodes, key=lambda p: p.getFin()).getFin()
        desc = ", ".join(p.desc for p in periodes)
        color = periodes[0].getColor()
        
        # Supprimer toutes les périodes sélectionnées :
        self.supprimerPeriode()
        
        self.ajouter(Periode(nom, debut, fin, desc, color))
        
    def lierTachePeriode(self):
        pass
