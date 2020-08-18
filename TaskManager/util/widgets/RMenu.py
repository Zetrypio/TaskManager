# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

class RMenu(Menu):
    """
    Classe permettant de faire un menu en clic-droit.
    """
    def __init__(self, master = None, andInside = False, binder = None, bindWithId = None, **args):
        """
        Constructeur du RMenu.
        @param master: master du tkinter.Menu() que cet widget est.
        @param andInside: binder sur tout les widgets trouvés dedans de manière récursive ?
        @param biner: le widget binder avec la méthode bind. Si None : master sera utilisé.
        @param bindWithId: permet de bind seulement un id ou tag d'un item d'un widget si celui-ci
        les supporte. Si sur None, bind sur le widget tout entier.
        @param **args: Paramètre supplémentaire pour le tkinter.Menu() que ce widget est.
        """
        try:del args["tearoff"]
        except:pass
        if not binder:
            binder = master
        if not hasattr(master, "tk"):
            master = master.canvas
        self.binder = binder
        Menu.__init__(self, master, tearoff=0, **args)
        self.__bindWithId = bindWithId
        if bindWithId is None:
            self.__binding = self.binder.bind("<Button-3>", self.right_menu_event)
            self.__bind_inside_of(binder)
        else:
            self.__binding = self.binder.tag_bind(bindWithId, "<Button-3>", self.right_menu_event)

    "" # Marque pour le repli de code
    ##############
    # Méthodes : #
    ##############
    ""
    def __bind_inside_of(self, widget):
        """
        Permet de binder récursivement sur tout les widgets trouvés
        À l'intérieur de celui passé en argument.
        @param widget: le widget en question.
        """
        widget.bind("<Button-3>", self.right_menu_event)
        try:
            subwidget = widget.slaves()
        except:
            return
        for w in subwidget:
            self.__bind_inside_of(w)

    def destroy(self):
        """
        Méthode pour détruire le RMenu, et le débinder.
        """
        try:
            self.binder.unbind(self.__binding)
        except:
            pass
        Menu.destroy(self)

    def right_menu_event(self, event):
        """
        Méthode exécutée lors d'un clic-droit.
        Sert à ouvrir le menu à la position de la
        souris trouvée dans le
        @param event: événement avec la position de la souris.
        """
        ## Note de Zetrypio :
        # Le try-except ici est nécessaire, car lors de la suppression
        # de cet objet, si le RMenu était bind sur un tag, il ne peut
        # pas se débind (ou alors je n'ai pas trouvé la méthode,
        # pourtant j'ai pas mal cherché), et donc cette méthode est
        # tout de même exécutée. Mais comme ce RMenu est destroyed,
        # les lignes suivantes causent une erreur dans la console.
        # Pour moi, il s'agit d'un bug (pas de méthode d'unbind de tags),
        # mais je ne vois pas comment le régler autrement.
        # Le binding est censé réellement se supprimer quand le master
        # de ce widget se supprime, mais ce n'est pas normal qu'on ne puisse
        # pas enlever un bind sur un item ou un tag sans supprimer l'item/ le tag/ le binder.
        try:
            self.event_generate("<<RMenu-Opened>>", x = event.x, y = event.y, rootx = event.x_root, rooty = event.y_root)
            self.tk_popup(event.x_root, event.y_root)
        except:
            pass
