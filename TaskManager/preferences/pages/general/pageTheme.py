# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor

from ..AbstractPage import *

class PageTheme(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
        super().__init__(master, nom = "Thème", iid_parent ="-General", **kwargs)

        self.__currentElem = None # iid de l'élément sélectionné dans le TreeView
        self.__listValueComboTheme = ["Classique"]


        self.__varAdapteTexteTache = BooleanVar()
        self.__caseAdaptTexteTache = Checkbutton(self._mFrame, text="Changer la couleur du texte d'une tache (noir/blanc) en fonction de la couleur de fond de la tache", variable=self.__varAdapteTexteTache)

        ## Frame choix thème
        self.__frameChoixTheme = Frame(self._mFrame)
        # Widget
        self.__lbCombo = Label(self.__frameChoixTheme, text = "Sélectionnez un thème")
        self.__comboThemeExistant = Combobox(self.__frameChoixTheme, value=self.__listValueComboTheme, state="readonly")


        self.__sep = Separator(self._mFrame, orient=HORIZONTAL)
        self.__lbThemeCustom = Label(self._mFrame, text = "Crée votre thème personnalisé")

        ## Frame des couleur du thème custom
        self.__frameCouleurCustom = Frame(self._mFrame)

        # Widgets
        self.__lbColorTxt1 = Label(self.__frameCouleurCustom, text="Couleur principale :")
        self.__boutonColor1 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(1), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb1 = StringVar()
        self.__lbColor1 = Label(self.__frameCouleurCustom, textvariable=self.__varLb1)

        self.__lbColorTxt2 = Label(self.__frameCouleurCustom, text="Couleur secondaire :")
        self.__boutonColor2 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(2), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb2 = StringVar()
        self.__lbColor2 = Label(self.__frameCouleurCustom, textvariable=self.__varLb2)

        self.__lbColorTxt3 = Label(self.__frameCouleurCustom, text="Couleur tertiaire :")
        self.__boutonColor3 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(3), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb3 = StringVar()
        self.__lbColor3 = Label(self.__frameCouleurCustom, textvariable=self.__varLb3)
        # Config des var
        self.__varLb1.set(self.__boutonColor1.cget("bg"))
        self.__varLb2.set(self.__boutonColor2.cget("bg"))
        self.__varLb3.set(self.__boutonColor3.cget("bg"))


        self.__frameZoneSelection = Frame(self._mFrame)
        ## TreeView des zones dont les couleurs sont configurables
        self.__tree = Treeview(self.__frameZoneSelection)
        self.__tree.bind("<Button-1>", self.onclick)
        self.__scrollbar = Scrollbar(self.__frameZoneSelection, orient = VERTICAL, command = self.__tree.yview)
        self.__tree.configure(yscrollcommand = self.__scrollbar.set)

        # Ajout des options
        self.__tree.insert("", END, text="Liste des tâches", iid="Liste des tâches")
        self.__tree.insert("Liste des tâches", END, text="Couleur de fond", iid="Liste des tâches"+"Couleur de fond")
        self.__varLDTCDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("", END, text="Ajout des tâches", iid="Ajout des tâches")
        self.__tree.insert("Ajout des tâches", END, text="Couleur de fond", iid="Ajout des tâches"+"Couleur de fond")
        self.__varADTCDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("", END, text="Zone des onglets", iid="Zone des onglets")
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond", iid="Zone des onglets"+"Couleur de fond")
        self.__varZDOCDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond du calendrier", iid="Zone des onglets"+"Couleur de fond du calendrier")
        self.__varZDOCDFDC = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage Gantt", iid="Zone des onglets"+"Couleur de fond de l'affichage Gantt")
        self.__varZDOCDFDAG = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage des périodes", iid="Zone des onglets"+"Couleur de fond de l'affichage des périodes")
        self.__varZDOCDFDADP = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage des taches suivantes", iid="Zone des onglets"+"Couleur de fond de l'affichage des taches suivantes")
        self.__varZDOCDFDADTS = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("", END, text="Zone de l'affichage", iid="Zone de l'affichage")
        self.__tree.insert("Zone de l'affichage", END, text="Couleur de fond", iid="Zone de l'affichage"+"Couleur de fond")
        self.__varZDACDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("", END, text="Barre d'outils principale", iid="Barre d'outils principale")
        self.__tree.insert("Barre d'outils principale", END, text="Couleur de fond", iid="Barre d'outils principale"+"Couleur de fond")
        self.__varBOPCDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Barre d'outils principale", END, text="Couleur des boutons", iid="Barre d'outils principale"+"Couleur de boutons")
        self.__varBOPCDB = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("", END, text="Barre d'outils secondaire", iid="Barre d'outils secondaire")
        self.__tree.insert("Barre d'outils secondaire", END, text="Couleur de fond", iid="Barre d'outils secondaire"+"Couleur de fond")
        self.__varBOSCDF = None # variable pour stocker la couleur | initiaux de la iid
        self.__tree.insert("Barre d'outils secondaire", END, text="Couleur des boutons", iid="Barre d'outils secondaire"+"Couleur de boutons")
        self.__varBOSCDB = None # variable pour stocker la couleur | initiaux de la iid

        # Coté sélection de la couleur
        self.__comboCouleur = Combobox(self.__frameZoneSelection, value=['Couleur principale', "Couleur secondaire", "Couleur tertiaire", "Couleur personnalisé"], state = "readonly")
        self.__lbColorTxt4 = Label(self.__frameZoneSelection, text="Couleur personnalisé :")
        self.__boutonColor4 = TkButton(self.__frameZoneSelection, command = lambda e=None : self.__askcolor(4), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb4 = StringVar()
        self.__lbColor4 = Label(self.__frameZoneSelection, textvariable=self.__varLb4)
        self.__varLb4.set(self.__boutonColor4.cget("bg"))
        self.__btnEnregistrement = Button(self.__frameZoneSelection, text="Enregistrer", command=self.enregistrer)







        # Affichage
        self.__caseAdaptTexteTache.grid(column = 0, row = 0, sticky="WE")

        self.__frameChoixTheme.grid(column = 0, row = 1, sticky="WE", pady=2)
        self.__lbCombo.pack(side = LEFT, expand = NO)
        self.__comboThemeExistant.pack(side = LEFT, fill=Y, expand= YES)

        self.__sep.grid(column = 0, row=2, sticky="WE", pady=2)
        self.__lbThemeCustom.grid(column = 0, row = 3, sticky="WE")

        self.__frameCouleurCustom.grid(column = 0, row = 4, sticky="WE")
        self.__lbColorTxt1.pack(side=LEFT)
        self.__boutonColor1.pack(side=LEFT)
        self.__lbColor1.pack(side=LEFT)
        self.__lbColorTxt2.pack(side=LEFT)
        self.__boutonColor2.pack(side=LEFT)
        self.__lbColor2.pack(side=LEFT)
        self.__lbColorTxt3.pack(side=LEFT)
        self.__boutonColor3.pack(side=LEFT)
        self.__lbColor3.pack(side=LEFT)

        self.__frameZoneSelection.grid(column = 0, row = 5, sticky="NSEW")
        self.__tree.pack(side = LEFT, fill = BOTH, expand = NO)
        self.__scrollbar.pack(expand = NO, fill = BOTH, side = LEFT)
        # Pack la solution de prévisualisation en side=TOP
        self.__comboCouleur.pack(side = LEFT)
        self.__lbColorTxt4.pack(side=LEFT)
        self.__boutonColor4.pack(side=LEFT)
        self.__lbColor4.pack(side=LEFT)
        self.__btnEnregistrement.pack(side = BOTTOM, pady=3)


        self.configCombobox()

    def __askcolor(self, value):
        color = askcolor()[1]
        # Si on clique sur la croix on annule l'opération
        if color is None:
            return

        if value == 1:
            self.__boutonColor1.config(bg = color, activebackground = color)
            self.__varLb1.set(color)
        elif value == 2:
            self.__boutonColor2.config(bg = color, activebackground = color)
            self.__varLb2.set(color)
        elif value == 3:
            self.__boutonColor3.config(bg = color, activebackground = color)
            self.__varLb3.set(color)
        elif value == 4:
            self.__boutonColor4.config(bg = color, activebackground = color)
            self.__varLb4.set(color)

        if not "Thème personalisé" in self.__listValueComboTheme:
            self.__listValueComboTheme.append("Thème personalisé")
            self.__comboThemeExistant.config(value = self.__listValueComboTheme)
        self.__comboThemeExistant.set(self.__listValueComboTheme[-1])

    def configCombobox(self):
        """
        Fonction qui va ajouter tous les thèmes qui ont été créer et tous les thèmes créé par l'utilisateur
        """
        # Mise en place dans le combobox du thème actuel
        self.__comboThemeExistant.set(self.getApplication().getData().getCurrentThemeName())

    def enregistrer(self): pass #TODO : enregistrer toutes les options
    """
    On demande le nom du nouveau thème
    On enregistre tous les __varSEFSJ
    """

    def appliqueEffet(self, application):
        # Récupération des valeurs
        nomTheme = self.__comboThemeExistant.get()
        adaptCouleur = self.__varAdapteTexteTache.get()

        # Enregistrements
        self.getApplication().getData().setCurrentThemeName(nomTheme)
        self.getApplication().getData().setAdaptColorTask(adaptCouleur)


    def onclick(self, e):
        def recupAuBonEndroit():
            """ Fonction embarqué qui va retourner la valeur qu'il faut selon le choix su combobox """
            ou = self.__comboCouleur.get()
            if ou == "Couleur principale":
                return self.__varLb1
            elif ou == "Couleur secondaire":
                return self.__varLb2
            elif ou == "Couleur tertiaire":
                return self.__varLb3
            elif ou == "Couleur personnalisé":
                return self.__varLb4
        # On récupère la cage qu'on a cliqué
        iidElementSelectionne = self.__tree.focus()
        if self.__currentElem is not None:
            # A la recherche qui est self.__currentElem
            if   self.__currentElem == "Liste des tâches"+"Couleur de fond":
                self.__varLDTCDF = recupAuBonEndroit()
            elif self.__currentElem == "Ajout des tâches"+"Couleur de fond":
                self.__varADTCDF = recupAuBonEndroit()
            elif self.__currentElem == "Zone des onglets"+"Couleur de fond":
                self.__varZDOCDF = recupAuBonEndroit()
            elif self.__currentElem == "Zone des onglets"+"Couleur de fond du calendrier":
                self.__varZDOCDFDC = recupAuBonEndroit()
            elif self.__currentElem == "Zone des onglets"+"Couleur de fond de l'affichage Gantt":
                self.__varZDOCDFDAG = recupAuBonEndroit()
            elif self.__currentElem == "Zone des onglets"+"Couleur de fond de l'affichage des périodes":
                self.__varZDOCDFDADP = recupAuBonEndroit()
            elif self.__currentElem == "Zone des onglets"+"Couleur de fond de l'affichage des taches suivantes":
                self.__varZDOCDFDADTS = recupAuBonEndroit()
            elif self.__currentElem == "Zone de l'affichage"+"Couleur de fond":
                self.__varZDACDF = recupAuBonEndroit()
            elif self.__currentElem == "Barre d'outils principale"+"Couleur de fond":
                self.__varBOPCDF = recupAuBonEndroit()
            elif self.__currentElem == "Barre d'outils principale"+"Couleur de boutons":
                self.__varBOPCDB = recupAuBonEndroit()
            elif self.__currentElem == "Barre d'outils secondaire"+"Couleur de fond":
                self.__varBOSCDF = recupAuBonEndroit()
            elif self.__currentElem == "Barre d'outils secondaire"+"Couleur de boutons":
                self.__varBOSCDB = recupAuBonEndroit()

        self.__currentElem = iidElementSelectionne
