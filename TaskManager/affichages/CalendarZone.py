# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
from tkinter.messagebox import showerror

from schedulable.groupe.dialog.groupDialog import *

from toolbar.ToolBar import *
from toolbar.PeriodToolBar import *
from toolbar.dialog.decalageHeureDialog import *
from toolbar.dialog.decalageJourDialog import *
from toolbar.dialog.gestionHeureCalendrierDialog import *
from toolbar.dialog.gestionJourDialog import *

from .periode.dialog.dateDialog import *
from .ZoneAffichage import *

class CalendarZone(Frame):
    """
    Classe contenant la barre d'outil et la zone d'affichage.
    """
    def __init__(self, master = None, periodeManager = None, **kwargs):
        """
        Constructeur de CalendarZone.
        @param master: master du tkinter.Frame() que cet objet est.
        @param periodeManager: le PeriodeManager pour la barre d'outil des périodes, connue dans cet objet.
        @param **kwargs: Les options d'affichages pour le tkinter.Frame() que cet objet est.
        """
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

    "" # Pour le repli de code je rappelle
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'application.
        @return l'application.
        """
        return self.master

    def getBarreOutilActive(self):
        """
        Getter pour la barre d'outil des périodes active.
        @return la barre d'outil des périodes active.
        """
        if self.__isBarrePeriode:
            return self.outilBarPeriode
        else:
            return self.outilBar

    def getDonneeCalendrier(self):
        """
        Getter pour le DonneeCalendrier.
        @return le DonneeCalendrier.
        """
        return self.getZoneAffichage().getDonneeCalendrier()

    def getFirstAndLast(self):
        """
        Getter parmi les tâches sélectionnés
        Permet de déterminer la tache qui fini le plus tôt et la tache qui commence le plus tard
        @return first : (Task) tache qui fini le plus tôt
        @return last  : (Task) tache qui commence le plus tard
        """

        # Manière la plus simple avec min() et max() comme ceci, le critère se faisant suivant la lambda :
        first = min(self.getDonneeCalendrier().getSelectedSchedulable(), key=lambda t: t.getFin())
        last  = max(self.getDonneeCalendrier().getSelectedSchedulable(), key=lambda t: t.getDebut())

        return first, last

    def getPanneauActif(self):
        """
        Getter pour le panneau actif dans DonneeCalendrier.
        @return le panneau actif dans DonneeCalendrier.
        """
        return self.getZoneAffichage().getPanneauActif()

    def getParametreAffichage(self):
        """
        Getter pour les ParametreAffichage.
        @return le ParametreAffichage.
        """
        return self.getZoneAffichage().getParametreAffichage()

    def getPeriodeActive(self):
        """
        Getter de la periode active.
        @return la période active.
        """
        return self.getDonneeCalendrier().getPeriodeActive()

    def getZoneAffichage(self):
        """
        Getter pour la ZoneAffichage.
        @return la ZoneAffichage.
        """
        return self.zoneDynamicCalendarFrame

    ""
    #############
    # Setters : #
    #############
    ""
    def setBarreOutilPeriode(self, value):
        """
        Permet de switcher entre la barre d'outil normale
        et la barre d'outil des périodes.
        @param value: True si c'est la barre d'outil des périodes, False sinon.
        """
        self.__isBarrePeriode = value
        if value:
            self.outilBarPeriode.pack(side=TOP, fill=X, expand=NO)
            self.outilBar.pack_forget()
        else:
            self.outilBarPeriode.pack_forget()
            self.outilBar.pack(side=TOP, fill=X, expand=NO)

    ""
    ####################################################
    # Pour la barre d'outil des calendries standards : #
    ####################################################
    ""
    def afficherMasquerJour(self):
        """
        Permet d'afficher ou masquer un jour... TODO
        """
        pass # TODO

    def ajouterHeure(self):
        """
        Méthode exécutée par la barre d'outil des périodes
        quand l'utilisateur appuie sur le bouton pour rajouter des heures.
        """
        min = self.getDonneeCalendrier().getHeureDebut()
        max = datetime.timedelta(hours=23) - datetime.timedelta(hours=self.getDonneeCalendrier().getHeureFin().hour)
        max2 = self.getDonneeCalendrier().getHeureFin()
        nbHeure = max2.hour - min.hour
        nb, pos = askAjouterHeure(min, max, nbHeure)
        self.gestionHeure(nb, pos)
        self.getDonneeCalendrier().updateAffichage(force = True)

    def ajouterJour(self):
        """
        Méthode exécutée par la barre d'outil des périodes
        quand l'utilisateur appuie sur le bouton pour rajouter des jours.
        """
        totalJour = self.getDonneeCalendrier().getLongueurPeriode().days-1
        nb, pos = askAjouterJour(totalJour)
        self.gestionJour(nb, pos)

    def avancementMannuel(self):
        """
        Permet de valider les tâches sélectionnées.
        """
        for tache in self.getPeriodeActive().getPrimitivesSchedulables():
            if tache.isSelected():
                tache.setDone(True)
        self.getApplication().getTaskEditor().redessiner()

    def avancementNormal(self):
        """
        Valide TOUTES les tâches qui sont avant maintenant.
        """
        now = datetime.datetime.now()
        for schedulable in self.getDonneeCalendrier().getPeriodeActive().getInstanciatedSchedulables():
            if schedulable.getFin() <= now:
                schedulable.setDone(True)
            schedulable.updateStatut()
        self.getApplication().getTaskEditor().redessiner()

    def avancementJourFini(self):
        """
        Valide toutes les tâches qui sont terminées aujourd'hui.
        """
        now = datetime.date.today()
        for tache in self.getDonneeCalendrier().getPeriodeActive().getInstanciatedSchedulables():
            if tache.getFin().date() == now:
                tache.setDone(True)
            tache.updateStatut()
        self.getApplication().getTaskEditor().redessiner()

    def decalerHeure(self): # TODO : gérer une tâche de plusieurs jours (peut-être)
        """
        Permet de décaler les tâches sélectionnées par l'utilisateur,
        d'un certain nombre d'heures, suivant ce que l'utilisateur souhaite.
        Un message lui sera demandé si jamais cela dépasse de la journée.
        """
        # Si la liste est vide on évite la question
        if len(list(self.getDonneeCalendrier().getSelectedSchedulable())) == 0:
            return
        # S'il y a une tache de plus j'un jour on est mal enfin à voir #TODO
        for tache in self.getDonneeCalendrier().getSelectedSchedulable():
            if tache.getDuree() > datetime.timedelta(days=1):
                showerror("Selection invalide", "Vous ne pouvez pas décaler en heure une tache de plus d'un jour.")
                return

        # On détermine le nombre d'heure min et max
        first, last = self.getFirstAndLast()

        periode = self.getPeriodeActive()

        heureDebut = self.getDonneeCalendrier().getHeureDebut()
        heureFin   = self.getDonneeCalendrier().getHeureFin()

        lastDiffJour = (last.getDebut().date() - periode.getDebut()).days # .days pour int-ifier le tout
        firstDiffJour = (periode.getFin() - first.getFin().date()).days
        heureRetirerMax = last.getDebut().hour + lastDiffJour * 24
        heureAjoutMax = heureFin.hour - first.getFin().hour + 1 + firstDiffJour * 24
        nb, pos, param = askDecalHeure(heureRetirerMax, heureAjoutMax, heureDebut, heureFin, last.getDebut().hour - heureDebut.hour, heureFin.hour - first.getFin().hour+1)


        if nb is None or pos is None or param is None or nb == 0:
            return

        # Ajustement des heures
        horsChamp = False

        for tache in self.getDonneeCalendrier().getSelectedSchedulable():
            if isinstance(tache, Task):
                # Si tout va bien
                if  (tache.getDebut()+datetime.timedelta(hours=nb)).date() == (tache.getFin()+datetime.timedelta(hours=nb)).date()\
                and heureDebut <= (tache.getDebut()+datetime.timedelta(hours=nb)).time()\
                and heureFin   >= (tache.getFin()+datetime.timedelta(hours=nb)).time():
                    tache.setDebut(tache.getDebut()+datetime.timedelta(hours=nb))

                # Si on dépasse, on cadre selon les limites et mode bloquer
                elif param == "bloquer":
                    # Si on retire des heures au début
                    if nb < 0:
                        # On peut pas mettre un
                        tache.setDebut(datetime.datetime.combine(tache.getDebut().date(), heureDebut))
                    # Si on ajoute pour mettre à la fin
                    else:
                        heureFin = heureFin # Time
                        time = datetime.datetime.combine(tache.getFin().date(), heureFin) - tache.getDuree() # datetime - timedelta
                        tache.setDebut(time)

                # Si on dépasse et que l'on ne bloque pas
                elif param == "duree":
                    tache.setDebut(tache.getDebut()+datetime.timedelta(hours=nb))
                    horsChamp = True

                # Si au final il y a des tâches hors champs on demande si on affiche les heures pour voir le.s tache.s
                if horsChamp and askChangerHeure():
                    timeAvant = heureDebut
                    timeApres = heureFin
                    tacheAvant = None
                    tacheApres = None
                    for tache in self.getDonneeCalendrier().getSelectedTask():
                        # Si le début est avant la fin (hors date) ET qu'il est avant le referent
                        if tache.getDebut().time() < tache.getFin().time() and tache.getDebut().time() < timeAvant:
                            tacheAvant = tache
                            timeAvant  = tache.getDebut().time()

                        # Si la fin est avant le début (hors date) ET qu'il est avant le referent
                        elif tache.getDebut().time() > tache.getFin().time() and tache.getFin().time() < timeAvant:
                            tacheAvant = tache
                            timeAvant  = tache.getFin().time()

                        # Si la fin est après le début (hors date) ET qu'il est après le referent
                        if tache.getDebut().time() < tache.getFin().time() and tache.getFin().time() > timeApres:
                            tacheApres = tache
                            timeApres  = tache.getFin().time()

                        # Si le début est après la fin (hors date) ET qu'il est après le referent
                        elif tache.getDebut().time() > tache.getFin().time() and tache.getDebut().time() > timeApres:
                            tacheApres = tache
                            timeApres  = tache.getDebut().time()

                    # Maintenant on applique les changements
                    if tacheAvant is not None:
                        addAvant = heureDebut.hour - timeAvant.hour
                        self.gestionHeure(addAvant, "Avant")
                    if tacheApres is not None:
                        addApres = timeApres.hour - heureFin.hour
                        self.gestionHeure(addApres, "Apres")

        self.getDonneeCalendrier().updateAffichage()

    def decalerJour(self):
        """
        Permet de décaler les tâches sélectionnées par l'utilisateur,
        d'un certain nombre de jours, suivant ce que l'utilisateur souhaite.
        Un message lui sera demandé si jamais cela dépasse de la période.
        """
        # Si la liste est vide on évite la question
        if len(list(self.getDonneeCalendrier().getSelectedSchedulable())) == 0:
            return

        # On détermine le nombre de jour min et max
        first, last = self.getFirstAndLast()

        debut = self.getPeriodeActive().getDebut() # Date de début
        fin   = self.getPeriodeActive().getFin()   # Date de fin

        # Les variables ci-dessous calculent le nombre max de jours pour le décalage
        # si il y a un bloquage dans un sens ou dans l'autre. Cependant, quand on
        # bloque, on peut bouger jusqu'à ce que la fin de la tâche la plus tôt
        # atteigne la fin de la période ; ou que le début de la tâche la plus tard
        # atteigne le début de la période.
        jourRetireBloque = (last.getDebut().date() - debut).days
        jourAjoutBloque  = (fin - first.getFin().date()).days

        # Appel du dialogue à l'utilisateur :
        nb, pos, param = askDecalJour(debut, fin, jourRetireBloque, jourAjoutBloque)

        if nb is None or pos is None or param is None or nb == 0:
            return

        # Ajustement des jours
        horsChamp = False
        duree = datetime.timedelta(days = nb)

        for tache in self.getDonneeCalendrier().getSelectedSchedulable():
            if isinstance(tache, Task): # TODO avec groupe.
                # Si tout va bien
                if  debut <= (tache.getDebut()+duree).date()\
                and fin   >= (tache.getFin()+duree).date():
                    tache.setDebut(tache.getDebut()+duree)

                # Si on dépasse, on cadre selon les limites et mode bloquer
                elif param == "bloquer":
                    # Si on retire des heures au début
                    if nb < 0:
                        # On peut pas mettre un
                        tache.setDebut(datetime.datetime.combine(debut, tache.getDebut().time()))
                    # Si on ajoute pour mettre à la fin
                    else:
                        time = datetime.datetime.combine(fin, tache.getFin().time()) - tache.getDuree() # datetime - timedelta
                        tache.setDebut(time)

                # Si on dépasse et que l'on ne bloque pas
                elif param == "duree":
                    tache.setDebut(tache.getDebut()+datetime.timedelta(days=nb))
                    horsChamp = True

                # Si au final il y a des tâches hors champs on demande si on affiche les heures pour voir le.s tache.s
                if horsChamp:
                    horsChamp = False
                    choix, periode = askComplicationjour(tache, self.getApplication().getPeriodManager())
                    # On annule les changements
                    if choix is None:
                        tache.setDebut(tache.getDebut()-datetime.timedelta(days=nb))
                        continue
                    # On agrandit la période
                    elif choix == "agrandir":
                        if tache.getDebut().date() < debut:
                            addAvant = (debut - tache.getDebut().date()).days
                            self.gestionJour(addAvant, "Avant")

                        else:
                            addApres = (last.getFin().date()-fin).days
                            self.gestionJour(addApres, "Apres")
                    elif choix == "supprimer": # TODO supprimer la tache
                        pass
                    elif choix == "independante": # TODO rendre la tache indépendante
                        pass
                    elif choix =="changer":
                        tache.setPeriode(periode)

        self.getDonneeCalendrier().updateAffichage()

    def degrouper(self):
        """
        Permet de dégrouper un groupe.
        """
        # Obtention de la période et des schedulables instanciés sélectionnés :
        periode = self.getDonneeCalendrier().getPeriodeActive()
        schedulables = list(self.getDonneeCalendrier().getSelectedSchedulable())
        # Petite vérification :
        if any(not isinstance(obj, Groupe) for obj in schedulables): # Si il y en a au moins UN qui n'est pas un groupe :
            return showerror("Sélection invalide", "Vous ne pouvez dégrouper que des groupes.")
        print("b", schedulables, set(schedulables))
        # Pour chaque groupes sélectionnés :
        for groupe in set(schedulables):
            print(groupe)
            # Ré-ajout des tâches qui étaient dans le groupe :
            for t in groupe.getListTasks():
                if t in groupe.getSelectedTask():
                    periode.addPrimitiveSchedulable(t)
                    t.instantiate()
                    groupe.removeTask(t)

            # Suppression du groupe , s'il n'y a plus qu'une ou 0 tache :
            if len(groupe.getListTasks()) <= 1:
                if groupe.getListTasks() != set():
                    lastTache = list(groupe.getListTasks())[-1]
                    periode.addPrimitiveSchedulable(lastTache)
                    lastTache.instantiate()
                    groupe.removeTask(lastTache)

                periode.removeInstanciatedSchedulable(groupe)
                periode.removePrimitiveSchedulable(groupe)

        # Mise à jour de l'affichage qu'à la fin :
        self.getApplication().getTaskEditor().redessiner()
        self.getDonneeCalendrier().updateAffichage()

    def deplacerIntervertir(self):
        """
        Permet d'intervertir 2 jours exactement.
        Ce sont ceux sélectionnés par l'utilisateur.
        """
        self.getDonneeCalendrier().intervertir()

    def gestionHeure(self, nombreHeure, position):
        """
        Fonction qui s'occupe de rajouter des heures visibles.
        En dehors de la fonction ajouterHeure lié au bouton car on pourrait avoir à ajouter des heures autrement que par le bouton
        @param nombreHeure : int relatif, permet d'ajouter ou retirer des heures
        @param position    : string "Avant" / "Apres" pour savoir ou appliquer les changements
        """
        if nombreHeure is not None and position is not None:
            if   position == "Avant":
                timeHeure = datetime.time(self.getDonneeCalendrier().getHeureDebut().hour - nombreHeure)
                self.getDonneeCalendrier().setHeureDebut(timeHeure)
            elif position == "Apres":
                timeHeure = datetime.time(self.getDonneeCalendrier().getHeureFin().hour + nombreHeure, self.getDonneeCalendrier().getHeureFin().minute)
                self.getDonneeCalendrier().setHeureFin(timeHeure)

    def gestionJour(self, nombreDeJour, position):
        """
        Fonction qui s'occupe d'ajouter ou de supprimer des jours
        En dehors de la fonction ajouterJour lié au bouton car on pourrait avoir à ajouter des jours autrement que par le bouton
        @param nombreDeJour : int relatif, permet d'ajouter ou retirer des jours
        @param position     : string "Avant" / "Apres" pour savoir ou appliquer les changements
        """
        if nombreDeJour is not None and position is not None:
            periode = self.getPeriodeActive()
            if   position == "Avant":
                self.getDonneeCalendrier().setPeriodeActiveDebut(periode.getDebut() - datetime.timedelta(days=nombreDeJour))
            elif position == "Apres":
                self.getDonneeCalendrier().setPeriodeActiveFin(periode.getFin() + datetime.timedelta(days=nombreDeJour))

            # Mise à jour du Combobox
            self.getParametreAffichage().updateComboboxNbJour()

    def grouper(self):
        """
        Permet de grouper les tâches.
        """
        periode = self.getPeriodeActive()
        schedulables = list(self.getDonneeCalendrier().getSelectedSchedulable())
        # Petite vérification :
        if len(schedulables) < 2:
            return showerror("Sélection invalide", "Vous devez avoir au moins 2 éléments sélectionner pour pouvoir les grouper.")
        groupe = None
        taches = []
        for obj in schedulables:
            if isinstance(obj, Groupe):
                if groupe is None:
                    groupe = obj
                elif groupe != obj:
                    return showerror("Sélection invalide", "Vous ne pouvez pas grouper des tâches dans plusieurs groupes.")
            elif not isinstance(obj, Task):
                return showerror("Sélection invalide", "Vous ne pouvez grouper que des tâches.")
            else:
                taches.append(obj)
        
        # Création du groupe :
        ajout = True
        if groupe:
            ajout = False
        groupe = groupe or askGroup(periode)
        if groupe is None:
            return
        
        for t in taches:
            groupe.addTask(t)
        
        # "Suppression" des tâches de l'affichage global étant donné qu'elles sont dans le groupe.
        for t in taches:
            periode.removeInstanciatedSchedulable(t)
            try:
                periode.removePrimitiveSchedulable(t)
            except:
                for ta in periode.getPrimitivesSchedulables():
                    if ta.isContainer() and ta.getSubTasks() is not []:
                        if t in ta.getSubTasks():
                            ta.removeSubTask(t)
                            break

        if ajout:
            periode.addPrimitiveSchedulable(groupe)
            self.getApplication().getTaskEditor().redessiner()
            groupe.instantiate()
            self.getDonneeCalendrier().updateAffichage()

    def selectionnerJour(self):
        """
        Méthode pour demander un jour à sélectionner à l'utilisateur, pour le sélectionner ensuite où qu'il soit.
        """
        jour = askdate()
        if jour is not None:
            donneeCalendrier = self.getDonneeCalendrier()
            if jour >= donneeCalendrier.getDebutPeriode() and jour <= donneeCalendrier.getFinPeriode():
                donneeCalendrier.deselectJours()
                donneeCalendrier.selectJour(jour)
                dureeJours = donneeCalendrier.getDureeJour()
                if donneeCalendrier.getJourDebut() > jour:
                    donneeCalendrier.setJourDebut(jour)
                    donneeCalendrier.setDureeJour(dureeJours)
                    donneeCalendrier.updateAffichage()
                elif donneeCalendrier.getJourFin() < jour:
                    donneeCalendrier.setJourFin(jour)
                    donneeCalendrier.setJourDebut(jour - dureeJours + datetime.timedelta(days=1))
                    donneeCalendrier.updateAffichage()
            else:
                # TODO : mettre dans le dialogue lui-même
                showerror("Date invalide", "La date que vous avez choisie est en dehors des limites de la période.")

    ""
    ########################################
    # Pour la barre d'outil des périodes : #
    ########################################
    ""
    def voirTacheDansVue(self):
        """
        Permet de voir une tâche dans une autre vue, via demande
        à l'utilisateur dans une boîte de dialogue usuelle.
        TODO
        """
        pass

    def supprimerTache(self):
        """
        Permet de supprimer une tâche indépendante.
        Fera-t-on des groupes indépendants ? Si oui -> renommer en supprimerSchedulable()...
        TODO
        """
        pass


