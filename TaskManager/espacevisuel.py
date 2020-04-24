# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from affichageDonnee import *


# En général, ça s'appelle une ToolBar - soit une barre d'outils en français.
class MenuOutil(Frame):
    """
    Classe représentant la barre d'outils, contenant juste les boutons.
    Cette classe possède une mise en forme automatique des boutons et des
    catégories. Les commandes des boutons doivent présentes dans le master.
    """
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers CalendarZone.
        
        self.lesCategories = [] # liste de cadre
        self.lesBoutonsEnListes = [] # liste qui va contenir toutes les autres liste de bouton (pour un affichage cool) lesBoutonsEnListes[catégorie][bouton]
        self.lesFramesDesBoutons = [] # tout est dans le nom ... lesFramesDesBoutons[categorie][frame]
        self._ajouterCategoriesEtBoutons()
        
    def _ajouterCategoriesEtBoutons(self):
        # CADRE AJOUTER
        self._creationCategorie("Ajouter") #cadre ajouter
        # création des boutons
        self._creationBouton("heure", self.master.ajouterHeure)
        self._creationBouton("jour", self.master.ajouterJour)
        
        # CADRE RETIRER
        self._creationCategorie("Retirer") #cadre retirer
        # création des bouton
        self._creationBouton("heure", self.master.retirerHeure)
        self._creationBouton("jour", self.master.retirerJour)
        
        # CADRE VUE
        self._creationCategorie("Vue") #cadre vue
        # création des boutons
        self._creationBouton("sélectionner un jour", self.master.selectionnerJour)
        self._creationBouton("Afficher/masquer", self.master.afficherMasquerJour)
        
        # CADRE DÉPLACER
        self._creationCategorie("Déplacer") #cadre Déplacer
        # création des boutons
        self._creationBouton("Activité -> Jour", self.master.deplacerActiviteeVersJour)
        self._creationBouton("Intervertir", self.master.deplacerIntervertir)
        
        # CADRE DÉCALER
        self._creationCategorie("Décaler") #cadre Décaler
        # création des boutons
        self._creationBouton("toutes les activitées -> jour", self.master.decalerJour)
        self._creationBouton("toutes les activitées -> heure", self.master.decalerHeure)
        
        # CADRE AVANCEMENT
        self._creationCategorie("Avancement") #cadre Avancement
        # création des boutons
        self._creationBouton("Retard", self.master.avancementRetard)
        self._creationBouton("Jour fini", self.master.avancementJourFini)        
        self._creationBouton("Normal", self.master.avancementNormal)

    
    def _creationCategorie(self, texte):
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

    def _creationBouton(self, texte, fonction = None):
        # si il n'y a plus de place dans les frames, on en fait une autre (et ça marche aussi s'il n'y en a pas encore) :
        if len(self.lesFramesDesBoutons[-1]) == len(self.lesBoutonsEnListes[-1])/2: 
            self.lesFramesDesBoutons[-1].append(Frame(self.lesCategories[-1]))
            self.lesFramesDesBoutons[-1][-1].pack(side=TOP, expand=YES, fill=BOTH)            

        # Création et placement du bouton :
        b = Button(self.lesFramesDesBoutons[-1][-1], text=texte, command=fonction, width = len(texte))
        b.pack(side=LEFT, expand=YES, fill=BOTH, padx=2, pady=2)
        self.lesBoutonsEnListes[-1].append(b)


class MenuOutilPeriode(MenuOutil):
    def __init__(self, master, periodeManager, **kwargs):
        self.periodeManager = periodeManager
        super().__init__(master, **kwargs)
    def _ajouterCategoriesEtBoutons(self):
        # CADRE Gestion des périodes
        self._creationCategorie("Gestion des périodes")
        # création des boutons
        self._creationBouton("Déplacer",                self.periodeManager.deplacerPeriode)
        self._creationBouton("Dupliquer",               self.periodeManager.dupliquerPeriode)
        self._creationBouton("Supprimer",               self.periodeManager.supprimerPeriode)
        # CADRE Division des périodes
        self._creationCategorie("Division des périodes")
        # création des boutons
        self._creationBouton("Scinder",                 self.periodeManager.scinderPeriode)
        self._creationBouton("Fusionner",               self.periodeManager.fusionnerPeriodes)
        # CADRE Tâches indépendantes
        self._creationCategorie("Tâches indépendantes")
        # création des boutons
        self._creationBouton("Lier à une période",      self.periodeManager.lierTachePeriode)
        self._creationBouton("Voir dans une autre vue", self.master.voirTacheDansVue)
        self._creationBouton("Supprimer",               self.master.supprimerTache)
        

class CalendarZone(Frame):
    def __init__(self, master = None, periodeManager = None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers l'Application.
        
        self.__isBarrePeriode = False
        # Barre du haut
        self.outilBar = MenuOutil(self) # frame avec tous les boutons outils
        self.outilBar.pack(side=TOP, fill=X, expand=NO)
        
        # Barre du haut pour les périodes
        self.outilBarPeriode = MenuOutilPeriode(self, periodeManager) # frame avec tous les boutons outils
        
        # Zone calendrier
        self.zoneDynamicCalendarFrame = ZoneAffichage(self) # frame avec la zone d'affichage des paramètre et la zone avec les données
        self.zoneDynamicCalendarFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    def getApplication(self):
        return self.master
    def setBarreOutilPeriode(self, value):
        self.__isBarrePeriode = value
        if value:
            self.outilBarPeriode.pack(side=TOP, fill=X, expand=NO)
            self.outilBar.pack_forget()
        else:
            self.outilBarPeriode.pack_forget()
            self.outilBar.pack(side=TOP, fill=X, expand=NO)
    def getBarreOutilActive(self):
        if self.__isBarrePeriode:
            return self.outilBarPeriode
        else:
            return self.outilBar

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
    
    # Pour la barre d'outil des périodes :
    def voirTacheDansVue(self):
        pass
    def supprimerTache(self):
        pass
    



   
if __name__=='__main__':
    import Application
    Application.main()
