# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from dialog import *
import datetime
import math
from superclassCalendrier import *
from RMenu import *
from task import *

class LienDependance: # Classe qui gère toutes les dépendances niveau visuel
    def __init__(self, tacheDebut, tacheFin, canvas):
        self.tacheD = tacheDebut # Où part   le lien | TacheEnGantt
        self.tacheF = tacheFin #   Où arrive le lien | TacheEnGantt
        
        for tache in self.tacheD.task.dependences: # Tester si la dépendance existe déjà, si c'est vrai on ne le fait pas
            if self.tacheF.task == tache:
                raise NotImplementedError
        self.chemin = [] # Chemin que va suivre le lien pour la gestion de l'affichage
        
        
        self.canvas = canvas
        
        self.tacheD.task.dependences.append(self.tacheF.task) # On créer la dépendance dans la tache
    
    def suppression(self):
        self.tacheD.task.dependences.remove(self.tacheF.task) # On retire la dépendance dans la tache
        self.tacheD.master.listeLien.remove(self)

    def afficherLesLiens(self, couleur = "#000000"):

        if (self.tacheF.task.debut+self.tacheF.task.duree).isoweekday() <= self.tacheD.master.getJourDebut()+1 or (self.tacheD.task.debut).isoweekday() > self.tacheD.master.getNbJour()+self.tacheD.master.getJourDebut():
            return
        def mymap(n, a, b, x, y): # Fonction map classique
            return (n-a)/(b-a)*(y-x)+x

        def posY(t, x1, y1, x2, y2):
            return mymap(math.cos(mymap(t, x1, x2, 0, math.pi)), 1, -1, y1, y2)

        self.pathCalculing() # On calcul le nouveau chemin

        if self.tacheD.jeCherche == True or self.tacheF.jeCherche == True: # Change la couleur si on séléctionne une tache pour une action
            couleur = "#0B98DE"

        # Paramètre généraux
        tailleLigne   = self.tacheD.master.TAILLE_LIGNE
        tailleColonne = self.tacheD.master.tailleColonne
        facteurW      = self.tacheD.master.facteurW

        temp = self.tacheD.getPosPixel()
        if temp != None:
            x1D, y1D, x2D, y2D = temp
        else:
            print(self.tacheD.getPosGrille())
            x1D = x2D = 0
            y1D = self.tacheD.getPosGrille()[2]*tailleLigne
            y2D = y1D+tailleLigne-4

        heightD = y2D-y1D
        

        temp = self.tacheF.getPosPixel()
        if temp != None:
            x1F, y1F, x2F, y2F = temp
        else:
            # y1F et 2 avec chemin
            if self.tacheF.task.debut.isoweekday() == self.canvas.master.getNbJour()+self.canvas.master.getJourDebut()+1:
                x1F = self.canvas.winfo_width()
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+13
                        y2F = y1F+tailleLigne-4+13
            else:
                x1F = self.canvas.winfo_width()+50 # + 50 Pour faire sortire la flèche du cadre
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+20
                        y2F = y1F-self.canvas.master.espacement

        heightF = y2F-y1F



        if x1F < x2D: # Si la tache et son lien sont le même jour
            rayon = tailleLigne/4
            #arc = self.canvas.create_arc(x2D-rayon, 13+y1D+heightD/2-rayon, x2D+rayon, 13+y1D+heightD/2+rayon, start=-90, extent=180, style='arc', width=2,  outline=couleur, tags="lien")
            self.canvas.create_line(x2D+1, y2D+3, x1D-10, y2D+3, width=2, fill=couleur, smooth=1, tags="lien")
            self.canvas.create_arc(x1D-rayon-10,y1D+tailleLigne-rayon+12, x1D+rayon-10,y1D+tailleLigne+rayon+12,  start=90, extent=90, style='arc', width=2, outline=couleur, tags="lien")

            self.canvas.create_line(x1D-rayon-10,y1D+tailleLigne+rayon-1, x1D-rayon-10, y1F+rayon , width=2, fill=couleur, smooth=1, tags="lien")

            self.canvas.create_arc(x1F-rayon-10, y1F+heightF/2-2*rayon, x1F+rayon-10, y1F+heightF/2, start=180, extent=90, style='arc', width=2, outline=couleur, tags="lien")
            self.canvas.create_line(x1F-10, y1F+heightF/2, x1F, y1F+heightF/2, width=2, fill=couleur, arrow=LAST, smooth=1, tags="lien")

        else:
            mesPoints = []
            def dessineLiaison(x1, y1, x2, y2):
                  for x in range(int(x1), int(x2)+1):
                    y = posY(x, x1, y1, x2, y2)
                    mesPoints.append([x, y])

            dessineLiaison(x2D, y1D+heightD/2, x2D+tailleColonne*(1-facteurW),max(tailleLigne*self.chemin[(self.tacheD.task.debut+self.tacheD.task.duree).isoweekday()]+20 - self.canvas.master.espacement/2, 20))

            if self.tacheD.master.getNbJour()+self.tacheD.master.getJourDebut() >= self.tacheF.task.debut.isoweekday()-1:
                dessineLiaison(x1F-tailleColonne*(1-facteurW),max(tailleLigne*self.chemin[(self.tacheD.task.debut+self.tacheD.task.duree).isoweekday()]+20 - self.canvas.master.espacement/2, 20), x1F-10, max(y1F+heightF/2, 20))

            mesPoints.append([x1F, max(y1F+heightF/2, 20)])

            self.canvas.create_line(*mesPoints, width=2, arrow=LAST, fill=couleur, smooth=1, tags="lien")

            self.canvas.tag_bind("lien", "<Button-1>",self.__clique)





    def pathCalculing(self):
        " Fonction qui permet de calculer le chemin que va prendre le lien pour lier les 2 taches "
        self.chemin = [] # On réinitialise le parcours

        _, posXD, posYD = self.tacheD.getPosGrille()
        _, posXF, posYF = self.tacheF.getPosGrille()

        croissance = posYF-posYD # savoir si on descend ou si on monte (c'est à l'envers les axes

        for jour in range(self.canvas.master.getLongueurPeriode()): # et on recalcule
            if posXD == jour and posXF == jour: # Si la tacheD est le même jour que TacheF
                self.chemin.append(1+posYD)
            elif posXD < jour and posXF > jour:
                self.chemin.append(posYD+croissance)
            else:
                self.chemin.append(-1)

    def __clique(self, event):

        if (chercheur := self.tacheD.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
            self.tacheD.master.updateAffichage()
            return
        chercheur.jeCherche = False

        if self.tacheD.master.mode =="delDep":
            self.tacheD.master.mode = ""
            if len(self.tacheD.task.dependences) == 1: # S'il n'y a qu'une seule dépendance on peut retirer le choix
                self.tacheD.RMenu.delete("Retirer un lien")

            # TODO : a refactor, comme la version dans tache en Gantt
            nbDep = 0
            for lien in self.tacheD.master.listeLien:
                if lien.tacheF == self.tacheF or lien.tacheD == self.tacheF:
                    nbDep +=1
            if nbDep == 1: # S'il n'y a qu'une seule dépendanec lié à tache F
                self.tacheF.RMenu.delete("Retirer un lien")

            self.suppression()



class TacheEnGantt(SuperTache):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageGantt
        self.jeCherche = False
        
        self.bind("<Button-1>", self.__clique)       # On bind la frame
        self.texte.bind("<Button-1>", self.__clique) # On bind le Text qui remplie tout la Frame
        # RMenu
        self.RMenu = RMenu(self, tearoff=0)
        self.RMenu.add_command(label="Ajouter un lien", command=self.addDependance)


    def getPosPixel(self):
        return self.master.mainCanvas.bbox("num%s"%self.master.getIndiceTacheEnGantt(self))
    def getPosGrille(self):
        x1 = self.task.debut.isoweekday()-1
        x2 = (self.task.duree + self.task.debut).isoweekday()-1
        y = self.master.getNbTacheJour(self.task.debut.isoweekday(), self.master.listeTache.index(self))
        return x1, x2, y

    def affichePlusLien(self, tag):
        # Récupération des valeurs
        tailleColonne = self.master.tailleColonne
        tailleLigne   = self.master.TAILLE_LIGNE
        facteur       = self.master.facteurW

        espaceLibre = (1-facteur)*tailleColonne
        facteurTaille = 0.5
        x1, y1, x2, y2 = self.getPosPixel()


        diametreCercle=min(facteurTaille*espaceLibre, facteurTaille*tailleLigne)

        if (diametreCercle)%2 == 0: # Pour avoir un truc impair et joli
             diametreCercle+=1

        tailleTrait = diametreCercle-4
        centre = [x2+5 + diametreCercle*0.5, (y1+y2)/2]
        self.master.mainCanvas.create_oval(centre[0]-diametreCercle/2, centre[1]-diametreCercle/2, centre[0]+diametreCercle/2,centre[1]+diametreCercle/2, fill="lightgray", tags=tag)
        self.master.mainCanvas.create_line(centre[0]-tailleTrait/2,centre[1],centre[0]+tailleTrait/2+1, centre[1], tags=tag) # ligne horizontale
        self.master.mainCanvas.create_line(centre[0],centre[1]-tailleTrait/2, centre[0],centre[1]+tailleTrait/2+1,  tags=tag)

    def addDependance(self): # Mise en mode recherche
        self.master.mode = "addDep"
        self.jeCherche = True
        self.master.mainCanvas.bind("<Motion>", self.afficherLesSemiDependances)
        self.master.updateAffichage()


    def __destDependance(self):
        self.master.mode = "delDep"
        self.jeCherche = True
        self.master.updateAffichage()
        

    def __clique(self, event):

        def chercheLien(tacheA, tacheB): # Fonction embarqué qui retourne le lien qui à tacheD = tache
            for lien in self.master.listeLien:
                if lien.tacheD == tacheA and lien.tacheF == tacheB:
                    return lien
                elif lien.tacheD == tacheB and lien.tacheF == tacheA:
                    return lien
    
        if (chercheur := self.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
            self.master.updateAffichage()
            return
        chercheur.jeCherche = False
        
        if self.master.mode == "addDep": # On commence par savoir dans quelle mode on est
            self.master.mode = ""    # On réinitialise le mode        
            self.master.mainCanvas.unbind("<Motion>")
            if  chercheur.task.debut+chercheur.task.duree < self.task.debut: # Si le chercheur est avant
                try : # on essaye de voir si c'est pas déjà existant
                    self.master.listeLien.append(LienDependance(chercheur, self, self.master.mainCanvas))
                except:pass
            elif chercheur.task.debut > self.task.debut+self.task.duree: # Si on est avant le chercheur
                try :
                    self.master.listeLien.append(LienDependance(self, chercheur, self.master.mainCanvas))
                except :pass
            elif chercheur.task == self.task:            # Si on est la même tache on annule l'opération
                self.jeCherche = False
                self.master.updateAffichage()
                return
            else:                                        # Si on est 2 taches commençant au même moment
                showerror("Tache incorrecte", "Vous ne pouvez pas choisir 2 taches commençant au même moment.")
            
            try :
                self.RMenu.index("Retirer un lien")
            except :
                self.RMenu.add_command(label = "Retirer un lien", command=self.__destDependance) # On bind la nouvelle possibilité
            
            try :
                chercheur.RMenu.index("Retirer un lien")
            except :               
                chercheur.RMenu.add_command(label = "Retirer un lien", command=chercheur.__destDependance)
            
            chercheur.jeCherche = False 
    

        elif self.master.mode == "delDep":
            if (lienaime := chercheLien(chercheur, self)) == None: # Objet Lien qui lie les 2 taches
                self.master.updateAffichage()
                return            
            self.master.mode = ""    # On réinitialise le mode
            if   chercheur.task.debut < self.task.debut or chercheur.task.debut > self.task.debut: # Si le chercheur est avant ou après
                lienaime.suppression()
            elif chercheur.task == self.task:            # Si on est la même tache on annule l'opération
                self.jeCherche = False
                self.master.updateAffichage()
                return
            chercheur.jeCherche = False 

            self.gestionRMenu(self, chercheur) #savvoir si on supprime l'option retirer lien
        chercheur.jeCherche = False
        self.master.updateAffichage()
            

    def gestionRMenu(self, tacheA, tacheB):
        # On supprime le choix seulement si il n'y en a pas d'autre lien avec eux
        # TODO : A Refactor
        trouve = False
        for lien in self.master.listeLien:
            if lien.tacheD == tacheA or lien.tacheF == tacheA:
                trouve = True
        if trouve == False:
            tacheA.RMenu.delete("Retirer un lien")
        trouve = False
        for lien in self.master.listeLien:
            if lien.tacheD == tacheB or lien.tacheF == tacheB:
                trouve = True
        if trouve == False:
            tacheB.RMenu.delete("Retirer un lien")
        
        self.master.updateAffichage()

    def afficherLesSemiDependances(self, event):
        x1, y1, x2, y2 = self.getPosPixel()
        self.master.mainCanvas.coords(self.maLigneDepEnCours, x2, (y1+y2)/2, event.x, event.y)

    def creerLigne(self):
        " Fonction qui créer une ligne seulement si on est en tran de créer une ligne que l'on peut ensuite bouger à notre curseur "
        if self.jeCherche == True:
            self.maLigneDepEnCours = self.master.mainCanvas.create_line(-10,-10,-10,-10, fill="lime", width=2)




class AffichageGantt(SuperCalendrier):
    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        self.listeTache = []
        self.listeLien    = []
        
        self.espacement = 4 # Entre 2 tache pour laisser passer les liens
        self.TAILLE_LIGNE = 50+self.espacement
        self.tailleColonne = 0
        
        self.tailleBandeauJour = 20
        
        self.facteurW = 0.8 # facteur de taille que prend une tache
        
        self.mainCanvas = Canvas(self, width=0, height=0)
        self.mainCanvas.pack(fill=BOTH, expand=YES)
        self.mainCanvas.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre



        
        self.mode = ""        

    def getQuiCherche(self): # retourne la tache qui est en train de chercher une dépandance
        for tache in self.listeTache:
            if tache.jeCherche == True:
                return tache

    def getNbTacheJour(self, jourSemaine, arret):
        nombre = 0
        for tache in self.listeTache:
            if self.listeTache.index(tache) == arret:
                return nombre
            
            if tache.task.debut.isoweekday() == jourSemaine:
                nombre+=1
        return nombre
  
    def getTacheEnGantt(self, tacheT):
        for tacheC in self.listeTache:
            if tacheC.task == tacheT:
                return tacheC
    
    def getIndiceTacheEnGantt(self, tache):
        return self.listeTache.index(tache)
    

    def updateAffichage(self):
        if self.mainCanvas.winfo_width() != 0:
            self.mainCanvas.delete(ALL)


            self.__afficherLesJours()
            self.__afficherLesTaches()
            self.__afficherLesDependances()

    def addTask(self, tache, region = None):
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        # NOTE : il faut aussi changer ici pour avoir unu affichage plusierus jours.
        t = TacheEnGantt(self, tache, bg= tache.color) # on crée notre objet
        self.mainCanvas.create_window(int(self.tailleColonne*(t.task.debut.isoweekday()-1)+2), # X en fonction du jour de la tache
                                      self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(t.task.debut.isoweekday(), len(self.listeTache)) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                      , width=int(self.tailleColonne-1)*self.facteurW, height=self.TAILLE_LIGNE ,anchor=NW, window=t,
                                      tags="num%s"%len(self.listeTache)
                                      )
        
        
        
        self.listeTache.append(t) # On rajoute la tache après dans la liste pour ne pas la tester au moment de l'affichage
        return tache

    def __afficherLesJours(self):    
        for jour in range(self.getNbJour()): # Traçage des lignes de division et des noms de jour
            x = int(jour*self.mainCanvas.winfo_width()/self.getNbJour())
            self.mainCanvas.create_rectangle(x, 0, x+(self.mainCanvas.winfo_width()//self.getNbJour()), self.tailleBandeauJour, fill="#BBBBBB", outline="") # création de bandeau pour les jours
            
            if jour !=0:
                self.mainCanvas.create_line(x, 0, x, self.mainCanvas.winfo_height())
            
            self.mainCanvas.create_text(x+(self.mainCanvas.winfo_width()//self.getNbJour())//2, 2, text=JOUR[(jour+self.getJourDebut())%7], anchor=N)
            
        self.tailleColonne = (self.mainCanvas.winfo_width()/self.getNbJour())

    def __afficherLesTaches(self):

        self.listeTache.sort(key=lambda t:t.task.debut) #trie par début des taches
        ID_TACHE = 0
        self.mainCanvas.unbind("<Button-1>")

        for tache in self.listeTache:
            if tache.task.debut.isoweekday() >= self.getJourDebut() and tache.task.debut.isoweekday()-1 <= self.getJourDebut()+self.getNbJour():
                tache.creerLigne()
                # NOTE : ici, il faudra adapter pour gérer une tache sur plusieurs jours.
                # width = int(self.tailleColonne-1)*tache.task.duree.days-1 + int(self.tailleColonne-1)*self.facteurW
                self.mainCanvas.create_window(int(self.tailleColonne*(tache.task.debut.isoweekday()-1)+2), # X en fonction du jour de la tache
                                              (self.tailleBandeauJour+self.TAILLE_LIGNE*self.getNbTacheJour(tache.task.debut.isoweekday(), self.listeTache.index(tache))) # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le meme jour
                                              , width=int(self.tailleColonne-1)*self.facteurW, height=self.TAILLE_LIGNE-self.espacement ,anchor=NW, window = tache, tags="num%s"%self.listeTache.index(tache)) # Le 0.975 et 1.025 c'est un espacement pour laisser les liens entre les lignes

                if tache.task.dependences == []:
                    tache.affichePlusLien("a"+str(ID_TACHE))

                    self.mainCanvas.tag_bind("a"+str(ID_TACHE), "<Button-1>", lambda e, t=tache: t.addDependance())

                    ID_TACHE += 1

    def __afficherLesDependances(self):
        for lien in self.listeLien:
            lien.afficherLesLiens()

            

if __name__=='__main__':
    import Application
    Application.main()
