# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror

from util.widgets.RMenu import *
from util.widgets.infobulle import *

from ..AbstractDisplayedTask import * 
from .LienDependance import *

class TacheEnGantt(AbstractDisplayedTask):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageGantt
        self.jeCherche = False
        
        #self.bind("<Button-1>", self.__clique)       # On bind la frame
        #self.texte.bind("<Button-1>", self.__clique) # On bind le Text qui remplie tout la Frame
        self.ID_PLUS = None

        # RMenu
        self.RMenu = RMenu(self, tearoff=0)
        self.RMenu.add_command(label="Ajouter un lien", command=self.addDependance)

        self.PlusCoord = None

    def getPosPixel(self):
        return self.master.can.bbox("num%s"%self.master.getIndiceTacheEnGantt(self))
    def getPosGrille(self):
        x1 = self.task.debut.weekday()
        x2 = self.task.getFin().weekday()
        y = self.master.getNbTacheJour(self.task.debut.date(), self.master.listeTaskAffichees.index(self))
        return x1, x2, y

    def affichePlusLien(self, tag):
        # Récupération des valeurs
        from .AffichageGantt import AffichageGantt
        tailleColonne = self.master.tailleColonne
        tailleLigne   = AffichageGantt.TAILLE_LIGNE
        facteur       = self.master.facteurW

        espaceLibre = (1-facteur)*tailleColonne
        facteurTaille = 0.5
        x1, y1, x2, y2 = self.getPosPixel()


        diametreCercle=min(facteurTaille*espaceLibre, facteurTaille*tailleLigne)

        if (diametreCercle)%2 == 0: # Pour avoir un truc impair et joli =)
             diametreCercle+=1

        tailleTrait = diametreCercle-4
        self.PlusCoord = centre = [x2+5 + diametreCercle*0.5, (y1+y2)/2]
        self.master.can.create_oval(centre[0]-diametreCercle/2, centre[1]-diametreCercle/2, centre[0]+diametreCercle/2,centre[1]+diametreCercle/2, fill="lightgray", tags=(tag, "topPlus"))
        self.master.can.create_line(centre[0]-tailleTrait/2,centre[1],centre[0]+tailleTrait/2+1, centre[1], tags=(tag, "topPlus")) # ligne horizontale
        self.master.can.create_line(centre[0],centre[1]-tailleTrait/2, centre[0],centre[1]+tailleTrait/2+1,  tags=(tag, "topPlus"))

        ajouterInfoBulleTagCanvas(self.master.can, tag, "Ajouter un lien")

    def addDependance(self): # Mise en mode recherche
        self.master.mode = "addDep"
        self.reinitialisationCherche()
        self.jeCherche = True
        self.__bindBouge = self.master.can.bind("<Motion>", self.afficherLesSemiDependances, add=True)
        self.master.updateAffichage()

    def __destDependance(self):
        self.master.mode = "delDep"
        self.reinitialisationCherche()
        self.jeCherche = True
        self.master.updateAffichage()

    def reinitialisationCherche(self):
        if self.master.getQuiCherche() is not None:
            self.master.getQuiCherche().jeCherche = False

    def chercheLien(self, tacheA, tacheB): # Fonction embarqué qui retourne le lien qui à tacheD = tache
        for lien in self.master.listeLien:
            if lien.tacheD == tacheA and lien.tacheF == tacheB:
                return lien
            elif lien.tacheD == tacheB and lien.tacheF == tacheA:
                return lien

    def _clique(self, event):
        if (chercheur := self.master.getQuiCherche()) != None: # Objet TacheEnGantt qui a la variable jeCherche = True
            chercheur.jeCherche = False

        if self.master.mode == "addDep": # On commence par savoir dans quelle mode on est
            self.master.mode = ""    # On réinitialise le mode
            if  chercheur.task.debut+chercheur.task.duree < self.task.debut: # Si le chercheur est avant
                try : # on essaye de voir si c'est pas déjà existant
                    self.master.listeLien.append(LienDependance(chercheur, self, self.master.can))
                except ValueError:pass
            elif chercheur.task.debut > self.task.debut+self.task.duree: # Si on est avant le chercheur
                try :
                    self.master.listeLien.append(LienDependance(self, chercheur, self.master.can))
                except ValueError:pass
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
            if (lienaime := self.chercheLien(chercheur, self)) == None: # Objet Lien qui lie les 2 taches
                self.master.updateAffichage()
                return
            self.master.mode = ""    # On réinitialise le mode
            if chercheur.task.debut < self.task.debut or chercheur.task.debut > self.task.debut: # Si le chercheur est avant ou après
                lienaime.suppression()
            elif chercheur.task == self.task:   # Si on est la même tache on annule l'opération
                self.jeCherche = False
                self.master.updateAffichage()
                return
            chercheur.jeCherche = False

        else:
            super()._clique(event)

        if chercheur is not None:
            chercheur.jeCherche = False
        self.master.updateAffichage()

    def gestionRMenu(self):
        trouve = False
        for lien in self.master.getLiens():
            if lien.tacheD is self or lien.tacheF is self:
                trouve = True
                break
        if not trouve:
            self.RMenu.delete("Retirer un lien")
        
        self.master.updateAffichage()

    def afficherLesSemiDependances(self, event):
        """Fonction qui ajuste la position du trait vert lorsqu'on clique sur le plus pour ajouter un lien"""
        if self.PlusCoord is not None:
            x1, y1 = self.PlusCoord
        else:
            y1=(self.getPosGrille()[-1]+0.5)*self.master.TAILLE_LIGNE+self.master.TAILLE_BANDEAU_JOUR
            # TODO : le x1 n'est pas détecté car soucis de datetime
             #Si on est après la période affiché
            if self.task.debut.date() > self.master.getJourFin() - datetime.timedelta(days=1):
                x1 = self.master.can.winfo_width()+10 # On se place en dehors du cote droit
             #Si on est avant le début
            elif self.task.debut.date() < self.master.getJourDebut():
                x1 = -10 # On se place en dehors du cote gauche
            # Si c'est juste le plus qui n'est plus affiché car il y a déjà un lien existant
            else :
                x1 = self.getPosPixel()[2] # Ici le getPosPixel est autorisé car la tache est affiché

        pos = self.master.getScrolledPosition(event)
        self.master.can.coords(self.maLigneDepEnCours, x1, y1, pos.x, pos.y)

    def creerLigne(self):
        """Fonction qui créer une ligne seulement si on est en tran de créer une ligne que l'on peut ensuite bouger à notre curseur"""
        if self.jeCherche and self.master.mode == "addDep":
            self.maLigneDepEnCours = self.master.can.create_line(-10,-10,-10,-10, fill="#00BB00", width=2, tags="topLine")

