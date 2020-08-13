# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
import time

from ..AbstractDisplayedCalendar import *
from .PeriodAdder import *
from .dialog.scinderPeriodDialog import *


class AffichageCalendrierPeriode(AbstractDisplayedCalendar):
    """
    Classe permettant la vision des périodes dans un mois.
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de l'affichage en calendrier des périodes.
        @param master: NoteBook de DonneeCalendrier, master du tkinter.Frame() que cet objet est.
        @param **kwargs: Options de configuration du tkinter.Frame() que cet objet est.
        """
        # Constructeur parent :
        super().__init__(master, **kwargs)
        # Note : self.master est une référence vers le NoteBook à l'intérieur de DonneeCalendrier.

        # Information du temps de l'affichage.
        self.annee = time.localtime().tm_year
        self.mois = time.localtime().tm_mon

        # Nécessaire pour gérer l'affichage non-superposé des périodes qui sont en même temps.
        self.__listeHauteur = {}

        # tkinter.Canvas() sur lequel tout s'affiche.
        self.can = Canvas(self, width = 1, height = 1, bd = 0, bg = self.getPalette()["background"])
        self.can.pack(expand = YES, fill = BOTH)
        self.can.bind("<Configure>", lambda e: self.updateAffichage())
        self.can.bind("<Button-1>", self.clic)
        self.can.bind("<Control-Button-1>", lambda e: self.clic(e, True))

    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getJourDebut(self):
        """
        Override, car en fait ça fonctionne avec un mois.
        @return datetime.date() correspondant au premier jour du mois actuellement sélectionné.
        """
        return datetime.date(self.annee, self.mois, 1)

    def getJourFin(self):
        """
        Override, car en fait ça fonctionne avec un mois.
        @return datetime.date() correspondant au dernier jour du mois actuellement sélectionné.
        """
        return self.getJourDebut() + datetime.timedelta(days = tailleMois(self.mois, self.annee))

    def getPeriodHeight(self):
        """
        Renvoie la hauteur des périodes.
        TODO : Faire que ça compacte les périodes si manque de place.
        @return la hauteur des périodes à afficher.
        """
        return 10

    def getPeriodeYPosition(self, p):
        """
        Permet d'obtenir la position Y de la période pour qu'elle ne se superpose pas avec les autres lors de l'affichage.
        @param p: la période à tester.
        @return un int correspondant à la ligne de la période sur l'affichage par rapport aux autres.
        """
        if p in self.__listeHauteur:
            return self.__listeHauteur[p]*self.getPeriodHeight()
        bannedHeight = []
        for per, haut in self.__listeHauteur.items():
            if per.intersectWith(p):
                bannedHeight.append(haut)
        for i in range(len(self.__listeHauteur)+2):
            if i not in bannedHeight:
                self.__listeHauteur[p] = i
                return self.__listeHauteur[p]*self.getPeriodHeight()

    def getSemaineOf(self, jour):
        """
        Renvoie le numéro de la ligne de la semaine correspondant au jour demandé.
        @param jour: datetime.date() correspondant au jour dont on veut savoir la semaine.
        @return le numéro de la semaine dans le mois à partir de 0.
        """
        return (jour.day + self.getJourDebut().weekday()-1) // 7

    ""
    #############
    # Setters : #
    #############
    ""
    def setMois(self, mois):
        """
        Permet de changer le mois d'affichage
        @param mois : <int> n° correspondant au mois (version ok pour datetime)
        """
        self.mois = mois
        self.updateAffichage()

    ""
    ##################################
    # Méthodes liées à l'affichage : #
    ##################################
    ""
    def changeAnnee(self, value):
        """
        Permet de changer le mois d'affichage
        @param value : <int> +/- 1 par rapport a l'année actuelle
        """
        self.annee += value
        self.getParametreAffichage().setLabelAnnee(self.annee)
        self.updateAffichage()

    def changeMoisAffiche(self, value):
        """
        Méthode qui permet de se balader entre les mois
        @param value : <int> +/- 1 nombre à rajouter a self.mois pour obtenir celui qu'on veut afficher
        """
        self.mois += value
        # On change l'année si besoin (+ gestion du dépassement)
        if self.mois > 12:
            self.mois = 1
            self.changeAnnee(1)
        elif self.mois < 1:
            self.mois = 12
            self.changeAnnee(-1)
        self.getDonneeCalendrier().getZoneAffichage().getParametreAffichage().changeMoisCombobox(self.mois)
        self.updateAffichage()

    def doConfiguration(self, paramAffichage):
        """
        Méthode pour éventuellement changer la barre d'outil
        secondaire quand ce panneau est actif.

        Ce widget diffère pour afficher "1 Mois" dans la liste (et désactive la liste).
        @override doConfiguration() in AbstractDisplayedCalendar().
        """
        paramAffichage.setPeriodeMode(True, self.mois, self.annee)
        self.getApplication().setModeEditionPeriode(True)
        self.getDonneeCalendrier().updateAffichage()

    def updateAffichage(self, force = False):
        """
        Permet de mettre à jour l'affichage.
        """
        self.can.delete(ALL)
        self.__listeHauteur = {}
        hh = 20
        w = self.can.winfo_width()
        h = self.can.winfo_height()
        self.can.create_rectangle(0, 0, w, hh, fill = "light grey")
        for i, j in enumerate(JOUR):
            self.can.create_text(int(i*w/7+w/14), int(hh/2), width = w, text = j)
            self.can.create_line(int(i*w/7), hh+1, int(i*w/7), h, fill = "light grey")
        for i in range(5):
            self.can.create_line(0, hh+(h-hh)/5*(i+1), w, hh+(h-hh)/5*(i+1))
        jour = self.getJourDebut()
        semaine = 1
        while jour.month == self.mois:
            self.can.create_text(int(jour.weekday())*w/7+5, semaine*(h-hh)/5+hh, anchor = "sw", text = jour.day)
            if jour.isoweekday()%7 == 0:
                semaine += 1
            jour += datetime.timedelta(days = 1)
        
        ############################
        # Affichage des périodes : #
        ############################
        
        NEW_TAG_ID = 0
        for p in self.getApplication().getPeriodManager().getPeriodes():

            if (p.getDebut().month != self.mois and p.getFin().month != self.mois) or p.getDebut().year != self.annee:
                continue

            jour = p.getDebut()
            # On va chercher le 1er jour
            i=1
            while jour.month != self.mois:
                jour = p.getDebut() + datetime.timedelta(days = i)
                i+=1
            semaine = self.getSemaineOf(jour)
            jourDebutSemaine = jour
            isFirst = 2
            #p.tag = str(NEW_TAG_ID)
            while jour < p.getFin():
                jour += datetime.timedelta(days = 1)
                if jour.weekday()%7 == 0:
                    self.can.create_rectangle(int(jourDebutSemaine.weekday())*w/7 + isFirst,
                                              semaine*(h-hh)/5+hh+self.getPeriodeYPosition(p),
                                              w,
                                              semaine*(h-hh)/5+hh+self.getPeriodeYPosition(p)+self.getPeriodHeight(),
                                              fill = p.getColor() if not p.isSelected() else "#0078FF", tags = [p.getUniqueID(), "DoubleForSet"])
                    isFirst = 0
                    semaine += 1
                    jourDebutSemaine = jour
            self.can.create_rectangle(int(jourDebutSemaine.weekday())*w/7 + isFirst,
                                      semaine*(h-hh)/5+self.getPeriodeYPosition(p)+hh,
                                      int(jour.weekday()+1)*w/7 -3,
                                      semaine*(h-hh)/5+self.getPeriodeYPosition(p)+hh+self.getPeriodHeight(),
                                      fill = p.getColor() if not p.isSelected() else "#0078FF", tags = [p.getUniqueID(), "DoubleForSet"])

            NEW_TAG_ID += 1
            self.can.tag_bind("DoubleForSet", '<Double-Button-1>', lambda e : self.getApplication().getPeriodManager().setActivePeriode(self.findItem(e)))

    def updateColor(self):
        """
        Permet de mettre à jour les couleurs des objets affichés.
        Ici, comme il n'y a pour le moment pas moyen de faire autrement,
        on redessine tout, comme un #updateAffichage() normale.
        """
        self.updateAffichage()

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def addSchedulable(self, schedulable, region = None):
        """
        Fonction qui rajoute une task/groupe, ne sert à rien ici donc "pass"
        """
        pass

    def clic(self, event, control = False):
        """
        Méthode appelée lors d'un clic sur le Canvas().
        @param event: Événement du clic.
        @param control=False: True si l'événement est avec le modifier dû à la touche Contrôle, False sinon.
        Si c'est avec la touche contrôle, alors la/les période(s) précédemment sélectionnées ne sont pas désélectionnées.
        """
        #x, y = event.x, event.y
        if not control:
            for p in self.getApplication().getPeriodManager().getPeriodes():
                p.setSelected(False)

        if self.findItem(event) is not None:
            self.findItem(event).setSelected(True if not control else not self.findItem(event).isSelected())
        self.updateAffichage()

    def findItem(self, event):
        """
        Retourne la période qui est à coté de l'event
        @return <periode> ou <None>
        """
        for item in self.can.find_overlapping(event.x, event.y, event.x, event.y):
            for tag in self.can.gettags(item):
                if tag == "current":
                    continue
                for p in self.getApplication().getPeriodManager().getPeriodes():
                    if p.getUniqueID() == tag:
                        return p
        else :
            return None

    def removeSchedulable(self, schedulable):
        """
        Fonction qui retire une task/groupe, ne sert à rien ici donc "pass"
        """
        pass

    def resetSchedulable(self):
        """
        Permet de vider self._list
        """
        pass
