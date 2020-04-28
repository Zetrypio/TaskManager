# -*- coding:UTF-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from superclassCalendrier import *

class TacheEnCalendrier(SuperTache):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageCalendier
    

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
        self.listeLabelHeure = []       # \
        self.listeLabelJour = []        #  )-> Tout est dans le nom de ces trois listes.
        self.listeSeparateurJour = []   # /
#        self.__listeTache = []
        self.frame = Frame(self)
        self.frame.pack(expand = YES, fill = BOTH)
        
        self.updateAffichage()

        # self.bind("<Configure>", lambda e : self.updateAffichage())

    def updateAffichage(self): # override
        # On détruit et recrée le Frame
        self.frame.destroy()
        self.frame = Frame(self)
        self.frame.pack(expand = YES, fill = BOTH)
        
        # On affiche les trucs
        self.__afficherLesHeures()
        self.__afficherLesJours()
        self.__afficherLesTaches()
    
    def addTask(self, tache, region = None):
        '''Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas.'''
        # ":=  on attribut la variable en plus de tester la condition
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return

#        # Calcul du début :
#        debut = tache.debut.hour*60 + tache.debut.minute + 1
#        # Calcul du nombre de lignes :
#        # Si ça dépasse : on restreint (TODO : à améliorer)
#        if (tache.debut + tache.duree).time() > self.getHeureFin() or tache.debut.date() != (tache.debut + tache.duree).date():
#            fin = self.getHeureFin() # Conversion en time
#            duree = datetime.timedelta(fin.hour) - datetime.timedelta(tache.debut.time().hour) # Conversion en duree
#            duree = duree.total_seconds()//60%1440
#            tache.visible = False
#            
#        else: # Si ça dépasse pas :
#            duree = tache.duree.total_seconds()//60%1440 # 1440 est le nombre de minutes dans un jour
                                            
        # Ajout graphique :
        
        
#        t = TacheEnCalendrier(self, tache, bg = tache.color, bd = 1, relief = SOLID)
#       t.grid(row = int(debut)-self.getHeureDebut().hour*60, rowspan = int(duree),
#              column = ((tache.debut.isoweekday()-1)%7)*2+1, sticky = "nesw")
#       t.grid_propagate(0)
        
#        self.__listeTache.append(t)
        self.updateAffichage()

        return tache # on revoie la tache avec son début et sa duree. TRÈS IMPORTANT.

    def identify_region(self, x, y):
        # On regarde si c'est trop à gauche (sur les heures):
        colonne, ligne = self.frame.grid_location(x, y)
        colonne = (colonne-1)//2
        #print("Case : ", ligne, colonne)
        jour = self.getJourDebut() + datetime.timedelta(days = colonne)
        jour = datetime.datetime(jour.year, jour.month, jour.day)
        minute = self.getHeureDebut().hour*60 +(ligne - 1)
        heure, minute = minute//60, minute%60
        #print("Jour, heure, minute : ", jour, heure, minute)
        # TODO : A Changer :
        return jour + datetime.timedelta(hours = heure, minutes = minute)
        
    def __afficherLesHeures(self):
        # On efface ceux déjà présent :
        self.listeLabelHeure = []

        # et on les recrées :
        for heure in range(self.getHeureDebut().hour, self.getHeureFin().hour+1): # le +1 pour compter Début ET Fin.
            self.listeLabelHeure.append(Label(self.frame, text=heure, bd = 1, relief = SOLID))
            # Note : Un détail à la minute près va être fait,
            # donc on compte 60 lignes pour une heure.
            # La ligne 0 étant la ligne des labels des jours,
            # On compte à partir de 1, c'est-à-dire en ajotuant 1.
            self.listeLabelHeure[-1].grid(row=(heure-self.getHeureDebut().hour)*60+1, # le *60 pour faire un détail à la minute près
                                          column=0,      # Les labels des heures sont réservés à la colonne de gauche.
                                          rowspan=60,    # Mais ils prennent 60 minutes et lignes.
                                          sticky="NSWE") # Permet de centrer le label et d'en reomplir les bords par la couleur du fond.
        # Cela permet de réadapter les lignes et colones qui sont en expand pour le grid.
        self.__adapteGrid()
    
    def __afficherLesJours(self):
        self.listeLabelJour = []
        self.listeSeparateurJour = []
        
        for jour in self.rangeDate(self.getJourDebut(), self.getJourFin(), last = False):
            self.listeLabelJour.append(Label(self.frame, text=JOUR[jour.weekday()], bg = "light grey"))
            self.listeLabelJour[-1].grid(row=0, column=1+((jour-self.getJourDebut()).days)*2, sticky="NSWE")
            if jour < self.getJourFin():
                self.listeSeparateurJour.append(Separator(self.frame, orient=VERTICAL))
                self.listeSeparateurJour[-1].grid(row=0, column=2+2*(jour-self.getJourDebut()).days, rowspan = 60*(self.getHeureFin().hour+1-self.getHeureDebut().hour)+1, sticky="NS")
            
        self.__adapteGrid()

    def __afficherLesTaches(self):

        for task in self.listeTaches:
            tache = TacheEnCalendrier(self.frame, task)
            if tache.task.debut.date() >= self.getJourDebut() and tache.task.debut.date() <= self.getJourFin():
                # Calcul du début :
                debut = tache.task.debut.hour*60 + tache.task.debut.minute + 1
                ## Calcul du nombre de lignes :
                # Si c'est hors cadre ou pas sur le même jour
                print(self.getHeureFin())
                if tache.task.getFin().time() <= self.getHeureDebut() or tache.task.getDebut().time() > self.getHeureFin() or tache.task.debut.date() != tache.task.getFin().date():
                    tache.task.setVisible(False)
                # Si ça dépasse : on restreint
                elif tache.task.getFin().time() > self.getHeureFin() and tache.task.getDebut().time() < self.getHeureFin():
                    enleve = datetime.datetime.combine(tache.task.getFin().date(), self.getHeureFin()) - tache.task.getFin()
                    duree = tache.task.getDuree() - enleve
                    duree = duree.total_seconds()//60%1440
                    tache.task.setVisible(True)
                # Si c'est seulement le début qui manque on adapte
                elif tache.task.debut.time() < self.getHeureDebut() and tache.task.getFin().time() > self.getHeureDebut():
                    debut = self.getHeureDebut().hour*60 + 1

                    enleve = datetime.datetime.combine(tache.task.getDebut().date(), self.getHeureDebut()) - tache.task.getDebut()
                    duree = tache.task.getDuree() - enleve
                    duree = duree.total_seconds()//60%1440
                    tache.task.setVisible(True)
                else: # Si ça dépasse pas :
                    duree = tache.task.duree.total_seconds()//60%1440 # 1440 est le nombre de minutes dans un jour
                    tache.task.setVisible(True)

                if tache.task.getVisible():
                    tache.grid(row = int(debut)-self.getHeureDebut().hour*60, rowspan = int(duree),
                           column = (tache.task.debut.date()-self.getJourDebut()).days*2+1, sticky = "nesw")

    def __adapteGrid(self):
        # à mettre À LA FIN ! ! ! (pour les expands)
        for column in range(self.nbJour*2+1):
            if column%2 ==0:
                self.frame.columnconfigure(column,weight=0)
            else:
                self.frame.columnconfigure(column, weight=1)
        self.frame.rowconfigure(ALL,weight=1)
        self.frame.rowconfigure(0, weight=0)


if __name__=='__main__':
    import Application
    Application.main()
