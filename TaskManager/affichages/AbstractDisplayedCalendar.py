# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from .items.DatetimeItemPart import *

from util.widgets.Dialog import *
from util.widgets.TextWidget import *

from schedulable.task.Task import *
from schedulable.groupe.Groupe import *
from schedulable.task.dialog.askDureeTache import *

JOUR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

class AbstractDisplayedCalendar(Frame):
    """
    Classe représentant un calendrier qui doit être affiché,
    il se trouve qu'il y a également la classe qui contient tout
    ces affichages de calendrier qui hérite aussi de cette classe
    (je parle ici de DonneeCalendrier).
    """

    def __init__(self, master = None, **kwargs):
        """
        Constructeur d'un calendrier quelconque.
        Classe abstraite, donc veuillez utiliser une
        sous-classe pour éviter d'obtenir une erreur.
        Les paramètres sont ceux donnés au constructeur parent,
        celui de tkinter.Frame().
        """
        assert self.__class__ != AbstractDisplayedCalendar # interdire instanciation direct (classe abstraite version simple)
        super().__init__(master, **kwargs)
        # Forcement après le constructeur parent à cause d'un self.master requis pour le getPalette()
        super().config(bg = self.getPalette()["background"])
        # Note : self.master est référence vers DonneeCalendrier.

        # infos des heures :
        if self.getData().testDataExist("Calendrier", "Classique", "heure de début"):
            h = self.getData().getOneValue("Calendrier", "Classique", "heure de début").split(":")
            self.heureDebut = datetime.time(int(h[0]), int(h[1]), 0)
        if self.getData().testDataExist("Calendrier", "Classique", "heure de fin"):
            h = self.getData().getOneValue("Calendrier", "Classique", "heure de fin").split(":")
            self.heureFin = datetime.time(int(h[0]), int(h[1]), 0)

        # infos des jours :
        self.jourDebut = self.getDebutPeriode()
        self.jourFin   = self.getFinPeriode()

    "" #Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'application.
        @return l'application.
        """
        return self.getDonneeCalendrier().getApplication()

    def getData(self):
        """
        Getter pour le Data
        @return <Data>
        """
        return self.getApplication().getData()

    def getDebutPeriode(self):
        """
        Permet d'obtenir le jour du début de la période active si elle existe.
        @return datetime.date() correspondant au début de la période active si elle existe.
        @return None si elle n'existe pas.
        """
        return self.getPeriodeActive().getDebut() if self.getPeriodeActive() is not None else None

    def getDureeJour(self):
        """
        Permet d'obtenir un timedelta correspondant au nombre de jours affichés dans le calendrier.
        @return un datetime.timedelta() correspondant au nombre de jours affichés.
        """
        return (self.jourFin - self.jourDebut + datetime.timedelta(days=1)) if self.jourDebut is not None and self.jourFin is not None else datetime.timedelta()

    def getDonneeCalendrier(self):
        """
        Getter pour le DonneeCalendrier.
        @return : le DonneeCalendrier.
        """
        return self.master.master # Skip le NoteBook : pas le choix, désolé l'OO :/

    def getFinPeriode(self):
        """
        Permet d'obtenir le jour de fin de la période active si elle existe.
        @return datetime.date() correspondant à la fin de la période active si elle existe.
        @return None si elle n'existe pas.
        """
        return self.getPeriodeActive().getFin()   if self.getPeriodeActive() is not None else None

    def getHeureDebut(self):
        """
        Getter pour l'heure du début de l'affichage.
        @return datetime.time() de l'heure du début de l'affichage.
        """
        return self.heureDebut

    def getHeureFin(self):
        """
        Getter pour l'heure de fin de l'affichage.
        @return datetime.time() de l'heure de fin de l'affichage.
        """
        return self.heureFin

    def getJourDebut(self):
        """
        Permet d'avoir le jour du début de l'affichage.
        @return datetime.date() du début de l'affichage.
        """
        return self.jourDebut

    def getJourFin(self):
        """
        Getter pour le jour de fin de l'affichage.
        @return le datetime.date() correspondant au jour de fin
        de l'affichage.
        """
        return self.jourFin

    def getLongueurPeriode(self):
        """
        Permet d'obtenir la longueur de la période.
        @return un datetime.timedelta, de la longueur de la période
        (seulement les jours comptent). Le début autant que la fin sont pris en compte (Est-ce une bonne idée ?)
        @return datetime.timedelta(0) si la période active n'existe pas.
        """
        return (self.getFinPeriode() - self.getDebutPeriode() + datetime.timedelta(days=1)) if self.getPeriodeActive() is not None else datetime.timedelta()

    def getNbHeure(self):
        """
        Permet de savoir le nombre d'heures affichés dans ce calendrier.
        @return un nombre entier correspondant au nombre d'heures affichées.
        """
        return self.getHeureFin().hour - self.getHeureFin().hour

    def getNbJour(self):
        """
        Permet d'obtenir le nombre de jours affichés dans le calendrier.
        @return un int correspondant au nombre de jours affichés.
        """
        return self.getDureeJour().days

    def getPalette(self):
        """
        Getter pour la palette du couleur qui ne sont pas toutes dans ttk.Style
        @return <dict> data.palette
        """
        return self.getData().getPalette()

    def getParametreAffichage(self):
        """
        Getter du frame ParametreAffichage
        @return ParametreAffichage
        """
        return self.getZoneAffichage().getParametreAffichage()

    def getPartPosition(self, part):
        """
        Permet d'obtenir l'information de position de la partie à afficher.
        @return diffère suivant les besoins dans les sous-classes.
        """
        raise NotImplementedError

    def getPartRectangle(self, part):
        """
        Permet d'obtenir le rectangle dans laquelle la part doit être dessiné.
        Aussi utilisé par les ItemButtonPlus et les AbstractLink pour calculer
        leur positionnement.
        @param part: La partie dont on veut tester la position.
        @return util.geom.Rectangle() correspondant à la zone de cette partition.
        """
        raise NotImplementedError

    def getPartsOfDay(self, day):
        """
        @note: Peut-être que ce ne devrait pas être abstrait ?
        Permet de d'obtenir toutes les parties du jour choisi.
        @param day: Permet de choisir quel jour on regarde.
        @return La liste parties du jour choisi.
        """
        raise NotImplementedError

    def getPartSpan(self, part):
        """
        Permet d'obtenir l'information de répartition de la partie à afficher.
        @return diffère suivant les besoins dans les sous-classes.
        """
        raise NotImplementedError

    def getPeriodeActive(self):
        """
        Getter pour la période active.
        Nécessaire pour savoir quelle période afficher.
        @return la période active.
        """
        return self.getApplication().getPeriodManager().getActivePeriode()

    def getSelectedSchedulable(self):
        s = set()
        for schedulable in self.getPeriodeActive().getInstanciatedSchedulables():
            if schedulable.isSelected():
                s.add(schedulable)
            if isinstance(schedulable, Groupe):
                for task in schedulable.getSelectedTask():
                    s.add(schedulable) # Si on met task on peut plus dégrouper, si on met schedulable on peut pas décaler jour/heure

        return s # old : (schedulable for schedulable in self.getPeriodeActive().getInstanciatedSchedulables() if schedulable.isSelected())

    def getVisiblePart(self, part):
        """
        Permet d'obtenir la partie visible d'un DatetimeItemPart.
        @return l'objet inchangé si celui-ci est complètement visible.
        @return un nouveau DatetimeItemPart si celui-ci est partiellement visible,
        ce nouvel objet sera normalement entièrement visible.
        @return None si l'objet n'est pas visible du tout.
        """
        ## Test du jour :
        if part.getJour() < self.getJourDebut() or part.getJour() > self.getJourFin() + datetime.timedelta(days=1):
            return None

        ## Test de l'intégrité :
        # Est ce que la tache est dans les bonnes heures ?
        if part.getHeureDebut() >= self.getHeureFin() or part.getHeureFin() <= self.getHeureDebut():
            return None
        # Est ce que la tache dépasse ?
        if part.getHeureDebut() >= self.getHeureDebut() and part.getHeureFin() <= self.getHeureFin():
            return part

        # Sinon : correction du début et de la fin :
        debut = max(part.getHeureDebut(), self.getHeureDebut())
        fin   = min(part.getHeureFin(),   self.getHeureFin())

        return DatetimeItemPart(part.getJour(), debut, fin, part.getSchedulable())

    def getZoneAffichage(self):
        """
        Getter pour la ZoneAffichage
        @return : la ZoneAffichage
        """
        return self.getDonneeCalendrier().getZoneAffichage()

    ""
    ##############
    # Setters :  #
    ##############
    ""
    def setDureeJour(self, valeur):
        """
        Setter pour le nombre de jours affichés, via un timedelta.
        Change la position de la fin de la période pour y arriver.
        @param valeur: datetime.timedelta() correspondant au nombre de
        jours à afficher.
        """
        # XXX : Pourquoi faire "valeur - datetime.timedelta(days=1)" ?
        # Ne serait-ce pas en dehors de la fonction de faire cette vérification ?
        self.jourFin = (self.jourDebut + valeur - datetime.timedelta(days=1)) if self.jourDebut is not None else None

        # TODO : À revoir. -> utiliser une nouvelle méthode.
        if self.getJourFin() > self.getFinPeriode():
            self.setJourFin(self.getFinPeriode())

        self.updateAffichage()

    def setHeureDebut(self, valeur):
        """
        Setter pour l'heure du début de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure du début de l'affichage.
        """
        self.heureDebut = valeur
        self.updateAffichage()

    def setHeureFin(self, valeur):
        """
        Setter pour l'heure de fin de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure de fin de l'affichage.
        """
        self.heureFin = valeur
        self.updateAffichage()

    def setJourDebut(self, valeur):
        """
        Permet de modifier le jour de début de l'affichage.
        @param valeur: Le datetime.time() à mettre
        """
        self.jourDebut = valeur + datetime.timedelta()

    def setJourFin(self, valeur):
        """
        Setter pour le jour de fin de l'affichage.
        @param valeur: le datetime.date() du jour de fin de l'affichage.
        """
        self.jourFin = valeur

    def setNbJour(self, valeur):
        """
        Setter pour le nombre de jours affichés, via un nombre entier.
        Change la position du jour de fin afin d'y parvenir.
        @param valeur : int correspondant au nombre de jours à afficher.
        """
        # TODO : Rajouter le check de dépassement de fin de période -> nouvelle méthode.
        self.jourFin = (self.jourDebut + datetime.timedelta(days=valeur-1)) if self.jourDebut is not None else None
        self.updateAffichage()

    ""
    ######################
    # Methodes liées aux #
    #    schedulables    #
    ######################
    ""
    def addSchedulable(self, schedulable, region = None):
        """
      - Permet d'ajouter un schedulable sur le panneau d'affichage.

      - Méthode à redéfinir dans les sous-classes, en appelant
        la variante parent (celle de SuperCalendrier), car celle-ci
        s'occuppe de mettre le schedulable dans la liste et de demander la durée
        à l'utilisateur quand celle-ci n'est pas définie (càd: elle est de 0).

      - Cependant, la suite doit être redéfinie dans les sous-classes pour gérer
        l'affichage de la tâche.

      - Et le plus important : la méthode doit renvoyer le schedulable avec sa durée prédéfinie.

      - Dans les sous-classes, ça donne :
        def addSchedulable(self, schedulable, region = None):
            '''Permet d'ajouter une schedulable, region correspond au début de la tâche si celle-ci n'en a pas.'''
            if (schedulable := SuperCalendrier.addSchedulable(self, schedulable, region)) == None: # region est géré dans la variante parent : on ne s'en occupe plus ici.
                return

            ####################
            # Ajout graphique. #
            ####################
            ... # Note : on utilisera très probablement une liste, non ?
            ... # et peut-être une classe particulière, défini dans le même fichier ?
            ... # Quand je dis une liste, c'est une liste différente de self.listeTask,
                # car celle-ci existe déjà, mais qui contiendrait les cadres/panneaux des classes
                # que l'on va créer pour cette représentation. Cependant, on pourrais dire, si
                # c'est possible, que cette classe pourrait être utilisée pour plusieurs dispositions
                # si celles-cis sont similaires. Mais chaque disposition pourra aussi avoir sa classe
                # d'affichage d'une tâche custom.

            return schedulable # on renvoie la tache avec son début et sa durée.
            # C'était "TRÈS IMPORTANT", maintentant que c'est la période qui s'en occupe, ce n'est plus nécéssaire

        @param schedulable: le schedulable à rajouter
        @param region: datetime.datetime() correspondant au début du schedulable si celui-ci n'en a pas (notamment le cas via Drag&Drop)
        @return le schedulable, potentiellement changé.
        """
        raise NotImplementedError

    def applyRegion(self, schedulable, region):
        """
        Cette méthode permet d'appliquer une région à une tâche, pour le dnd.
        Cela permet de créer la sous-tâche.
        @param tache: la tâche à mettre.
        @param region: la région à appliquer.
        @return la sous-tâche juste créée.
        """
        if region and schedulable.getDebut() is None:
            # Important de copier pour ne pas altérer l'originelle :
            # Cela permet de pouvoir Drag&Drop une même tâche
            # plusieurs fois.
            schedulable = schedulable.copy()
            schedulable.setDebut(region)
        if isinstance(schedulable, Task) and schedulable.getDuree() <= datetime.timedelta():
            schedulable.setDuree(askDureeTache(self, self.getLongueurPeriode()))
            if not schedulable.getDuree():
                return None
        return schedulable

    def clicSurObjet(self, objet):
        """
        Méthode à exécuter quand on clic sur l'un des objets.
        Utile pour sélectionner une tâche par exemple.
        @param objet: l'objet sur lequel on a cliqué.
        """
        raise NotImplementedError

    def deleteSelected(self):
        """
        Méthode qui supprime tous les schedulables sélectionné
        """
        for s in self.getSelectedSchedulable():
            s.delete()

    def deselectEverything(self):
        """
        Méthode qui permet de désélectionner tout ce qui l'est actuellement.
        """
        for s in self.getPeriodeActive().getInstanciatedSchedulables():
            s.setSelected(False)
        self.getDonneeCalendrier().deselectJours() # Appel updateColor au passage, donc tant mieux =)

    def identify_region(self, x, y):
        """
        Renvoie la région à la position X et Y.
        X et Y sont relatifs à ce widget.

        La région doit être quelque chose qui doit permettre de
        savoir où ajouter une tâche si celle-ci n'a pas de début/période
        prédéfinie. (voir #addTask(tache, REGION = ...))

        Cela doit donc correspondre à un ensemble avec une date/heure
        de début, on utilisera pour cela la classe datetime.datetime().

        Méthode à redéfinir dans les sous-classes.
        @param x: Position X relative à ce widget, sera bien souvent la position de la souris.
        @param y: Position Y relative à ce widget, sera bien souvent la position de la souris.
        @return datetime.datetime() indiquant la région trouvé aux coordonnées indiquées.
        """
        raise NotImplementedError

    def onIntervertir(self):
        pass # Juste pour qu'elle existe # Sera considérablement changé

    def removeSchedulable(self, obj):
        """
        Retire un schedulable
        à redefinir dans chaque sous classe
        """
        raise NotImplementedError

    def selectJour(self, jour, control=False):
        """
        Permet de sélectionner toutes les objets d'un jour en sélectionnant le jour.
        @param jour: le jour à sélectionner.
        @param control: False si on désélectionne d'abord, True si on ajoute.
        """
        if not control:
            self.deselectEverything()

        for schedulable in self.getPeriodeActive().getInstanciatedSchedulables():
            # Si l'objet est partiellement sur le jour :
            if schedulable.getDebut().date() <= jour and schedulable.getFin().date() >= jour:
                schedulable.setSelected(True)
        self.updateColor()

        self.getDonneeCalendrier().selectJour(jour) # C'est l'une des raison pour lesquelles on a besoin d'un truc similaire à la branche Calendrier_data.

    ""
    ####################
    # Méthodes liées à #
    #   l'affichage    #
    ####################
    ""
    def _makeTextWidget(self, dt ,master = None):
        """
        Méthode qui permet d'obtenir un textWidget avec toutes les options qu'il faut (couleur + texte)
        @param dt     : <datetime.date> le jour du TextWidget
        @param master : <container> ce sur quoi est le TextWidget
        @return <TextWidget> tout beau, tout bien fait
        """
        # On donne une référence à data pour qu'elle est la Palette, comme c'est statique on regarde si elle en a une d'abord
        TextWidget.giveData(self.getData())

        ## Gestion du texte
        # Le fichier existe ?
        if not self.getData().testDataExist("Calendrier"):
            texte = dt.year + " " + dt.month + " " + dt.day
        # On cherche le lien
        if self.getData().testDataExist("Calendrier", "Calendrier", "Lien"):
            lien = self.getData().getOneValue("Calendrier", "Calendrier", "Lien")[1]
        else :
            lien = "."
        # On cherche le style
        if self.getData().testDataExist("Calendrier", "Calendrier", "sytle d'affichage"):
            ## Traitement du texte
            # Constantes
            jour        = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            mois        = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

            texte = self.getData().getOneValue("Calendrier", "Calendrier", "sytle d'affichage")

            numJour     = str(dt.day)
            numMois     = str(dt.month)
            numJour2C   = "%02i"%dt.day
            numMois2C   = "%02i"%dt.month
            numAnnee    = str(dt.year)
            jourSemaine = str(jour[dt.weekday()])
            mois        = str(mois[dt.month-1])

            texte = texte.replace("NJ2", numJour2C)
            texte = texte.replace("JS0", jourSemaine[0])
            texte = texte.replace("NM2", numMois2C)
            texte = texte.replace("NA", numAnnee)
            texte = texte.replace("JS", jourSemaine)
            texte = texte.replace("M3", mois[:3])
            texte = texte.replace("NJ", numJour)
            texte = texte.replace("MO", mois)

            texte = texte.replace("_", lien)

        ## gestion du mode
        # Si c'est aujourd'hui
        if datetime.date.today() == dt:
            mode = 'jour'
        else :
            mode = "highlightedWidget"
        # S'il est sélectionné
        mode = "selected" if self.getDonneeCalendrier().isJourSelected(dt) else mode

        return TextWidget(master, text = texte, nbJour = self.getNbJour(), mode = mode)

    def doConfiguration(self, paramAffichage):
        """
        Méthode pour éventuellement changer la barre d'outil secondaire + taskEditor + parametreAffichage
        quand ce panneau est actif.

        Par défaut, fait un reset normal de cette barre.
        """
        self.getApplication().setModeEditionPeriode(False)
        paramAffichage.setPeriodeMode(False)
        #paramAffichage.setStateListe(NORMAL)
        for duree in self.getZoneAffichage().getListeDuree():
            if self.getNbJour() == int(duree[1]):
                paramAffichage.setModeListe(duree[0])
                break # Car on a trouvé et on veux pas faire le else
        else:
            # Pour le tout début comme self.getDureeJour() (et self.getNbJour()) renvoient 0, on préfèrera "Période"
            if self.getDureeJour() == self.getLongueurPeriode():
                paramAffichage.setModeListe("Période")
            else:
                paramAffichage.setModeListe("%s jours"%self.getNbJour())

    def updateAffichage(self, force = False):
        """
        Méthode pour mettre à jour l'affichage.
        Appelée lors de chaque changements avec
        setHeureDebut, setHeureFin, setJourDebut et setNbJour
        @param force: Si mis sur True, force la mise à jour totale de l'affichage,
        utile quand il y a des bugs sur les liens d'"interframmeInner link" quand
        le nombre d'heures de la journée à été changé.
        """
        raise NotImplementedError

    def updateColor(self):
        """
        Permet de mettre à jour la couleur uniquement de tout les IDisplayableItems
        """
        raise NotImplementedError

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def _setBinding(self, nomCalendrier, aBinder):
        """
        Fonction qui va charger tous les bind a mettre
        @param nomCalendrier : <str> nom du calendrier pour connaître le dictionnaire à aller chercher (!) avec majuscule (!)
        @param aBinder       : <objet> a bind, un Canvas ou self tout simplement
        """
        dictionnaire = self.getApplication().getBindingIn("Affichage-" + nomCalendrier)
        for binding in dictionnaire:
            for key in dictionnaire[binding]["bindings"]:
                aBinder.bind_all(key, lambda e, binding = binding : self.event_generate("<<" + "Affichage-" + nomCalendrier + "-" + binding + ">>"), add=1)

    def hasParent(self, parent, widget):
        """
        Méthode qui cherche si le widget à un parent précis
        @param parent : <str> le parent recherché
        @param widget : <tkinter.widget> celui dont on cherche la provenance

        @return : <bool> True si le widget l'a comme parent sinon False
        """
        master = widget.master
        while True:
            try:
                if master == parent:
                    return True
                elif master == self.getDonneeCalendrier().getCalendarZone():
                    return self.getDonneeCalendrier().getPanneauActif() == parent
                master = master.master
            except AttributeError:
                return False
