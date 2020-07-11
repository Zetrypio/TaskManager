# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from preferences.fenetre import *

class MenuBar(Menu):
    """
    Classe de la barre de menus.
    """
    def __init__(self, root, master):
        """
        Constructeur de la barre de menus.
        @param root: fenêtre sur laquelle mettre cette barre de menus.
        @param master: l'Application du programme.
        """
        Menu.__init__(self, master)
        root.configure(menu = self)
        # Menus Principaux :
        self.menuFichier = Menu(self, tearoff=0)
        self.menuEdition = Menu(self, tearoff=0)
        self.menuAffichage = Menu(self, tearoff=0)
        
        self.add_cascade(label = "Fichier", menu=self.menuFichier)
#        self.add_cascade(label = "Edition", menu=self.menuEdition)
        self.add_cascade(label = "Affichage", menu=self.menuAffichage)

        # Menu Fichier :
        #self.menuFichier.add_command(label = "Changer d'utilisateur", accelerator="Ctrl+N", command = master.changeUser) # À faire dans un autre menu je pense...
        #self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Enregistrer", accelerator="Ctrl+S", command = master.save)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Restart", accelerator="Ctrl+R", command = master.restart)
        self.menuFichier.add_command(label = "Quitter", accelerator="Ctrl+Q", command = master.quit)

        # Menu Affichage/Style Horloge :
        self.variableHorlogeStyle = StringVar(value="nombre")
        self.menuHorlogeStyle = Menu(self.menuAffichage, tearoff=0)
        self.menuHorlogeStyle.add_radiobutton(label = "Normal", variable=self.variableHorlogeStyle, value = "normal")
        self.menuHorlogeStyle.add_radiobutton(label = "Nombre", variable=self.variableHorlogeStyle, value = "nombre")

        # Menu Affichage :
        self.menuAffichage.add_cascade(label = "Style d'horloge", menu = self.menuHorlogeStyle)

        self.menuAffichage.add_cascade(label = "Préférences", accelerator="Ctrl+,", command=master.preferences)

