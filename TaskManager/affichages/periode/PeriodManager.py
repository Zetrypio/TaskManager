# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror

from util.widgets.Dialog import *

from .dialog.periodDialog import *
from .dialog.scinderPeriodDialog import *
from .Periode import *

class PeriodManager:
    """
    Gestionnaire des périodes.
    """
    def __init__(self, app):
        """
        Constructeur du gestionnaire de périodes.
        @param app: Référence vers l'application.
        """
        self.app = app
        self.periodes = []
        self.taskEditor = None
        self.activePeriode = None

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getActivePeriode(self):
        """
        Getter pour la période active.
        @return la période active, ou None le cas échéant.
        """
        return self.activePeriode

    def getApplication(self):
        """
        Getter pour l'Application().
        @return l'Application().
        """
        return self.app

    def getPeriodes(self):
        """
        Getter pour les périodes.
        @return une copie de la liste contenant les périodes.
        """
        return self.periodes[:]

    def getPeriodesSelectionnees(self):
        """
        Permet d'obtenir la liste des périodes sélectionnées dans l'affichage de calendrier des périodes.
        @return la liste des périodes sélectionnées dans l'affichage de calendrier des périodes.
        """
        return [periode for periode in self.periodes if periode.isSelected()]

    ""
    #############
    # Setters : #
    #############
    ""
    def setActivePeriode(self, periode):
        """
        Setter pour la période active.
        @param periode: la période à mettre.
        """
        if not isinstance(periode, (Periode, None.__class__)):
            raise ValueError("La période ne peut pas être %s")
        self.activePeriode = periode
        self.app.getDonneeCalendrier().setJourDebut(periode.getDebut() if periode is not None else None) # TODO : Désactiver l'affichage période (faire en sorte que ca bug pas).
        self.app.getDonneeCalendrier().setJourFin(periode.getFin() if periode is not None else None)     # TODO : idem.

        # Configuration du combobox en fonction de la durée de la période
        self.app.getDonneeCalendrier().getZoneAffichage().getParametreAffichage().configPossibiliteListe()
        self.app.getDonneeCalendrier().getZoneAffichage().getParametreAffichage().setPeriodeActiveInCombo()

        self.app.getDonneeCalendrier().switchPeriode()
        self.app.getTaskEditor().redessiner()

    def setActivePeriodeWithName(self, name):
        """
        Méthode qui permet de set une période active à partir du nom de cette période
        @param name : <str> nom de la période
        """
        for p in self.getPeriodes():
            if p.getNom() == name:
                self.setActivePeriode(p)

    
    def setTaskEditor(self, taskEditor):
        """
        Setter pour le TaskEditor() car celui-ci n'existait
        probablement pas lors de la création de cet objet.
        @param taskEditor: le TaskEditor() à mettre.
        """
        self.taskEditor = taskEditor

    ""
    ###############################################
    # Méthodes liées à la gestion des périodes  : #
    ###############################################
    ""
    def ajouter(self, periode):
        """
        Permet d'ajouter une période au gestionnaire.
        @param periode: la période à ajouter.
        """
        # On vérifie le nom :
        for p in self.periodes:
            if p.nom == periode.nom:
                # on le modifie si il est pas bon car déjà pris :
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

        # On ajoute la période :
        self.periodes.append(periode)
        self.periodes.sort(key = lambda p: p.getDebut())
        self.app.getDonneeCalendrier().getPanneauActif().updateAffichage()
        self.app.getTaskEditor().ajouter(periode)
        
        # Si il n'y a pas de période active, alors on dit
        # que c'est automatiquement celle-ci par défaut.
        if self.activePeriode is None:
            self.setActivePeriode(periode)

        # On met le combobox des périodes à jour
        self.getApplication().getDonneeCalendrier().getParametreAffichage().updateComboboxPeriode()
    
    def supprimer(self, periode):
        """
        Permet de supprimer une période passée en argument.
        @param periode: la période à supprimer.
        """
        self.periodes.remove(periode)
        self.app.getDonneeCalendrier().getPanneauActif().updateAffichage()
        self.app.getTaskEditor().supprimer(periode)
        if self.activePeriode == periode:
            if len(self.periodes) > 0:
                self.setActivePeriode(self.periodes[0]) # TODO : Trouver la première période actuelle, ou prochaine le cas échéant.
            else:
                self.setActivePeriode(None)

    ""
    ######################################################
    # Méthodes liées aux fonctions de la barre d'outil : #
    ######################################################
    ""
    def deplacerPeriode(self):
        """
        Permet de déplacer la ou les périodes sélectionnées, via
        demande à l'utilisateur dans une boîte de dialogue usuelle.
        Il doit y avoir au moins une période sélectionnée.
        """
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
        """
        Permet de dupliquer la période sélectionnée, via
        demande à l'utilisateur dans une boîte de dialogue usuelle.
        Il doit y avoir exactement une seule période sélectionnée.
        """
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) != 1:
            showerror("Erreur de sélection", "Vous ne pouvez effectuer cette action qu'avec exactement une seule période sélectionnée.")
            return
        askPeriode(self, self.taskEditor, from_ = periodes[0], duplicate = True)

    def fusionnerPeriodes(self):
        """
        Permet de fusionner au moins deux périodes.
        Si il y a un trou qui n'était pas couvert auparavant par l'ensemble des périodes sélectionnées,
        il deviendra couvert par la nouvelle période créée.
        Il doit y avoir au moins deux périodes sélectionnées.
        """
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) < 2:
            return showerror("Erreur de sélection", "Vous devez avoir au moins 2 périodes sélectionnées pour pouvoir effectuer cette action.")

        # Fuuusioonnnnnn !!!!! :

        # TODO : changer les périodes des tâches concernées.
        nom = "Fusion de " + ", ".join(p.nom for p in periodes) + "."
        debut = min(periodes, key=lambda p: p.getDebut()).getDebut()
        fin   = max(periodes, key=lambda p: p.getFin()).getFin()
        desc = ", ".join(p.desc for p in periodes)
        color = periodes[0].getColor()

        # Supprimer toutes les périodes sélectionnées :
        self.supprimerPeriodes()

        # et créer la nouvelle née :
        self.ajouter(Periode(nom, debut, fin, desc, color))

    def lierSchedulablePeriode(self, periode, schedulable):
        """
        Permet de lier un schedulable à une période pour que le schedulable soit maintenant dans la période demandée.
        @param periode: la période dans laquelle mettre le schedulable demandée.
        @param schedulable: le schedulable à rajouter à la période.
        """
        raise NotImplementedError # TODO

    def scinderPeriode(self):
        """
        Permet de scinder la période sélectionnée, via
        demande à l'utilisateur dans une boîte de dialogue usuelle.
        Il doit y avoir exactement une seule période sélectionnée.
        """
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
            newPeriode = Periode(self, periode.nom, dateScindage, prevFin, periode.desc, periode.getColor())
            # TODO : changer les périodes des tâches concernées.
            self.ajouter(newPeriode)
        
    def supprimerPeriodes(self):
        """
        Permet de supprimer les périodes sélectionnées.
        Il doit y avoir au moins une période sélectionnée.
        """
        periodes = self.getPeriodesSelectionnees()
        if len(periodes) == 0:
            return showerror("Erreur de sélection", "Vous devez avoir au moins une période sélectionnée pour effectuer cette action.")
        for periode in reversed(periodes):
            self.periodes.remove(periode)
            self.app.getTaskEditor().supprimer(periode)
        self.app.getDonneeCalendrier().updateAffichage()
