# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from superclassCalendrier import *

class TacheEnCalendrier(Frame):
    def __init__(self, master, task, **kwargs):
        bg = kwargs.get("bg", "#FFFFFF")
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers AffichageCalendrier
        Label(self, text = task.nom, font = "Arial 12 bold", bg = bg).grid(sticky = "w")
        Label(self, text = task.desc, bg = bg).grid(sticky = "w", row = 1)

class AffichageCalendrier(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        """Affichage par défaut du calendrier et de ses tâches."""
        SuperCalendrier.__init__(self, master, bg="violet")
        # Note : self.master est référence vers Notebook.
 
        # Exemple pour le grid
        # self.bouton = Button(self, text="je suis ici")
        #
        # Le sticky dans tous les sens pour un expand dans tous les sens
        # self.bouton.grid(row=0, column=0, sticky ="NSWE")
        
        self.__afficherLesHeures() # à la fin pour avoir les variables créées.
        self.__afficherLesJours()

    def updateAffichage(self): # override
        self.__afficherLesHeures()
        self.__afficherLesJours()

    def addTask(self, tache, region = None):
            '''Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas.'''
            if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici.
                return

            # Calcul du début :
            debut = tache.debut.hour*60 + tache.debut.minute + 1
            # Calcul du nombre de lignes :
            # Si ça dépasse : on restreint
            if (tache.debut + tache.duree).hour > self.getHeureFin() or tache.debut.date() != (tache.debut + tache.duree).date():
                fin = datetime.time(self.getHeureFin() + 1) # Conversion en time
                duree = fin - tache.debut.time() # Conversion en duree
                duree = duree.total_seconds()//60%1440
                
            else: # Si ça dépasse pas :
                duree = tache.duree.total_seconds()//60%1440 # 1440 est le nombre de minutes dans un jour
                                                
            # Ajout graphique :
            t = TacheEnCalendrier(self, tache, bg = tache.color, bd = 1, relief = SOLID)
            t.grid(row = int(debut)-self.getHeureDebut()*60, rowspan = int(duree),
                   column = ((tache.debut.isoweekday()-1)%7)*2+1, sticky = "nesw")
            # TODO : Rajouter t à une liste.

            return tache # on revoie la tache avec son début et sa duree. TRÈS IMPORTANT.

    def identify_region(self, x, y):
        # On regarde si c'est trop à gauche (sur les heures):
        colonne, ligne = self.grid_location(x, y)
        colonne = (colonne-1)//2
        #print("Case : ", ligne, colonne)
        jour = self.getJourDebut() + colonne
        minute = self.getHeureDebut()*60 +(ligne - 1)
        heure, minute = minute//60, minute%60
        #print("Jour, heure, minute : ", jour, heure, minute)
        return datetime.datetime(2020, 4, # TODO : remplacer avce la future méthode getDebutPeriode() qui renvoie un datetime
            jour+6, heure, minute) # +6 à changer aussi (c'est parce que le premier lundi du mois d'avril 2020 est le 6.
        
    def __afficherLesHeures(self):
        # On efface ceux déjà présent :
        for label in self.listeLabelHeure: 
            label.destroy()
        self.listeLabelHeure = []

        # et on les recrées :
        for heure in range(self.getHeureDebut(), self.getHeureFin()+1): # le +1 pour compter Début ET Fin.
            self.listeLabelHeure.append(Label(self, text=heure, bd = 1, relief = SOLID))
            # Note : Un détail à la minute près va être fait,
            # donc on compte 60 lignes pour une heure.
            # La ligne 0 étant la ligne des labels des jours,
            # On compte à partir de 1, c'est-à-dire en ajotuant 1.
            self.listeLabelHeure[-1].grid(row=(heure-self.getHeureDebut())*60+1, # le *60 pour faire un détail à la minute près
                                          column=0,      # Les labels des heures sont réservés à la colonne de gauche.
                                          rowspan=60,    # Mais ils prennent 60 minutes et lignes.
                                          sticky="NSWE") # Permet de centrer le label et d'en reomplir les bords par la couleur du fond.
        # Cela permet de réadapter les lignes et colones qui sont en expand pour le grid.
        self.__adapteGrid()
    
    def __afficherLesJours(self):
        for indice, jour in enumerate(self.listeLabelJour): # on efface ceux déjà présent
            jour.destroy()
            self.columnconfigure(indice*2+1,weight=0)
            
        for indice, separator in enumerate(self.listeSeparateurJour): # on efface aussi les separator
            separator.destroy()
            self.columnconfigure(indice*2+2,weight=0)
        
        self.listeLabelJour = []
        self.listeSeparateurJour = []
        
        for jour in range(self.getJourDebut(), self.getJourDebut()+self.getNbJour()):
            self.listeLabelJour.append(Label(self, text=JOUR[jour%7]))
            self.listeLabelJour[-1].grid(row=0, column=1+(jour-self.getJourDebut())*2, sticky="NSWE")

            if jour != self.getJourDebut() + self.getNbJour() - 1:
                self.listeSeparateurJour.append(Separator(self, orient=VERTICAL))
                self.listeSeparateurJour[-1].grid(row=0, column=2+2*(jour-self.getJourDebut()), rowspan = 60*(self.getHeureFin()+1-self.getHeureDebut())+1, sticky="NS")
            
        self.__adapteGrid()

    def __adapteGrid(self):
        # à mettre À LA FIN ! ! ! (pour les expands)
        for column in range(self.nbJour*2+1):
            if column%2 ==0:
                self.columnconfigure(column,weight=0)
            else:
                self.columnconfigure(column, weight=1)
        self.rowconfigure(ALL,weight=1)
        self.rowconfigure(0, weight=0)


if __name__=='__main__':
    import Application
    Application.main()
