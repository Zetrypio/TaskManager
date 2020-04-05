# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from dialog import *
import datetime
from superclassCalendrier import *
from RMenu import *
from task import *

class LienDependance: # Classe qui gère toutes les dépendances niveau visuel
    def __init__(self, tacheDebut, tacheFin, canvas):
        
        self.chemin = [] # Chemi que va suivre le lien pour la gestion de l'affichage
        
        self.tacheD = tacheDebut # Où part   le lien | TacheEnGantt
        self.tacheF = tacheFin #   Où arrive le lien | TacheEnGantt
        
        self.canvas = canvas
        
        self.tacheD.task.dependences.append(self.tacheF.task) # On créer la dépendance dans la tache
        
    #def afficherLesLiens(self, couleur = None):
        #print("bbox", self.canvas.bbox("num%s"%self.canvas.master.getIndiceTacheEnGantt(self.tacheD)))
        #print("coords", self.canvas.coords("num%s"%self.canvas.master.getIndiceTacheEnGantt(self.tacheD)))
        
        #print(self.canvas.bbox(self.canvas.find_all()[5]))
        
        #self.canvas.create_line(1, 1, 100, 100, fill = couleur)        
    

class TacheEnGantt(SuperTache):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageGantt
        
        self.bind("<Button-1>", self.__clique)       # On bind la frame
        self.texte.bind("<Button-1>", self.__clique) # On bind le Text qui remplie tout la Frame
        # RMenu
        self.RMenu = RMenu(self, tearoff=0)
        self.RMenu.add_command(label="Ajouter un lien", command=self.__addDependance)
        
        self.jeCherche = False


    def __addDependance(self): # Mise en mode recherche
        self.master.mode = "addDep"
        self.jeCherche = True 
    
    def __destDependance(self):
        self.master.mode = "delDep"
        self.jeCherche = True
        

    def __clique(self, event):
        if (chercheur := self.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
            return
        
        if self.master.mode == "addDep": # On commence par savoir dans quelle mode on est
            self.master.mode = ""    # On réinitialise le mode
            
            if   chercheur.task.debut < self.task.debut: # Si le chercheur est avant
                self.master.listeLien.append(LienDependance(chercheur, self, self.master.mainCanvas))
            elif chercheur.task.debut > self.task.debut: # Si on est avant le chercheur
                self.master.listeLien.append(LienDependance(self, chercheur, self.master.mainCanvas))
            elif chercheur.task == self.task:            # Si on est la même tache on annule l'opération
                self.jeCherche = False
                return
            else:                                        # Si on est 2 taches commençant au même moment
                showerror("Tache incorrecte", "Vous ne pouvez pas choisir 2 taches commençant au même moment.")
            
            if self.RMenu.index('end') == 0: # Si c'est son premier lien
                self.RMenu.add_command(label = "Retirer un lien", command=self.__destDependance) # On bind la nouvelle possibilité
            if chercheur.RMenu.index('end') ==0:
                chercheur.RMenu.add_command(label = "Retirer un lien", command=self.__destDependance)
    
        
        self.master.updateAffichage()
        chercheur.jeCherche = False
        self.master.mode = ""    # On réinitialise le mode


class AffichageGantt(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        self.__listeTache = []
        self.listeLien    = []
        
        self.TAILLE_LIGNE = 50
        self.tailleColonne = 0
        
        self.tailleBandeauJour = 20
        
        self.mainCanvas = Canvas(self, width=0, height=0)
        self.mainCanvas.pack(fill=BOTH, expand=YES)
        self.mainCanvas.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        
        self.mode = ""        

    def getQuiCherche(self): # retourne la tache qui est en train de chercher une dépandance
        for tache in self.__listeTache:
            if tache.jeCherche == True:
                return tache

    def getNbTacheJour(self, jourSemaine, arret):
        nombre = 0
        for tache in self.__listeTache:
            if self.__listeTache.index(tache) == arret:
                return nombre
            
            if tache.task.debut.isoweekday() == jourSemaine:
                nombre+=1
        return nombre
  
    def getTacheEnGantt(self, tacheT):
        for tacheC in self.__listeTache:
            if tacheC.task == tacheT:
                return tacheC
    
    def getIndiceTacheEnGantt(self, tache):
        return self.__listeTache.index(tache)
    

    def updateAffichage(self):
        if self.mainCanvas.winfo_width() != 0:
            self.__afficherLesJours()
            
        self.__afficherLesTaches()
        self.__afficherLesDependances()


    def addTask(self, tache, region = None):
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        t = TacheEnGantt(self, tache, bg= tache.color) # on crée notre objet
        self.mainCanvas.create_window(self.tailleColonne*(t.task.debut.isoweekday()-1)+2, # X en fonction du jour de la tache
                                      self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(t.task.debut.isoweekday(), len(self.__listeTache)) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                      , width=(self.tailleColonne-1)*0.8, height=self.TAILLE_LIGNE ,anchor=NW, window=t,
                                      tags="num%s"%len(self.__listeTache))
        
        self.__listeTache.append(t) # On rajoute la tache après dans la liste pour ne pas la tester au moment de l'affichage
        return tache

    def __afficherLesJours(self):
        self.mainCanvas.delete(ALL)
        
        for jour in range(self.getNbJour()): # Traçage des lignes de division et des noms de jour
            x = int(jour*self.mainCanvas.winfo_width()/self.getNbJour())
            
            self.mainCanvas.create_rectangle(x, 0, x+(self.mainCanvas.winfo_width()//self.getNbJour()), self.tailleBandeauJour, fill="#BBBBBB", outline="") # création de bandeau pour les jours
            
            if jour !=0:
                self.mainCanvas.create_line(x, 0, x, self.mainCanvas.winfo_height())
            
            self.mainCanvas.create_text(x+(self.mainCanvas.winfo_width()//self.getNbJour())//2, 2, text=JOUR[(jour+self.getJourDebut())%7], anchor=N)
            
        self.tailleColonne = int(self.mainCanvas.winfo_width()/self.getNbJour())

    def __afficherLesTaches(self):
        for tache in self.__listeTache:
            if tache.task.debut.isoweekday() >= self.getJourDebut() and tache.task.debut.isoweekday()-1 <= self.getJourDebut()+self.getNbJour():
                
                self.mainCanvas.create_window(self.tailleColonne*(tache.task.debut.isoweekday()-1)+2, # X en fonction du jour de la tache
                                              self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(tache.task.debut.isoweekday(), self.__listeTache.index(tache)) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                              , width=(self.tailleColonne-1)*0.8, height=self.TAILLE_LIGNE ,anchor=NW, window = tache)

    def __afficherLesDependances(self):pass
        #for lien in self.listeLien:
            #lien.afficherLesLiens()
            
 
if __name__=='__main__':
    import Application
    Application.main()
