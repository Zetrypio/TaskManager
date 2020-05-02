# -*- coding:utf-8 -*-
from .ToolBar import *

class PeriodToolBar(ToolBar):
    def __init__(self, master, periodeManager, **kwargs):
        self.periodeManager = periodeManager
        super().__init__(master, **kwargs)
    def _ajouterCategoriesEtBoutons(self):
        # CADRE Gestion des périodes
        self._creationCategorie("Gestion des périodes")
        # création des boutons
        self._creationBouton("Déplacer",                self.periodeManager.deplacerPeriode,   getImage("Ressources/textures/periode/deplacer.png"),   textVisible=False)
        self._creationBouton("Dupliquer",               self.periodeManager.dupliquerPeriode,  getImage("Ressources/textures/periode/dupliquer.png"),  textVisible=False)
        self._creationBouton("Supprimer",               self.periodeManager.supprimerPeriode,  getImage("Ressources/textures/periode/supprimer.png"),  textVisible=True)
        # CADRE Division des périodes
        self._creationCategorie("Division des périodes")
        # création des boutons
        self._creationBouton("Scinder",                 self.periodeManager.scinderPeriode,    getImage("Ressources/textures/periode/scinder.png"),    textVisible=False)
        self._creationBouton("Fusionner",               self.periodeManager.fusionnerPeriodes, getImage("Ressources/textures/periode/fusiioooon.png"), textVisible=False)
        # CADRE GESTION Tâches indépendantes
        self._creationCategorie("Gestion des tâches indépendantes")
        # création des boutons
        self._creationBouton("Lier à une période",      self.periodeManager.lierTachePeriode,  getImage("Ressources/textures/periode/lier tache indé.png"),  textVisible=False)
        self._creationBouton("Supprimer",               self.master.supprimerTache,            getImage("Ressources/textures/periode/supprimer.png"),            textVisible=True)
        # CADRE VUE Tâches indépendantes
        self._creationCategorie("Vue des tâches indépendantes")
        # Création des bouton(s)
        self._creationBouton("Voir dans une autre vue", self.master.voirTacheDansVue,          getImage("Ressources/textures/periode/changer vue tache inde.png"),          textVisible=False)
        

