# -*- coding:utf-8 -*-
from dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

def askDureeJours():
    duree = None
    def onClose(button):
        nonlocal duree
        if button == "Ok":
            duree = datetime.timedelta(**{{"Semaines":"weeks", "Jours": "days"}[unit.get()]:int(delta.get())})
        fen.destroy()
    
    fen = Dialog(title = "Décaler des périodes", buttons = ("Ok", "Annuler"), command = onClose)
    delta = Spinbox(fen, from_ = 0, to = 1000)
    delta.pack(side = LEFT, expand = YES, fill = X)
    delta.set(0)
    unit = Combobox(fen, values = ["Jours", "Semaines"])
    unit.set(unit.cget("values")[0])
    unit.pack(side = RIGHT, expand = YES, fill = X)
    
    fen.activateandwait()

    return duree

if __name__ == '__main__':
    import Application
    Application.main()
