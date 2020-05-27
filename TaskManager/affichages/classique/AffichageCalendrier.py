# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from ..AbstractDisplayedCalendar import *
from .ObjetClassique import *

class AffichageCalendrier(AbstractDisplayedCalendar):
    def __init__(self, master = None, **kwargs):
        """Affichage par défaut du calendrier et de ses tâches."""
        super().__init__(master, bg="violet")
        # Note : self.master est référence vers Notebook.
 
        self.listeLabelHeure = []       # \
        self.listeLabelJour = []        #  )-> Tout est dans le nom de ces trois listes.
        self.listeSeparateurJour = []   # /
        
        self.listeDisplayableItem = []

        self.frame = Frame(self)
        self.frame.pack(expand = YES, fill = BOTH)

        self.updateAffichage()
        
        self.__parts = []

        # self.bind("<Configure>", lambda e : self.updateAffichage())

    def updateAffichage(self): # override
        # On détruit et recrée le Frame
        self.frame.destroy()
        self.__parts = []
        self.frame = Frame(self)
        self.frame.pack(expand = YES, fill = BOTH)
        self.frame.bind("<Button-1>", self.mouseClicked, add = True)
        #self.frame.bind("<Escape>",  self.escapePressed)

        # On précalcule :
        self.__precalculer()

        # On affiche les trucs
        self.__afficherLesHeures()
        self.__afficherLesJours()
        self.__afficherLesTaches()

    def getPartPosition(self, part):
        return 1+ 2*(part.getJour() - self.getJourDebut()).days

    def getPartSpan(self, part):
        return 1 # TODO
    
    def getPartsOfDay(self, day):
        return (part for part in self.__parts if part.getJour() == day)

    def escapePressed(self, event):
        super().escapePressed(event)
    
    def addTask(self, schedulable, region = None):
        """
        Permet d'ajouter un objet planifiable à l'affichage dans le calendrier.
        @param schedulable: l'objet à rajouter pour l'affichage.
        @param region : correspond au début de l'objet planifiable si celle-ci n'en a pas.
        @return la tâche qui à peut-être été changé pour des raisons d'affichage.
        """
        # :=  on attribut la variable en plus de tester la condition
        if not (schedulable := super().addTask(schedulable, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        self.listeDisplayableItem.append(ObjetClassique(self, schedulable))

        self.updateAffichage()

        return schedulable # on revoie le schedulable avec éventuellement son début et sa duree. TRÈS IMPORTANT.

    def identify_region(self, x, y):
        # On regarde si c'est trop à gauche (sur les heures):
        colonne, ligne = self.frame.grid_location(x, y)
        colonne = (colonne-1)//2

        jour = self.getJourDebut() + datetime.timedelta(days = colonne)
        jour = datetime.datetime(jour.year, jour.month, jour.day)
        
        minute = self.getHeureDebut().hour*60 +(ligne - 1)
        heure, minute = minute//60, minute%60

        # TODO : A Changer :
        return jour + datetime.timedelta(hours = heure, minutes = minute)

    def __precalculer(self):
        """
        Permet de préculculer les Parts non fusionnées
        des tâches affichées dans ce calendrier.
        """
        for displayable in self.listeDisplayableItem:
            if isinstance(displayable, AbstractMultiFrameItem):
                self.__parts.extend(displayable.getRepartition())

    def __afficherLesHeures(self):
        """
        Permet de mettre à jour les labels des heures.
        """
        # On efface ceux déjà présent :
        self.listeLabelHeure = []

        # et on les recrées :
        for heure in range(self.getHeureDebut().hour, self.getHeureFin().hour+1): # le +1 pour compter Début ET Fin.
            self.listeLabelHeure.append(Label(self.frame, text=heure, bd = 1, relief = SOLID))
            # Note : Un détail à la minute près va être fait,
            # donc on compte 60 lignes pour une heure.
            # La ligne 0 étant la ligne des labels des jours,
            # On compte à partir de 1, c'est-à-dire en ajoutant 1.
            self.listeLabelHeure[-1].grid(row=(heure-self.getHeureDebut().hour)*60+1, # le *60 pour faire un détail à la minute près
                                          column=0,      # Les labels des heures sont réservés à la colonne de gauche.
                                          rowspan=60,    # Mais ils prennent 60 minutes et lignes.
                                          sticky="NSWE") # Permet de centrer le label et d'en remplir les bords par la couleur du fond.
        # Cela permet de réadapter les lignes et colones qui sont en expand pour le grid.
        self.__adapteGrid()
    
    def __afficherLesJours(self):
        """
        Permet de mette à jour les labels des jours.
        """
        self.listeLabelJour = []
        self.listeSeparateurJour = []
        
        # Variable qui parcours la liste, rangeDate n'est pas fonctionnelle car après il y un soucis de last entre période et 2/5/... jours
        jour = self.getJourDebut()
        for compteur in range(self.getNbJour()):

            self.listeLabelJour.append(Label(self.frame, text=JOUR[jour.weekday()], bg = "light grey"))
            self.listeLabelJour[-1].bind("<Button-1>",        lambda e, jour=jour: self.selectTaskJour(jour))
            self.listeLabelJour[-1].bind("<Control-Button-1>",lambda e, jour=jour: self.selectTaskJour(jour, control=True))
            self.listeLabelJour[-1].grid(row=0, column=1+((jour-self.getJourDebut()).days)*2, sticky="NSWE")
            if jour < self.getJourFin():
                self.listeSeparateurJour.append(Separator(self.frame, orient=VERTICAL))
                self.listeSeparateurJour[-1].grid(row=0, column=2+2*(jour-self.getJourDebut()).days, rowspan = 60*(self.getHeureFin().hour+1-self.getHeureDebut().hour)+1, sticky="NS")

            jour += datetime.timedelta(days = 1)
            
        self.__adapteGrid()

    def __afficherLesTaches(self):
        """
        Permet de mettre à jour l'affichage des tâches.
        """
        for displayable in self.listeDisplayableItem:
            displayable.redraw(self.frame)

    def __adapteGrid(self):
        """
        Permet d'étirer les cases du grid, sauf la ligne d'entête des jours
        et la colonne d'entête des heures.
        
        Cette méthode se doit d'être appelée une fois que tout est dessiné,
        sinon ce qui serais rajouté après n'aurait pas forcément eu cet étirage des cases.
        """
        # à mettre À LA FIN ! ! ! (pour les expands)
        for column in range(self.getNbJour()*2+1):
            if column%2 ==0:
                self.frame.columnconfigure(column,weight=0)
            else:
                self.frame.columnconfigure(column, weight=1)
        self.frame.rowconfigure(ALL,weight=1)
        self.frame.rowconfigure(0, weight=0)

