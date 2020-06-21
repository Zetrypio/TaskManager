# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.geom.Point import *
from util.geom.Rectangle import *
from util.widgets.Dialog import *
from util.widgets.infobulle import *
from util.widgets.RMenu import *
from util.util import *

from ..AbstractDisplayedCalendar import *
from .liens.DependanceLink import *

from schedulable.groupe.Groupe import *
from schedulable.task.Task import *

class AffichageGantt(AbstractDisplayedCalendar):
    """
    Classe qui fait un affichage des tâches selon Gantt.
    Hérite de AbstractDisplayedCalendar et donc de Frame.
    """
    ESPACEMENT = 4
    HAUTEUR_TACHE = 50
    TAILLE_LIGNE = HAUTEUR_TACHE + ESPACEMENT
    TAILLE_BANDEAU_JOUR = 20

    def __init__(self, master = None, **kwargs):
        """
        Constructeur de l'affichage gantt.

        @param master: Notebook de DonneeCalendrier, master du tkinter.Frame() que cet objet est.
        @param **kwargs: Configuration du tkinter.Frame() que cet objet est.
        """
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers Notebook.
        
        # Listes des tâches, groupes et liens :
        self.listeDisplayableItem = []
        
        # Liste des datetimeItemParts :
        self.__parts = []

        # Ligne verte pour quand on est en train de relier plusieurs tâches ou autre :
        self.__id_LinkingLine = None
        self.__x1_LinkingLine = None
        self.__y1_LinkingLine = None
        self.__color_LinkingLine = None
        self.__activeGanttObject = None

        # La taille de la colonne dépend de la taille du Canvas :
        self.tailleColonne = 0
        
        # Pourcentage de la taille d'une colonne pour une tâche ou un groupe :
        # (l'autre partie sert pour afficher les liens).
        self.facteurW = 0.8
        
        # Canvas de l'affichage (et scrollbar) :
        self.can = Canvas(self, width=1, height=1, scrollregion = (0, 0, 1, 1))
        self.can.pack(fill=BOTH, expand=YES, side = LEFT)
        self.can.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        self.scrollbar = Scrollbar(self, command = self.can.yview) # Premier reliage de la scrollbar
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.can.config(yscrollcommand = self.scrollbar.set) # 2e reliage de la scrollbar

        # Bindings du Canvas :
        #
        # TODO : Utiliser des events virtuels,
        # et un gestionnaire de clavier.
        # En attente des préférences du clavier
        #

        # Pour savoir si un événement à été annulé.
        # Seul événement annulable : clic sur le canvas.
        self.__eventCanceled = False
        
        # Binding d'events virtuels : ?
        self.can.bind("<Escape>", lambda e: self.can.event_generate("<<deselect-all>>")   , add=1)
        self.can.bind("<Delete>", lambda e: self.can.event_generate("<<delete-selected>>"), add=1)
        
        # Définition des events virtuels :
        self.can.bind_all("<<deselect-all>>", lambda e: self.__onClicSurCanvas())
        self.can.bind("<Button-1>", lambda e: self.__onClicSurCanvas())
        self.can.bind("<Motion>", self.__updateLinkingLine)

        # Infobulle toujours vraie :
        ajouterInfoBulleTagCanvas(self.can, "plus", "Ajouter un lien.")

        # TODO : RMenu des liens

    def deselectEverything(self):
        super().deselectEverything()
        for item in self.listeDisplayableItem:
            if isinstance(item, DependanceLink):
                item.setSelected(False)
                item.updateColor(self.can)

    def __highlightLinks(self, mode):
        for l in self.listeDisplayableItem:
            if isinstance(l, DependanceLink):
                if mode == "+" and (self.__activeGanttObject.getSchedulable() is l.getPartA().getSchedulable()
                                 or self.__activeGanttObject.getSchedulable() is l.getPartB().getSchedulable()):
                    l.highlight("#FFAF00")
                elif mode == "-":
                    l.highlight("#FF3F3F")
                else:
                    l.highlight(None)
        self.updateColor()

    def beginLinkingLine(self, objGantt, mode="+"):
        """
        Permet de commencer une ligne verte pour un lien depuis un objetGantt.
        @param objGantt: l'objetGantt depuis lequel commence le lien.
        """
        self.__onClicSurCanvas()
        self.__activeGanttObject = objGantt
        self.__highlightLinks(mode)
        self.__x1_LinkingLine = self.__activeGanttObject.getXDebutLinkingLine()
        self.__y1_LinkingLine = self.__activeGanttObject.getYDebutLinkingLine()
        self.__color_LinkingLine = "#00CF00" if mode == "+" else "#CF0000"
        self.__id_LinkingLine = self.can.create_line(self.__x1_LinkingLine,
                                                     self.__y1_LinkingLine,
                                                     self.__x1_LinkingLine,
                                                     self.__y1_LinkingLine,
                                                     fill=self.__color_LinkingLine,
                                                     width = 2)

    def __updateLinkingLine(self, event):
        """
        Permet de mettre à jour la ligne verte.
        Appelée quand la souris bouge sur le Canvas() contenu dans cet objet.
        @param event: informations sur l'événement contenant la position de la souris.
        """
        if self.__id_LinkingLine is not None:
            pos = self.getScrolledPosition(event)
            self.__x1_LinkingLine = pos.x
            self.__y1_LinkingLine = pos.y
            self.can.coords(self.__id_LinkingLine,
                            pos.x, pos.y,
                            self.__activeGanttObject.getXDebutLinkingLine(), self.__activeGanttObject.getYDebutLinkingLine())

    def __endLinkingLine(self):
        try:
            self.can.delete(self.__id_LinkingLine)
        except:
            pass
        self.__id_LinkingLine = None
        self.__x1_LinkingLine = None
        self.__y1_LinkingLine = None
        self.__activeGanttObject = None
        

    def clicSurObjet(self, objGantt):
        """
        Méthode à exécuter quand on clic sur l'un des objets de gantt.
        Peut créer un lien si on était en mode d'ajout de liens etc.
        @param objGantt: l'objet sur lequel on a cliqué.
        @override clicSurObjet(objet) in AbstractDisplayedCalendar()
        """
        # Si on est en mode ajout de lien :
        if objGantt is not self.__activeGanttObject and self.__activeGanttObject is not None and objGantt is not None:
            # Si le lien est accepté :
            if objGantt.getSchedulable().acceptLinkTo(self.__activeGanttObject.getSchedulable()):
                # On inverse le lien si il est à l'envers.
                if objGantt.getSchedulable().getDebut() < self.__activeGanttObject.getSchedulable().getDebut():
                    self.__activeGanttObject, objGantt = objGantt, self.__activeGanttObject

                # On crée le lien et met donc à jour l'affichage.
                self.listeDisplayableItem.append(
                    DependanceLink(
                        self,
                        self.getVisiblePart(self.__activeGanttObject.getLastPart()),
                        self.getVisiblePart(objGantt.getFirstPart())))
                self.__highlightLinks(None)
                self.__endLinkingLine()
                self.updateAffichage()
        elif self.__activeGanttObject is None:
            self.deselectEverything()
            objGantt.getSchedulable().setSelected(True)
            self.getDonneeCalendrier().updateColor()

    def __onClicSurCanvas(self):
        """
        Méthode exécutée quand on appuie sur échappe ou qu'on appuie
        dans le vide pour annuler le lien de la ligne verte. Sinon pour désélectionner les tâches.
        """
        self.__highlightLinks(None)
        if not self.__eventCanceled:
            if self.__activeGanttObject is not None:
                self.__endLinkingLine()
            else:
                self.deselectEverything()
        self.__eventCanceled = False

    def cancelEvent(self):
        self.__eventCanceled = True

    def __precalculer(self):
        """
        Permet de précalculer les Parts non fusionnées
        des tâches affichées dans ce calendrier.
        """
        self.__parts = []
        for displayable in self.listeDisplayableItem:
            if isinstance(displayable, AbstractMultiFrameItem):
                self.__parts.extend(self.getVisiblePart(part) for part in displayable.getRepartition() if self.getVisiblePart(part))

#    def __trouverItems(self, pos):
#        """
#        Trouver les items à la position donnée
#        @param pos : objet avec un attribut x et un attribut y, correspondant à la position souhaitée.
#        """
#        return self.can.find_overlapping(pos.x-1, pos.y-1, pos.x+1, pos.y+1)
#    def __getBtnChangeJour(self):
#        return self.getParametreAffichage().getBoutonsChangementJours()

    def getParametreAffichage(self):
        """
        Getter de ParametreAffichage.
        @return ParametreAffichage.
        """
        return self.master.master.getParametreAffichage() # Skip le Notebook

#    def __trouverTags(self, pos):
#        # On parcours les items
#        for item in self.__trouverItems(pos):
#            # On déduit leurs tags :
#            tags = self.can.gettags(item)
#
#            # Si il n'existent pas :
#            if tags is None or len(tags) == 0:
#                continue
#            yield from tags

#    def _deselectionnerLesLiens(self):
#        # On cherche ce qui fait le trait vert
#        chercheur = self.getQuiCherche()
#        
#        # Si c'est lui qui existe, c'est lui qui est annulé:
#        if chercheur is not None:
#            chercheur.jeCherche = False
#
#        # Sinon c'est la désélection des liens si on clique ailleurs
#        else:
#            for lien in self.getLiensSelectionnes():
#                lien.select = False

#    def __multiSelection(self, event):
#        """Ajoute ou enlève les liens à la sélection."""
#        # Petite vérification élémentaire
#        if self.getDonneeCalendrier().getPanneauActif() != self:
#            return
#
#        # On corrige la position selon le scroll
#        pos = self.getScrolledPosition(event)
#
#        # Test si on est sur le bandeau des jours
#        if pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
#            indice = pos.x//self.tailleColonne
#            jour = self.getJourDebut() + datetime.timedelta(days=indice)
#            self.selectTaskJour(jour, control=True)
#            return
#
#        # On boucle sur les items qui sont on niveau du clic :
#        for tag in self.__trouverTags(pos):
#            # Pour tout les liens, on cherche lequel est le bon :
#            for lien in self.listeLien:
#                if lien.ID_LIEN == tag:
#                    # Si il est bon : on inverse la sélection du lien.
#                    lien.changeSelect()

#    def escapePressed(self, event):
#        # Petite vérification élémentaire
#        if self.getDonneeCalendrier().getPanneauActif() != self:
#            return
#        super().escapePressed(event)
#        # On retourne sur le mode par défaut :
#        self.mode = ""
#        self._deselectionnerLesLiens()
#        self.updateAffichage()
#
#    def mouseClicked(self, event):
#        # Petite vérification élémentaire
#        if self.getDonneeCalendrier().getPanneauActif() != self:
#            return
#        # On corrige la position selon le scroll
#        pos = self.getScrolledPosition(event)
#        
#        # On cherche à détruire le lien si on est dans le mode adéquat
#        if self.mode == "delDep":
#            for tag in self.__trouverTags(pos):
#                if tag == "top":
#                    continue
#                # Détection des lien :
#                for lien in self.listeLien[:]:
#                    if lien.ID_LIEN == tag:
#                        lien.cliqueSuppr()
#
#        # Si on clique que un bouton de changement de jour (on ne déselectionne pas) pour la ligne verte
#        if event.widget in self.__getBtnChangeJour():
#            self.updateAffichage()
#            return
#
#        # On retourne sur le mode par défaut :
#        self.mode = ""
#        self._deselectionnerLesLiens()
#
#        # Si c'est pas le canvas, on s'en fiche (on joue le truc qu'on a cliqué) :
#        if event.widget != self.can or event.widget in self.listeTaskAffichees:
#            # Mise à jour graphique :
#            self.updateAffichage()
#            return
#        # On désélectionne les tâches si c'est effectivement pas une tache sur quoi on a cliqué (condition ci dessus)
#        super().mouseClicked(event)
#
#        # Test si on est sur le bandeau des jours
#        if pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
#            indice = pos.x//self.tailleColonne
#            jour = self.getJourDebut() + datetime.timedelta(days=indice)
#            self.selectTaskJour(jour)
#            return
#
#        for tag in self.__trouverTags(pos):
#            # Détection des lien :
#            for lien in self.listeLien:
#                if lien.ID_LIEN == tag:
#                    lien.select = True
#            # Détection des plus :
#            for t in self.listeTaskAffichees:
#                if t.ID_PLUS == tag:
#                    t.addDependance()
#
#        # Mise à jour graphique :
#        self.updateAffichage()
#
#    def __suppr(self, event): # TODO : ce serait bien de supprimer des tâches aussi =)
#        for lien in self.getLiensSelectionnes():
#            lien.suppression()
#
#    def getLiensSelectionnes(self):
#        return [lien for lien in self.listeLien if lien.select]
#
#    def getQuiCherche(self): # retourne la tache qui est en train de chercher une dépendance
#        for tache in self.listeTaskAffichees:
#            if tache.jeCherche == True:
#                return tache

    def getNbTacheJour(self, jour):
        """
        Permet d'obtenir le nombre de de AbstractItemContent à mettre sur un jour donné.
        @param jour: le jour dont on veut savoir le nombre de parts.
        @return le nombre de part sur le jour donné.
        """
        return len(list(self.getPartsOfDay(jour)))
    
    def getNbLigneTotal(self):
        """
        Permet de savoir le nombre de ligne totale sur l'ensemble des jours affichés.
        Utile pour savoir jusqu'à où va le scrolling.
        @return le maximum de #getNbTacheJour() pour tout les jours qui sont actuellement visibles.
        """
        nbLigne = 1
        for jour in self.rangeDate(self.getJourDebut(), self.getJourFin()):
            nbLigne = max(nbLigne, self.getNbTacheJour(jour))
        return nbLigne
    
    def getYScrolling(self):
        """
        Permet de savoir de combien le Canvas est scrollé.
        @return un int correspondant au nombre de pixels scrollées dans le canvas via la scrollbar.
        """
        return int(round(self.can.yview()[0]*int(self.can.cget("scrollregion").split(" ")[3])))-1
    
    def getScrolledPosition(self, pos):
        """
        Permet d'obtenir la position de manipulation des données via programme à partir d'une position reçue via un event.
        @param pos: Point() (ou Event() car il a les bons attributs aussi) correspondant à la
        position reçue via événement ou qu'on veut scroller.
        @return un Point() avec la position corrigée selon le scrolling du Canvas(), utilisable donc via le programme sans soucis.
        """
        return Point(pos.x, pos.y + self.getYScrolling())
    
    def getScrollableHeight(self):
        """
        Renvoie la partie visible du canvas en comptant tout ce qui peut être scrollé,
        mais si la partie scrollable est plus petite que la partie visible, renvoie quand même
        la partie visible.
        @return le plus grand entre la partie scrollable et la hauteur du Canvas
        """
        return max(self.can.winfo_height(), int(self.can.cget("scrollregion").split(" ")[3]))

    def updateAffichage(self):
        """
        Mise à jour graphique.
        """
        # Sécurité :
        if self.can.winfo_width() != 0:
            # On efface TOUT :
            self.can.delete(ALL)

            # On réaffiche touououououout :
            self.__precalculer()
            self.__afficherLesJours()
            self.__afficherLesTaches()
            self.__afficherLesDependances()

            # On update la zone scrollable :
            w = self.can.winfo_width()
            h = self.getNbLigneTotal() * AffichageGantt.TAILLE_LIGNE + AffichageGantt.TAILLE_BANDEAU_JOUR
            self.can.config(scrollregion = (0, 0, w, h))

    def updateColor(self):
        """
        Permet de mettre à jour la couleur de tout les IDisplayableItem()s.
        """
        for displayable in self.listeDisplayableItem:
            displayable.updateColor(self.can)

    def getPartPosition(self, part):
        """
        Permet de savoir en combientième la DatetimeItemPart() reçue en paramètre
        doit être affichée.
        Note : la valeur renvoyée n'est pas en pixels, mais en lignes.
        @param part: la DatetimeItemPart() à tester.
        @return un int correspondant à la ligne d'affichage dans le gantt.
        """
        index = 0
        for p in self.__parts:
            if p == part:
                return index
            if p.getJour() == part.getJour():
                index += 1
        return index

    def getPartRectangle(self, part):
        """
        Permet d'obtenir la zone qui est réservée à l'affichage de la DatetimeItemPart.
        @param part: le DatetimeItemPart dont on veut savoir la position.
        @return util.geom.Rectangle() contenant les coordonnées en pixels de la zone réservée à cette DatetimeItemPart().
        """
        colonne = (part.getJour() - self.getJourDebut()).days
        return Rectangle(x1 = int(self.tailleColonne * colonne),
                         y1 = AffichageGantt.TAILLE_BANDEAU_JOUR + self.getPartPosition(part)*AffichageGantt.TAILLE_LIGNE,
                         width = self.tailleColonne,
                         height = AffichageGantt.TAILLE_LIGNE)

    def getPartsOfDay(self, day):
        """
        Permet d'obtenir la liste des DatetimeItemPart()s qui sont le jour demandé.
        @param day: datetime.date() correspondant au jour dont on cherche les parts.
        @return un générateur de DatetimeItemPart dont ne sont gardé que celles qui sont le jour demandé.
        """
        return (part for part in self.__parts if part.getJour() == day)

    def onIntervertir(self):
        """
        Méthode appelée lorsqu'on interverti 2 jours.
        S'occupe de rétablir les liens dans le bon sens.
        @deprecated: TODO : Il faut revoir cette méthode ou alors en/la changer.
        """
        for lien in self.listeLien:
            if lien.tacheD.task.getDebut() > lien.tacheF.task.getDebut():
                lien.inverserLaDependances()

    def identify_region(self, x, y):
        """
        Renvoie la région à la position X et Y.
        X et Y sont relatifs à ce widget.

        La région doit être quelque chose qui doit permettre de
        savoir où ajouter une tâche si celle-ci n'a pas de début/période
        prédéfinie. (voir #addTask(tache, REGION = ...))

        Cela doit donc correspondre à un ensemble avec une date/heure
        de début, on utilisera pour cela la classe datetime.datetime().

        @param x: Position X relative à ce widget, sera bien souvent la position de la souris.
        @param y: Position Y relative à ce widget, sera bien souvent la position de la souris.
        @return datetime.datetime() indiquant la région trouvé aux coordonnées indiquées.
        @override indentify_region in AbstractDisplayedCalendar
        """
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
                heure = self.getTache(jour, self.getNbTacheJour(jour)-1).getSchedulable().getFin().time()
            except ValueError:
                heure = (datetime.datetime.combine(jour, self.getHeureDebut()) + \
                (datetime.datetime.combine(jour, self.getHeureFin  ())
                -datetime.datetime.combine(jour, self.getHeureDebut()) ) /2).time()
        else:
            try:
                heure = self.getTache(jour, y//AffichageGantt.TAILLE_LIGNE).getSchedulable().getFin().time()
            except ValueError:
                heure = (datetime.datetime.combine(jour, self.getHeureDebut()) + \
                (datetime.datetime.combine(jour, self.getHeureFin  ())
                -datetime.datetime.combine(jour, self.getHeureDebut()) ) /2).time()
        
        date = datetime.datetime.combine(jour, heure)
        return date

    def addTask(self, schedulable, region = None):
        """
        Permet d'ajouter une tâche OU AUTRE SCHEDULABLE, region correspond au début de la tâche si celle-ci n'en a pas.
        @deprecated: Va être renommé en addSchedulable().
        """
        if not (schedulable := super().addTask(schedulable, region)): # region est géré dans la variante parent : on ne s'en occupe plus ici. 
            return

        self.listeDisplayableItem.append(ObjetGantt(self, schedulable))

        self.updateAffichage()
        return schedulable

    def __afficherLesJours(self):
        """
        Permet d'afficher les noms des jours en haut de l'affichage, en fonction du début et de al fin de l'affichage.
        """
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
        """
        Permet d'afficher les tâches et autres schedulables et les liens.
        @deprecated: va être renommé en __afficherLesSchedulable() ou un truc du genre.
        """
        # Va changer :
#        self.listeTaskAffichees.sort(key=lambda t:t.task.getDebut()) # trie par début des tâches

        for displayable in self.listeDisplayableItem:
            displayable.redraw(self.can)

    def __afficherLesDependances(self):
        """
        Au final cette méthode n'affiche pas les dépendances...
        Elle ne gère que l'ordre des plans d'affichage.
        @deprecated: Va changer de nom.
        """

        # Ordre d'affichage
        self.can.tag_raise("top")
        self.can.tag_raise("topLine")
        self.can.tag_raise("topPlus")

from .ObjetGantt import *
