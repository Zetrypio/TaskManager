# -*- coding:utf-8 -*-
import math
import datetime

def adaptTextColor(color):
    """
    Fonction qui permet de renvoyer la couleur du texte, selon que la couleur passé est sombre ou claire
    @param color : <str> "#......" couleur a test
    @return "#000000" or "#ffffff"
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    if 0.3*r+0.59*g+0.1*b < 128:
        return "#FFFFFF"
    else:
        return "#000000"

def err(e):
    """Return a nice string representation for error objects."""
    return "%s : %s" % (e.__class__.__name__, e)

def mymap(n, a, b, x, y): # Fonction map classique
    """
    Permet de mapper n entre a et b, vers entre x et y.
    @param n: le nombre à mapper.
    @param a: le début du premier interval.
    @param b: la fin du premier interval.
    @param x: le début du deuxième interval.
    @param y: la fin du deuxième interval.
    @return n converti entre x et y depuis entre a et b.
    """
    return (n-a)/(b-a)*(y-x)+x

def posY(t, x1, y1, x2, y2):
    """
    Permet d'obtenir la position Y d'une interpolation sinusoïdale horizontale allant de X1 Y1 à X2 Y2.
    @param t: entre X1 et X2.
    @param x1: Position X de départ de la courbe.
    @param y1: Position Y de départ de la courbe.
    @param x2: Position X de fin de la courbe.
    @param y2: Position Y de fin de la courbe.
    @return la position Y du point en X dans cette courbe.
    """
    return mymap(math.cos(mymap(t, x1, x2, 0, math.pi)), 1, -1, y1, y2)



def ppcm(a, b):
    """Renvoie le plus petit commun multiple (ppcm) des 2 nombres a et b."""
    return (a*b)//math.gcd(a,b)

def rangeDate(jourA, jourB, last = True):
    """
    Permet de faire un générateur renvoyant des jours
    d'un début vers une fin.
    @bug: Essai de correction cependant (en test), mais : Il semblerait que cela ne fonctionne pas correctement.
    @param jourA: début du générateur, sera yield.
    @param jourB: fin du générateur, sera yield si et
    seulement si last est sur True (défaut).
    @param last = True: True si on doit inclure le jour de fin.
    """
    if jourA is not None and jourB is not None:
        jour = jourA + datetime.timedelta()
        while jour < jourB:
            yield jour
            jour += datetime.timedelta(days = 1)
        if last:
            yield jourB

def adaptDate(data, dt):
    """
    Fonction qui permet d'avoir un texte d'une date en adéquation avec les préférences
    @param data : <Data> l'objet data de l'Application
    @param dt : <datetime.date> la date à transformer
    @return texte : <str> le string adéquat
    """
    # Le fichier existe ?
    if not data.testDataExist("Calendrier"):
        texte = dt.year + " " + dt.month + " " + dt.day
    # On cherche le lien
    if data.testDataExist("Calendrier", "Calendrier", "Lien"):
        lien = data.getOneValue("Calendrier", "Calendrier", "Lien")[1]
    else :
        lien = "."
    # On cherche le style
    if data.testDataExist("Calendrier", "Calendrier", "sytle d'affichage"):
        ## Traitement du texte
        # Constantes
        jour        = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        mois        = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

        texte = data.getOneValue("Calendrier", "Calendrier", "sytle d'affichage")

        numJour     = str(dt.day)
        numMois     = str(dt.month)
        numJour2C   = "%02i"%dt.day
        numMois2C   = "%02i"%dt.month
        numAnnee    = str(dt.year)
        jourSemaine = str(jour[dt.weekday()])
        mois        = str(mois[dt.month-1])

        texte = texte.replace("NJ2", numJour2C)
        texte = texte.replace("JS0", jourSemaine[0])
        texte = texte.replace("NM2", numMois2C)
        texte = texte.replace("NA", numAnnee)
        texte = texte.replace("JS", jourSemaine)
        texte = texte.replace("M3", mois[:3])
        texte = texte.replace("NJ", numJour)
        texte = texte.replace("MO", mois)

        texte = texte.replace("_", lien)

    return texte

## Conversion datetime et str
def datetimeToStr(d):
    """
    Permet de transformer un datetime en str selon le format suivant : YYYY-MM-DD-HH-MM-SS
    @param d : <datetime.datetime> celui qu'on doit transformer
    """
    return "-".join([str(d.year), str(d.month), str(d.day), str(d.hour), str(d.minute), str(d.second)]) if isinstance(d, datetime.datetime) else None

def dateToStr(d):
    """
    Permet de transformer un datetime en str selon le format suivant : YYYY-MM-DD
    @param d : <datetime.date> celui qu'on doit transformer
    """
    return "-".join([str(d.year), str(d.month), str(d.day)]) if isinstance(d, datetime.date) else None

def strToDate(dt):
    """
    Permet de transformer un str (convertie par dateToStr()) en date
    @param dt : <str>
    @return <datetime.date>
    """
    if not isinstance(dt, str):
        return None
    y, m, d = dt.split("-")
    return datetime.date(int(y), int(m), int(d))

def strToDatetime(dt):
    """
    Permet de transformer un str (convertie par datetimeToStr()) en datetime
    @param dt : <str>
    @return <datetime.datetime>
    """
    if not isinstance(dt, str):
        return None
    y, m, d, h, mi, s = dt.split("-")
    return datetime.datetime(int(y), int(m), int(d), int(h), int(mi), int(s))

def strToTimedelta(dt):
    """
    Permet de transformer un str (convertie par timedeltaToStr()) en timedelta
    @param dt : <str>
    @return <datetime.timedelta>
    """
    if not isinstance(dt, str):
        return None
    d, s = dt.split("-")
    return datetime.timedelta(days = int(d), seconds = int(s))

def timedeltaToStr(d):
    """
    Permet de transformer un datetime en str selon le format suivant : DD-SS
    @param d : <datetime.timedelta> celui qu'on doit transformer
    """
    return "-".join([str(d.days), str(d.seconds)]) if isinstance(d, datetime.timedelta) else None
