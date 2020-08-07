# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

class TextWidget(Canvas):
    """
    Classe qui permet de faire des widgets de texte avec une taille fixée en pixel
    L'astuce consite à mettre un Text dans un Frame.
    De plus on peux ainsi obtenir sa taille
    """
    def __init__(self, master, width = None, height = None, text = None, **kw):
        """
        @param master : <conteneur> sur lequel va se poser notre Text
        @param width  : <int> longueur en pixel
        @param height : <int> hauteur en pixel
        """
        Canvas.__init__(self, master, width = width, height = height)

        self.__text = Text(self, height = 0, width = 0, **kw)
        if text is None:
            text = "ERROR"
        self.__text.insert(END, text)
        self.__text.config(state = DISABLED)
        self.create_window(0, 0, width = width, height = height, anchor = "nw", window = self.__text)

    "" # Marque pour le repli de code
    ##############
    # Méthodes : #
    ##############
    ""
    def bind(self, *args, **kwargs):
        super().bind(*args, **kwargs)
        self.__text.bind(*args, **kwargs)

    ""
    #############################
    # Redéfinition des méthodes #
    #        d'affichage        #
    #############################
    ""
    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.grid_propagate(False)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.pack_propagate(False)
