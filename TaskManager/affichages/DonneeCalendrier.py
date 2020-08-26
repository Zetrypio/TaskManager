# -*- coding:utf-8 -*-

from .classique.AffichageCalendrier import *
from .gantt.AffichageGantt import *
from .periode.AffichageCalendrierPeriode import *

from .AbstractDisplayedCalendar import *

class DonneeCalendrier(AbstractDisplayedCalendar):
    """
    Classe contenant le panneau à onglets avec tout les
    affichages des calendriers.
    """
    CLIPBOARD = []
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de DonneeCalendrier.
        @param master: master du tkinter.Frame que cet objet est.
        @param **kwargs: configurations de l'affichage du tkinter.Frame que cet objet est.
        """
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers ZoneAffichage.

        # Ceci est un panneau à onglet.
        self.panneau = Notebook(self)

        # Création du contenu des différents onglets.
        self.listPanneau = []
        self.listPanneau.append(AffichageCalendrier(self.panneau)) # Liste de tout les panneaux pour appliquer un changement à tous
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

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'application.
        @return l'Application.
        """
        return self.master.getApplication()

    def getDonneeCalendrier(self):
        """
        Il est important de redéfinir cette méthode car sinon
        ça prend la variante parente qui n'est pas bonne.
        @return self
        """
        return self

    def getPanneauActif(self):
        """
        Getter pour le panneau actif.
        @return le panneau actif.
        """
        # self.panneau.select() renvoie l'id du panneau actif
        # self.panneau.index() renvoie l'index d'un panneau selon son id
        # on peut donc utiliser notre liste avec cet index.
        return self.listPanneau[self.panneau.index(self.panneau.select())]

    def getParametreAffichage(self):
        """
        Getter pour le ParametreAffichage.
        @return le ParametreAffichage.
        """
        return self.master.getParametreAffichage()

    def getToutLesPanneaux(self):
        """
        Renvoie une copie de la liste de tout les panneaux.
        @return une copie de la liste de tout les panneaux.
        """
        return self.listPanneau[:]

    def getZoneAffichage(self):
        """
        Getter pour la ZoneAffichage.
        @return la ZoneAffichage.
        """
        return self.master

    def isJourSelected(self, jour):
        """
        Permet de savoir si un jour est sélectionné.
        @return True si le jour est sélectionné, False sinon.
        """
        return jour in self.jourSelectionnes

    ""
    #############
    # Setters : #
    #############
    ""
    def setDureeJour(self, jour):
        """
        Setter pour le nombre de jour via datetime.timedelta().
        @param jour: datetime.timedelta() correspondant au nombre de jours à afficher.
        """
        for panneau in self.listPanneau:
            panneau.setDureeJour(jour)
        super().setDureeJour(jour)

    def setHeureDebut(self, heure):
        """
        Setter pour l'heure du début.
        @param heure: datetime.time() de l'heure du début.
        """
        for panneau in self.listPanneau:
            panneau.setHeureDebut(heure)
        super().setHeureDebut(heure)

    def setHeureFin(self, heure):
        """
        Setter pour l'heure de la fin.
        @param heure: datetime.time() de l'heure de la fin.
        """
        for panneau in self.listPanneau:
            panneau.setHeureFin(heure)
        super().setHeureFin(heure)

    def setJourDebut(self, jour):
        """
        Setter pour le jour du début de l'affichage.
        @param jour: datetime.date() du jour du début.
        """
        for panneau in self.listPanneau:
            panneau.setJourDebut(jour)
        super().setJourDebut(jour)

    def setJourFin(self, jour):
        """
        Setter pour le jour de fin de l'affichage.
        @param jour: datetime.date() du jour de fin.
        """
        for panneau in self.listPanneau:
            panneau.setJourFin(jour)
        super().setJourFin(jour)

    def setNbJour(self, jour):
        """
        Setter pour le nombre de jour via nombre entier.
        @param jour: int correspondant au nombre de jours à afficher.
        """
        for panneau in self.listPanneau:
            panneau.setNbJour(jour)
        super().setNbJour(jour)

    def setPeriodeActiveDebut(self, jour):
        """
        Setter pour le jour du début de la période active.
        @param jour: datetime.date() correspondant au jour
        du début de la période active à mettre.
        """

        ### Option utile ou pas ?, à voir dans le préférences ?, faire ça seulement si on est au début ? ##

        # Si le nouveau jour de début de la période est avant, il faut changer le nouveau jour de début
        #if jour < self.getJourDebut():
        duree = self.getJourFin() - jour + datetime.timedelta(days=1)
        self.setJourDebut(jour)
        self.setDureeJour(duree)
        self.getPeriodeActive().setDebut(jour)

    def setPeriodeActiveFin(self, jour):
        """
        Setter pour le jour de fin de la période active.
        @param jour: datetime.date() correspondant au jour
        de fin de la période active à mettre.
        """
        self.getPeriodeActive().setFin(jour)
        # Si le nouveau jour de fin de la période est avant, il faut changer le nouveau jour de fin
        if jour < self.getJourFin():
            self.setJourFin(jour)

    ""
    ######################
    # Méthodes liées aux #
    #    schedulables    #
    ######################
    ""
    def addSchedulable(self, schedulable):
        """
        Permet d'ajouter un objet planifiable, répercute l'appel sur tout les différents calendriers.
        @param schedulable: l'objet planifiable à ajouter.
        @param region: correspond au début de la tâche si celle-ci n'en a pas.
        """
        ####################
        # Ajout graphique. #
        ####################
        for panneau in self.listPanneau:
            panneau.addSchedulable(schedulable)

    def deselectJours(self):
        """
        Permet de désélectionner tout les jours sélectionnés.
        """
        self.jourSelectionnes.clear()
        self.updateColor()

    def removeSchedulable(self, obj):
        """
        Permet d'enlever un objet du calendrier.
        @param obj: L'objet à enlever.
        """
        for panneau in self.listPanneau:
            panneau.removeSchedulable(obj)

    def selectJour(self, jour):
        """
        Permet d'ajouter un jour à la liste de ceux sélectionnés.
        @param jour: le datetime.date() à sélectionner.
        """
        self.jourSelectionnes.add(jour)
        self.updateColor()

    def switchPeriode(self):
        """
        Méthode qui met à jour les schedulables de chaque calendrier
        """
        # On vide tout
        for panneau in self.getToutLesPanneaux():
            panneau.resetSchedulable()

        ## Sur la nouvelle période
        # Quand on charge pas de période via Application#load(), self.getPeriodeActive() is None
        if self.getPeriodeActive() is None:
            return
        periode = self.getPeriodeActive()
        periode.resetInstanciatedSchedulables()

        # On instancie tout :
        for schedulable in periode.getPrimitivesSchedulables():
            schedulable.instantiate()

        # Et on met à jour
        self.updateAffichage()

    ""
    ####################
    # Méthodes liées à #
    #   l'affichage    #
    ####################
    ""
    def panneauChange(self, e):
        """
        Méthode effectuée lors de l'événement d'un panneau qui à changé,
        pour faire la configuration des barres d'outils ou autre.
        @param e: Événement non utilisé.
        """
        p = self.getPanneauActif()
        p.doConfiguration(self.master.getParametreAffichage())

    def updateAffichage(self, force = False):
        """
        Permet de mettre à jour l'affichage.
        """
        # Faire un parcours des panneaux pour pouvoir effectuer les changements
        # sur TOUTES les disposition de calendriers (Gantt, calendrier classique etc)
        for panneau in self.listPanneau:
            panneau.updateAffichage(force)

        if self.getJourDebut() == self.getDebutPeriode():
            self.master.zoneParametre.boutonBienAvant.configure(state=DISABLED)
            self.master.zoneParametre.boutonAvant.configure(state=DISABLED) # Désactive le bouton quand on est au début de la période
        else:
            self.master.zoneParametre.boutonBienAvant.configure(state=NORMAL)
            self.master.zoneParametre.boutonAvant.configure(state=NORMAL)

        # Si on est sur le panneau des périodes on garde les boutons
        if isinstance(self.getPanneauActif(), AffichageCalendrierPeriode):
            self.master.zoneParametre.boutonBienAvant.configure(state=NORMAL)
            self.master.zoneParametre.boutonAvant.configure(state=NORMAL)
            self.master.zoneParametre.boutonBienApres.configure(state=NORMAL)
            self.master.zoneParametre.boutonApres.configure(state=NORMAL)

        elif self.getFinPeriode() is None or self.getJourFin() is None:
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

    def updateColor(self):
        """
        Permet de mettre à jour la couleur de toutes les tâches de tout les panneaux.
        """
        for p in self.getToutLesPanneaux():
            p.updateColor()

    ""
    #################
    # Copier/Coller #
    #################
    ""
    def coller(self):
        """
        Methode qui permet de coller ce qu'il y a d'enregistré
        dans la liste DonneeCalendrier.CLIPBOARD
        """
        for dico in DonneeCalendrier.CLIPBOARD:
            # Si c'est un groupe :
            if "listTasks" in dico:
                g = Groupe.load(dico, self.getPeriodeActive())
                # Si on sélectionne un jour, on place le groupe dessus
                if len(self.jourSelectionnes) == 1 and (list(self.jourSelectionnes)[0] >= self.getPeriodeActive().getDebut() and list(self.jourSelectionnes)[0] <= self.getPeriodeActive().getFin()):
                    # On place à ce moment là la tache
                    ecart = g.getDebut().date() - list(self.jourSelectionnes)[0]
                    for tache in g.getListTasks():
                        tache.setDebut(tache.getDebut() - ecart)
                elif g.getFin().date() < self.getPeriodeActive().getDebut() or g.getDebut().date() > self.getPeriodeActive().getFin():
                    # On remet en place tout le monde
                    ecart = g.getDebut().date() - self.getPeriodeActive().getDebut()
                    for tache in g.getListTasks():
                        tache.setDebut(tache.getDebut() - ecart)
                # Si on est pas dans la période :
                self.getPeriodeActive().addPrimitiveSchedulable(g)
                g.instantiate()

            # Sinon c'est une tâche standard :
            else :
                t = Task.load(dico, self.getPeriodeActive())
                # Si on sélectionne un jour, on place la tache dessus
                if len(self.jourSelectionnes) == 1 and (list(self.jourSelectionnes)[0] >= self.getPeriodeActive().getDebut() and list(self.jourSelectionnes)[0] <= self.getPeriodeActive().getFin()):
                    # On place à ce moment là la tache
                    ecart = t.getDebut().date() - list(self.jourSelectionnes)[0]
                    t.setDebut(t.getDebut() - ecart)
                elif t.getFin().date() < self.getPeriodeActive().getDebut() or t.getDebut().date() > self.getPeriodeActive().getFin():
                    t.setDebut(datetime.datetime(year   = self.getPeriodeActive().getDebut().year,
                                                 month  = self.getPeriodeActive().getDebut().month,
                                                 day    = self.getPeriodeActive().getDebut().day,
                                                 hour   = t.getDebut().hour,
                                                 minute = t.getDebut().minute
                               ))
                self.getPeriodeActive().addPrimitiveSchedulable(t)
                t.instantiate()

        # Pas de dépendances, car on supprime l'UID
        self.updateAffichage()

    def copier(self):
        """
        Méthode qui enregistre la selection
        dans DonneeCalendrier.CLIPBOARD
        """
        # On vide tout
        DonneeCalendrier.CLIPBOARD.clear()
        # On met tout dans la liste
        for s in self.getSelectedSchedulable():
            dico = s.saveByDict()
            # On reset l'id
            dico["id"] = None
            DonneeCalendrier.CLIPBOARD.append(dico)

    def couper(self):
        """
        Méthode qui enregistre la sélection dans
        DonneeCalendrier.CLIPBOARD et qui la supprime ensuite
        """
        # On copie
        self.copier()
        # Et on supprime
        for s in self.getSelectedSchedulable():
            s.delete()

    ""
    ###################
    # Autres methodes #
    ###################
    ""
    def escapePressed(self, event):
        """
        Méthode appelée lors de l'appuie de la touche Échappe.
        On annule ce qu'on fait sur tous les panneaux.
        @param event: l'événement, possiblement utilisé par les panneaux.
        """
        for panneau in self.listPanneau:
            panneau.escapePressed(event)

    def intervertir(self):
        """
        Permet d'intervertir les 2 jours exactement sélectionnés, affiche une erreur à l'utilisateur sinon.
        """
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

        # Seulement les tâches sélectionnés au cas où il y en a qu'on veux pas switch
        for tache in self.getSelectedSchedulable():
            if   tache.getDebut().date() <= jour1 and tache.getFin().date() >= jour1 and isinstance(tache, Task): # On ne peut déplacer ici que les tâches pour le moment...
                tacheJour1.add(tache)
            elif tache.getDebut().date() <= jour2 and tache.getFin().date() >= jour2 and isinstance(tache, Task): # aussi
                tacheJour2.add(tache)

        diff = datetime.datetime.combine(jour2, datetime.time()) - datetime.datetime.combine(jour1, datetime.time())
        # On applique les changements
        for tache in tacheJour1-tacheJour2:
            tache.setDebut(tache.getDebut()+diff)
        for tache in tacheJour2-tacheJour1:
            tache.setDebut(tache.getDebut()-diff)

        for p in self.getToutLesPanneaux():
            p.onIntervertir()
        self.updateAffichage(force=True)

    def mouseClicked(self, event):
        """
        Méthode effectuée lors d'un clic.
        Répercutée sur le panneau actif.
        @param event: l'événement, envoyé au panneau actif.
        """
        self.getPanneauActif().mouseClicked(event)
