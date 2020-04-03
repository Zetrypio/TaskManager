# -*- coding:utf-8 -*-
from tkinter import *
from horloge import *
from ttkcalendar import *
from dialog import *
from tkinter import Label, Frame
import re
import datetime

CALENDARDATE_TO_NORMALDATE = re.compile(r"(\d+)-(\d+)-(\d+)")
FIND_IN_NORMALDATE = re.compile(r"(\d+)/(\d+)/(\d+)")

def askdate(style="nombre"):
    # Callback quand on ferme la fenêtre par l'un des boutons :
    date = ""
    heure = ""
    dateheure = None
    EXIT = False
    def onClose(a):
        nonlocal EXIT, date, heure, dateheure
        EXIT = True

        # Si on annule :
        if a == 'Annuler' or a=='WM_DELETE_WINDOW':
            fen.destroy()
        else: # Si on accepte :
            # on met en forme la date
            date = str(cal.selection).split(" ")[0]
            if date == "None":
                date = time.strftime("%d/%m/%Y")
            else:
                date = CALENDARDATE_TO_NORMALDATE.sub(r"\3/\2/\1", date)
            j, m, y = FIND_IN_NORMALDATE.findall(date)[0]
            # et l'heure :
            dateheure = datetime.datetime(int(y), int(m), int(j), hor.heure, hor.minute)
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
        except: # Il peut y avoir une exception si on ferme la fenêtre : on s'en fiche.
            pass

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
    v1 = Variable()
    h = Spinbox(cadre, from_ = -1, to=24, increment = 1, width = 4, command = heureChange, textvariable = v1)
    h.pack(side = LEFT, expand = YES, fill = X)
    # choix de la minute : TODO : in-/dé-crémenter les minutes ou les heures au delà de leurs périodes de définition doit augmenter les heures/ les
    v2 = Variable()
    m = Spinbox(cadre, from_ = -1, to=60, increment = 1, width = 4, command = heureChange, textvariable = v2)
    m.pack(side = LEFT, expand = YES, fill = X)
    # valeurs de bases :
    h.set(time.localtime().tm_hour)
    m.set(time.localtime().tm_min)

    v1.trace("rwua", lambda *a: heureChange())
    v2.trace("rwua", lambda *a: heureChange())

    # print(fen.master.master.slaves()[0].taskEditor.slaves()[1].slaves())
    # et on active le dialogue.
    fen.activateandwait()
    print(dateheure)
    return dateheure


if __name__=='__main__':
    import Application
    Application.main()
