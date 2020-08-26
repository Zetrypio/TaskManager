# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label, Button as TkButton
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showerror
import datetime
import time

from affichages.periode.Periode import *
from util.widgets.ColorButton import *
from util.widgets.Dialog import askyesnowarning

from .dialog.datetimeDialog import *
from .Task import *

class TaskAdder(Frame):
    """
    Classe permettant d'ajouter des tâches (widget de gauche de l'Application).
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur du TaskAdder.
        @param master : TaskEditor.
        @param **kwargs : options de configuration du Frame, voir Frame.config() et Frame.keys()
        """
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers TaskEditor

        # Attributs normaux:
        date = time.localtime()
        self.debut = None #datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
        self.fin = datetime.datetime(date.tm_year, date.tm_mon, date.tm_mday)
        del date

        # Widgets non référencés.
        Label(self, text="Nom :").grid(row = 0, column = 0, sticky="e")
        Label(self, text="De :").grid(row = 1, column = 0, sticky="e")
        Label(self, text="À :").grid(row = 1, column = 6, sticky="e")
        Label(self, text="Répétitions :").grid(row = 2, column = 0, columnspan = 2, sticky = "e")
        Label(self, text="répétitions tout les").grid(row = 2, column = 3, columnspan = 2)
        Label(self, text="Période :").grid(row = 3, column = 0, columnspan = 2, sticky = "e")

        # Widgets :
        # Nom :
        self.champNom           = Entry(self)
        # Début :
        self.champDebut         = Button(self, command = self.askDateDebut)
        # Fin :
        self.champFin           = Button(self, command = self.askDateFin)
        # Durée
        self.champJour          = Spinbox(self, from_ = 0, to=31, increment = 1, width = 4, command = self.setAutoFin)
        self.champHeure         = Spinbox(self, from_ = 0, to=23, increment = 1, width = 4, command = self.setAutoFin)
        self.champMinute        = Spinbox(self, from_ = 0, to=59, increment = 1, width = 4, command = self.setAutoFin)
        # Répétitions :
        self.champNbRepetition  = Spinbox(self, from_ = -1, to=100, increment = 1, width = 4) # Nombre de répétition
        self.champRepetition    = Spinbox(self, from_ = 1, to=100, increment = 1, width = 4) # quantitée d'unitée de temps entre 2 répétition.
        self.champUniteeRepet   = Combobox(self, values = ["minutes", "heures", "jours", "semaines", "mois", "années"], state = "readonly", width = 4)
        # valeurs par défaut :
        self.champNbRepetition.set(0)
        self.champRepetition.set(1)
        self.champUniteeRepet.set(self.champUniteeRepet.cget("values")[2])
        # Autres :
        self.champDescription   = Text(self, height = 3, width = 10, wrap = "word")
        self.boutonColor        = ColorButton(self)
        # Valider
        self.boutonValider      =   Button(self, command = self.valider, text = "Ajouter")

        # Placements :
        # Ligne 0 :
        self.champNom         .grid(row = 0, column = 1, columnspan = 4, sticky ="ew")
        self.boutonColor      .grid(row = 0, column = 5, sticky="ew", padx = 2)
        self.boutonValider    .grid(row = 0, column = 6, columnspan = 2, sticky="ew")
        # Ligne 1 :
        self.champDebut       .grid(row = 1, column = 1, columnspan = 2)
        self.champJour        .grid(row = 1, column = 3)
        self.champHeure       .grid(row = 1, column = 4)
        self.champMinute      .grid(row = 1, column = 5)
        self.champFin         .grid(row = 1, column = 7) # Column 6 est pris par label "À :"
        # Ligne 2 :
        self.champNbRepetition.grid(row = 2, column = 2, sticky = "ew")
        self.champRepetition  .grid(row = 2, column = 5, sticky = "ew")
        self.champUniteeRepet .grid(row = 2, column = 6, sticky = "ew", columnspan = 2)
        # Ligne 3 :
        self.champDescription .grid(row = 3, column = 0, columnspan = 8, sticky ="ew")

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getApplication(self):
        """
        Getter pour l'application.
        @return l'Application.
        """
        return self.master.getApplication()

    def getData(self):
        """
        Getter pour le data
        @return <Data>
        """
        return self.getApplication().getData()

    def getDebut(self):
        """
        Permet d'obtenir le début déjà choisi par l'utilisateur.
        @return le début de la tâche à créer.
        """
        return (self.debut + datetime.timedelta()) if self.debut is not None else None

    def getDuree(self):
        """
        Permet d'obtenir la durée calculée selon le début et la fin.
        @return la durée de la tâche à créer.
        """
        ecart = self.fin - (self.debut if self.debut is not None else self.fin)
        return ecart

    def getFin(self):
        """
        Permet d'obtenir la fin déjà choisie par l'utilisateur.
        @return la fin de la tâche à créer.
        """
        return (self.fin + datetime.timedelta()) if self.fin is not None else None

    def getRepetitionTime(self):
        """
        Permet d'obtenir les informations de répétition.
        @return val, unit : val est tout les combien d'unit on répète.
        """
        unit = self.champUniteeRepet.get()
        val = int(self.champRepetition.get())
        if unit == "minutes":
            return datetime.timedelta(minutes=val)
        elif unit == "heures":
            return datetime.timedelta(hours=val)
        elif unit == "jours":
            return datetime.timedelta(days=val)
        elif unit == "semaines":
            return datetime.timedelta(weeks=val)
        
        # ATTENTION LES ECARTS NE SONT PAS EXACT SUR CES SUIVANTS :
        elif unit == "mois":
            return datetime.timedelta(days=val*30)
        elif unit == "années":
            return datetime.timedelta(days=val*365)
        else:
            return val, unit

    def getStyleHorloge(self):
        """
        Permet de savoir si on affiche les heures sur le cadran
        @return <bool> , par défaut c'est False qui est retourné
        """
        # On va chercher le style avec data
        if self.getApplication().getData().testDataExist("General", "General", "afficher les heures sur l'horloge"):
            return 'True' == self.getApplication().getData().getOneValue("General", "General", "afficher les heures sur l'horloge")
        else:
            return False

    def getTaskEditor(self):
        """
        Getter du taskEditor
        @return taskEditor
        """
        return self.master

    ""
    #############
    # Setters : #
    #############
    ""
    def __adaptText(self, dt):
        """
        Méthode qui Fait un texte joli avec un date
        @param dt : <datetime.date> celui du jour
        @return texte : <str> un truc en accord avec les préférences
        """
        ## Gestion du texte
        # Le fichier existe ?
        if not self.getData().testDataExist("Calendrier"):
            texte = dt.year + " " + dt.month + " " + dt.day
        # On cherche le lien
        if self.getData().testDataExist("Calendrier", "Calendrier", "Lien"):
            lien = self.getData().getOneValue("Calendrier", "Calendrier", "Lien")[1]
        else :
            lien = "."
        # On cherche le style
        if self.getData().testDataExist("Calendrier", "Calendrier", "sytle d'affichage"):
            ## Traitement du texte
            # Constantes
            jour        = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            mois        = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

            texte = self.getData().getOneValue("Calendrier", "Calendrier", "sytle d'affichage")

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

    def setDebut(self, value):
        """
        Méthode qui fixe le début + met un joli texte sur le bouton
        @param value : <datetime.datetime> celui du moment a afficher
        """
        self.debut = value
        self.champDebut.config(text = self.__adaptText(value.date()) + " " + str(value.time()) if value is not None else "")
        self.autoSetDuree()

    def setFin(self, value):
        """
        Méthode qui fixe la fin + met un joli texte sur le bouton
        @param value : <datetime.datetime> celui du moment a afficher
        """
        if value is not None:
            self.fin = value
        self.champFin.config(text = self.__adaptText(value.date()) + " " + str(value.time()) if value is not None else "")
        self.autoSetDuree()

    ""
    ##################################
    # Méthodes liées aux dialogues : #
    ##################################
    ""
    def askDateDebut(self):
        """
        Permet de demander le début de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        ## demande de la date
        date = askdatetime(self.getStyleHorloge())
        self.setDebut(date)

    def askDateFin(self):
        """
        Permet de demander la fin de la tâche à l'utilisateur via boîte de dialogue usuelle.
        """
        # Pour un obscure raison, il faut appeler cette méthode :
        self.master.redessiner()

        # demande de la date
        date = askdatetime(self.getStyleHorloge())
        self.setFin(date)

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def autoSetDuree(self):
        """
        Permet de mettre à jour les widgets de durée de tâche.
        """
        ecart = self.getDuree()
        self.champJour.set(ecart.days)
        self.champHeure.set(ecart.seconds//3600)
        self.champMinute.set(ecart.seconds//60%60)
        self.verifyDuree()

    def setAutoFin(self):
        """
        Méthode qui met à jour la fin si on change les durée
        """
        ecart = datetime.timedelta(days = int(self.champJour.get()), hours = int(self.champHeure.get()), minutes = int(self.champMinute.get()))
        if self.debut is not None:
            self.setFin(self.debut + ecart)
        elif self.debut is None and self.fin is not None:
            self.setDebut(self.fin - ecart)
        else:
            return # Pour ne pas faire le test Durée
        # On met le text en rouge si l'écart est négatif
        self.verifyDuree()

    def verifyDuree(self):
        """
        Méthode qui change la couleur du text des widgets de la durée si ecart est négatif
        """
        ecart = self.getDuree()
        self.champJour.config(foreground = "#FF0000") if ecart < datetime.timedelta(0) else self.champJour.config(foreground = self.getApplication().getData().getPalette()["foreground"])
        self.champHeure.config(foreground = "#FF0000") if ecart < datetime.timedelta(0) else self.champHeure.config(foreground = self.getApplication().getData().getPalette()["foreground"])
        self.champMinute.config(foreground = "#FF0000") if ecart < datetime.timedelta(0) else self.champMinute.config(foreground = self.getApplication().getData().getPalette()["foreground"])


    def valider(self):
        """
        Méthode quand on valide la création d'une tâche.
        @return la nouvelle tâche juste créée.
        """
        debut = self.getDebut()
        duree = self.getDuree()
        if duree < datetime.timedelta(0) or (debut is not None and duree <= datetime.timedelta(0)):
            showerror("Durée incorrect", "Vous ne pouvez pas créer une tache avec une durée négative ou nulle")
            return
        rep   = self.getRepetitionTime()
        nbrep = int(self.champNbRepetition.get())
        periode = self.getApplication().getPeriodManager().getActivePeriode()
        # On check si on est dans la période
        if debut is not None and (debut.date() < periode.getDebut() or (duree is not None and (debut + duree).date() > periode.getFin())\
        or (duree is not None and (debut + duree + nbrep * rep).date() > periode.getFin()) \
        or (debut + nbrep * rep).date() > periode.getFin()): # Si ne nombre de répétition fait que c'est après la fin de la période
            if not askyesnowarning(title = "Tache hors période", message = "Vous voulez créer une tache qui n'est pas entièrement dans la période actuelle.\nVoulez-vous vraiment créer cette tache ?"):
                return
        nom = self.champNom.get()
        desc  = self.champDescription.get("0.0", END)
        color = self.boutonColor.get()
        self.getTaskEditor().ajouter(Task(nom, periode, desc, color, debut, duree, rep, nbrep))
