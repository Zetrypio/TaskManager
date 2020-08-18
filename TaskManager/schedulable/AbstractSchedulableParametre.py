# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Frame, Label

from util.widgets.ColorButton import *

class AbstractSchedulableParametre(Notebook):
    """
    Classe abstraite contenant les attributs standards des schedulables
    ceux présent dans la classe abstraite AbstractSchedulableObject
    """
    def __init__(self, master, schedulable, **kw):
        """
        @param master      : <tkinter.frame> ou autre conteneur
        @param schedulable : <AbstractSchedulableObject> le schedulable dont les parametres sont a afficher Task/Groupe
        """
        self.__schedulable = schedulable
        super().__init__(master, **kw)

        self.__pageGeneral = Frame(self)
        self.__pageAvancee = Frame(self)
        self.add(self.__pageGeneral, text = "Général")
        self.add(self.__pageAvancee, text = "Avancée")


        # Variable modifiable
        self.__varNom = StringVar()
        self.__varPeriode = StringVar()
        #varCouleur = StringVar()
        # textDesc (je le met ici pour ne pas l'oublier)

        # Affectation des variables
        self.__varNom.set(self.getSchedulable().getNom())
        self.__varPeriode.set(self.getSchedulable().getPeriode().getNom())
        #varCouleur.set(self.getSchedulable().getColor())
        # textDesc (je le met ici pour ne pas l'oublier)

        # Attributs généraux :
        self._frameGeneral = LabelFrame(self.__pageGeneral, text = "Attributs généraux")
        self.__lbNom        = Label(      self._frameGeneral, text = "Nom :")
        self.__entryNom     = Entry(      self._frameGeneral, textvariable = self.__varNom)
        self.__lbPeriode    = Label(      self._frameGeneral, text = "Période :")
        self.__comboPeriode = Combobox(   self._frameGeneral, textvariable = self.__varPeriode, value = [p.getNom() for p in self.getSchedulable().getApplication().getPeriodManager().getPeriodes()], state = "readonly")
        self.__lbColor      = Label(      self._frameGeneral, text = "Couleur :")
        #colbut       = ColorButton(_frameGeneral, bg = varCouleur.get())
        self.__colbut       = ColorButton(self._frameGeneral, bg = self.getSchedulable().getColor())
        self.__lbDesc       = Label(      self._frameGeneral, text = "Description :")
        self.__textDesc     = Text(       self._frameGeneral, wrap = "word", height = 3, width = 30)
        self.__textDesc.insert(END, self.getSchedulable().getDescription()) # Car on peut pas mettre de variable
        self.__sep = Separator(           self._frameGeneral, orient = HORIZONTAL)

        # Attributs avancées :
        self._frameAdvanced = LabelFrame(self.__pageAvancee, text = "Options avancées")

        ## Affichage
        # Général
        self._frameGeneral.pack(side = TOP, fill = BOTH, expand = YES)
        self.__lbNom.grid(       row = 0, column = 0, sticky = "e" )
        self.__entryNom.grid(    row = 0, column = 1, sticky = "we")
        self.__lbPeriode.grid(   row = 1, column = 0, sticky = "e" )
        self.__comboPeriode.grid(row = 1, column = 1, sticky = "we")
        self.__lbColor.grid(     row = 2, column = 0, sticky = "e" )
        self.__colbut.grid(      row = 2, column = 1)
        self.__lbDesc.grid(      row = 3, column = 0, sticky = "e" )
        self.__textDesc.grid(    row = 4, column = 0, sticky = "we", columnspan = 2)
        self.__sep.grid(         row = 5, column = 0, sticky = "we", columnspan = 2, pady = 2)
        # Avancée
        self._frameAdvanced.pack(side = TOP, fill = BOTH, expand = YES)

    "" # Marque pour le repli de code
    #############
    # Getters : #
    #############
    ""
    def getSchedulable(self):
        """
        Getter pour le schedulable
        @return <AbstractSchedulableObject> l'objet en question
        """
        return self.__schedulable

    ""
    #############
    # onClose : #
    #############
    ""
    def onClose(self):
        """
        On change tout ce qu'il faut
        @change nom
        @change periode (with name)
        @change color
        @change description
        """
        self.getSchedulable().setNom(            self.__varNom.get())
        self.getSchedulable().setPeriodeWithName(self.__varPeriode.get())
        #self.getSchedulable().setColor(varCouleur.get())
        self.getSchedulable().setColor(         self.__colbut.get())
        self.getSchedulable().setDescription(   self.__textDesc.get("0.0", END))
