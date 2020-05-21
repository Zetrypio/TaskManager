# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *
from util.widgets.infobulle import *
from util.widgets.RMenu import *
from util.util import *
from util.Point import *

from ..AbstractDisplayedCalendar import *
from .TacheEnGantt import *

class AffichageGantt(AbstractDisplayedCalendar):
    """
    Classe qui fait un affichage des tâches selon Gantt.
    Hérite de SuperCalendrier et donc de Frame.
    """
    ESPACEMENT = 4
    TAILLE_LIGNE = 50 + ESPACEMENT
    TAILLE_BANDEAU_JOUR = 20

    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        # Listes des tâches et des liens :
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
        self.can.bind_all("<ButtonRelease-1>", lambda e: self.updateAffichage()) # Faire en sorte que les coordonées de la scrollbar soient prisent en compte quand on la bouge.
        self.can.bind_all("<Button-1>",         self.mouseClicked)
        self.can.bind_all("<Control-Button-1>", self.__multiSelection)
        self.can.bind_all("<Escape>",           self.escapePressed)
        self.can.bind_all("<Delete>",           self.__suppr)

        ## Valeurs possibles : "", "delDep" et "addDep"
        # Défini les différents modes pour savoir si on ajoute ou retire qqchose ou pas.
        self.mode = ""

        #RMenu des liens
        self.can.bind_all("<<RMenu-Opened>>", self.configureRMenu)
        self.rmenu = RMenu(self, binder = self.can, bindWithId="lienDep")
        self.event_generate("<<RMenu-Opened>>")

    def configureRMenu(self, event):
        # On déselectionne
        self._deselectionnerLesLiens()
        pos = self.getScrolledPosition(event) # Si ca marche pas, 2 solutions, mais on verra plus tard
        lesliens = set()
        self.rmenu.delete(0, 'end')
        for tag in self.__trouverTags(pos):
            for lien in self.listeLien: # On pourrait pas faire une méthode ? (je sais ça n'a rien à voir)
                if lien.ID_LIEN == tag:# and tag!="top":
                    self.rmenu.add_command(label = "suppression %s→%s"%(lien.tacheD.task.nom, lien.tacheF.task.nom), command = lambda l=lien: l.suppression())
                    lesliens.add(lien)
                    lien.select = True
                    #else:
                    #lien.select = False
        self.updateAffichage()
        self.update()
        self.rmenu.add_separator()
        self.rmenu.add_command(label = "Supprimer tout les liens sélectionnés", command = lambda :  self.supprimerLiens(lesliens))

    def supprimerLiens(self, lesliens):
        for lien in lesliens:
            lien.suppression()

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

    def _deselectionnerLesLiens(self):
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
        # Petite vérification élementaire
        if self.getDonneeCalendrier().getPanneauActif() != self:
            return

        # On corrige la position selon le scroll
        pos = self.getScrolledPosition(event)

        # Test si on est sur le bandeau des jours
        if pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
            indice = pos.x//self.tailleColonne
            jour = self.getJourDebut() + datetime.timedelta(days=indice)
            self.selectTaskJour(jour, control=True)
            return

        # On boucle sur les items qui sont on niveau du clic :
        for tag in self.__trouverTags(pos):
            # Pour tout les liens, on cherche lequel est le bon :
            for lien in self.listeLien:
                if lien.ID_LIEN == tag:
                    # Si il est bon : on inverse la sélection du lien.
                    lien.changeSelect()

    def escapePressed(self, event):
        # Petite vérification élementaire
        if self.getDonneeCalendrier().getPanneauActif() != self:
            return
        super().escapePressed(event)
        # On retourne sur le mode par défaut :
        self.mode = ""
        self._deselectionnerLesLiens()
        self.updateAffichage()

    def mouseClicked(self, event):
        # Petite vérification élementaire
        if self.getDonneeCalendrier().getPanneauActif() != self:
            return
        # On corrige la position selon le scroll
        pos = self.getScrolledPosition(event)
        
        # On cherche à détruire le lien si on est dans le mode adéquat
        if self.mode == "delDep":
            for tag in self.__trouverTags(pos):
                if tag == "top":
                    continue
                # Détection des lien :
                for lien in self.listeLien[:]:
                    if lien.ID_LIEN == tag:
                        lien.cliqueSuppr()

        # Si on clique que un bouton de changement de jour (on ne déselectionne pas) pour la ligne verte
        if event.widget in self.__getBtnChangeJour():
            self.updateAffichage()
            return

        # On retourne sur le mode par défaut :
        self.mode = ""
        self._deselectionnerLesLiens()

        # Si c'est pas le canvas, on s'en fiche (on joue le truc qu'on a cliqué) :
        if event.widget != self.can or event.widget in self.listeTaskAffichees:
            # Mise à jour graphique :
            self.updateAffichage()
            return
        # On deselectionne les Taches si c'est effectivement pas une tache sur quoi on a cliqué (condition ci dessus)
        super().mouseClicked(event)

        # Test si on est sur le bandeau des jours
        if pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
            indice = pos.x//self.tailleColonne
            jour = self.getJourDebut() + datetime.timedelta(days=indice)
            self.selectTaskJour(jour)
            return

        for tag in self.__trouverTags(pos):
            # Détection des lien :
            for lien in self.listeLien:
                if lien.ID_LIEN == tag:
                    lien.select = True
            # Détection des plus :
            for t in self.listeTaskAffichees:
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
        for tache in self.listeTaskAffichees:
            if tache.jeCherche == True:
                return tache

    def getNbTacheJour(self, dateJour, arret = None):
        nombre = 0
        for tache in self.listeTaskAffichees:
            if self.getIndiceTacheEnGantt(tache) == arret:
                return nombre

            if tache.task.getDebut().date() == dateJour:
                nombre+=1
        return nombre
    
    def getNbLigneTotal(self):
        nbLigne = 1
        for jour in self.rangeDate(self.getJourDebut(), self.getJourFin()):
            nbLigne = max(nbLigne, self.getNbTacheJour(jour))
        return nbLigne
    
    def getYScrolling(self):
        return int(round(self.can.yview()[0]*int(self.can.cget("scrollregion").split(" ")[3])))-1
    
    def getScrolledPosition(self, pos):
        return Point(pos.x, pos.y + self.getYScrolling())
    
    def getScrollableHeight(self):
        """Renvoie le plus grand entre la partie scrollable et la hauteur du Canvas"""
        return max(self.can.winfo_height(), int(self.can.cget("scrollregion").split(" ")[3]))
  
    def getIndiceTacheEnGantt(self, tache):
        return self.listeTaskAffichees.index(tache)
    
    def updateAffichage(self):
        """Mise à jour graphique."""
        # Sécurité :
        if self.can.winfo_width() != 0:
            # On efface TOUT :
            for tache in self.listeTaskAffichees:
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

    def onIntervertir(self):
        for lien in self.listeLien:
            if lien.tacheD.task.getDebut() > lien.tacheF.task.getDebut():
                lien.inverserLaDependances()

    def identify_region(self, x, y):
        # Position :
        pos = Point(x, y)
        pos = self.getScrolledPosition(pos)
        
        # Jour :
        indiceJour = pos.x//self.tailleColonne;
        decalageJour = datetime.timedelta(days = indiceJour)
        jour = self.getJourDebut() + decalageJour
        
        # Heures :
        y = pos.y - AffichageGantt.TAILLE_BANDEAU_JOUR
        if y < 0:
            heure = datetime.time(self.getHeureDebut())
        elif y > self.getNbTacheJour(jour) * AffichageGantt.TAILLE_LIGNE:
            try:
                heure = self.getTache(jour, self.getNbTacheJour(jour)-1).task.getFin().time()
            except ValueError:
                heure = (datetime.datetime.combine(jour, self.getHeureDebut()) + \
                (datetime.datetime.combine(jour, self.getHeureFin  ())
                -datetime.datetime.combine(jour, self.getHeureDebut()) ) /2).time()
        else:
            try:
                heure = self.getTache(jour, y//AffichageGantt.TAILLE_LIGNE).task.getFin().time()
            except ValueError:
                heure = (datetime.datetime.combine(jour, self.getHeureDebut()) + \
                (datetime.datetime.combine(jour, self.getHeureFin  ())
                -datetime.datetime.combine(jour, self.getHeureDebut()) ) /2).time()
        
        date = datetime.datetime.combine(jour, heure)
        return date

    def getTache(self, jour, nb):
        compteur = 0
        for tache in self.listeTaskAffichees:
            if tache.task.getDebut().date() == jour:
                if compteur == nb:
                    return tache
                compteur += 1

    def addTask(self, tache, region = None):
        """Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas."""
        if not (tache := super().addTask(tache, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return
        
        # NOTE : il faut aussi changer ici pour avoir un affichage plusieurs jours.
        t = TacheEnGantt(self, tache, bg= tache.getColor()) # on crée notre objet
        self.listeTaskAffichees.append(t) # On rajoute la tache après dans la liste pour ne pas la tester au moment de l'affichage
        self.updateAffichage()
        return tache

    def __afficherLesJours(self):
        """Traçage des lignes de division et des noms de jour."""
        # Largeur :
        if self.getNbJour() == 0:
            return
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
        self.listeTaskAffichees.sort(key=lambda t:t.task.getDebut()) # Trie par début des taches

        for tache in self.listeTaskAffichees:
            ID_TACHE = self.listeTaskAffichees.index(tache)

            tache.updateColor() # fonction pour mettre à jour la couleur


            # Ligne verte :
            tache.creerLigne()
            if tache.task.getDebut().date() >= self.getJourDebut() and tache.task.getDebut().date() <= self.getJourFin():
                
                # TODO : ici, il faudra adapter pour gérer une tache sur plusieurs jours.
                # width = int(self.tailleColonne-1)*tache.task.duree.days-1 + int(self.tailleColonne-1)*self.facteurW
                w = self.tailleColonne
                # X en fonction du jour de la tache :
                x = int(w*(tache.task.getDebut().date()-self.getJourDebut()).days + 2)
                # Y en fonction de la taille d'une ligne * le nombre de tache déjà présente le même jour :
                y = (AffichageGantt.TAILLE_BANDEAU_JOUR + AffichageGantt.TAILLE_LIGNE*self.getNbTacheJour(tache.task.getDebut().date(), self.getIndiceTacheEnGantt(tache)))

                self.can.create_window(x, y, # Position
                                       width=int(w*self.facteurW),
                                       height=AffichageGantt.TAILLE_LIGNE-AffichageGantt.ESPACEMENT,
                                       anchor=NW,
                                       window = tache,
                                       tags="num%s"%self.getIndiceTacheEnGantt(tache))

                if len(tache.task.getDependantes()) == 0:
                    tache.ID_PLUS = "plus"+str(ID_TACHE)
                    tache.affichePlusLien(tache.ID_PLUS)

    def __afficherLesDependances(self):
        for lien in self.listeLien:
            lien.afficherLesLiens()

        # Ordre d'affichage
        self.can.tag_raise("top")
        self.can.tag_raise("topLine")
        self.can.tag_raise("topPlus")
