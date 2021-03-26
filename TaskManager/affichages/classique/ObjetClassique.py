# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.RMenu import *
from schedulable.task.Task import *
from schedulable.task.dialog.askEditTask import askEditTask
from schedulable.groupe.Groupe import *
from schedulable.groupe.dialog.askEditGroupe import askEditGroupe

from ..items.AbstractMultiFrameItem import *

class ObjetClassique(AbstractMultiFrameItem):
    """
    Classe représentant un contenu dans
    l'affichage calendrier classique.
    """
    def __init__(self, master, schedulable):
        """
        Constructeur d'un objet classique.
        @param master: AffichageClassique.
        @param schedulable: Objet à afficher.
        """
        super().__init__(master, schedulable)
        self.__listeCadre = []
        self.__widget = []
        self.__rmenu = {}

    def delete(self):
        for f in self.__listeCadre:
            try:
                f.destroy()
            except:
                pass
        self.__listeCadre = []
        self.__widget = []
        for widget in self.__rmenu:
            try:
                self.__rmenu[widget].destroy()
            except:
                pass
        self.__rmenu = {}

    def redraw(self, frame):
        # On se supprime :
        self.delete()
        
        # Et on se redessine :
        for part in self.getRepartition():
            # Si la partie est visible :
            if part := self.getVisiblePart(part):
                # On crée le cadre
                f = Frame(frame, bg=self._schedulable.getColor())

                # Ce "widget" est une instance d'une sous-classe de AbstractItemContent :
                widget = self._schedulable.createDisplayableInstance(f, part)
                widget.pack(expand = YES, fill = BOTH)
                # C'est pour ça que l'on fait cette méthode-ci pour le bind.
                # Cela permet de s'assurer que tout les sous-widgets seront binds aussi,
                # ainsi que de récupérer l'objet réellement cliqué, par exemple une sous-tâche d'un groupe :
                widget.bindTo("<Button-1>",         lambda obj: self.master.clicSurObjet(self, obj, control=False))
                widget.bindTo("<Control-Button-1>", lambda obj: self.master.clicSurObjet(self, obj, control=True))

                # RMenu :
                rmenu = RMenu(widget, False)
                self.getSchedulable().setRMenuContent(self.getSchedulable().getApplication().getTaskEditor(), rmenu)

                # On le place :
                rect = self.master.getPartRectangle(part)
                ligne       = int(rect.getY1())
                lignespan   = int(rect.getHeight())
                colonne     = int(rect.getX1())
                colonnespan = int(rect.getWidth())

                f.grid(row=ligne, rowspan=lignespan, column=colonne, columnspan=colonnespan, sticky=NSEW)

                # On le mémorise :
                self.__listeCadre.append(f)
                self.__widget.append(widget)
                self.__rmenu[widget] = rmenu

    def updateColor(self, frame):
        for w in self.__widget:
            w.updateColor()
