# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label


class TextWidget(Canvas):
    # C'est la hauteur minimum pour après reset un truc beau
    MINHEIGHT = 0
    # Dictionnaire de palette
    PALETTE = {"selected" : "#91C9F7", "normal" : "#d3d3d3", "jour" : "#ffffff"}
    """
    Classe qui permet de faire des widgets de texte avec une taille fixée en pixel
    L'astuce consite à mettre un Text dans un Frame.
    De plus on peux ainsi obtenir sa taille
    """
    def __init__(self, master, width = None, height = None, text = None, nbJour = None, bg = "#d3d3d3", mode = "normal",  **kw):
        """
        @param master : <conteneur> sur lequel va se poser notre Text
        @param width  : <int> longueur en pixel
        @param height : <int> hauteur en pixel

        @param text : <str> pour le texte à l'intérieur du Text
        @param nbJour : <int> nombre de jour au total a afficher (pour avoir le nombre de ligne)
        @param mode : <str> pour la couleur, la valeur doit est une clé de self.__palette
        """
        # Calcul pour la hauteur des widget Texts
        # Pour l'instant basé sur mon écran et ma résolution (1080x1920)
        if nbJour is not None and text is not None:
            # Fonction défini par une approximation de fonction
            # Ce qui donne quelques erreurs, parfoir 1 de trop (arrondi)
            j = 193.72*pow(nbJour,-1.074)
            Ligne = (len(text)//j) +1
            height = Ligne*18
            if height > TextWidget.MINHEIGHT:
                TextWidget.MINHEIGHT = height

        Canvas.__init__(self, master, width = width, height = height, bg = bg)

        self.__text = Text(self, height = 0, width = 0, bg = bg, **kw)
        if text is None:
            text = "ERROR"
        self.__text.insert(END, text)
        self.__text.config(state = DISABLED)
        self.__idText = self.create_window(0, 0, width = width, height = height, anchor = "nw", window = self.__text)
        self.__width = width
        self.__height = height

        self.setColor(mode = mode)
        self.after(1, self.__resize)
        super().bind("<Configure>", lambda e: self.__resize(), 1)

    "" # Marque pour le repli de code
    ##############
    # Méthodes : #
    ##############
    ""
    def bind(self, *args, **kwargs):
        super().bind(*args, **kwargs)
        self.__text.bind(*args, **kwargs)

    def changeColor(color, value):
        """
        Permet de changer la couleur de la palette
        @param color : <str> correspond à la clé du dictionnaire à changer
        @param value : <str> couleur au format tkinter
        """
        if color in TextWidget.PALETTE:
            print("changé")
            TextWidget.PALETTE[color] = value
        else:
            raise ValueError("\"%s\" not in TextWidget#__palette"%color)

    def resize(self, width = None, height = None):
        """
        Permet de changer la taille
        @param width : None: change pas. 0: adapte largeur. autre : taille fixe.
        @param height: None: change pas. 0: adapte hauteur. autre : taille fixe.
        """
        self.__width  = width  if width  is not None else self.__width
        self.__height = height if height is not None else self.__height
        self.__resize()

    def __resize(self):
        self.itemconfigure(self.__idText, width = self.__width or self.winfo_width(), height = self.__height or self.winfo_height())

    def setColor(self, mode = "normal"):
        """
        Permet de mettre la couleur sur le canvas et le texte
        + avoir les couleurs du thèmes
        @param mode : <str> clé pour acceder à la couleur de TextWidget.PALETTE
        """
        if mode == "jour" or mode == "selected" or mode == "normal":
            self.config(bg = TextWidget.PALETTE[mode])
            self.__text.config(bg = TextWidget.PALETTE[mode])
        else :
            raise ValueError('mode (="%s") must be "selected", "jour" or "normal"'%mode)

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
