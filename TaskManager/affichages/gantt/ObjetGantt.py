# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.geom.Point import *
from util.widgets.RMenu import *

from ..items.AbstractMultiFrameItem import *
from .AffichageGantt import *
from .ItemButtonPlus import *
from .liens.MultiFrameItemInnerLink import *

class ObjetGantt(AbstractMultiFrameItem):
    """
    Classe représentant un contenu dans
    l'affichage calendrier classique.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur d'un objet classique.
        @param master: AffichageGantt.
        @param schedulable: objet dont on fait l'affichage.
        """
        super().__init__(master, schedulable)

        # Liste des différentes DatetimeItemPart(), Frame(), AbstractItemContent(), et ItemBoutonPlus().
        self.__parts = []
        self.__liens = []

        # Permet d'avoir l'info de Où commence la ligne verte.
        self.__debutLinkingLine = Point()

    def __del__(self):
        """
        Destructeur de cet objet : S'assure que tout les cadres disparaissent avec...
        """
        for p in self.__parts:
            try:
                p[1].destroy()
            except:
                pass
        self.__parts = []

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def __getFrameForPart(self, part):
        """
        Permet d'obtenir le tkinter.Frame() qui contient le AbstractItemContent() qui correspond à la DatetimeItemPart() demandé.
        @param part: la DatetimeItemPart() dont on veut trouver le tkinter.Frame()
        @return le tkinter.Frame() trouvé, ou None dans le cas échéant.
        """
        for p in self.__parts:
            if p[0] == part:
                return p[1]

    def __getPlusForPart(self, part):
        """
        Permet d'obtenir le ItemButtonPlus() qui correspond à la DatetimeItemPart() demandé, si il existe.
        @param part: la DatetimeItemPart() dont on veut trouver le tkinter.Frame()
        @return le ItemButtonPlus() trouvé, ou None dans le cas échéant.
        """
        for p in self.__parts:
            if p[0] == part:
                return p[4] if len(p) > 4 else None # On stop la boucle dans tout les cas car de toutes façon ca veut dire qu'on le trouvera pas.

    def __getRMenuForPart(self, part):
        """
        Permet d'obtenir le RMenu() qui correspond à la DatetimeItemPart() demandé.
        @param part: la DatetimeItemPart() dont on veut trouver le tkinter.Frame()
        @return le RMenu() trouvé, ou None dans le cas échéant.
        """
        for p in self.__parts:
            if p[0] == part:
                return p[3]

    def __getWidgetForPart(self, part):
        """
        Permet d'obtenir le AbstractItemContent() qui correspond à la DatetimeItemPart() demandé.
        @param part: la DatetimeItemPart() dont on veut trouver le tkinter.Frame()
        @return le AbstractItemContent() trouvé, ou None dans le cas échéant.
        """
        for p in self.__parts:
            if p[0] == part:
                return p[2]

    def getXDebutLinkingLine(self):
        """
        Permet d'obtenir la coordonnée X du centre du plus actif.
        @return le milieu en X du plus actif.
        """
        return self.__debutLinkingLine.x

    def getYDebutLinkingLine(self):
        """
        Permet d'obtenir la coordonnée Y du centre du plus actif.
        @return le milieu en Y du plus actif.
        """
        return self.__debutLinkingLine.y

    def __isPartPresent(self, part):
        """
        Permet de savoir si la part est déjà parmi la liste de celles qui sont dessinées
        (pour ne pas avoir à la redessiner, mais juste la mettre à jour - et aussi pour
        ne pas en avoir 500000000 de part si jamais on oublie d'effacer les précédentes =) ).
        @param part: la DatetimeItemPart() dont on veut savoir sa présence.
        @return True si la part est présente, False sinon.
        """
        for p in self.__parts:
            if p[0] == part:
                return True
        return False

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def beginLinkingLine(self, point, mode = "+"):
        """
        Permet de commencer la ligne verte,
        et mémorise sur quel plus (+) on a cliqué.
        @param plus: le plus sur lequel on a cliqué.
        """
        self.__debutLinkingLine = point
        self.master.beginLinkingLine(self, mode)

    def redraw(self, canvas, force = False):
        """
        Permet de mettre à jour l'affichage de l'objet.
        @param canvas: le Canvas sur lequel dessiner l'objet (et son plus etc.)
        """
        # On se supprime :
        self.delete()

        # Si on force le redessinement tout entier :
        if force:
            self.__parts = []

        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                if not self.__isPartPresent(part): # Si on a pas déjà créé ce cadre exact :
                    # On fait dans tout les cas un frame pour ne pas prendre de risque de positionnement :
                    f = Frame(canvas, bg=self._schedulable.getColor())

                    # Ce "widget" est une instance d'une sous-classe de AbstractItemContent :
                    widget = self._schedulable.createDisplayableInstance(f, part)
                    widget.pack(expand = YES, fill = BOTH)
                    # C'est pour ça que l'on fait cette méthode-ci pour le bind.
                    # Cela permet de s'assurer que tout les sous-widgets seront binds aussi :
                    widget.bindTo("<Button-1>",         lambda obj: self.master.clicSurObjet(self, obj, control=False))
                    widget.bindTo("<Control-Button-1>", lambda obj: self.master.clicSurObjet(self, obj, control=True))

                    # Ajout du RMenu :
                    rmenu = RMenu(widget, False)

                    # Si cette part à besoin d'un plus :
                    if widget.needButtonPlus(self.master):
                        # On crée le plus qui correspond à cet objet.
                        plus = ItemButtonPlus(self, part)

                        # On mémorise tout cet ensemble.
                        self.__parts.append((part, f, widget, rmenu, plus))
                    else:
                        # Sinon pas de plus
                        self.__parts.append((part, f, widget, rmenu))

                # On récupère les informations si jamais on était pas en mode de création
                # au quel cas les variables juste au-dessus n'existent pas...
                f      = self.__getFrameForPart(part)
                widget = self.__getWidgetForPart(part)
                rmenu  = self.__getRMenuForPart(part)
                plus   = self.__getPlusForPart(part)
                
                # Ainsi que quelques informations supplémentaire, pour pouvoir positionner correctement le cadre de l'objet.
                rect = self.master.getPartRectangle(part)
                x = rect.getX1()+1
                y = rect.getY1()+1
                width = rect.getWidth() * self.master.facteurW
                height = rect.getHeight() - 4

                # Positionnement de l'objet dans le canvas :
                canvas.create_window(x, y, width=width, height=height, window = f, anchor="nw")

                # Pour le RMenu : on commence par supprimer tout.
                try:
                    rmenu.delete(0, rmenu.index(END))

                    # Puis on ajoute :
                    # Si il est en capacité d'ajouter un lien :
                    if self._schedulable.acceptLink():
                        rmenu.add_command(label = "Créer un lien", command = lambda : self.beginLinkingLine(rect.getCenterPoint()))
    
                        # Si il est en capacité de supprimer un lien :
                        if len(self._schedulable.getDependances()) or len(self._schedulable.getDependantes()):
                            rmenu.add_command(label = "Supprimer un lien", command = lambda : self.beginLinkingLine(rect.getCenterPoint(), mode = "-"))

                        rmenu.add_separator()
                    self.getSchedulable().setRMenuContent(self.getSchedulable().getApplication().getTaskEditor(), rmenu)
                except:
                    pass

                # Mise à jour de la présence du bouton Plus (+) :
                if plus is not None:
                    if widget.needButtonPlus(self.master):
                        plus.redraw(canvas)

        # Suppression des parties qui ne sont plus visibles :
        for p in reversed(self.__parts):
            if not self.getVisiblePart(p[0]):
                p[1].destroy()
                self.__parts.remove(p)

        # Mise à jour des liens d'intra-multi-Frame-Item.
        self.__liens = []
        self.__parts.sort(key=lambda p:p[0].getDebut())
        for i in range(len(self.__parts)-1):
            l = MultiFrameItemInnerLink(self.master, self.__parts[i][0], self.__parts[i+1][0])
            l.redraw(canvas)
            self.__liens.append(l)

    def updateColor(self, canvas):
        for p in self.__parts:
            p[2].updateColor()
        for l in self.__liens:
            l.updateColor(canvas)

    ""
    #####################
    # Autres Méthodes : #
    #####################
    ""

    def delete(self):
        """
        Permet de se supprimer lol ça fait rien car il suffit que cet objet soit delete
        et que le canvas fasse un delete(ALL) ce qui se fait à chaque update d'affichage.
        """
        pass
