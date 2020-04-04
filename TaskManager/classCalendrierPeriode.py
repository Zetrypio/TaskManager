# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
import time
from superclassCalendrier import *
from periode import *


class AffichageCalendrierPeriode(SuperCalendrier):
    """Classe permettant la vision des périodes dans un mois."""
    def __init__(self, master = None, **kwargs):
        super().__init__(master, **kwargs)
        self.annee = time.localtime().tm_year
        self.mois = time.localtime().tm_mon
    def updateAffichage(self):
        pass


if __name__=='__main__':
    import Application
    Application.main()