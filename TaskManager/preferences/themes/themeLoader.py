# *-* coding: utf-8 *-*
from tkinter import *
from tkinter.ttk import *

sty = Style()

THEMES = list(sty.theme_names())
NEWTHEMES = ["black", "aquativo", "equilux", "scidblue", "scidmint", "scidgreen", "scidpurple", "scidsand", "scidpink", "scidgrey"]
DIR = "preferences/themes/"

def themeUse(tcl, name, widget, app):
    """
    Fonction qui va mettre en place un thème chargé
    @param tcl    : <tkinter.tk> à peu près n'importe quel widget de tkinter peut le faire, il faut juste un interprêteur TCL
    @param name   : <str> c'est le thème a charger
    @param widget : <widget> pour le tk_setPalette() n'import quel widget lié à l'Application
    @param app   : <Application> pour changer setCurrentThemeBg (data) + redessiner (taskEditor)
    """
    color = None
    if name in NEWTHEMES and name not in sty.theme_names():
        fileName = name
        if "scid" in name:
            fileName = "scid"
        color = tcl.eval("source " + DIR + fileName + ".tcl")

    sty.theme_use(name)


    if color is not None:
        # Traitement des couleurs pour le setPalette
        bg , fg = color.split(" ")
        widget.tk_setPalette(background=bg[1:-1], foreground = fg)
        app.getData().setCurrentThemeBg(bg[1:-1])
    else:
        widget.tk_setPalette(background=sty.lookup(".", "background"), foreground = sty.lookup(".", "foreground"))
        app.getData().setCurrentThemeBg(sty.lookup(".", "background"))


def getThemes():
    l = THEMES+NEWTHEMES
    l.sort()
    return l
