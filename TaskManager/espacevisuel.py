# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime
from affichageDonnee import *
from importPIL import *
from infobulle import *
import gestionCalendrier



#img = Image.open("Ressources/textures/ECDV/a_test.png")

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
        # CADRE GESTION
        self._creationCategorie("Gestion") #cadre gestion
        # création des boutons
        self._creationBouton("heure", self.master.ajouterHeure, getImage("Ressources/textures/gestion.png"), textVisible=True)
        self._creationBouton("jour", self.master.ajouterJour, getImage("Ressources/textures/gestion.png"), textVisible=True)
        
        # CADRE VUE
        self._creationCategorie("Vue") #cadre vue
        # création des boutons
        self._creationBouton("sélectionner un jour", self.master.selectionnerJour, getImage("Ressources/textures/selectionner_un_jour.png"))
        self._creationBouton("Afficher/masquer", self.master.afficherMasquerJour, getImage("Ressources/textures/afficher masquer a.png"))
        
        # CADRE INTERVERTIR
        self._creationCategorie("Intervertir")
        # création des boutons
        self._creationBouton("Intervertir", self.master.deplacerIntervertir, getImage("Ressources/textures/intervertir.png"))

        # CADRE DÉCALER
        self._creationCategorie("Décaler") #cadre Décaler
        # création des boutons
        self._creationBouton("toutes les activitées -> jour", self.master.decalerJour, getImage("Ressources/textures/decalage_J.png"))
        self._creationBouton("toutes les activitées -> heure", self.master.decalerHeure, getImage("Ressources/textures/decalage_H.png"))

        # CADRE GROUPE
        self._creationCategorie("Groupe") #cadre groupe
        # création des boutons
        self._creationBouton("Grouper", self.master.grouper, getImage("Ressources/textures/grouper.png"))
        self._creationBouton("dégrouper", self.master.degrouper, getImage("Ressources/textures/degrouper.png"))
        
        # CADRE AVANCEMENT
        self._creationCategorie("Avancement") #cadre Avancement
        # création des boutons
        self._creationBouton("Validation", self.master.avancementRetard, getImage("Ressources/textures/case à cocher parfaite.png"))
        self._creationBouton("Jour fini", self.master.avancementJourFini, getImage("Ressources/textures/avancement_Jour.png"))
        self._creationBouton("Normal", self.master.avancementNormal, getImage("Ressources/textures/avancement normal.png"))

    
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

    def _creationBouton(self, texte, fonction = None, img = None, textVisible = False):
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


class MenuOutilPeriode(MenuOutil):
    def __init__(self, master, periodeManager, **kwargs):
        self.periodeManager = periodeManager
        super().__init__(master, **kwargs)
    def _ajouterCategoriesEtBoutons(self):
        # CADRE Gestion des périodes
        self._creationCategorie("Gestion des périodes")
        # création des boutons
        self._creationBouton("Déplacer",                self.periodeManager.deplacerPeriode,   textVisible=True)
        self._creationBouton("Dupliquer",               self.periodeManager.dupliquerPeriode,  textVisible=True)
        self._creationBouton("Supprimer",               self.periodeManager.supprimerPeriode,  textVisible=True)
        # CADRE Division des périodes
        self._creationCategorie("Division des périodes")
        # création des boutons
        self._creationBouton("Scinder",                 self.periodeManager.scinderPeriode,    textVisible=True)
        self._creationBouton("Fusionner",               self.periodeManager.fusionnerPeriodes, textVisible=True)
        # CADRE Tâches indépendantes
        self._creationCategorie("Tâches indépendantes")
        # création des boutons
        self._creationBouton("Lier à une période",      self.periodeManager.lierTachePeriode,  textVisible=True)
        self._creationBouton("Voir dans une autre vue", self.master.voirTacheDansVue,          textVisible=True)
        self._creationBouton("Supprimer",               self.master.supprimerTache,            textVisible=True)
        

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
        min = self.getDonneeCalendrier().getHeureDebut()
        max = datetime.timedelta(hours=23) - datetime.timedelta(hours=self.getDonneeCalendrier().getHeureFin().hour)
        max2 = self.getDonneeCalendrier().getHeureFin()
        nbHeure = max2.hour - min.hour
        nb, pos = gestionCalendrier.ajouterHeure(min, max, nbHeure)
        if nb is not None and pos is not None:
            if pos == "Avant":
                min = datetime.time(min.hour - nb)
                self.getDonneeCalendrier().setHeureDebut(min)
            elif pos == "Apres":
                max = datetime.time(max2.hour + nb, max2.minute)
                self.getDonneeCalendrier().setHeureFin(max)


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

    def grouper(self):
        pass
    def degrouper(self):
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
