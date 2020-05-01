# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

class MenuBar(Menu):
    """Classe de la barre de menu"""
    def __init__(self, root, master):
        """root est la fen�tre, master est l'Application."""
        Menu.__init__(self, master)
        root.configure(menu = self)
        # Menus Principaux :
        self.menuFichier = Menu(self, tearoff=0)
        self.menuEdition = Menu(self, tearoff=0)
        self.menuAffichage = Menu(self, tearoff=0)
        
        self.add_cascade(label = "Fichier", menu=self.menuFichier)
        self.add_cascade(label = "Edition", menu=self.menuEdition)
        self.add_cascade(label = "Affichage", menu=self.menuAffichage)

        # Menu Fichier :
        self.menuFichier.add_command(label = "Nouveau", accelerator="Ctrl-N", command = master.nouveau)
        self.menuFichier.add_command(label = "Ouvrir", accelerator="Ctrl-O", command = master.nouveau)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Enregistrer", accelerator="Ctrl-S", command = master.nouveau)
        self.menuFichier.add_command(label = "Enregistrer sous", accelerator="Ctrl-Maj-S", command = master.nouveau)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Quitter", accelerator="Ctrl-Q", command = master.nouveau)

        # Menu Affichage/Style Horloge :
        self.variableHorlogeStyle = StringVar(value="nombre")
        self.menuHorlogeStyle = Menu(self.menuAffichage, tearoff=0)
        self.menuHorlogeStyle.add_radiobutton(label = "Normal", command = master.nouveau, variable=self.variableHorlogeStyle, value = "normal")
        self.menuHorlogeStyle.add_radiobutton(label = "Nombre", command = master.nouveau, variable=self.variableHorlogeStyle, value = "nombre")

        # Menu Affichage :
        self.menuAffichage.add_cascade(label = "Style d'horloge", menu = self.menuHorlogeStyle)

