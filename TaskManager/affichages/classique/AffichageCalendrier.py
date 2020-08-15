# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from ..AbstractDisplayedCalendar import *
from .ObjetClassique import *
from util.geom.Rectangle import *
from util.util import *
from util.widgets.TextWidget import *

class AffichageCalendrier(AbstractDisplayedCalendar):
    """
    Affichage de calendrier classique.
    Si deux objets sont en même temps, ils sont affichés dans des colonnes séparées.
    """
    def __init__(self, master = None, **kwargs):
        """
        Affichage par défaut du calendrier et de ses tâches.
        @param master: NoteBook du DonneeCalendrier, master du tkinter.Frame() que cet objet est.
        @param **kwargs: Options de configuration du tkinter.Frame() que cet objet est.
        """
        super().__init__(master)
        # Note : self.master est référence vers Notebook.
 
        self.__listeLabelHeure = []       # \
        self.__listeLabelJour = []        #  )-> Tout est dans le nom de ces trois listes.
        self.__listeSeparateurJour = []   # /
        
        # Vaudrait-il mieux pas utiliser la liste héritée self.listeTaskAffichees ?
        self.listeDisplayableItem = []  # Liste de la variante affichée de ces tâches.

        self.__frame = Frame(self, bg = self.getPalette()["background"])        # Frame dans lequel tout s'affiche.
        self.__frame.pack(expand = YES, fill = BOTH)

        # Mise à jour de l'affichage.
        self.updateAffichage()
        
        # Pour mémoriser les différentes parts pour savoir si elles sont le même jour qu'une autre.
        # Est-ce vraiment nécessaire au vu de l'attribut self.__partsParColonnes qui répartie les parts
        # selon leurs colonnes ET DONC leur jour ?
        self.__parts = []

        # Nombre de colonne par jour.
        # En effet, pour que le grid fasse en sorte que toutes les colonnes des jours soient de même taille,
        # il faut que toutes les colonnes de jours aient le même nombre de jours de grille chacunes.
        # C'est pour cela qu'il s'agit que d'une seule valeur. Elle est recalculée lors de chaque mise à jour
        # d'affichage via la méthode #updateAffichage()
        self.__nbColonneParJour = 1
        self.__partsParColonnes = []

        ## Binding
        #self.bind("<Delete>", lambda e = None : self.event_generate("<<delete-selected>>"))
        # self.bind("<Configure>", lambda e : self.updateAffichage())

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def __getNbColonnePourJour(self, jour):
        """
        Permet d'obtenir le nombre de colonne qu'il y a dans un jour donné.
        Note : la méthode __computePartsParColonnesDuJour appelée avec le même jour
        doit avoir été appelée auparavant pour travailler sur les dernières données.
        @param jour: datetime.date() correspondant au jour dont cherche le nombre de colonne d'items superposés.
        @return le nombre de colonne qu'il y a dans le jour demandé.
        """
        try:
            return max(1, len(self.__partsParColonnes[(jour - self.getJourDebut()).days]))
        except:
            return 1

    def __getNoColonnePourPart(self, part):
        """
        Permet de savoir la colonne sur laquelle une DatetimeItemPart() doit
        être positionnée par rapport à la colonne de son jour.
        @param part: le DatetimeItemPart() dont on veut savoir la position.
        @return le numéro de la colonne par rapport à sa colonne de son jour.
        """
        for jour in range(len(self.__partsParColonnes)):
            colonne = 0
            colPerColumn = self.__nbColonneParJour / max(1, len(self.__partsParColonnes[jour]))
            for st in self.__partsParColonnes[jour]:
                for p in st:
                    if p == part:
                        return colonne
                colonne +=colPerColumn
        return 0

    def getPartRectangle(self, part):
        """
        Permet d'obtenir le rectangle qui contient les informations
        de placement du AbstractItemContent lié à la DatetimeItemPart.
        Les coordonnées du rectangle sont comptées en coordonnées des
        cases dans la grille, et non en pixels. Une unité correspond à une case,
        si l'objet doit se mettre sur plusieurs cases, la largeur ou la hauteur du rectangle
        sera changé sur plus de 1. Dans tout les cas, faites attention à caster les coordonnées en int
        pour éviter les soucis lors du grid, car c'est bel et bien un grid qu'il faut faire ici.
        @param part: Le DatetimeItemPart dont on doit calculer la zone.
        @return le rectangle contenant les informations de placement du AbstractItemContent lié à la
        DatetimeItemPart demandé. Les informations sont données en cases de grid comme indiqué ci-dessus.
        """
        # Colonnes :
        colonnespan = self.__nbColonneParJour / self.__getNbColonnePourJour(part.getJour())
        colonne = 1 + ((part.getJour() - self.getJourDebut()).days)*(self.__nbColonneParJour+1) + self.__getNoColonnePourPart(part)

        # Note : à chaque fois le 1 + au début du calcul sert pour les lignes autant
        # que pour les colonnes à ignorer la première ligne ou la première colonne d'entête.
        # Lignes :
        temps0 = 1 + self.getHeureDebut().hour * 60 + self.getHeureDebut().minute
        temps1 = 1 + part.getHeureDebut().hour * 60 + part.getHeureDebut().minute
        temps2 = 1 + part.getHeureFin()  .hour * 60 + part.getHeureFin()  .minute

        ligne1 = 1 + temps1 - temps0
        ligne2 = 1 + temps2 - temps0

        # Création et renvoi du rectangle.
        rect = Rectangle(x1 = colonne, width = colonnespan, y1 = ligne1, y2 = ligne2)
        return rect

    def getPartsOfDay(self, day):
        """
        Permet d'obtenir toutes les DatetimeItemPart actuellement enregistrées via
        la méthode __precalculer() (qui ne prend en compte que les parts qui sont visibles)
        qui sont dans le jour demandé.
        @param day: Jour sur lequel on demande les parts.
        @return un générateur avec toutes les DatetimeItemPart qui sont le jour demandé.
        """
        return (part for part in self.__parts if part.getJour() == day)

    ""
    ######################
    # Méthodes liées aux #
    #    schedulables    #
    ######################
    ""
    def addSchedulable(self, schedulable):
        """
        Permet d'ajouter un objet planifiable à l'affichage dans le calendrier.
        @param schedulable: l'objet à rajouter pour l'affichage.
        @param region : correspond au début de l'objet planifiable si celle-ci n'en a pas.
        @return la tâche qui à peut-être été changé pour des raisons d'affichage.
        """
        self.listeDisplayableItem.append(ObjetClassique(self, schedulable))
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
        # On regarde si c'est trop à gauche (sur les heures):
        colonne, ligne = self.__frame.grid_location(x, y)
        colonne = (colonne-1)//2

        jour = self.getJourDebut() + datetime.timedelta(days = colonne)
        jour = datetime.datetime(jour.year, jour.month, jour.day)

        minute = self.getHeureDebut().hour*60 +(ligne - 1)
        heure, minute = minute//60, minute%60

        # TODO : A Changer :
        return jour + datetime.timedelta(hours = heure, minutes = minute)

    def removeSchedulable(self, obj):
        """
        Retire un schedulable de la liste
        @param obj : <schedulable> celui qu'il faut retirer
        """
        print("removing :", obj)
        for item in reversed(self.listeDisplayableItem):
            if isinstance(item, ObjetClassique):
                if item.getSchedulable() == obj:
                    self.listeDisplayableItem.remove(item)
                    print ("removed")

        self.updateAffichage(True)

    def resetSchedulable(self):
        """
        Permet de vider self.listeDisplayableItem
        """
        self.listeDisplayableItem = []

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def __adapteGrid(self):
        """
        Permet d'étirer les cases du grid, sauf la ligne d'entête des jours
        et la colonne d'entête des heures.

        Cette méthode se doit d'être appelée une fois que tout est dessiné,
        sinon ce qui serais rajouté après n'aurait pas forcément eu cet étirage des cases.
        """
        # à mettre À LA FIN ! ! ! (pour les expands)
        for column in range(self.getNbJour()*(self.__nbColonneParJour+1)):
            if column % (self.__nbColonneParJour+1) ==0:
                self.__frame.columnconfigure(column,weight=0)
            else:
                self.__frame.columnconfigure(column, weight=1)
        self.__frame.rowconfigure(ALL,weight=1)
        self.__frame.rowconfigure(0, weight=0)

    def __afficherLesHeures(self):
        """
        Permet de mettre à jour les labels des heures.
        """
        # On efface ceux déjà présent :
        self.__listeLabelHeure = []

        # et on les recrées :
        for heure in range(self.getHeureDebut().hour, self.getHeureFin().hour+1): # le +1 pour compter Début ET Fin.
            self.__listeLabelHeure.append(Label(self.__frame, text=heure, bd = 1, relief = SOLID, bg = self.getPalette()["highlightedWidget"]))
            # Note : Un détail à la minute près va être fait,
            # donc on compte 60 lignes pour une heure.
            # La ligne 0 étant la ligne des labels des jours,
            # On compte à partir de 1, c'est-à-dire en ajoutant 1.
            self.__listeLabelHeure[-1].grid(row=(heure-self.getHeureDebut().hour)*60+1, # le *60 pour faire un détail à la minute près
                                          column=0,      # Les labels des heures sont réservés à la colonne de gauche.
                                          rowspan=60,    # Mais ils prennent 60 minutes et lignes.
                                          sticky="NSWE") # Permet de centrer le label et d'en remplir les bords par la couleur du fond.

        #self.__adapteGrid()

    def __afficherLesJours(self):
        """
        Permet de mette à jour les labels des jours.
        """
        self.__listeLabelJour = []
        self.__listeSeparateurJour = []

        # Variable qui parcours la liste, rangeDate n'est pas fonctionnelle car après il y un soucis de last entre période et 2/5/... jours
        jour = self.getJourDebut()
        for compteur in range(self.getNbJour()):

            # Est-ce que le jour est sélectionné ?
            jourSelectionne = self.getDonneeCalendrier().isJourSelected(jour)

            #self.__listeLabelJour.append(Label(self.__frame, text=JOUR[jour.weekday()]+"\nfisefoijsoifjsoiejfiosef\njofijesoifjosiejfoi", bg = "#91C9F7" if jourSelectionne else "light grey", font = ("TkFixedFont")))
            self.__listeLabelJour.append(self._makeTextWidget(jour, master = self.__frame))
            #self.__listeLabelJour.append(TextWidget(self.__frame, text=JOUR[jour.weekday()] + "", nbJour = self.getNbJour()))
            self.__listeLabelJour[-1].bind("<Button-1>",        lambda e, jour=jour: self.selectJour(jour))
            self.__listeLabelJour[-1].bind("<Control-Button-1>",lambda e, jour=jour: self.selectJour(jour, control=True))
            self.__listeLabelJour[-1].grid(row=0, column=1 + ((jour-self.getJourDebut()).days)*(self.__nbColonneParJour+1), columnspan = self.__nbColonneParJour, sticky="NSWE")
            if jour < self.getJourFin():
                self.__listeSeparateurJour.append(Separator(self.__frame, orient=VERTICAL))
                self.__listeSeparateurJour[-1].grid(row=0, column=(self.__nbColonneParJour+1)*(1+(jour-self.getJourDebut()).days), rowspan = 60*(self.getHeureFin().hour+1-self.getHeureDebut().hour)+1, sticky="NS")


            jour += datetime.timedelta(days = 1)

        # Cela permet de réadapter les lignes et colonnes qui sont en expand pour le grid.
        self.__adapteGrid()

    def __afficherLesTaches(self):
        """
        Permet de mettre à jour l'affichage des tâches et autres objets planifiables.
        """
        for displayable in self.listeDisplayableItem:
            displayable.redraw(self.__frame)

    def __computePartsParColonnesDuJour(self, jour):
        """
        Permet de calculer les multi-colonne d'un jour donné.
        @param jour: datetime.date() correspondant au jour dont on calcule le multi-colonne des objets.
        @return une liste de set() correspondant chacuns à la répartition des DatetimeItemPart()s dans les différentes colonnes.
        Un set() est une colonne, et chaques éléments de ces set()s est un DatetimeItemPart
        """
        partsParColonnes = []
        for part in self.getPartsOfDay(jour):
            index = 0
            intersecting = True
            while intersecting:
                intersecting = False
                if len(partsParColonnes) <= index:
                    partsParColonnes.append(set())
                for p in partsParColonnes[index]:
                    if part.intersectWith(p):
                        index += 1
                        intersecting = True
                        break
            partsParColonnes[index].add(part)
        return partsParColonnes

    def __precalculer(self):
        """
        Permet de précalculer les Parts non fusionnées des tâches affichées dans ce calendrier.
        Permet aussi de calculer les multi-colonnes quand deux objets sont censés s'afficher en même temps.
        """
        for displayable in self.listeDisplayableItem:
            if isinstance(displayable, AbstractMultiFrameItem):
                self.__parts.extend(displayable.getRepartition())
        jour = self.getJourDebut()
        self.__nbColonneParJour = 1
        self.__partsParColonnes = []
        for compteur in range(self.getNbJour()):
            self.__partsParColonnes.append(self.__computePartsParColonnesDuJour(jour))
            self.__nbColonneParJour = ppcm(self.__nbColonneParJour, self.__getNbColonnePourJour(jour))
            jour += datetime.timedelta(days = 1)

    def updateAffichage(self, force = False):
        """
        Permet de mettre à jour l'affichage.
        @override #updateAffichage() in AbstractDisplayedCalendar
        """
        # On détruit et recrée le Frame
        self.__frame.destroy()
        self.__parts = []
        self.__frame = Frame(self, bg = self.getPalette()["background"])
        self.__frame.pack(expand = YES, fill = BOTH)
        self.__frame.bind("<Button-1>", lambda e: self.__onClicSurFrame(), add = True)

        # On précalcule :
        self.__precalculer()

        # On affiche les trucs
        self.__afficherLesHeures()
        self.__afficherLesJours()
        self.__afficherLesTaches()

    def updateColor(self):
        """
        Permet de mettre à jour la couleur de tout les IDisplayableItem()s.
        """
        for displayable in self.listeDisplayableItem:
            displayable.updateColor(self.__frame)

        # Ci-dessous, une petite customisation, qui permet de faire que les labels des jours soient en bleu quand le jour en question est sélecionné.

        # Variable qui parcours la liste, rangeDate n'est pas fonctionnelle car après il y un soucis de last entre période et 2/5/... jours
        jour = self.getJourDebut()
        for compteur in range(self.getNbJour()):
            # Est-ce que le jour est sélectionné ?
            jourSelectionne = "jour" if jour == datetime.date.today() else "highlightedWidget"
            jourSelectionne = "selected" if self.getDonneeCalendrier().isJourSelected(jour) else jourSelectionne

            self.__listeLabelJour[compteur].setColor(mode = jourSelectionne)

            # On incrémente le jour, car on a pas rangeDate, comme indiqué plus haut.
            jour += datetime.timedelta(days = 1)

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def __onClicSurFrame(self):
        self.deselectEverything()

    def clicSurObjet(self, objClassique):
        """
        Méthode exécutée lors d'un clic sur un objet.
        @param objClassique: l'objet sur lequel l'utilisateur à cliqué.
        """
        for s in self.getPeriodeActive().getInstanciatedSchedulables():
            s.setSelected(False)
        objClassique.getSchedulable().setSelected(True)
        self.getDonneeCalendrier().updateColor()
