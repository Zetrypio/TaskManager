# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

from util.importPIL import *
from util.widgets.infobulle import *

from .dialog.gestionHeureCalendrierDialog import *

class ToolBar(Frame):
    """
    Classe représentant la barre d'outils, contenant juste les boutons.
    Cette classe possède une mise en forme automatique des boutons et des
    catégories. Les commandes des boutons doivent présentes dans le master.
    """
    def __init__(self, master, **kwargs):
        """
        Constructeur de la barre d'outil.
        @param master: master du tkinter.Frame() que cet objet est.
        @param **kwargs: Fonctionnalités d'affichage du tkinter.Frame() que cet objet est.
        """
        super().__init__(master, **kwargs)
        # Note : self.master est référence vers CalendarZone.

        self.lesCategories = [] # liste de cadre
        self.lesBoutonsEnListes = [] # liste qui va contenir toutes les autres liste de bouton (pour un affichage cool) lesBoutonsEnListes[catégorie][bouton]
        self.lesFramesDesBoutons = [] # tout est dans le nom ... lesFramesDesBoutons[categorie][frame]
        self._ajouterCategoriesEtBoutons()

    ""
    ##############
    # Méthodes : #
    ##############
    ""
    def _ajouterCategoriesEtBoutons(self):
        """
        Méthode pour ajouter tout les boutons de la barre d'outil.
        Bon pour une redéfinition dans des sous-classes.
        """
        # CADRE GESTION
        self._creationCategorie("Gestion") #cadre gestion
        # création des boutons
        self._creationBouton("heure", self.master.ajouterHeure, getImage("Ressources/textures/par defaut/gestion.png"), textVisible=True)
        self._creationBouton("jour", self.master.ajouterJour, getImage("Ressources/textures/par defaut/gestion.png"), textVisible=True)
        
        # CADRE VUE
        self._creationCategorie("Vue") #cadre vue
        # création des boutons
        self._creationBouton("sélectionner un jour", self.master.selectionnerJour, getImage("Ressources/textures/par defaut/selectionner_un_jour.png"))
        self._creationBouton("Afficher/masquer", self.master.afficherMasquerJour, getImage("Ressources/textures/par defaut/afficher masquer a.png"))
        
        # CADRE INTERVERTIR
        self._creationCategorie("Intervertir")
        # création des boutons
        self._creationBouton("Intervertir", self.master.deplacerIntervertir, getImage("Ressources/textures/par defaut/intervertir.png"))

        # CADRE DÉCALER
        self._creationCategorie("Décaler") #cadre Décaler
        # création des boutons
        self._creationBouton("toutes les activités -> jour", self.master.decalerJour, getImage("Ressources/textures/par defaut/decalage_J.png"))
        self._creationBouton("toutes les activités -> heure", self.master.decalerHeure, getImage("Ressources/textures/par defaut/decalage_H.png"))

        # CADRE GROUPE
        self._creationCategorie("Groupe") #cadre groupe
        # création des boutons
        self._creationBouton("grouper", self.master.grouper, getImage("Ressources/textures/par defaut/grouper.png"))
        self._creationBouton("dégrouper", self.master.degrouper, getImage("Ressources/textures/par defaut/degrouper.png"))
        
        # CADRE AVANCEMENT
        self._creationCategorie("Avancement") #cadre Avancement
        # création des boutons
        self._creationBouton("Validation", self.master.avancementMannuel, getImage("Ressources/textures/par defaut/case a cocher parfaite.png"))
        self._creationBouton("Jour fini", self.master.avancementJourFini, getImage("Ressources/textures/par defaut/avancement_Jour.png"))
        self._creationBouton("Normal", self.master.avancementNormal, getImage("Ressources/textures/par defaut/avancement normal.png"))

    def _creationBouton(self, texte, fonction = None, img = None, textVisible = False):
        """
        Permet de créer un bouton dans la dernière catégorie crée.
        L'ordre de création est important, car il est répercuté sur l'affichage.
        @param texte: Texte du bouton, quand textVisible = True ou que l'image manque.
        Ce texte sera aussi utilisé pour l'infobulle. TODO : Mettre un message d'infobulle à part, custom ?
        @param fonction = None: callback du bouton quand celui-ci est appuyé.
        @param img = None: Image à mettre sur le bouton, ou None si celui-ci n'as pas d'image.
        @param textVisible = False: True si on affiche toujours le texte, False sinon.
        """
        # si il n'y a plus de place dans les frames, on en fait une autre (et ça marche aussi s'il n'y en a pas encore) :
        if len(self.lesFramesDesBoutons[-1]) == len(self.lesBoutonsEnListes[-1])/2:
            self.lesFramesDesBoutons[-1].append(Frame(self.lesCategories[-1]))
            self.lesFramesDesBoutons[-1][-1].pack(side=TOP, expand=YES, fill=BOTH)

        # Création et placement du bouton :
        if textVisible:
            b = Button(self.lesFramesDesBoutons[-1][-1], text=texte, compound=LEFT, command=fonction, image = img, width = 0)
        else:
            b = Button(self.lesFramesDesBoutons[-1][-1], compound=LEFT, command=fonction, image = img, width = 0) # text=texte,
        b.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        self.lesBoutonsEnListes[-1].append(b)
        ajouterInfoBulle(b, self.lesCategories[-1].cget("text")+" "+texte)

    def _creationCategorie(self, texte):
        """
        Permet de créer une catégorie.
        L'ordre de création est important, car il est répercuté sur l'affichage.
        @param texte : le nom de la catégorie.
        """
        self.lesCategories.append(LabelFrame(self, text=texte))
        self.lesCategories[-1].pack(side=LEFT, fill=BOTH, expand=YES)

        # Liste vide à remplir de bouton :
        self.lesBoutonsEnListes.append([])
        
        # Liste qui va contenir les futurs frames
        self.lesFramesDesBoutons.append([]) 

    def changeAfficherMasquerMode(self, hide):
        """
        Méthode qui change l'image du bouton si des schedulables sont cachées
        @param hide : <bool> False alors il n'y a rien de masqué
        """
        if not hide:
            self.lesBoutonsEnListes[1][1].config(image = getImage("Ressources/textures/par defaut/afficher masquer a.png"))
        else:
            self.lesBoutonsEnListes[1][1].config(image = getImage("Ressources/textures/par defaut/afficher masquer b.png"))
