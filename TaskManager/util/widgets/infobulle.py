# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame

from ..Point import *

# Instance unique de l'infobulle
INFOBULLE = None


def infobulle(event, text=""):
    global INFOBULLE
    if INFOBULLE is None:
        INFOBULLE = Toplevel()
    #INFOBULLE.transient(INFOBULLE.master)
    INFOBULLE.overrideredirect(1)
    for w in INFOBULLE.slaves():
        w.destroy()
    Label(INFOBULLE, text = text, bg = "white", bd = 1, relief = SOLID).pack(expand = YES, fill = BOTH)
    INFOBULLE.update()
    x = event.x_root+10
    y = event.y_root+10
    try: # peut en effet générer des erreures randoms
        if x + INFOBULLE.winfo_width() > INFOBULLE.winfo_screenwidth():
            x = x-20-INFOBULLE.winfo_width()
        if y + INFOBULLE.winfo_height() > INFOBULLE.winfo_screenheight():
            y = Y-20-INFOBULLE.winfo_height()
    except:pass
    try: # ici aussi
        INFOBULLE.geometry("+%s+%s"%(x, y))
    except:pass

def delete_infobulle():
    global INFOBULLE
    try:
        INFOBULLE.destroy()
    except:
        pass
    INFOBULLE = None

def ajouterInfoBulle(widget, text):
    widget.bind("<Enter>", lambda e: infobulle(e, text))
    widget.bind("<Leave>", lambda e: delete_infobulle())

def ajouterInfoBulleTag(widget, tag, text):
    widget.tag_bind(tag, "<Enter>", lambda e: infobulle(e, text))
    widget.tag_bind(tag, "<Leave>", lambda e: delete_infobulle())


# Dictionnaires des infos des canvas
_info_infobulles = {}

def ajouterInfoBulleTagCanvas(canvas, tag, text):
    # Si le canvas n'a jamais été référencé auparavant :
    if not _isCanvasAdded(canvas):
        _addCanvas(canvas)

    if isinstance(tag, (str, bytes)):
        tag = (tag,)
    for t in tag:
        _info_infobulles[canvas]["texteTags"][t] = text

def ajouterInfoBulleItemCanvas(canvas, tag, text):
    # Si le canvas n'a jamais été référencé auparavant :
    if not _isCanvasAdded(canvas):
        _addCanvas(canvas)

    _info_infobulles[canvas]["texteItems"][tag] = text

def _isCanvasAdded(canvas):
    return canvas in _info_infobulles

def _addCanvas(canvas):
    _info_infobulles[canvas] = {"texteItems" : {}, "texteTags":{}}
    canvas.bind("<Motion>", _bouge, add=True)
    canvas.bind("<Leave>", lambda e: delete_infobulle())

# Pour le Scrolling :
def _getYScrolling(canvas):
    return int(round(canvas.yview()[0]*int(canvas.cget("scrollregion").split(" ")[3])))-2
    
def _getXScrolling(canvas):
    return int(round(canvas.xview()[0]*int(canvas.cget("scrollregion").split(" ")[2])))
    
def _getScrolledPosition(canvas, pos):
    return Point(pos.x + _getXScrolling(canvas), pos.y + _getYScrolling(canvas))

# Méthode quand la souris bouge : mettre à jour l'infobulle.
def _bouge(event):
    # On récupère le canvas
    canvas = event.widget
    # On corrige la position suivant le scrolling:
    pos = _getScrolledPosition(canvas, event)
    # Liste des items trouvés :
    listeItems = canvas.find_overlapping(pos.x-1, pos.y-1, pos.x+1, pos.y+1)
    # En déduire la liste des tags :
    listeTags = []
    for item in listeItems:
        tags = canvas.gettags(item)
        if tags is None or len(tags) == 0:
            continue
        listeTags += tags

    listeTags = list(set(listeTags))

    # On trouve la liste des textes :
    listeTextes = []
    for item in listeItems:
        if item in _info_infobulles[canvas]["texteItems"]:
            listeTextes.append(_info_infobulles[canvas]["texteItems"][item])
    for tag in listeTags:
        if tag in _info_infobulles[canvas]["texteTags"]:
            listeTextes.append(_info_infobulles[canvas]["texteTags"][tag])

    # On crée le texte et l'infobulle :
    listeTextes = list(set(listeTextes))
    if len(listeTextes) == 0:
        delete_infobulle()
    elif len(listeTextes) == 1:
        infobulle(event, listeTextes[0])
    else:
        texte = "Multiple Info at this point :"
        for txt in listeTextes:
            texte += "\n- %s.\t    \t"%txt
        infobulle(event, texte)

__all__ = ("INFOBULLE", "infobulle", "delete_infobulle", "ajouterInfoBulle", "ajouterInfoBulleTag", "ajouterInfoBulleTagCanvas", "ajouterInfoBulleItemCanvas")
