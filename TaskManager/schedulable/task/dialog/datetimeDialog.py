# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.widgets.Dialog import *
from util.widgets.ttkcalendar import *
from util.widgets.Horloge import *

def askdatetime(style="nombre"):
    # Callback quand on ferme la fenêtre par l'un des boutons :
    date = ""
    heure = ""
    dateheure = None
    EXIT = False
    prevHWas0 = prevMWas0 = False
    def onClose(a):
        nonlocal EXIT, date, heure, dateheure
        EXIT = True

        # Si on annule :
        if a == 'Annuler' or a=='WM_DELETE_WINDOW':
            fen.destroy()
        elif a == 'Ok': # Si on accepte :
            # on met en forme la date
            date = cal.selection.date()
            if date == None:
                date = datetime.datetime.now().date()
            # et l'heure :
            dateheure = datetime.datetime.combine(date, datetime.time(hor.heure, hor.minute))
            # et on ferme la fenêtre.
            fen.destroy()

    def heureChange():
        try:
            hor.setAuto(False)
            hh = int(h.get()if h.get()else 0)
            mm = int(m.get()if m.get()else 0)
            while mm < 0:
                mm += 60
                hh -= 1
            while mm >= 60:
                mm -= 60
                hh += 1
            while hh < 0:
                hh += 24
                # cal.date -= 1
            while hh >= 24:
                hh -= 24
                # cal.date += 1
            m.set(mm)
            h.set(hh)
            hor.set(hh, mm)
        except TclError: # Il peut y avoir une exception si on ferme la fenêtre : on s'en fiche.
            pass
        except Exception as e:
            showerror("Symbol Interdit", err(e))
            m.set(0)
            h.set(0)
            hor.set(0, 0)
    
    def heureChange2():
        try:
            print("I'm using it")
            if prevHWas0:
                h.delete(INSERT, END)
            if prevMWas0:
                m.delete(INSERT, END)

            hor.setAuto(False)
            hh = int(h.get() if h.get() else 0)
            mm = int(m.get() if m.get() else 0)
            
            while mm < 0:
                mm += 60
                hh -= 1
            while mm >= 60:
                mm -= 60
                hh += 1
            if hh < 0:
                hh = 0
                mm = 0
            if hh >= 24:
                hh = 23
                mm = 59
            m.set(mm)
            h.set(hh)
            hor.set(hh, mm)
        #except TclError: # Il peut y avoir une exception si on ferme la fenêtre : on s'en fiche.
        #    pass
        except Exception as e:
            showerror("Symbol Interdit", err(e))
            m.set(0)
            h.set(0)
            hor.set(0, 0)
    
    def prechange():
        nonlocal prevHWas0, prevMWas0
        prevHWas0 = int(h.get() if h.get() else 0) == 0
        prevMWas0 = int(m.get() if m.get() else 0) == 0
        print("pre", prevHWas0, prevMWas0)

    # Construction du dialogue :
    fen = Dialog(title = "Choix de la date et l'heure", buttons = ("Ok", "Annuler"), command=onClose)
    cadre = Frame(fen)
    cadre.pack(side = RIGHT)
    # création des widgets :
    cal = Calendar(fen, firstweekday=calendar.MONDAY)
    hor = Horloge(cadre, style=="nombre")
    # placement des widgets :
    cal.pack(side = LEFT, expand=1, fill='both')
    hor.pack(side = TOP)

    # choix de l'heure :
    h = Spinbox(cadre, from_ = -1, to=24, increment = 1, width = 4, command = heureChange)
    h.bind("<Key>", lambda e: prechange(), add = 1)
    h.bind("<Key>", lambda e: h.after(10, heureChange2), add = 1)
    h.pack(side = LEFT, expand = YES, fill = X)
    # choix de la minute : TODO : in-/décrémenter les minutes ou les heures au delà de leurs périodes de définition doit augmenter les heures/ les
    m = Spinbox(cadre, from_ = -1, to=60, increment = 1, width = 4, command = heureChange)
    m.bind("<Key>", lambda e: prechange(), add = 1)
    m.bind("<Key>", lambda e: m.after(10, heureChange2), add = 1)
    m.pack(side = LEFT, expand = YES, fill = X)
    # valeurs de bases :
    h.set(time.localtime().tm_hour)
    m.set(time.localtime().tm_min)

    prechange()
    # print(fen.master.master.slaves()[0].taskEditor.slaves()[1].slaves())
    # et on active le dialogue.
    fen.activateandwait()
    print(dateheure)
    return dateheure

