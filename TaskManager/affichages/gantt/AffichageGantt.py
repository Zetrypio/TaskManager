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
from util.widgets.TextWidget import *
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

        # Ligne verte pour quand on est en train de relier plusieurs tâches ou autre : TODO : utiliser un dictionnaire
        self.__id_LinkingLine = None
        self.__x1_LinkingLine = None
        self.__y1_LinkingLine = None
        self.__mode_LinkingLine = None
        self.__activeGanttObject = None

        # La taille de la colonne dépend de la taille du Canvas :
        self.tailleColonne = 0

        # Dictionnaire des rectangles de sélection selon les jours :
        self.__rectangleSelection = {}
        
        # Pourcentage de la taille d'une colonne pour une tâche ou un groupe :
        # (l'autre partie sert pour afficher les liens).
        self.facteurW = 0.8
        
        # Canvas de l'affichage (et scrollbar) :
        self.can = Canvas(self, width=1, height=1, scrollregion = (0, 0, 1, 1), bg = self.getPalette()["background"])
        self.can.pack(fill=BOTH, expand=YES, side = LEFT)
        self.can.bind("<Configure>", lambda e:self.updateAffichage()) # Faire en sorte que la fenêtre se redessine si on redimensionne la fenêtre
        self.scrollbar = Scrollbar(self, command = self.can.yview) # Premier reliage de la scrollbar
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.can.config(yscrollcommand = self.scrollbar.set) # 2e reliage de la scrollbar

        # Bindings du Canvas :
        self._setBinding("Gantt", self.getApplication())

        # Pour savoir si un événement à été annulé.
        # Seul événement annulable : clic sur le canvas.
        self.__eventCanceled = False

        # Binding d'events virtuels : ?
        #self.can.bind("<Escape>", lambda e: self.can.event_generate("<<deselect-all>>")   , add=1)
        #self.can.bind("<Delete>", lambda e: self.can.event_generate("<<delete-selected>>"), add=1)
        #self.master.bind("<Delete>", print)#lambda e: self.can.event_generate("<<delete-selected>>"), add=1)
        #self.can.bind("<Delete>", print)#lambda e: self.can.event_generate("<<delete-selected>>"), add=1)

        # Définition des events virtuels :
        self.getApplication().bind_all("<<Affichage-Gantt-deselect-all>>",    self.deselectAll     , add=1)
        self.getApplication().bind_all("<<Affichage-Gantt-delete-selected>>", self.__deleteSelected, add=1)
        self.getApplication().bind_all("<<Affichage-Gantt-select-all>>",      self.selectAll, add=1)

        # Définition des bindings inchangeables (souris):
        self.can.bind("<Control-Button-1>", self.__onControlClicSurCanvas) # TODO : fusionner control avec l'autre ?
        self.can.bind("<Button-1>"        , self.__onClicSurCanvas)
        self.can.bind("<Motion>"          , self.__updateLinkingLine)

        # Infobulle toujours vraie :
        ajouterInfoBulleTagCanvas(self.can, "plus", "Ajouter un lien.")

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    #def __getBtnChangeJour(self):
        #return self.getParametreAffichage().getBoutonsChangementJours()

    #def __trouverItems(self, pos):
        #"""
        #Trouver les items à la position donnée
        #@param pos : objet avec un attribut x et un attribut y, correspondant à la position souhaitée.
        #"""
        #return self.can.find_overlapping(pos.x-1, pos.y-1, pos.x+1, pos.y+1)

    def __getLien(self, taskA, taskB):
        """
        Fonction qui dit si un objet dépendance link existe entre les 2 tasks
        @param taskA : <Task> Tache de départ du lien
        @param taskB : <Task> Tache d'arrivée du lien
        @return <bool> True  : le lien existe
                <bool> False : Le lien n'existe pas
        """
        for lien in self.listeDisplayableItem:
            if isinstance(lien, DependanceLink):
                # Est ce que ce lien va fais la liaison de notre schdulable
                if lien.getPartObjA() is taskA and lien.getPartObjB() is taskB:
                    return True
        else :
            return False

    def getNbLigneTotal(self):
        """
        Permet de savoir le nombre de ligne totale sur l'ensemble des jours affichés.
        Utile pour savoir jusqu'à où va le scrolling.
        @return le maximum de #getNbTacheJour() pour tout les jours qui sont actuellement visibles.
        """
        nbLigne = 1
        for jour in rangeDate(self.getJourDebut(), self.getJourFin()):
            nbLigne = max(nbLigne, self.getNbTacheJour(jour))
        return nbLigne

    def getNbTacheJour(self, jour):
        """
        Permet d'obtenir le nombre de de AbstractItemContent à mettre sur un jour donné.
        @param jour: le jour dont on veut savoir le nombre de parts.
        @return le nombre de part sur le jour donné.
        """
        return len(list(self.getPartsOfDay(jour)))

    def getParametreAffichage(self):
        """
        Getter de ParametreAffichage.
        @return ParametreAffichage.
        """
        return self.master.master.getParametreAffichage() # Skip le Notebook

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

    def getYScrolling(self):
        """
        Permet de savoir de combien le Canvas est scrollé.
        @return un int correspondant au nombre de pixels scrollées dans le canvas via la scrollbar.
        """
        return int(round(self.can.yview()[0]*int(self.can.cget("scrollregion").split(" ")[3])))-1

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def __afficherLesJours(self):
        """
        Permet d'afficher les noms des jours en haut de l'affichage, en fonction du début et de al fin de l'affichage.
        """
        # Largeur :
        if self.getNbJour() == 0:
            return
        self.tailleColonne = w = self.can.winfo_width()/self.getNbJour()

        # création de bandeau pour les jours
        #self.can.create_rectangle(0, 0, self.can.winfo_width(), AffichageGantt.TAILLE_BANDEAU_JOUR, fill="#BBBBBB", outline="")
        self.__textwidgets = []

        # Pour chaques jours :
        for jour in range(self.getNbJour()):
            # Position X :
            x = int(jour * w)

            # Est-ce que le jour est sélectionné ?
            leJour = self.getJourDebut()+datetime.timedelta(days=jour)
            jourSelectionne = self.getDonneeCalendrier().isJourSelected(leJour)

            self.__textwidgets.append(self._makeTextWidget(leJour, master = self.can))
            self.__textwidgets[-1].bind("<Button-1>", lambda e = None, leJour = leJour: self.__onSelectJour(leJour))
            self.__textwidgets[-1].bind("<Control-Button-1>", lambda e = None, leJour = leJour: self.__onSelectJour(leJour, crtl = True), add = 1)

            # Séparateurs :
            if jour !=0:
                self.can.create_line(x, 0, x, self.getScrollableHeight(), fill = self.getPalette()["foreground"])

            # Texte des jours :
            self.can.create_window(x, 0,
                                    width = w,
                                    window = self.__textwidgets[-1], tag = "bandeauJour",
                                    anchor = "nw")


        # Ajustement des TextWidgets
        self.update()
        AffichageGantt.TAILLE_BANDEAU_JOUR = max(t.winfo_height() for t in self.__textwidgets)#int(TextWidget.MINHEIGHT)
        #for tw, idTw in zip(self.__textwidgets, self.can.find_withtag("bandeauJour")):
            #tw.resize(height = TextWidget.MINHEIGHT) # La taille du widget
            #self.can.itemconfigure(idTw, height = TextWidget.MINHEIGHT) # La taille alloué au widget
        #self.can.move("bandeauJour", 0, AffichageGantt.TAILLE_BANDEAU_JOUR//2)
        #TextWidget.MINHEIGHT = 0

    def __afficherLesTaches(self, force = False):
        """
        Permet d'afficher les tâches et autres schedulables et les liens.
        @deprecated: TODO va être renommé en __afficherLesSchedulable() ou un truc du genre.
        """
        def getObjGantt(schedulable):
            """
            Fonction embarqué qui retourne l'objet Gantt en fonction de la task
            @param schedulable : <Task> celle a tester
            @return <objGantt> celui qui affiche la Task "schedulable"
                        None si celui-ci n'a pas été trouvé
            """
            for s in self.listeDisplayableItem:
                if isinstance(s, ObjetGantt) and isinstance(s.getSchedulable(), Task) and s.getSchedulable() is schedulable:
                    return s
            else :
                return None

        if force is True:
            self.listeDisplayableItem = [i for i in self.listeDisplayableItem if isinstance(i, ObjetGantt)] # efface les liens de la liste.

        for displayable in self.listeDisplayableItem:
            displayable.redraw(self.can, force)
            # Si le displayable est un schedulable de gantt :
            if isinstance(displayable, ObjetGantt):

                # Si le schedulable a une dépendance
                schedulable = displayable.getSchedulable()
                if schedulable.acceptLink() and schedulable.getDependantes():

                    # Recherche des liens
                    for dep in schedulable.getDependantes():
                        if not self.__getLien(schedulable, dep):

                            # Si la dep n'est pas encore dans la liste des listeDisplayableItem, on attends
                            objGanttDep = getObjGantt(dep)
                            if objGanttDep is not None:
                                self.createLink(displayable, objGanttDep)

    def __endLinkingLine(self):
        try:
            self.can.delete(self.__id_LinkingLine)
        except:
            pass
        self.__id_LinkingLine = None
        self.__x1_LinkingLine = None
        self.__y1_LinkingLine = None
        self.__mode_LinkingLine = None
        self.__activeGanttObject = None

    def __highlightLinks(self, mode):
        for l in self.listeDisplayableItem:
            if isinstance(l, DependanceLink):
                if mode == "+" and (self.__activeGanttObject.getSchedulable() is l.getPartA().getSchedulable()
                                 or self.__activeGanttObject.getSchedulable() is l.getPartB().getSchedulable()):
                    l.highlight(self.getPalette()["addLink"])
                elif mode == "-" and (self.__activeGanttObject.getSchedulable() is l.getPartA().getSchedulable()
                                   or self.__activeGanttObject.getSchedulable() is l.getPartB().getSchedulable()):
                    l.highlight(self.getPalette()["deleteLink"])
                else:
                    l.highlight(None)
        self.updateColor()
        self.__ordonnerAffichage()

    def __ordonnerAffichage(self):
        """
        Cette méthode gère l'ordre des plans d'affichage.
        """
        # Ordre d'affichage
        self.can.tag_raise("line")
        self.can.tag_raise("highlight")
        self.can.tag_raise("plus")

    def __onClicSurCanvas(self, pos=None):
        """
        Méthode exécutée quand on appuie sur échappe ou qu'on appuie
        dans le vide pour annuler le lien de la ligne verte. Sinon pour désélectionner les tâches.
        @param pos: Event avec la position de la souris par rapport au Canvas().
        """
        if not self.__eventCanceled:
            if self.__activeGanttObject is not None:
                self.__endLinkingLine()

            # Avec les TextWidget, on ne clique plus sur le canvas, donc ne sert à rien
            #elif pos is not None and pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
                #self.selectJour(self.getJourDebut()+datetime.timedelta(days=pos.x/self.tailleColonne))
            else:
                self.deselectEverything()
        self.__highlightLinks(None)
        self.__eventCanceled = False
        self.can.focus_set()

    def __onControlClicSurCanvas(self, pos=None):
        """
        Méthode exécutée quand on appuie sur Control-Clic.
        @param pos: Event avec la position de la souris par rapport au Canvas().
        """
        #if not self.__eventCanceled:
            # Avec les TextWidget, on ne clique plus sur le canvas, donc ne sert à rien
            #if pos is not None and pos.y <= AffichageGantt.TAILLE_BANDEAU_JOUR:
                #self.selectJour(self.getJourDebut()+datetime.timedelta(days=pos.x/self.tailleColonne), control=True)
        self.__eventCanceled = False
        self.can.focus_set()

    def __onSelectJour(self, jour, crtl = False):
        """
        Méthode qui permet de sélectionner un jour
        (elle est là, car il y a besoin d'un self.updateAffichage())
        @param jour : <datetime.date> correspond au jour sélectionné
        @param crtl : <bool> la touche "control" est appuyé ?
        """
        self.selectJour(jour, crtl)
        self.updateAffichage()

    def __precalculer(self):
        """
        Permet de précalculer les Parts non fusionnées
        des tâches affichées dans ce calendrier.
        """
        self.__parts = []
        for displayable in self.listeDisplayableItem:
            if isinstance(displayable, AbstractMultiFrameItem):
                self.__parts.extend(self.getVisiblePart(part) for part in displayable.getRepartition() if self.getVisiblePart(part))
        self.__parts.sort(key=lambda e:e.getDebut())

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
        self.__mode_LinkingLine = mode
        self.__id_LinkingLine = self.can.create_line(self.__x1_LinkingLine,
                                                     self.__y1_LinkingLine,
                                                     self.__x1_LinkingLine,
                                                     self.__y1_LinkingLine,
                                                     fill="#00CF00" if mode == "+" else "#CF0000",
                                                     width = 2)

    def cancelEvent(self):
        self.__eventCanceled = True

    def updateAffichage(self, force = False):
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
            self.__afficherLesTaches(force)
            self.__ordonnerAffichage()

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

        # Mise à jour des rectangles qui font la couleur de sélection des labels des jours.
        for jour in self.__rectangleSelection:
            # Est-ce que le jour est sélectionné ?
            jourSelectionne = self.getDonneeCalendrier().isJourSelected(jour)
            self.can.itemconfig(self.__rectangleSelection[jour], fill="#91C9F7" if jourSelectionne else "light grey")

    ""
    ######################
    # Méthodes liées aux #
    #    schedulables    #
    ######################
    ""
    def addSchedulable(self, schedulable):
        """
        Permet d'ajouter une tâche OU AUTRE SCHEDULABLE, region correspond au début de la tâche si celle-ci n'en a pas.
        """
        self.listeDisplayableItem.append(ObjetGantt(self, schedulable))
        #self.updateAffichage()

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
        nbTacheJour = self.getNbTacheJour(jour)

        # Heures :
        y = pos.y - AffichageGantt.TAILLE_BANDEAU_JOUR
        ligne = min(y//AffichageGantt.TAILLE_LIGNE, nbTacheJour-1)
        heure = self.getHeureDebut()
        if y > 0 and ligne >= 0:
            try:
                heure = list(self.getPartsOfDay(jour))[ligne].getSchedulable().getFin().time()
            except ValueError:
                heure = self.getHeureDebut()

        date = datetime.datetime.combine(jour, heure)
        return date

    def removeSchedulable(self, obj):
        """
        Retire un schedulable de la liste
        @param obj : <schedulable> celui qu'il faut retirer
        """
        for item in reversed(self.listeDisplayableItem):
            if isinstance(item, ObjetGantt):
                if item.getSchedulable() == obj:
                    self.listeDisplayableItem.remove(item)
            elif isinstance(item, AbstractLink):
                if item.getPartA().getSchedulable() == obj or item.getPartB().getSchedulable() == obj:
                    if isinstance(item, DependanceLink):
                        item.getPartB().getSchedulable().removeDependance(item.getPartA().getSchedulable())
                    self.listeDisplayableItem.remove(item)
            elif isinstance(item, ItemButtonPlus):
                if item.getSchedulable() == obj:
                    self.listeDisplayableItem.remove(item)

        self.updateAffichage(True)

    def resetSchedulable(self):
        """
        Permet de vider self._list
        """
        self.listeDisplayableItem = []

    ""
    #################################
    # Méthodes liées aux bindings : #
    #################################
    ""
    def __deleteSelected(self, event):
        """
        Permet de supprimer les objets qui sont actuellements sélectionnés.
        @param event : <event> set à chercher la provenance de l'event
        """
        # Si c'est bien sur le ce calendrier que l'on est
        if self.hasParent(self, event.widget):
            for item in reversed(self.listeDisplayableItem):
                if isinstance(item, AbstractLink):
                    if item.isSelected():
                        item.delete()
                        self.listeDisplayableItem.remove(item)
                elif isinstance(item, ObjetGantt):
                    obj = item.getSchedulable()
                    if obj.isSelected():
                        obj.delete()
                        self.listeDisplayableItem.remove(item)

            self.updateAffichage()

    def deselectAll(self, event):
        """
        Désélectionne tout ce qui est actuellement sélectionné
        @param event : <event> sert à chercher la provenance de l'event
        """
        if self.hasParent(self, event.widget):
            self.deselectEverything()

    def selectAll(self, event):
        """
        Sélectionne tous les schedulables mais pas les jours
        @param event : <event> sert à chercher la provenance de l'event
        """
        if self.hasParent(self, event.widget):
            for item in self.listeDisplayableItem:
                if isinstance(item, AbstractLink):
                    item.setSelected(True)
                elif isinstance(item, ObjetGantt):
                    item.getSchedulable().setSelected(True, andInside=True)
            self.getDonneeCalendrier().updateColor()

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def clicSurObjet(self, objGantt, schedulableDisp=None, control=False):
        """
        Méthode à exécuter quand on clic sur l'un des objets de gantt.
        Peut créer un lien si on était en mode d'ajout de liens etc.
        @param objGantt: l'objet sur lequel on a cliqué.
        @param schedulable: l'objet planifiable cliqué si il y en a un.
        @param control: True si la touche control (command sur mac) a été
        activé lors de ce clic, False sinon.
        @override clicSurObjet(objet) in AbstractDisplayedCalendar()
        """
        # Si on est en mode ajout ou suppression de lien :
        if objGantt is not self.__activeGanttObject and self.__activeGanttObject is not None and objGantt is not None:
            # Pour le mode d'ajout :
            if self.__mode_LinkingLine == "+":
                # Si le lien est accepté :
                if objGantt.getSchedulable().acceptLinkTo(self.__activeGanttObject.getSchedulable()):
                    # On inverse le lien si il est à l'envers.
                    if objGantt.getSchedulable().getDebut() < self.__activeGanttObject.getSchedulable().getDebut():
                        self.__activeGanttObject, objGantt = objGantt, self.__activeGanttObject

                    # A faire car on perd activeGanttObject dans createLink
                    # De plus l'ajout de dépendance dois se faire après sinon on raise RunTimeError
                    objA, objB = objGantt, self.__activeGanttObject

                    ## Check si le lien existe déjà
                    if self.__getLien(objB.getSchedulable(), objA.getSchedulable()):
                       raise RuntimeError("Lien déjà existant.") # On garde l'erreur ?

                    # On crée le lien et met donc à jour l'affichage.
                    self.createLink(objB, objA)

                    # Création de la dépendance :
                    objA.getSchedulable().addDependance(objB.getSchedulable())
                    self.getApplication().getTaskEditor().redessiner()
                    self.updateAffichage()

            # Pour le mode de suppression de liens :
            elif self.__mode_LinkingLine == "-":
                # Si les liens sont normalement possibles :
                if self.__activeGanttObject.getSchedulable().acceptLinkTo(objGantt.getSchedulable()):
                    print("Suppression du lien entre %s et %s"%(self.__activeGanttObject.getSchedulable(), objGantt.getSchedulable()))

                    # Il faut trouver le lien :
                    for lien in reversed(self.listeDisplayableItem):
                        if isinstance(lien, DependanceLink):
                            if (lien.getPartA().getSchedulable() in (self.__activeGanttObject.getSchedulable(), objGantt.getSchedulable())
                            and lien.getPartB().getSchedulable() in (self.__activeGanttObject.getSchedulable(), objGantt.getSchedulable())):
                                self.listeDisplayableItem.remove(lien)
                                break

                    # Si le la dépendance existe dans un premier sens :
                    if self.__activeGanttObject.getSchedulable() in objGantt.getSchedulable().getDependances():
                        objGantt.getSchedulable().removeDependance(self.__activeGanttObject.getSchedulable())
                    # Dans l'autre sens :
                    elif self.__activeGanttObject.getSchedulable() in objGantt.getSchedulable().getDependantes():
                        self.__activeGanttObject.getSchedulable().removeDependance(objGantt.getSchedulable())

                    # On met à jour l'affichage :
                    self.__highlightLinks(None)
                    self.__endLinkingLine()
                    self.updateAffichage()

        # Les liens ne se font pas ici, ils sont indépendants chez eux même. Est-ce bien ? pour le moment ça va ok.
        # Sinon on désélectionne tout les liens et les tâches,
        # pour ne sélectionner que la tâche sur laquelle on a cliqué.
        elif self.__activeGanttObject is None:
            if control is False:
                self.deselectEverything()
            schedulableDisp.onClic(control)

            self.getDonneeCalendrier().updateColor()

    def createLink(self, objA, objB):
        """
        Méthode qui crée un dependanceLink et le rajoute à la liste
        @param objA : <ObjetGantt> départ  de la flèche
        @param objB : <ObjetGantt> arrivée de la flèche
        Sens de la flèche : objA --> objB
        """
        partA = self.getVisiblePart(objA.getLastPart())
        partB = self.getVisiblePart(objB.getFirstPart())
        if None in (partA, partB):
            print("Cannot create link between %s and %s because one part is not visible."%(objA, objB))
        else:
            self.listeDisplayableItem.append(
                DependanceLink(
                    self,
                    partA,
                    partB))
        self.__highlightLinks(None)
        self.__endLinkingLine()


    def deselectEverything(self):
        super().deselectEverything()
        for item in self.listeDisplayableItem:
            if isinstance(item, DependanceLink):
                item.setSelected(False)

        #self.updateAffichage()
        self.updateColor()

    def onIntervertir(self):
        """
        Méthode appelée lorsqu'on interverti 2 jours.
        S'occupe de rétablir les liens dans le bon sens.
        @deprecated: TODO : Il faut revoir cette méthode ou alors en/la changer.
        """
        for lien in self.listeDisplayableItem:
            if isinstance(lien, DependanceLink) and lien.getPartA().getSchedulable().getDebut() > lien.getPartB().getSchedulable().getDebut():
                lien.inverserLaDependances()

from .ObjetGantt import *
