# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label
import sys

__INSTANCE = None

class __TaskInDnd(Toplevel):
    """Cette classe correspond à une tâche en mouvement."""
    def __init__(self, pos, master, task, command, **kwargs):
        # Note : On utilise une fenêtre dépendente (Toplevel) car c'est un truc
        # qui doit pouvoir se déplacer indépendamment de toute chose.
        Toplevel.__init__(self, master, **kwargs)

        self.__command = command
        self.__task = task

        # on enlève le bandeau et la bordure :
        self.overrideredirect(1)
        # on reègle les dimensions et la position :
        self.geometry("200x50+%s+%s"%pos)
        # ça c'est pour faire une animation fluide :
        self.__alpha = 0
        # toujours en avant plan :
        self.attributes("-topmost", True)
        # encore l'animation (le début)
        self.attributes("-alpha", self.__alpha)
        # on règle la couleur du fond et de la brodure
        self.configure(background = "#0078FF")
        self.__frame = Frame(self, bg = "#CCDDFF")
        self.__frame.pack(expand = YES, fill = BOTH, padx = 2, pady = 2)
        self.update()
        # on écrit le texte dedans :
        Label(self.__frame, text = task.nom, font = "Arial 12 bold", bg = "#CCDDFF").grid(sticky = "w")
        Label(self.__frame, text = task.desc, bg = "#CCDDFF").grid(sticky = "w", row = 1)
        # l'animation est-elle finie ?
        self.__commence = False
        self.__fin = False
        # position de la souris pour le déplacement :
        self.__x = self.winfo_pointerx()
        self.__y = self.winfo_pointery()
        # événements pour le déplacement :
        self.__b1 = self.bind_all("<B1-Motion>", self.__dnd)
        self.__b2 = self.bind_all("<ButtonRelease-1>", self.__end)
        # le fondu du début :
        self.__fondudebut()
    def __fondudebut(self):
        """Méthode pour faire un petit fondu au début."""
        self.__alpha += 0.05
        self.attributes("-alpha", self.__alpha)
        if self.__alpha < 1: # si on a pas fini, on continue :
            self.after(5, self.__fondudebut)
        else: # sinon on indique qu'on a fini :
            self.__commence = True
    def __dnd(self, event = None):
        """Méthode pour bouger l'ensemble."""
        if not self.__fin:
            try: # il peut y avoir des exceptions avec la fermeture etc.
                dx = self.winfo_pointerx() - self.__x
                dy = self.winfo_pointery() - self.__y
                dim, x, y = self.geometry().split("+") # on extrait la géométrie actuelle
                x = int(x)
                y = int(y)
                # et on fait tout pleins de calculs trop cools qui marchent,
                # et qui correspondent à ceux qu'on doivent faire pour un DnD
                x += dx
                y += dy
                self.__x += dx
                self.__y += dy
                self.geometry("+%s+%s"%(x, y))
            except:
                pass#self.after(50, self.__dnd)
    def __end(self, event = None):
        """Méthode pour terminer le drag&drop."""
        if self.__commence and self.__fin == False: # on ne peut disparaître seulement si on est complètement commencé (=apparu)
            self.__fin = True
            self.unbind_all(self.__b1)
            self.unbind_all(self.__b2)
            self.__fondufin()
        else:
            self.after(50, self.__end) # sinon on attend un peu.
    def __fondufin(self):
        """
        Méthode pour faire un fondu quand ca disparaît.
        C'est le même qu'à l'apparition mais dans l'autre sens.
        """
        if self.__commence:
            self.__alpha -= 0.05
            try: # il peut ici aussi y avoir des excpetions, mais c'est pas grave.
                self.attributes("-alpha", self.__alpha)
                if self.__alpha > 0:
                    self.after(5, self.__fondufin)
                else:
                    self.destroy()
                    self.__vraieFin()
            except:
                pass
    def __vraieFin(self):
        try:
            self.__command(self.__task, self.__x, self.__y)
        except:
            sys.stderr.write("Exception in Drag&Drop callback\nfrom ")
            self._report_exception()
        try:
            self.destroy()
        except:
            pass

def TaskInDnd(pos, master, task, **kwargs):
    """
    Cette classe correspond à une tâche en mouvement.
    Elle est Singleton.
    """
    global __INSTANCE
    if __INSTANCE != None:
        __INSTANCE.destroy()
    __INSTANCE = __TaskInDnd(pos, master, task, **kwargs)
    return __INSTANCE
