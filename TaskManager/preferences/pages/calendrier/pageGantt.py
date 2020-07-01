# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from ..AbstractPage import *

class PageGantt(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
        super().__init__(master,nom = "Gantt", iid_parent ="-Calendrier", **kwargs)


        self.btn = Button(self._mFrame, text="clickme")
        self.btn.grid(column = 0, row = 2, sticky = "NSEW")

    def appliqueEffet(self, application):
        pass
        #self._makeDictAndSave(self.getParent()[1:]) Quand il y aura des choses ici
