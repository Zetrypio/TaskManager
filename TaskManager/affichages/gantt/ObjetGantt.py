# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

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
        self.__rmenu = []

        # Permet d'avoir l'info de Où commence la ligne verte quand il y a plusieurs plus.
        self.__activePlus = None

    def __del__(self):
        """
        Destructeur de cet objet : S'assure que tout les cadres disparaissent avec...
        """
        for p in self.__parts:
            p[1].destroy()
        self.__parts = []

    def redraw(self, canvas):
        """
        Permet de mettre à jour l'affichage de l'objet.
        @param canvas: le Canvas sur lequel dessiner l'objet (et son plus etc.)
        """
        # On se supprime :
        self.delete()
        for rmenu in self.__rmenu:
            rmenu.destroy()
        self.__rmenu = []

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
                    widget.bindTo("<Button-1>", lambda e: self.__onSelect())
                    widget.bindTo("<Control-Button-1>", lambda e: self.__onMultiSelect())

                    # Si cette part à besoin d'un plus :
                    if widget.needButtonPlus(self.master):
                        # On crée le plus qui correspond à cet objet.
                        plus = ItemButtonPlus(self, part)

                        # On mémorise tout cet ensemble.
                        self.__parts.append((part, f, widget, plus))
                    else:
                        # Sinon pas de plus
                        self.__parts.append((part, f, widget))

                # On récupère et met à jour la position :
                f = self.__getFrameForPart(part)
                rect = self.master.getPartRectangle(part)
                x = rect.getX1()+1
                y = rect.getY1()+1
                width = rect.getWidth() * self.master.facteurW
                height = rect.getHeight() - 4
                canvas.create_window(x, y, width=width, height=height, window = f, anchor="nw")

        # Suppression des parties qui ne sont plus visibles :
        for p in reversed(self.__parts):
            if not self.getVisiblePart(p[0]):
                p[1].destroy()
                self.__parts.remove(p)
            else:
                if self._schedulable:
                    # Ajout du RMenu :
                    rmenu = RMenu(p[1], True, p[2])
                    if self._schedulable.acceptLink():
                        rmenu.add_command(label = "Créer un lien")
                        if len(self._schedulable.getDependances()) or len(self._schedulable.getDependantes()):
                            rmenu.add_command(label = "Supprimer un lien")
                        rmenu.add_separator()
                    rmenu.add_command(label = "Supprimer %s"%self._schedulable)
                    self.__rmenu.append(rmenu)
                if len(p) > 3:
                    # Mise à jour de la présence du bouton Plus (+) :
                    if p[2].needButtonPlus(self.master):
                        p[3].redraw(canvas)
        
        self.__liens = []
        self.__parts.sort(key=lambda p:p[0].getDebut())
        for i in range(len(self.__parts)-1):
            self.__liens.append(MultiFrameItemInnerLink(self.master, self.__parts[i][0], self.__parts[i+1][0]))
        for l in self.__liens:
            l.redraw(canvas)

    def beginLigneVerte(self, plus):
        """
        Permet de commencer la ligne verte,
        et mémorise sur quel plus (+) on a cliqué.
        @param plus: le plus sur lequel on a cliqué.
        """
        self.__activePlus = plus
        self.master.beginLigneVerte(self)

    def __onSelect(self):
        """
        Permet d'informer à l'affichage gantt que l'on a appuyé sur cet objet.
        Utile pour la création des liens par exemple, ou la sélection des tâches etc.
        """
        self.master.clicSurObjet(self)

    def __onMultiSelect(self):
        """
        Permet d'inverser l'état de sélection de l'objet schedulable.
        """
        self._schedulable.inverseSelection()
        self.master.getDonneeCalendrier().updateColor()

    def updateColor(self, canvas):
        for p in self.__parts:
            p[2].updateColor()
        for l in self.__liens:
            l.updateColor(canvas)

    def getXPlus(self):
        """
        Permet d'obtenir la coordonnée X du centre du plus actif.
        @return le milieu en X du plus actif.
        """
        return self.__activePlus.getX()

    def getYPlus(self):
        """
        Permet d'obtenir la coordonnée Y du centre du plus actif.
        @return le milieu en Y du plus actif.
        """
        return self.__activePlus.getY()

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

    def __getFrameForPart(self, part):
        """
        Permet d'obtenir le tkinter.Frame() qui contient le AbstractItemContent qui correspond à la DatetimeItemPart() demandé.
        @param part: la DatetimeItemPart() dont on veut trouver le tkinter.Frame()
        @return le tkinter.Frame() trouvé, ou None dans le cas échéant.
        """
        for p in self.__parts:
            if p[0] == part:
                return p[1]

    def delete(self):
        """
        Permet de se supprimer lol ça fait rien car il suffit que cet objet soit delete
        et que le canvas fasse un delete(ALL) ce qui se fait à chaque update d'affichage.
        """
        pass
