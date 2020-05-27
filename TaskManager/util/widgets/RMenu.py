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
        @param andInside: binder sur tout les widgets trouv�s dedans de mani�re r�cursive ?
        @param biner: le widget binder avec la m�thode bind. Si None : master sera utilis�.
        @param bindWithId: permet de bind seulement un id ou tag d'un item d'un widget si celui-ci
        les supporte. Si sur None, bind sur le widget tout entier.
        @param **args: Param�tre suppl�mentaire pour le tkinter.Menu() que ce widget est.
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

    def __bind_inside_of(self, widget):
        """
        Permet de binder r�cursivement sur tout les widgets trouv�s
        � l'int�rieur de celui pass� en arguement.
        @param widget: le widget en question.
        """
        widget.bind("<Button-3>", self.right_menu_event)
        try:
            subwidget = widget.slaves()
        except:
            return
        for w in subwidget:
            self.__bind_inside_of(w)

    def right_menu_event(self, event):
        """
        M�thode ex�cut�e lors d'un clic-droit.
        Sert � ouvrir le menu � la position de la
        souris trouv�e dans le
        @param event: �v�nement avec la position de la souris.
        """
        self.event_generate("<<RMenu-Opened>>", x = event.x, y = event.y, rootx = event.x_root, rooty = event.y_root)
        self.tk_popup(event.x_root, event.y_root)
    
    def destroy(self):
        """
        M�thode pour d�truire le RMenu, et le d�binder.
        """
        try:
            self.binder.unbind(self.__binding)
        except:
            pass
        Menu.destroy(self)
