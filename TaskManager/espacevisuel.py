# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from affichageDonnee import *
from importPIL import *
from infobulle import *



#img = Image.open("Ressources/textures/ECDV/a_test.png")

# En général, ça s'appelle une ToolBar - soit une barre d'outils en français.
class MenuOutil(Frame):
    """
    Classe représentant la barre d'outils, contenant juste les boutons.
    Cette classe possède une mise en forme automatique des boutons et des
    catégories. Les commandes des boutons doivent présentes dans le master.
    """
    def __init__(self, master, **kwargs):
        kwargs["bg"] = "green"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers CalendarZone.
        
        self.lesCategories = [] # liste de cadre
        self.lesBoutonsEnListes = [] # liste qui va contenir toutes les autres liste de bouton (pour un affichage cool) lesBoutonsEnListes[catégorie][bouton]
        self.lesFramesDesBoutons = [] # tout est dans le nom ... lesFramesDesBoutons[categorie][frame]
        
        # CADRE AJOUTER
        self.__creationCategorie("Ajouter") #cadre ajouter
        # création des boutons
        self.__creationBouton("heure", master.ajouterHeure, getImage("Ressources/textures/ajouter.png"), textVisible=True)
        self.__creationBouton("jour", master.ajouterJour, getImage("Ressources/textures/ajouter.png"), textVisible=True)
        
        # CADRE RETIRER
        self.__creationCategorie("Retirer") #cadre retirer
        # création des bouton
        self.__creationBouton("heure", master.retirerHeure, getImage("Ressources/textures/retirer.png"), textVisible=True)
        self.__creationBouton("jour", master.retirerJour, getImage("Ressources/textures/retirer.png"), textVisible=True)
        
        # CADRE VUE
        self.__creationCategorie("Vue") #cadre vue
        # création des boutons
        self.__creationBouton("sélectionner un jour", master.selectionnerJour, getImage("Ressources/textures/selectionner_un_jour.png"))
        self.__creationBouton("Afficher/masquer", master.afficherMasquerJour, getImage("Ressources/textures/afficher masquer a.png"))
        
        # CADRE INTERVERTIR
        self.__creationCategorie("Intervertir")
        # création des boutons
        self.__creationBouton("Intervertir", master.deplacerIntervertir, getImage("Ressources/textures/intervertir.png"))

        # CADRE DÉCALER
        self.__creationCategorie("Décaler") #cadre Décaler
        # création des boutons
        self.__creationBouton("toutes les activitées -> jour", master.decalerJour, getImage("Ressources/textures/decalage_J.png"))
        self.__creationBouton("toutes les activitées -> heure", master.decalerHeure, getImage("Ressources/textures/decalage_H.png"))
        
        # CADRE AVANCEMENT
        self.__creationCategorie("Avancement") #cadre Avancement
        # création des boutons
        self.__creationBouton("Validation", master.avancementRetard, getImage("Ressources/textures/case à cocher parfaite.png"))
        self.__creationBouton("Jour fini", master.avancementJourFini, getImage("Ressources/textures/avancement_Jour.png"))
        self.__creationBouton("Normal", master.avancementNormal, getImage("Ressources/textures/avancement normal.png"))

    
    def __creationCategorie(self, texte):
        """
        Permet de créer une catégorie.
        @param texte : le nom de la catégorie.
        """
        self.lesCategories.append(LabelFrame(self, text=texte))
        self.lesCategories[-1].pack(side=LEFT, fill=BOTH, expand=YES)

        # Liste vide à remplir de bouton :
        self.lesBoutonsEnListes.append([])
        
        # Liste qui va contenir les futurs frames
        self.lesFramesDesBoutons.append([]) 

    def __creationBouton(self, texte, fonction = None, img = None, textVisible = False):
        # si il n'y a plus de place dans les frames, on en fait une autre (et ça marche aussi s'il n'y en a pas encore) :
        if len(self.lesFramesDesBoutons[-1]) == len(self.lesBoutonsEnListes[-1])/2: 
            self.lesFramesDesBoutons[-1].append(Frame(self.lesCategories[-1]))
            self.lesFramesDesBoutons[-1][-1].pack(side=TOP, expand=YES, fill=BOTH)            

        # Création et placement du bouton :
        if textVisible:
            b = Button(self.lesFramesDesBoutons[-1][-1], text=texte, compound=LEFT, command=fonction, image = img)
        else:
            b = Button(self.lesFramesDesBoutons[-1][-1], compound=LEFT, command=fonction, image = img) # text=texte,
        b.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        self.lesBoutonsEnListes[-1].append(b)
        ajouterInfoBulle(b, self.lesCategories[-1].cget("text")+" "+texte)


class CalendarZone(Frame):
    def __init__(self, master = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers l'Application.
        
        # Barre du haut
        self.outilBar = MenuOutil(self) # frame avec tous les boutons outils
        self.outilBar.pack(side=TOP, fill=X, expand=NO)
        
        # Zone calendrier
        self.zoneDynamicCalendarFrame = ZoneAffichage(self) # frame avec la zone d'affichage des paramètre et la zone avec les données
        self.zoneDynamicCalendarFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    def ajouterHeure(self):
        pass
    def ajouterJour(self):
        pass

    def retirerHeure(self):
        pass
    def retirerJour(self):
        pass

    def selectionnerJour(self):
        pass
    def afficherMasquerJour(self):
        pass

    def deplacerActiviteeVersJour(self):
        pass
    def deplacerIntervertir(self):
        pass

    def decalerJour(self):
        pass
    def decalerHeure(self):
        pass

    def avancementRetard(self):
        pass
    def avancementJourFini(self):
        pass
    def avancementNormal(self):
        pass

    def getPanneauActif(self):
        return self.zoneDynamicCalendarFrame.getPanneauActif()
    def getDonneeCalendrier(self):
        return self.zoneDynamicCalendarFrame.getDonneeCalendrier()
    



   
if __name__=='__main__':
    import Application
    Application.main()
