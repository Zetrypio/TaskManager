# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from superclassCalendrier import *

class TacheEnGantt(SuperTache):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageGantt


class AffichageGantt(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        self.__listeTache = []
        
        self.TAILLE_LIGNE = 50
        
        self.mainCanvas = Canvas(self, width=0, height=0)
        self.mainCanvas.pack(fill=BOTH, expand=YES)
        self.mainCanvas.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
    
    def updateAffichage(self):
        if self.mainCanvas.winfo_width() != 0:
            self.__afficherLesJours()


    def addTask(self, tache, region = None):
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        t = TacheEnGantt(self, tache, bg= tache.color) # on crée notre objet
        self.__listeTache.append(t)
        self.mainCanvas.create_window(100,200, width=50, height=30,anchor=NW, window=t)
        
        return tache

    def __afficherLesJours(self):
        self.mainCanvas.delete(ALL)
        
        for jour in range(self.getNbJour()): # Traçage des lignes de division et des noms de jour
            x = int(jour*self.mainCanvas.winfo_width()/self.getNbJour())
            self.mainCanvas.create_rectangle(x, 0, x+(self.mainCanvas.winfo_width()//self.getNbJour()), 20, fill="#BBBBBB", outline="") # création de bandeau pour les jours
            
            if jour !=0:
                self.mainCanvas.create_line(x, 0, x, self.mainCanvas.winfo_height())
            
            self.mainCanvas.create_text(x+(self.mainCanvas.winfo_width()//self.getNbJour())//2, 2, text=JOUR[(jour+self.getJourDebut())%7], anchor=N)
    
if __name__=='__main__':
    import Application
    Application.main()
