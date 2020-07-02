# *-* coding:utf-8 *-*
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import tkinter.messagebox

from ..AbstractPage import *
from util.widgets.Dialog import askstring, askyesnowarning

"""
{"Name" : nomTheme,
            "Couleur principale": self.__lbColor1.cget("text") or "#ffffff",
            "Couleur secondaire": self.__lbColor2.cget("text") or "#ffffff",
            "Couleur tertiaire" : self.__lbColor3.cget("text") or "#ffffff",
            "# Couleur par élément" : "",
            "General-Couleur du texte" : self.__varGCDT or "Couleur principale",
            "Liste des tâches-Couleur de fond" : self.__varLDTCDF or "Couleur principale",
            "Ajout des tâches-Couleur de fond" : self.__varADTCDF or "Couleur principale",
            "Zone des onglets-Couleur de fond" : self.__varZDOCDF or "Couleur principale",
            "Zone des onglets-Couleur de fond du calendrier" : self.__varZDOCDFDC or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage Gantt" : self.__varZDOCDFDAG or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage des périodes" : self.__varZDOCDFDADP or "Couleur principale",
            "Zone des onglets-Couleur de fond de l'affichage des tâches suivantes" : self.__varZDOCDFDADTS or "Couleur principale",
            "Zone de l'affichage-Couleur de fond" : self.__varZDACDF or "Couleur principale",
            "Barre d'outils principale-Couleur de fond" : self.__varBOPCDF or "Couleur principale",
            "Barre d'outils principale-Couleur des boutons" : self.__varBOPCDB or "Couleur principale",
            "Barre d'outils secondaire-Couleur de fond" : self.__varBOSCDF or "Couleur principale",
            "Barre d'outils secondaire-Couleur des boutons" : self.__varBOSCDB or "Couleur principale",
            "# Autre que les couleurs" : "",
            "Boutons de ttk" : self.__varTtkButton.get()}
"""

NOMFICHIER = os.sep + "theme"


class PageTheme(AbstractPage):
    def __init__(self, master, **kwargs):
         # Note : self.master renvoie a ParametrageZone
         # Note : Si on rajoute une option ne pas oublier d'ajouter la variable de controle à self._listData.append([variable, "texte explicatif"])

        super().__init__(master, nom = "Thème", iid_parent ="-General", **kwargs)

        # Traitement du fichier .ini
        # self.getData() = ConfigParser()
        self.readFile(NOMFICHIER) # Prise de conscience de ce qu'il y a dedans


        self.__currentElem = None # iid de l'élément sélectionné dans le TreeView

        self.__listeVarTheme = ["nom"]


        self.__varAdapteTexteTache = BooleanVar()
        self._listData.append([self.__varAdapteTexteTache, "Couleur adaptative"])
        self.__caseAdaptTexteTache = Checkbutton(self._mFrame, text="Changer la couleur du texte d'une tache (noir/blanc) en fonction de la couleur de fond de la tache", variable=self.__varAdapteTexteTache)

        ## Frame choix thème
        self.__frameChoixTheme = Frame(self._mFrame)
        # Widget
        self.__lbCombo = Label(self.__frameChoixTheme, text = "Sélectionnez un thème")
        self.__varTheme = StringVar()
        self._listData.append([self.__varTheme, "Theme choisi"])
        self.__comboThemeExistant = Combobox(self.__frameChoixTheme, state="readonly", textvariable = self.__varTheme)
        self.__comboThemeExistant.bind("<<ComboboxSelected>>", self.loadTheme)
        self.__btnSuppr = Button(self.__frameChoixTheme, text="Supprimer", command = self.supprimerTheme)


        self.__sep = Separator(self._mFrame, orient=HORIZONTAL)
        self.__lbThemeCustom = Label(self._mFrame, text = "Crée votre thème personnalisé")

        ## Frame des couleur du thème custom
        self.__frameCouleurCustom = Frame(self._mFrame)

        # Widgets
        self.__lbColorTxt1 = Label(self.__frameCouleurCustom, text="Couleur principale :")
        self.__boutonColor1 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(1), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb1 = StringVar()
        self.__listeVarTheme.append(self.__varLb1)
        self.__lbColor1 = Label(self.__frameCouleurCustom, textvariable=self.__varLb1)

        self.__lbColorTxt2 = Label(self.__frameCouleurCustom, text="Couleur secondaire :")
        self.__boutonColor2 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(2), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb2 = StringVar()
        self.__listeVarTheme.append(self.__varLb2)
        self.__lbColor2 = Label(self.__frameCouleurCustom, textvariable=self.__varLb2)

        self.__lbColorTxt3 = Label(self.__frameCouleurCustom, text="Couleur tertiaire :")
        self.__boutonColor3 = TkButton(self.__frameCouleurCustom, command = lambda e=None : self.__askcolor(3), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb3 = StringVar()
        self.__listeVarTheme += [self.__varLb3] # Le str vide pour le commentaire
        self.__lbColor3 = Label(self.__frameCouleurCustom, textvariable=self.__varLb3)
        # Config des var
        self.__varLb1.set(self.__boutonColor1.cget("bg"))
        self.__varLb2.set(self.__boutonColor2.cget("bg"))
        self.__varLb3.set(self.__boutonColor3.cget("bg"))


        self.__frameZoneSelection = Frame(self._mFrame)
        ## TreeView des zones dont les couleurs sont configurables
        self.__tree = Treeview(self.__frameZoneSelection)
        self.__tree.bind("<ButtonRelease-1>", self.onclick)
        self.__scrollbar = Scrollbar(self.__frameZoneSelection, orient = VERTICAL, command = self.__tree.yview)
        self.__tree.configure(yscrollcommand = self.__scrollbar.set)

        # Ajout des options
        self.__tree.insert("", END, text="General", iid="General")
        self.__tree.insert("General", END, text="Couleur du texte", iid="General"+"-Couleur du texte")
        self.__varGCDT = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varGCDT)
        self.__tree.insert("", END, text="Liste des tâches", iid="Liste des tâches")
        self.__tree.insert("Liste des tâches", END, text="Couleur de fond", iid="Liste des tâches"+"-Couleur de fond")
        self.__varLDTCDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varLDTCDF)
        self.__tree.insert("", END, text="Ajout des tâches", iid="Ajout des tâches")
        self.__tree.insert("Ajout des tâches", END, text="Couleur de fond", iid="Ajout des tâches"+"-Couleur de fond")
        self.__varADTCDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varADTCDF)
        self.__tree.insert("", END, text="Zone des onglets", iid="Zone des onglets")
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond", iid="Zone des onglets"+"-Couleur de fond")
        self.__varZDOCDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDOCDF)
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond du calendrier", iid="Zone des onglets"+"-Couleur de fond du calendrier")
        self.__varZDOCDFDC = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDOCDFDC)
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage Gantt", iid="Zone des onglets"+"-Couleur de fond de l'affichage Gantt")
        self.__varZDOCDFDAG = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDOCDFDAG)
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage des périodes", iid="Zone des onglets"+"-Couleur de fond de l'affichage des périodes")
        self.__varZDOCDFDADP = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDOCDFDADP)
        self.__tree.insert("Zone des onglets", END, text="Couleur de fond de l'affichage des taches suivantes", iid="Zone des onglets"+"-Couleur de fond de l'affichage des taches suivantes")
        self.__varZDOCDFDADTS = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDOCDFDADTS)
        self.__tree.insert("", END, text="Zone de l'affichage", iid="Zone de l'affichage")
        self.__tree.insert("Zone de l'affichage", END, text="Couleur de fond", iid="Zone de l'affichage"+"-Couleur de fond")
        self.__varZDACDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varZDACDF)
        self.__tree.insert("", END, text="Barre d'outils principale", iid="Barre d'outils principale")
        self.__tree.insert("Barre d'outils principale", END, text="Couleur de fond", iid="Barre d'outils principale"+"-Couleur de fond")
        self.__varBOPCDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varBOPCDF)
        self.__tree.insert("Barre d'outils principale", END, text="Couleur des boutons", iid="Barre d'outils principale"+"-Couleur des boutons")
        self.__varBOPCDB = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varBOPCDB)
        self.__tree.insert("", END, text="Barre d'outils secondaire", iid="Barre d'outils secondaire")
        self.__tree.insert("Barre d'outils secondaire", END, text="Couleur de fond", iid="Barre d'outils secondaire"+"-Couleur de fond")
        self.__varBOSCDF = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varBOSCDF)
        self.__tree.insert("Barre d'outils secondaire", END, text="Couleur des boutons", iid="Barre d'outils secondaire"+"-Couleur des boutons")
        self.__varBOSCDB = StringVar() # variable pour stocker la couleur | initiaux de la iid
        self.__listeVarTheme.append(self.__varBOSCDB)

        # Coté sélection de la couleur
        self.__comboCouleur = Combobox(self.__frameZoneSelection, value=['Couleur principale', "Couleur secondaire", "Couleur tertiaire", "Couleur personnalisé"], state = "readonly")
        self.__lbColorTxt4 = Label(self.__frameZoneSelection, text="Couleur personnalisé :")
        self.__boutonColor4 = TkButton(self.__frameZoneSelection, command = lambda e=None : self.__askcolor(4), width = 4, relief = GROOVE, bg = "#ffffff", activebackground = "#ffffff")
        self.__varLb4 = StringVar()
        self.__lbColor4 = Label(self.__frameZoneSelection, textvariable=self.__varLb4)
        self.__varLb4.set(self.__boutonColor4.cget("bg"))

        # Frame de bas de page
        self.__frameZoneBasSelection = Frame(self.__frameZoneSelection)
        self.__varTtkButton = BooleanVar()
        self.__listeVarTheme += [self.__varTtkButton] # Le str vide pour le commentaire
        self.__caseTtkButton = Checkbutton(self.__frameZoneBasSelection, text="Voulez-vous utiliser les boutons de ttk ?", variable=self.__varTtkButton)
        self.__btnEnregistrement = Button(self.__frameZoneBasSelection, text="Enregistrer", command=lambda e=None :self.enregistrer(self.getNomCombobox()))
        self.__btnEnregistrementSous = Button(self.__frameZoneBasSelection, text="Enregistrer-sous", command=self.enregistrerSous)




        # Affichage
        self.__caseAdaptTexteTache.grid(column = 0, row = 0, sticky="WE")

        self.__frameChoixTheme.grid(column = 0, row = 1, sticky="WE", pady=2)
        self.__lbCombo.pack(side = LEFT, expand = NO)
        self.__comboThemeExistant.pack(side = LEFT, fill=Y, expand= YES)
        self.__btnSuppr.pack(side=LEFT)

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
        self.__frameZoneBasSelection.pack(side=BOTTOM, fill=BOTH) # ici pour le plaçage sinon il concerne btnEnregistrement/Sous et caseTtkButton
        self.__scrollbar.pack(expand = NO, fill = BOTH, side = LEFT)
        # Pack la solution de prévisualisation en side=TOP
        self.__comboCouleur.pack(side = LEFT)
        self.__lbColorTxt4.pack(side=LEFT)
        self.__boutonColor4.pack(side=LEFT)
        self.__lbColor4.pack(side=LEFT)

        self.__caseTtkButton.pack(side=LEFT)
        self.__btnEnregistrement.pack(side = LEFT, pady=3)
        self.__btnEnregistrementSous.pack(side=LEFT)


        # Final
        self.__listeVarTheme.append(StringVar()) # Pour la gestion d'une clé supplémentaire quand on passe par Data pour lire
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

    def getNomCombobox(self):
        return self.__varTheme.get()

    def setNomCombobox(self, nom):
        self.__varTheme.set(nom)
        self.__stateSaveBtn()

    def __stateSaveBtn(self):
        # Fonction qui gere l'état du bouton d'enregistrememnt
        self.readFile(NOMFICHIER, lireDef = False, lireCfg = True)
        if  self.getNomCombobox().upper() not in self.getData().sections():
            self.__btnEnregistrement.config(state = "disabled")
            self.__btnSuppr.config(state = "disabled")
        else:
            self.__btnEnregistrement.config(state = "normal")
            self.__btnSuppr.config(state = "normal")


    def configCombobox(self):
        """
        Fonction qui va ajouter tous les thèmes qui ont été créer et tous les thèmes créé par l'utilisateur
        """
        self.readFile(NOMFICHIER)
        # Mise en place dans le combobox du thème actuel
        self.__listValueComboTheme = []
        for section in self.getData().sections():
            self.__listValueComboTheme.append(self.getData()[section]["Name"])

        self.__comboThemeExistant.config(value=self.__listValueComboTheme)
        # A voir comment on fait, si on garde etc
        self.setNomCombobox(self.getApplication().getData().getCurrentThemeName())

    def dictTheme(self, nomTheme):
        """
        Fonction qui retourne un dictionnaire (enfin je crois que c'est ça) avec toutes les valeurs que contient la page
        """
        # Pour récupérer ce qu'on a commencé
        self.recupCouleur()
        dict = {}
        for indice, cle in enumerate(self.getData()[self.getData().getCurrentThemeName().upper()]):
            if indice == 0: # Pour le nom c'est un srting tout court
                print(indice, cle, self.__listeVarTheme[indice])
                dict[cle] = nomTheme
            else:
                print(indice, cle, self.__listeVarTheme[indice].get())
                # Ici c'est des StringVar() donc il faut un ".get()"
                dict[cle] = self.__listeVarTheme[indice].get()
        print("dict final :", dict)
        return dict

    def enregistrer(self, nom):
        """
        Enregistre les modifications
        @param nom : <str> nom du thème
        """
        print("nom : ",nom)
        # On doit lire le fichier en entier pour avoir les clés existantes
        self.readFile(NOMFICHIER)
        dict = self.dictTheme(nom)

        # On enregistre
        self.readFile(NOMFICHIER, lireDef = False, lireCfg = True)
        self.getData()[nom.upper()] = dict
        self.getData().sauv(self.getProfilFolder() + NOMFICHIER + ".cfg")

    def enregistrerSous(self):
        """
        On demande le nom du nouveau thème pour ensuite le créer
        """
        self.readFile(NOMFICHIER)
        name = askstring(self, "Choississez un nom", "Quelle est le nom de ce nouveau theme ?")
        if name is None:
            return
        while name.upper() in self.getData().sections():
            messagebox.showwarning("Nom incorrect", "Vous ne pouvez pas utiliser \"%s\" comme nom car c'est déjà le nom d'un autre thème.\n La casse n'est pas pris en compte."%name)
            name = askstring(self, "Choississez un nom", "Quelle est le nom de ce nouveau theme ?")
            # Quand on clique sur annuler
            if name is None:
                return

        # Enregistrement
        self.enregistrer(name)
        """
        self.readFile(NOMFICHIER) # Lire les clés qui existent
        dict = self.dictTheme(name)
        self.readFile(NOMFICHIER, lireDef=False)
        self.getData()[name.upper()] = dict

        self.getData().sauv(self.getProfilFolder() + NOMFICHIER + ".cfg")
        """
        # Bonus de enregistrer sous
        self.getApplication().getData().setCurrentThemeName(name)
        self.configCombobox()
        self.__varTheme.set(name)
        self.loadTheme()

    def supprimerTheme(self):
        """
        Fonction qui supprime le thème sélectionné dans le combobox
        """

        if askyesnowarning(title = "Supprimer ce thème", message="Êtes-vous sur de vouloir supprimer %s définitivement ?"%self.getNomCombobox()):
            self.readFile(NOMFICHIER, lireDef = False, lireCfg = True)
            self.getData().remove_section(self.get.upper())
            self.getData().sauv(self.getProfilFolder() + NOMFICHIER + ".cfg")

            self.configCombobox()
            self.loadTheme()

    def loadTheme(self, event=None):
        """
        Lorsqu'on change le combobox il faut recharger les couleurs en place du thème choisi
        + gérer la disponibilité de enregistrer
        """
        self.readFile(NOMFICHIER) # Si on change de page, il faut rappeler qui on est + sureté
        theme = self.getData()[self.getNomCombobox().upper()]


        # Permet de charger les options pour les sauvegarder
        for indice, cle in enumerate(theme):
            if indice == 0:
                self.__listeVarTheme[indice] = theme.get(cle)
            else:
                self.__listeVarTheme[indice].set(theme.get(cle))

        self.__boutonColor1.config(bg=theme["Couleur principale"], activebackground=theme["Couleur principale"])
        self.__boutonColor2.config(bg=theme["Couleur secondaire"], activebackground=theme["Couleur secondaire"])
        self.__boutonColor3.config(bg=theme["Couleur tertiaire"], activebackground=theme["Couleur tertiaire"])

        if self.__currentElem is not None:
            self.__comboCouleur.set(theme[self.__currentElem])

        self.__stateSaveBtn()

    def chercheComboValeur(self, val):
        """
        Fonction qui va chercher à quel iid val correspond, et va retourne la variable qui est lié a cet iid
        @param val : <str> iid sur le treeview
        @return var : <StringVar> qui est la valeur liée à l'iid (qui est aussi a clé du dictionnaire)
        """
        if val == "General"+"-Couleur du texte":
            return self.__varGCDT
        elif val == "Liste des tâches"+"-Couleur de fond":
            return self.__varLDTCDF
        elif val == "Ajout des tâches"+"-Couleur de fond":
            return self.__varADTCDF
        elif val == "Zone des onglets"+"-Couleur de fond":
            return self.__varZDOCDF
        elif val == "Zone des onglets"+"-Couleur de fond du calendrier":
            return self.__varZDOCDFDC
        elif val == "Zone des onglets"+"-Couleur de fond de l'affichage Gantt":
            return self.__varZDOCDFDAG
        elif val == "Zone des onglets"+"-Couleur de fond de l'affichage des périodes":
            return self.__varZDOCDFDADP
        elif val == "Zone des onglets"+"-Couleur de fond de l'affichage des taches suivantes":
            return self.__varZDOCDFDADTS
        elif val == "Zone de l'affichage"+"-Couleur de fond":
            return self.__varZDACDF
        elif val == "Barre d'outils principale"+"-Couleur de fond":
            return self.__varBOPCDF
        elif val == "Barre d'outils principale"+"-Couleur des boutons":
            return self.__varBOPCDB
        elif val == "Barre d'outils secondaire"+"-Couleur de fond":
            return self.__varBOSCDF
        elif val == "Barre d'outils secondaire"+"-Couleur des boutons":
            return self.__varBOSCDB

    def recupCouleur(self):
        """
        Va cherche la couleur et la valeur associé (ligne du treeview) concerné par cette couleur
        """
        def recupAuBonEndroit():
            """ Fonction embarqué qui va retourner la valeur qu'il faut selon le choix su combobox """
            ou = self.__comboCouleur.get()
            if ou == "Couleur personnalisé" or ou == "":
                return self.__varLb4.get()
            else:
                return ou

        if self.__currentElem is not None:
            # A la recherche qui est self.__currentElem et assignation de la bonne valeur
            self.chercheComboValeur(self.__currentElem).set(recupAuBonEndroit())


    def onclick(self, e):
        """
        Pour le treeview
        """
        self.readFile(NOMFICHIER)

        self.recupCouleur() # Enregistrement de la valer de l'ancienne case
        iidElementSelectionne = self.__tree.focus()

        # Si on est dans une catégorie c'est pas une clé donc pas de valeur
        try:
            self.__comboCouleur.set(self.chercheComboValeur(iidElementSelectionne).get())
            self.__currentElem = iidElementSelectionne
        except:pass

    def appliqueEffet(self, application):
        self._makeDictAndSave()

