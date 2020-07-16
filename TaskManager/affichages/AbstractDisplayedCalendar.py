# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from .items.DatetimeItemPart import *

from util.widgets.Dialog import *

from schedulable.task.Task import *

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
        kwargs["bg"] = "light gray"
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers DonneeCalendrier.

        # infos des heures :
        self.heureDebut = datetime.time(8, 0, 0)
        self.heureFin = datetime.time(17, 59, 0)

        # infos des jours :
        self.jourDebut = self.getDebutPeriode()
        self.jourFin   = self.getFinPeriode()

        # liste des tâches :
        self.listeTask = []

    def clicSurObjet(self, objet):
        """
        Méthode à exécuter quand on clic sur l'un des objets.
        Utile pour sélectionner une tâche par exemple.
        @param objet: l'objet sur lequel on a cliqué.
        """
        raise NotImplementedError

    def deselectEverything(self):
        """
        Méthode qui permet de désélectionner tout ce qui l'est actuellement.
        """
        for s in self.listeTask: # Getter ?
            s.setSelected(False)
        self.getDonneeCalendrier().deselectJours() # Appel updateColor au passage, donc tant mieux =)

    def onIntervertir(self):
        pass # Juste pour qu'elle existe # Sera considérablement changé

    #def getSelectedTask(self):
        #"""
        #Permet d'obtenir la liste des tâches sélectionnées.
        #@return: la liste des tâches sélectionnées.
        #@deprecated: permettra de renvoyer plus que des tâches,
        #dans le futur. Changera alors de nom.
        #"""
        #return [task for task in self.listeTask if task.isSelected()]

    def selectJour(self, jour, control=False):
        """
        Permet de sélectionner toutes les objets d'un jour en sélectionnant le jour.
        @param jour: le jour à sélectionner.
        @param control: False si on désélectionne d'abord, True si on ajoute.
        """
        if not control:
            self.deselectEverything()

        for schedulable in self.listeTask: # On pourrait pas renommer la liste ?
            # Si l'objet est partiellement sur le jour :
            if schedulable.getDebut().date() <= jour and schedulable.getFin().date() >= jour:
                schedulable.setSelected(True)
        self.updateColor()

        self.getDonneeCalendrier().selectJour(jour) # C'est l'une des raison pour lesquelles on a besoin d'un truc similaire à la branche Calendrier_data.

    def getSelectedSchedulable(self):
        return (schedulable for schedulable in self.listeTask if schedulable.isSelected())

    def getDonneeCalendrier(self):
        """
        Getter pour le DonneeCalendrier.
        @return: le DonneeCalendrier.
        """
        return self.master.master # Skip le NoteBook : pas le choix, désolé l'OO :/

    def getApplication(self):
        """
        Getter pour l'application.
        @return l'application.
        """
        return self.getDonneeCalendrier().getApplication()

    def getPeriodeActive(self):
        """
        Getter pour la période active.
        Nécessaire pour savoir quelle période afficher.
        @return la période active.
        """
        return self.getApplication().getPeriodManager().getActivePeriode()
    def getLongueurPeriode(self):
        """
        Permet d'obtenir la longueur de la période.
        @return un datetime.timedelta, de la longueur de la période
        (seulement les jours comptent). Le début autant que la fin sont pris en compte (Est-ce une bonne idée ?)
        @return datetime.timedelta(0) si la période active n'existe pas.
        """
        return (self.getFinPeriode() - self.getDebutPeriode() + datetime.timedelta(days=1)) if self.getPeriodeActive() is not None else datetime.timedelta()
    def getDebutPeriode(self):
        """
        Permet d'obtenir le jour du début de la période active si elle existe.
        @return datetime.date() correspondant au début de la période active si elle existe.
        @return None si elle n'existe pas.
        """
        return self.getPeriodeActive().getDebut() if self.getPeriodeActive() is not None else None
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
    def setHeureDebut(self, valeur):
        """
        Setter pour l'heure du début de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure du début de l'affichage.
        """
        self.heureDebut = valeur
        self.updateAffichage()
        
    def getNbheure(self):
        """
        Permet de savoir le nombre d'heures affichés dans ce calendrier.
        @return un nombre entier correspondant au nombre d'heures affichées.
        """
        return self.getHeureFin().hour - self.getHeureFin().hour

    def getHeureFin(self):
        """
        Getter pour l'heure de fin de l'affichage.
        @return datetime.time() de l'heure de fin de l'affichage.
        """
        return self.heureFin
    def setHeureFin(self, valeur):
        """
        Setter pour l'heure de fin de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure de fin de l'affichage.
        """
        self.heureFin = valeur
        self.updateAffichage()

    def getJourDebut(self):
        """
        Permet d'avoir le jour du début de l'affichage.
        @return datetime.date() du début de l'affichage.
        """
        return self.jourDebut
    def setJourDebut(self, valeur):
        """
        Permet de modifier le jour de début de l'affichage.
        @param valeur: Le datetime.time() à mettre 
        """
        self.jourDebut = valeur + datetime.timedelta()
        self.updateAffichage()

    def getNbJour(self):
        """
        Permet d'obtenir le nombre de jours affichés dans le calendrier.
        @return un int correspondant au nombre de jours affichés.
        """
        return self.getDureeJour().days
    def getDureeJour(self):
        """
        Permet d'obtenir un timedelta correspondant au nombre de jours affichés dans le calendrier.
        @return un datetime.timedelta() correspondant au nombre de jours affichés.
        """
        return (self.jourFin - self.jourDebut + datetime.timedelta(days=1)) if self.jourDebut is not None and self.jourFin is not None else datetime.timedelta()
    def setNbJour(self, valeur):
        """
        Setter pour le nombre de jours affichés, via un nombre entier.
        Change la position du jour de fin afin d'y parvenir.
        @param valeur : int correspondant au nombre de jours à afficher.
        """
        # TODO : Rajouter le check de dépassement de fin de période -> nouvelle méthode.
        self.jourFin = (self.jourDebut + datetime.timedelta(days=valeur-1)) if self.jourDebut is not None else None
        self.updateAffichage()

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

    def getVisiblePart(self, part):
        """
        Permet d'obtenir la partie visible d'un DatetimeItemPart.
        @return l'objet inchangé si celui-ci est complètement visible.
        @return un nouveau DatetimeItemPart si celui-ci est partiellement visible,
        ce nouvel objet sera normalement entièrement visible.
        @return None si l'objet n'est pas visible du tout.
        """
        # Test du jour :
        if part.getJour() < self.getJourDebut() or part.getJour() > self.getJourFin()  + datetime.timedelta(days=1):
            return None
        
        # Test de l'intégrité :
        if part.getHeureDebut() >= self.getHeureDebut() and part.getHeureFin() <= self.getHeureFin():
            return part
        
        # Sinon : correction du début et de la fin :
        debut = max(part.getHeureDebut(), self.getHeureDebut())
        fin   = min(part.getHeureFin(),   self.getHeureFin())
        
        return DatetimeItemPart(part.getJour(), debut, fin, part.getSchedulable())

    def getPartPosition(self, part):
        """
        Permet d'obtenir l'information de position de la partie à afficher.
        @return diffère suivant les besoins dans les sous-classes.
        """
        raise NotImplementedError

    def getPartSpan(self, part):
        """
        Permet d'obtenir l'information de répartition de la partie à afficher.
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

    def getJourFin(self):
        """
        Getter pour le jour de fin de l'affichage.
        @return le datetime.date() correspondant au jour de fin
        de l'affichage.
        """
        return self.jourFin
    def setJourFin(self, valeur):
        """
        Setter pour le jour de fin de l'affichage.
        @param valeur: le datetime.date() du jour de fin de l'affichage.
        """
        self.jourFin = valeur

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

    def addTask(self, schedulable, region = None): # TODO : renommer en addSchedulable
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

        def addTask(self, schedulable, region = None):
            '''Permet d'ajouter une schedulable, region correspond au début de la tâche si celle-ci n'en a pas.'''
            if (schedulable := SuperCalendrier.addTask(self, schedulable, region)) == None: # region est géré dans la variante parent : on ne s'en occupe plus ici.
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

            return schedulable # on renvoie la tache avec son début et sa durée. TRÈS IMPORTANT.
        
        @param schedulable: le schedulable à rajouter
        @param region: datetime.datetime() correspondant au début du schedulable si celui-ci n'en a pas (notamment le cas via Drag&Drop)
        @return le schedulable, potentiellement changé.
        @deprecated: va être renommé en addSchedulable()
        """
        if self.__class__ == AbstractDisplayedCalendar:
            raise NotImplementedError
        if region and schedulable.getDebut() is None:
            # Important pour ne pas altérer l'originelle :
            # Cela permet de pouvoir Drag&Drop une même tâche
            # plusieurs fois.
            schedulable = schedulable.copy()
            schedulable.setDebut(region)
        if isinstance(schedulable, Task) and schedulable.getDuree() <= datetime.timedelta():
            schedulable.setDuree(self.askDureeTache())
            if not schedulable.getDuree():
                return None
        if schedulable is None : return
        self.listeTask.append(schedulable)
        # SUITE À FAIRE DANS LES SOUS-CLASSES.
        return schedulable

    def removeSchedulable(self, obj):
        self.listeTask.remove(obj)
        self.updateAffichage(force = True)

    def askDureeTache(self):
        """
        Permet de demander la durée de la tâche à l'utilisateur.
        @return la durée choisie par l'utilisateur.
        """
        # TODO : bouger dans un fichier à part (comme tout les dialogues) ?
        # Fonction quand on ferme le dialogue :
        duree = None
        def onClose(bouton):
            """Exécutée quand l'un des boutons du dialogue est pressé."""
            nonlocal duree
            if bouton == "Ok":
                duree = datetime.timedelta(days = int(d.get()), hours = int(h.get()), minutes = int(m.get()))
                if duree > datetime.timedelta():
                    fen.quit()
                    fen.destroy()
                else:
                    showerror("Durée invalide", "Veuillez mettre une durée plus grande que 0.")
            else:
                fen.destroy()
        def adapteHeureJour():
            """Adaptation des heures et des jours quand on augmente ou diminue trop les heures ou les minutes."""
            minutes = int(m.get())
            heures  = int(h.get())
            jours   = int(d.get())
            
            while minutes >= 60:
                minutes -= 60
                heures += 1
            while minutes < 0:
                minutes += 60
                heures -= 1
            while heures >= 24:
                heures -= 24
                jours += 1
            while heures < 0:
                heures += 24
                jours -= 1
            jours = max(0, min(jours, self.getLongueurPeriode()))
            
            m.set(minutes)
            h.set(heures)
            d.set(jours)
            
        # Création du dialogue :
        fen = Dialog(self, title = "Choix de la durée de la tâche",
                   buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Annuler',))
        # Widgets du dialogue :
        Label(fen, text = "Choisissez la durée de la Tâche").pack(side = TOP, fill = X)
        d = Spinbox(fen, from_ = 0, to = self.getLongueurPeriode().days, increment = 1, width = 4)
        d.pack(side = LEFT)
        Label(fen, text = "Jours").pack(side = LEFT)
        h = Spinbox(fen, from_ = -1, to = 24, increment = 1, width = 4, command = adapteHeureJour)
        h.pack(side = LEFT)
        Label(fen, text = "Heures").pack(side = LEFT)
        m = Spinbox(fen, from_ = -1, to = 60, increment = 1, width = 4, command = adapteHeureJour)
        m.pack(side = LEFT)
        Label(fen, text = "Minutes").pack(side = LEFT)
        d.set(0)
        h.set(1)
        m.set(0)
        # lancement du dialogue:
        fen.activateandwait()
        return duree

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

    def doConfiguration(self, paramAffichage):
        """
        Méthode pour éventuellement changer la barre d'outil
        secondaire quand ce panneau est actif.
        
        Par défaut, fait un reset normal de cette barre.
        """
        self.getApplication().setModeEditionPeriode(False)
        paramAffichage.setStateListe(NORMAL)
        if self.getDureeJour() == self.getLongueurPeriode():
            paramAffichage.setModeListe("Période")
        elif self.getNbJour() == 7:
            paramAffichage.setModeListe("1 semaine")
        elif self.getNbJour() == 1:
            paramAffichage.setModeListe("1 jour")
        else:
            paramAffichage.setModeListe("%s jours"%self.getNbJour())

    def _setBinding(self, nomCalendrier, aBinder):
        """
        Fonction qui va charger tous les bind a mettre
        @param nomCalendrier : <str> nom du calendrier pour connaire le dictionnaire à aller chercher (!) avec majuscule (!)
        @param aBinder       : <objet> a bind, un canevas ou self tout simplement
        """
        dictionnaire = self.getApplication().getBindingIn("Affichage-" + nomCalendrier)
        for binding in dictionnaire:
            for key in dictionnaire[binding]["bindings"]:
                aBinder.bind(key, lambda e, binding = binding : self.event_generate("<<" + binding + ">>"), add=1)
