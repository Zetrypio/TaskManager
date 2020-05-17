# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from toolbar.ToolBar import *
from toolbar.PeriodToolBar import *
from toolbar.dialog.decalageHeureDialog import *
from toolbar.dialog.decalageJourDialog import *
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
        self.gestionHeure(nb, pos)

    def gestionHeure(self, nombreHeure, position):
        """
        Fonction qui s'occupe de rajouter des heures visibles.
        En dehors de la fonction ajouterHeure lié au bouton car on pourrait avoir à ajouter des heures autrements que par le bouton
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

    def ajouterJour(self):
        totalJour = self.getDonneeCalendrier().getLongueurPeriode().days-1
        nb, pos = askAjouterJour(totalJour)
        self.gestionJour(nb, pos)

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


    def selectionnerJour(self):
        pass
    def afficherMasquerJour(self):
        pass
    def deplacerIntervertir(self):
        self.getDonneeCalendrier().intervertir()

    def decalerJour(self):
        # Si la liste est vide on évite la question
        if len(self.getDonneeCalendrier().getSelectedTask()) == 0:
            return
        
        # On détermine le nombre de jour min et max
        first, last = self.getFirstAndLast()
        
        debut = self.getPeriodeActive().getDebut() # Date de début
        fin   = self.getPeriodeActive().getFin()   # Date de fin
        

        jourRetireBloque = (first.getFin().date() - debut).days
        jourAjoutBloque = (fin - last.getDebut().date()).days
        nb, pos, param = askDecalJour(debut, fin, jourRetireBloque, jourAjoutBloque)

        if nb is None or pos is None or param is None or nb == 0:
            return

        # Ajustement des jours
        horsChamp = False

        for tache in self.getDonneeCalendrier().getSelectedTask():
            # Si tout va bien
            if  (tache.getDebut()+datetime.timedelta(days=nb)).date() == (tache.getFin()+datetime.timedelta(days=nb)).date()\
            and debut <= (tache.getDebut()+datetime.timedelta(days=nb)).date()\
            and fin   >= (tache.getFin()+datetime.timedelta(days=nb)).date():
                print("125 CalZone ok")
                tache.setDebut(tache.getDebut()+datetime.timedelta(days=nb))

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

            # Si au final il y a des taches hors champs on demande si on affiche les heures pour voir le.s tache.s
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


    def decalerHeure(self): # TODO : gérer une tache de plusieurs jours (peut-être)
        # Si la liste est vide on évite la question
        if len(self.getDonneeCalendrier().getSelectedTask()) == 0:
            return
        # S'il y a une tache de plus j'un jour on est mal enfin à voir
        for tache in self.getDonneeCalendrier().getSelectedTask():
            if tache.getDuree() > datetime.timedelta(days=1):
                showerror("Selection invalide", "Vous ne pouvez pas décaler en heure une tache de plus d'un jour.")

        # On détermine le nombre d'heure min et max
        first, last = self.getFirstAndLast()

        periode = self.getPeriodeActive()

        heureDebut = self.getDonneeCalendrier().getHeureDebut()
        heureFin   = self.getDonneeCalendrier().getHeureFin()

        lastDiffJour = (last.getDebut().date() - periode.getDebut()).days # .days pour intifier le tout
        firstDiffJour = (periode.getFin() - first.getFin().date()).days
        heureRetirerMax = last.getDebut().hour + lastDiffJour * 24
        heureAjoutMax = heureFin.hour - first.getFin().hour + 1 + firstDiffJour * 24
        nb, pos, param = askDecalHeure(heureRetirerMax, heureAjoutMax, heureDebut, heureFin, last.getDebut().hour - heureDebut.hour, heureFin.hour - first.getFin().hour+1)


        if nb is None or pos is None or param is None or nb == 0:
            return

        # Ajustement des heures
        horsChamp = False

        for tache in self.getDonneeCalendrier().getSelectedTask():
            # Si tout va bien
            if  (tache.getDebut()+datetime.timedelta(hours=nb)).date() == (tache.getFin()+datetime.timedelta(hours=nb)).date()\
            and heureDebut <= (tache.getDebut()+datetime.timedelta(hours=nb)).time()\
            and heureFin   >= (tache.getFin()+datetime.timedelta(hours=nb)).time():
                print("219 CalZone ok")
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

            # Si au final il y a des taches hors champs on demande si on affiche les heures pour voir le.s tache.s
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

                    # Si la fin est apres le debut (hors date) ET qu'il est apres le referent
                    if tache.getDebut().time() < tache.getFin().time() and tache.getFin().time() > timeApres:
                        tacheApres = tache
                        timeApres  = tache.getFin().time()

                    # Si le début est apres la fin (hors date) ET qu'il est apres le referent
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

    def grouper(self):
        pass
    def degrouper(self):
        pass

    def avancementMannuel(self):
        for tache in self.getDonneeCalendrier().getSelectedTask():
            tache.reverseStateValide()

    def avancementJourFini(self):
        maintenantJour = datetime.datetime.combine(datetime.date.today(), datetime.time(23,59,59))
        self.getPeriodeActive().setDateStatut(maintenantJour)
        for tache in self.getDonneeCalendrier().listeTask:
            tache.updateStatut()


    def avancementNormal(self):
        maintenant = datetime.datetime.now()
        self.getPeriodeActive().setDateStatut(maintenant)
        for tache in self.getDonneeCalendrier().listeTask:
            tache.updateStatut()
        print(datetime.datetime.now())

    def getPanneauActif(self):
        return self.zoneDynamicCalendarFrame.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.zoneDynamicCalendarFrame.getDonneeCalendrier()
    
    def getPeriodeActive(self):
        """ Getter de la periode active """
        return self.getDonneeCalendrier().getPeriodeActive()
    # Pour la barre d'outil des périodes :
    def voirTacheDansVue(self):
        pass
    def supprimerTache(self):
        pass
    def getFirstAndLast(self):
        """
        Getter parmi les taches sélectionnés
        Permet de déterminer la tache qui fini le plus tot et la tache qui commence le plus tard
        @return first : (Task) tache qui fini le plus tot
        @return last  : (Task) tache qui commence le plus tard
        """
        first = None # Contient la tache qui finit    le plus tot
        last  = None # Contient la tache qui commence le plus tard
        for tache in self.getDonneeCalendrier().getSelectedTask():
            if first is None or first.getFin() > tache.getFin():
                first = tache
            if last is None or last.getDebut() < tache.getDebut():
                last = tache
        return first, last
