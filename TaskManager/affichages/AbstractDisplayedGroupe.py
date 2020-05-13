# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from AbstractDisplayedTask import *

class AbstractDisplayedGroupe(AbstractDisplayedTask):
    def __init__(self, master, groupe, **kwargs):
        super().__init__(master, **kwargs)
        # Note self.master est une référence vers AffichageCalendrier ou AffichageGantt, héritant de AbstractDisplayedCalendar

        self.groupe = groupe

    def getGroupe(self):
        """ Getter du groupe """
        return self.groupe
