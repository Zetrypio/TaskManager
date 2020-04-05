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
        self.tailleColonne = 0
        
        self.tailleBandeauJour = 20
        
        self.mainCanvas = Canvas(self, width=1, height=1, scrollregion = (0, 0, 1, 1))
        self.mainCanvas.pack(fill=BOTH, expand=YES, side = LEFT)
        self.mainCanvas.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        self.scrollbar = Scrollbar(self, command = self.mainCanvas.yview) # Premier reliage de la scrollbar
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.mainCanvas.config(yscrollcommand = self.scrollbar.set) # 2e reliage de la scrollbar

    def getNbTacheJour(self, jourSemaine, arret = None):
        if arret is None:
            arret = len(self.__listeTache)
        nombre = 0
        for tache in self.__listeTache:
            if self.__listeTache.index(tache) == arret:
                return nombre
            
            if tache.task.debut.isoweekday() == jourSemaine:
                nombre+=1
        return nombre
    
    def getNbLigneTotal(self):
        nbLigne = 1
        for jour in range(1, 8):
            nbLigne = max(nbLigne, self.getNbTacheJour(jour))
        return nbLigne
    
    def getScrollableHeight(self):
        """Renvoie le plus grand entre la partie scrollable et la hauteur du Canvas"""
        return max(self.mainCanvas.winfo_height(), int(self.mainCanvas.cget("scrollregion").split(" ")[3]))
  
    def updateAffichage(self):
        if self.mainCanvas.winfo_width() != 0:
            self.__afficherLesJours()
            
        self.__afficherLesTaches()
        
        # On update la zone scrollable :
        w = self.mainCanvas.winfo_width()
        h = self.getNbLigneTotal() * self.TAILLE_LIGNE + self.tailleBandeauJour
        self.mainCanvas.config(scrollregion = (0, 0, w, h))


    def addTask(self, tache, region = None):
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        t = TacheEnGantt(self, tache, bg= tache.color) # on crée notre objet
        self.mainCanvas.create_window(self.tailleColonne*(t.task.debut.isoweekday()-1)+2, # X en fonction du jour de la tache
                                      self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(t.task.debut.isoweekday()) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                      , width=(self.tailleColonne-1)*0.8, height=self.TAILLE_LIGNE ,anchor=NW, window=t)
        
        self.__listeTache.append(t) # On rajoute la tache après dans la liste pour ne pas la tester au moment de l'affichage
        return tache

    def __afficherLesJours(self):
        self.mainCanvas.delete(ALL)
        
        for jour in range(self.getNbJour()): # Traçage des lignes de division et des noms de jour
            x = int(jour*self.mainCanvas.winfo_width()/self.getNbJour())
            
            self.mainCanvas.create_rectangle(x, 0, x+(self.mainCanvas.winfo_width()//self.getNbJour()), self.tailleBandeauJour, fill="#BBBBBB", outline="") # création de bandeau pour les jours
            
            if jour !=0:
                self.mainCanvas.create_line(x, 0, x, self.getScrollableHeight())
            
            self.mainCanvas.create_text(x+(self.mainCanvas.winfo_width()//self.getNbJour())//2, 2, text=JOUR[(jour+self.getJourDebut())%7], anchor=N)
            
        self.tailleColonne = int(self.mainCanvas.winfo_width()/self.getNbJour())

    def __afficherLesTaches(self):
        for tache in self.__listeTache:
            if tache.task.debut.isoweekday() >= self.getJourDebut() and tache.task.debut.isoweekday()-1 <= self.getJourDebut()+self.getNbJour():
                
                self.mainCanvas.create_window(self.tailleColonne*(tache.task.debut.isoweekday()-1)+2, # X en fonction du jour de la tache
                                              self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(tache.task.debut.isoweekday(), self.__listeTache.index(tache)) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                              , width=(self.tailleColonne-1)*0.8, height=self.TAILLE_LIGNE ,anchor=NW, window = tache)
    
if __name__=='__main__':
    import Application
    Application.main()
