# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk     import *
from tkinter import Label, Frame

class ParametrageZone(Frame):
    def __init__(self, master = None, **kwargs):
        kwargs["bg"]= "pink"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers FenetrePreferences

    def getFenetrePreferences(self):
        return self.master

    def getApplication(self):
        return self.master.getApplication()
