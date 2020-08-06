# *-* coding: utf-8 *-*
from tkinter import *
from tkinter.ttk import *

sty = Style()

THEMES = list(sty.theme_names())
NEWTHEMES = ["black", "aquativo", "equilux", "scidblue", "scidmint", "scidgreen", "scidpurple", "scidsand", "scidpink", "scidgrey"]
DIR = "preferences/themes/"

def themeUse(tcl, name, widget):
    """
    Fonction qui va mettre en place un thème chargé
    @param tcl    : <tkinter.tk> à peu près n'importe quel widget de tkinter peut le faire, il faut juste un interprêteur TCL
    @param name   : <str> c'est le thème a charger
    @param widget : <widget> pour le tk_setPalette() n'import quel widget lié à l'Application
    """
    color = None
    if name in NEWTHEMES:
        fileName = name
        if "scid" in name:
            fileName = "scid"
        color = tcl.eval("source " + DIR + fileName + ".tcl")

    sty.theme_use(name)

    if color is not None:
        bg , fg = color.split(" ")
        print("bg :", bg, "fg :", fg)
        # Traitement des couleurs pour le setPalette
        widget.tk_setPalette(background=bg[1:-1], foreground = fg)


def getThemes():
    l = THEMES+NEWTHEMES
    l.sort()
    return l
