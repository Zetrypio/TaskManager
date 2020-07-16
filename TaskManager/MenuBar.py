# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from preferences.fenetrePreferences import *

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
        self.menuFichier   = Menu(self, tearoff=0)
        self.menuEdition   = Menu(self, tearoff=0)
        self.menuAffichage = Menu(self, tearoff=0)
        
        self.add_cascade(label = "Fichier", menu=self.menuFichier)
        # Il y a juste à décommenter cette ligne pour remettre le menu édition,
        # mais tant qu'il n'y a rien dedans, on s'en fiche...
        #self.add_cascade(label = "Edition", menu=self.menuEdition)
        self.add_cascade(label = "Affichage", menu=self.menuAffichage)

        # Menu Fichier :
        self.menuFichier.add_command(label = "Enregistrer", accelerator=self.__getBindingOf("save-file"), command = master.save)
        self.menuFichier.add_separator()
        self.menuFichier.add_command(label = "Restart",     accelerator=self.__getBindingOf("restart"),   command = master.restart)
        self.menuFichier.add_command(label = "Quitter",     accelerator=self.__getBindingOf("quit"),      command = master.quit)

        # Menu Affichage :
        self.menuAffichage.add_command(label = "Préférences", accelerator=self.__getBindingOf("preferences"), command = master.preferences)

    def __getBindingOf(self, bindingVirtuel):
        """
        @param bindingVirtuel : <str> nom du bindings dont on cherche la combinaison
        @return                 <str> les combinaisons séparées par une virgule
        """
        return ",".join(self.master.getBindingIn("Application")[bindingVirtuel]["bindings"])


