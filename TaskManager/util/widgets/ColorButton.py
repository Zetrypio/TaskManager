# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label, Button as TkButton
from tkinter.colorchooser import askcolor

class ColorButton(TkButton):
    """
    Classe qui permet de faire un bouton demandant une couleur à l'utilisateur.
    La couleur est récupérable avec la méthode get().
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur du ColorButton.
        @param master: master du tkinter.Button() que ce widget est.
        @param **kwargs: Options possibles :
            STANDARD OPTIONS :
            activeforeground, anchor, bitmap, cursor,
            disabledforeground, font, foreground
            highlightbackground, highlightcolor,
            highlightthickness, image, justify,
            padx, pady, repeatdelay,
            repeatinterval, takefocus, text,
            textvariable, underline, wraplength.
            
            BUTTON-SPECIFIC OPTIONS :
            compound, default,
            overrelief, state.
        """
        super().__init__(master, command = self.askcolor, width = 4, height = 1, relief = GROOVE, bd = 2, bg = "white", activebackground = "white", **kwargs)

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def get(self):
        """
        Permet d'obtenir la couleur (du bouton).
        @return la couleur du bouton.
        """
        # On passe par cette formulatio bizarre pour éviter un retour d'une énum tkinter
        # type "white" au lieu de "#ffffff"
        r, g, b = self.winfo_rgb(self.cget('bg')) # Donne du 16 bits
        r, g, b = hex(int(r/256)), hex(int(g/256)), hex(int(b/256)) # le int pour arrondir
        if r == hex(0):
            r += "0"
        if g == hex(0):
            g += "0"
        if b == hex(0):
            b += "0"
        return "#" + str(r)[2:] + str(g)[2:] + str(b)[2:]

    ""
    #############
    # Setters : #
    #############
    ""
    def set(self, color):
        """
        Permet de changer la couleur via programme, sans demander à l'utilisateur.
        @param color: la couleur selon le nomenclature de tkinter à mettre.
        """
        self.config(bg = color, activebackground = color)

    ""
    ##############################
    # Méthodes liées au bouton : #
    ##############################
    ""
    def askcolor(self):
        """
        Permet de demander une couleur à l'utilisateur et de l'appliquer sur ce bouton.
        """
        self.set(askcolor()[1])
