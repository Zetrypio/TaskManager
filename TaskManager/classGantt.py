# -*- coding:utf-8 -*-
from tkinter import *
from infobulle import *
from tkinter.ttk import *
from tkinter import Label, Frame
from dialog import *
import datetime
from superclassCalendrier import *
from RMenu import *
from task import *
from util import *


class LienDependance: # Classe qui gère toutes les dépendances niveau visuel
    def __init__(self, tacheDebut, tacheFin, canvas):
        self.tacheD = tacheDebut # Où part   le lien | TacheEnGantt
        self.tacheF = tacheFin #   Où arrive le lien | TacheEnGantt
        
        for tache in self.tacheD.task.dependences: # Tester si la dépendance existe déjà, si c'est vrai on ne le fait pas
            if self.tacheF.task == tache:
                raise ValueError("Lien déjà existant.")

        self.chemin = [] # Chemin que va suivre le lien pour la gestion de l'affichage
        
        self.ID_LIEN = None

        self.canvas = canvas
        self.select = False # variable qui sait si on est selectionne ou pas
        
        self.tacheD.task.dependantes.append(self.tacheF.task)
        self.tacheF.task.dependences.append(self.tacheD.task) # On créer la dépendance dans la tache
    
    def suppression(self):
        self.tacheD.gestionRMenu()
        self.tacheF.gestionRMenu() # Savvoir si on supprime l'option retirer lien A mettre avant suppresssion car on prends en compte le lien actuel
        self.tacheD.task.dependantes.remove(self.tacheF.task)
        self.tacheF.task.dependences.remove(self.tacheD.task) # On retire la dépendance dans la tache
        self.tacheD.master.listeLien.remove(self)
        self.tacheD.master.updateAffichage()

    def afficherLesLiens(self, couleur = "#000000"):
        # On retire 1 jour à la fin pour que le calcul soit correct
        if self.tacheF.task.getFin().date() <= self.tacheD.master.getJourDebut() \
        or (self.tacheD.task.debut.date() > self.tacheD.master.getJourFin()-datetime.timedelta(days=1) \
        and self.tacheD.task.debut.date() != self.tacheF.task.debut.date()):
            return
        

        self.pathCalculing() # On calcul le nouveau chemin

        # Gestion des couleurs
        w = 2
        if self.tacheD.jeCherche == True or self.tacheF.jeCherche == True: # Change la couleur si on séléctionne une tache pour une action
            couleur = "#FFAF00"
            if self.tacheD.master.mode == "delDep":
                couleur = "#FF3F3F"
            w = 3
        elif self.select == True:
            couleur = "#0078FF"
            w = 3

        # Paramètre généraux
        tailleLigne   = AffichageGantt.TAILLE_LIGNE
        tailleColonne = self.tacheD.master.tailleColonne
        facteurW      = self.tacheD.master.facteurW

        temp = self.tacheD.getPosPixel()
        if temp != None:
            x1D, y1D, x2D, y2D = temp
        else:
            x1D = x2D = 0
            y1D = self.tacheD.getPosGrille()[2]*tailleLigne
            y2D = y1D+tailleLigne-4

        heightD = y2D-y1D
        

        temp = self.tacheF.getPosPixel()
        if temp != None:
            x1F, y1F, x2F, y2F = temp
        else:
            # y1F et 2 avec chemin
            if self.tacheF.task.debut.date() == self.canvas.master.getJourFin():
                x1F = self.canvas.winfo_width()
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+13
                        y2F = y1F+tailleLigne-4+13
            else:
                x1F = self.canvas.winfo_width()+50 # + 50 Pour faire sortir la flèche du cadre
                for val in self.chemin:
                    if val != -1:
                        y1F = val*tailleLigne+20
                        y2F = y1F-AffichageGantt.ESPACEMENT

        heightF = y2F-y1F

        self.ID_LIEN = tag = "lienum"+str(self.tacheD.master.listeLien.index(self))
        
        if w == 3:
            tag = (tag, "top")

        if x1F < x2D: # Si la tache et son lien sont le même jour
            rayon = tailleLigne/4
            self.canvas.create_arc(x2D-rayon, 13+y1D+heightD/2-rayon, x2D+rayon, 13+y1D+heightD/2+rayon, start=-90, extent=180, style='arc', width=w,  outline=couleur, tags=tag)
            self.canvas.create_line(x2D+1, y2D+3, x1D-10, y2D+3, width=w, fill=couleur, smooth=1, tags=tag)
            self.canvas.create_arc(x1D-rayon-10,y1D+tailleLigne-rayon+12, x1D+rayon-10,y1D+tailleLigne+rayon+12,  start=90, extent=90, style='arc', width=w, outline=couleur, tags=tag)

            self.canvas.create_line(x1D-rayon-10,y1D+tailleLigne+rayon-1, x1D-rayon-10, y1F+rayon , width=w, fill=couleur, smooth=1, tags=tag)

            self.canvas.create_arc(x1F-rayon-10, y1F+heightF/2-2*rayon, x1F+rayon-10, y1F+heightF/2, start=180, extent=90, style='arc', width=w, outline=couleur, tags=tag)
            self.canvas.create_line(x1F-10, y1F+heightF/2, x1F, y1F+heightF/2, width=w, fill=couleur, arrow=LAST, smooth=1, tags=tag)

        else:
            mesPoints = []
            def dessineLiaison(x1, y1, x2, y2):
                  for x in range(int(x1), int(x2)+1):
                    y = posY(x, x1, y1, x2, y2)
                    mesPoints.append([x, y])


            dessineLiaison(x2D,
                           y1D+heightD/2,
                           x2D+tailleColonne*(1-facteurW),
                           max(tailleLigne*self.chemin[(self.tacheD.task.getFin()).isoweekday()]+AffichageGantt.TAILLE_BANDEAU_JOUR - AffichageGantt.ESPACEMENT/2, AffichageGantt.TAILLE_BANDEAU_JOUR))

            if self.tacheD.master.getJourFin() >= self.tacheF.task.debut.date():
                dessineLiaison(x1F-tailleColonne*(1-facteurW),
                               max(tailleLigne*self.chemin[(self.tacheD.task.getFin()).isoweekday()]+AffichageGantt.TAILLE_BANDEAU_JOUR - AffichageGantt.ESPACEMENT/2, AffichageGantt.TAILLE_BANDEAU_JOUR),
                               x1F-10,
                               max(y1F+heightF/2, 20))

            mesPoints.append([x1F, max(y1F+heightF/2, 20)])

            self.canvas.create_line(*mesPoints, width=w, arrow=LAST, fill=couleur, smooth=1, tags=tag)

        # On ajoute une infobulle :
        ajouterInfoBulleTagCanvas(self.canvas, tag, self.tacheD.task.nom+"→"+self.tacheF.task.nom)
#        self.canvas.tag_bind(tag, "<Button-1>",self.__clique, add='+')

#        self.canvas.tag_bind(tag,"<Control-Button-1>", self.changeSelect, add='+')

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

    def cliqueSuppr(self):
        if self.tacheD.master.mode == "delDep":
            if (chercheur := self.tacheD.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
                self.tacheD.master.updateAffichage()
                return
            chercheur.jeCherche = False
            self.suppression()


    def changeSelect(self):
        self.select = not self.select
        self.tacheD.master.updateAffichage()



class TacheEnGantt(SuperTache):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, task, **kwargs)
        # Note : self.master est une référence vers AffichageGantt
        self.jeCherche = False
        
        self.bind("<Button-1>", self.__clique)       # On bind la frame
        self.texte.bind("<Button-1>", self.__clique) # On bind le Text qui remplie tout la Frame
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
        y = self.master.getNbTacheJour(self.task.debut.date(), self.master.listeTache.index(self))
        return x1, x2, y

    def affichePlusLien(self, tag):
        # Récupération des valeurs
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

    def __clique(self, event):

        if (chercheur := self.master.getQuiCherche()) == None: # Objet TacheEnGantt qui a la variable jeCherche = True
            self.master.updateAffichage()
            return
        chercheur.jeCherche = False
        
        if self.master.mode == "addDep": # On commence par savoir dans quelle mode on est
            self.master.mode = ""    # On réinitialise le mode
            if  chercheur.task.debut+chercheur.task.duree < self.task.debut: # Si le chercheur est avant
                try : # on essaye de voir si c'est pas déjà existant
                    self.master.listeLien.append(LienDependance(chercheur, self, self.master.can))
                except:pass
            elif chercheur.task.debut > self.task.debut+self.task.duree: # Si on est avant le chercheur
                try :
                    self.master.listeLien.append(LienDependance(self, chercheur, self.master.can))
                except:pass
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
#             Si on est après la période affiché
            if self.task.debut.date() > self.master.getJourFin() - datetime.timedelta(days=1):
                x1 = self.master.can.winfo_width()+10 # On se place en dehors du cote droit
#             Si on est avant le début
            elif self.task.debut.date() < self.master.getJourDebut():
                x1 = -10 # On se place en dehors du cote gauche
            # Si c'est juste le plus qui n'est plus affiché car il y a déjà un lien existant
            else :
                x1 = self.getPosPixel()[2] # Ici le getPosPixel est autorisé car la tache est affiché

        self.master.can.coords(self.maLigneDepEnCours, x1, y1, event.x, event.y)

    def creerLigne(self):
        """Fonction qui créer une ligne seulement si on est en tran de créer une ligne que l'on peut ensuite bouger à notre curseur"""
        if self.jeCherche and self.master.mode == "addDep":
            self.maLigneDepEnCours = self.master.can.create_line(-10,-10,-10,-10, fill="#00BB00", width=2, tags="topLine")


class AffichageGantt(SuperCalendrier):
    """
    Classe qui fait un affichage des tâches selon Gantt.
    Hérite de SuperCalendrier et donc de Frame.
    """
    ESPACEMENT = 4
    TAILLE_LIGNE = 50 + ESPACEMENT
    TAILLE_BANDEAU_JOUR = 20

    def __init__(self, master = None, **kwargs):
        SuperCalendrier.__init__(self, master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        # Listes des tâches et des liens :
        self.listeTache = []
        self.listeLien  = []

        # La taille de la colonne dépend de la taille du Canvas :
        self.tailleColonne = 0
        
        # Pourcentage de la taille d'une colonne pour une tâche :
        self.facteurW = 0.8
        
        # Canvas de l'affichage :
        self.can = Canvas(self, width=1, height=1, scrollregion = (0, 0, 1, 1))
        self.can.pack(fill=BOTH, expand=YES, side = LEFT)
        self.can.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        self.scrollbar = Scrollbar(self, command = self.can.yview) # Premier reliage de la scrollbar
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.can.config(yscrollcommand = self.scrollbar.set) # 2e reliage de la scrollbar

        # Bindings du Canvas :
        self.can.bind("<Configure>", lambda e : self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        self.can.bind_all("<Button-1>",         self.__mouseClicked)
        self.can.bind_all("<Control-Button-1>", self.__multiSelection)
        self.can.bind_all("<Escape>",           self.__escapePressed)
        self.can.bind_all("<Delete>",           self.__suppr)

        ## Valeurs possibles : "", "delDep" et "addDep"
        # Défini les différents modes pour savoir si on ajoute ou retire qqchose ou pas.
        self.mode = ""

    def getLiens(self):
        return self.listeLien

    def __trouverItems(self, pos):
        """
        Trouver les items à la position donnée
        @param pos : objet avec un attribut x et un attribut y, correspondant à la position souhaitée.
        """
        return self.can.find_overlapping(pos.x-1, pos.y-1, pos.x+1, pos.y+1)
    def __getBtnChangeJour(self):
        return self.getParametreAffichage().getBoutonsChangementJours()
    def getParametreAffichage(self):
        return self.master.master.getParametreAffichage()

    def __trouverTags(self, pos):
        # On parcour les items
        for item in self.__trouverItems(pos):
            # On déduit leurs tags :
            tags = self.can.gettags(item)

            # Si il n'existent pas :
            if tags is None or len(tags) == 0:
                continue
            yield from tags

    def __deselectionner(self):
        # On cherche ce qui fait le trait vert
        chercheur = self.getQuiCherche()
        
        # Si c'est lui qui existe, c'est lui qui est annulé:
        if chercheur is not None:
            chercheur.jeCherche = False

        # Sinon c'est la désélection des liens si on clique ailleurs
        else:
            for lien in self.getLiensSelectionnes():
                lien.select = False

    def __multiSelection(self, event):
        """Ajoute ou enlève les liens à la sélection."""
        # On boucle sur les items qui sont on niveau du clic :
        for tag in self.__trouverTags(event):
            # Pour tout les liens, on cherche lequel est le bon :
            for lien in self.listeLien:
                if lien.ID_LIEN == tag:
                    # Si il est bon : on inverse la sélection du lien.
                    lien.changeSelect()

    def __escapePressed(self, event):
        # On retourne sur le mode par défaut :
        self.mode = ""
        self.__deselectionner()
        self.updateAffichage()

    def __mouseClicked(self, event):
        # On cherche à détruire le lien si on est dans le mode adéquat
        if self.mode == "delDep":
            for tag in self.__trouverTags(event):
                if tag == "top":
                    continue
                # Détection des lien :
                for lien in self.listeLien[:]:
                    if lien.ID_LIEN == tag:
                        lien.suppression()

#       Si on clique que un bouton de changement de jour (on ne déselectionne pas) pour la ligne verte
        if event.widget in self.__getBtnChangeJour():
            self.updateAffichage()
            return

        # On retourne sur le mode par défaut :
        self.mode = ""
        self.__deselectionner()

        # Si c'est pas le canvas, on s'en fiche (on joue le truc qu'on a cliqué) :
        if event.widget != self.can:
            # Mise à jour graphique :
            self.updateAffichage()
            return

        for tag in self.__trouverTags(event):
            # Détection des lien :
            for lien in self.listeLien:
                if lien.ID_LIEN == tag:
                    lien.select = True
            # Détection des plus :
            for t in self.listeTache:
                if t.ID_PLUS == tag:
                    t.addDependance()

        # Mise à jour graphique :
        self.updateAffichage()

    def __suppr(self, event): # TODO : ce serait bien de supprimer des taches aussi =)
        for lien in self.getLiensSelectionnes():
            lien.suppression()

    def getLiensSelectionnes(self):
        return [lien for lien in self.listeLien if lien.select]

    def getQuiCherche(self): # retourne la tache qui est en train de chercher une dépandance
        for tache in self.listeTache:
            if tache.jeCherche == True:
                return tache

    def getNbTacheJour(self, dateJour, arret = None):
        nombre = 0
        for tache in self.listeTache:
            if self.getIndiceTacheEnGantt(tache) == arret:
                return nombre

            if tache.task.debut.date() == dateJour:
                nombre+=1
        return nombre
    
    def getNbLigneTotal(self):
        nbLigne = 1
        for jour in self.rangeDate(self.getJourDebut(), self.getJourFin()):
            nbLigne = max(nbLigne, self.getNbTacheJour(jour))
        return nbLigne
    
    def getScrollableHeight(self):
        """Renvoie le plus grand entre la partie scrollable et la hauteur du Canvas"""
        return max(self.can.winfo_height(), int(self.can.cget("scrollregion").split(" ")[3]))
  
    def getIndiceTacheEnGantt(self, tache):
        return self.listeTache.index(tache)
    
    def updateAffichage(self):
        """Mise à jour graphique."""
        # Sécurité :
        if self.can.winfo_width() != 0:
            # On efface TOUT :
            for tache in self.listeTache:
                tache.PlusCoord = None
            self.can.delete(ALL)

            # On réaffiche touououououout :
            self.__afficherLesJours()
            self.__afficherLesTaches()
            self.__afficherLesDependances()

            # On update la zone scrollable :
            w = self.can.winfo_width()
            h = self.getNbLigneTotal() * AffichageGantt.TAILLE_LIGNE + AffichageGantt.TAILLE_BANDEAU_JOUR
            self.can.config(scrollregion = (0, 0, w, h))

    def addTask(self, tache, region = None):
        """Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas."""
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        # NOTE : il faut aussi changer ici pour avoir un affichage plusieurs jours.
        t = TacheEnGantt(self, tache, bg= tache.color) # on crée notre objet
        self.listeTache.append(t) # On rajoute la tache après dans la liste pour ne pas la tester au moment de l'affichage
        self.updateAffichage()
        return tache

    def __afficherLesJours(self):
        """Traçage des lignes de division et des noms de jour."""
        # Largeur :
        self.tailleColonne = w = self.can.winfo_width()/self.getNbJour()
        
        # création de bandeau pour les jours
        self.can.create_rectangle(0, 0, self.can.winfo_width(), AffichageGantt.TAILLE_BANDEAU_JOUR, fill="#BBBBBB", outline="")
        
        # Pour chaques jours :
        for jour in range(self.getNbJour()):
            
            # Position X :
            x = int(jour * w)
            
            # Séparateurs :
            if jour !=0:
                self.can.create_line(x, 0, x, self.getScrollableHeight())
            
            # Texte des jours :
            self.can.create_text(x + w/2, AffichageGantt.TAILLE_BANDEAU_JOUR//2,
                                 width = w,
                                 text=JOUR[(jour+self.getJourDebut().weekday())%7])

    def __afficherLesTaches(self):

        self.listeTache.sort(key=lambda t:t.task.debut) # Trie par début des taches

        for tache in self.listeTache:
            ID_TACHE = self.listeTache.index(tache)

            # Ligne verte :
            tache.creerLigne()
            if tache.task.debut.date() >= self.getJourDebut() and tache.task.debut.date() <= self.getJourFin():
                
                # TODO : ici, il faudra adapter pour gérer une tache sur plusieurs jours.
                # width = int(self.tailleColonne-1)*tache.task.duree.days-1 + int(self.tailleColonne-1)*self.facteurW
                w = self.tailleColonne
                # X en fonction du jour de la tache :
                x = int(w*(tache.task.debut.weekday()-self.getJourDebut().weekday()) + 2)
                # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le même jour :
                y = (AffichageGantt.TAILLE_BANDEAU_JOUR + AffichageGantt.TAILLE_LIGNE*self.getNbTacheJour(tache.task.debut.date(), self.getIndiceTacheEnGantt(tache)))

                self.can.create_window(x, y, # Position
                                       width=int(w*self.facteurW),
                                       height=AffichageGantt.TAILLE_LIGNE-AffichageGantt.ESPACEMENT,
                                       anchor=NW,
                                       window = tache,
                                       tags="num%s"%self.getIndiceTacheEnGantt(tache))

                if len(tache.task.dependantes) == 0:
                    tache.ID_PLUS = "plus"+str(ID_TACHE)
                    tache.affichePlusLien(tache.ID_PLUS)

    def __afficherLesDependances(self):
        for lien in self.listeLien:
            lien.afficherLesLiens()

        # Ordre d'affichage
        self.can.tag_raise("top")
        self.can.tag_raise("topLine")
        self.can.tag_raise("topPlus")


if __name__=='__main__':
    import Application
    Application.main()
