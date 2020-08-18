# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.ColorButton import *
from ...AbstractSchedulableParametre import *



class GroupeParametre(AbstractSchedulableParametre):
    """
    Notebook qui contient tous les paramètres du groupe
    fournis dans le constructeur.
    Permet aussi de changer ses attributs (au groupe)
    """
    def __init__(self, master, groupe, **kw):
        """
        @param master : <tkinter.frame>
        @param groupe   : <Groupe> ceux qui sont à afficher
        """
        super().__init__(master, groupe, **kw)
