# -*- coding:utf-8 -*-
# Installation auto au début:
from util.importPIL import *
# Imports :
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from tkinter.messagebox import showerror, showinfo
import os
import json

from affichages.CalendarZone import *
from affichages.periode.Periode import *
from affichages.periode.PeriodManager import *
from schedulable.groupe.Groupe import *
from schedulable.task.TaskEditor import *

from util.util import *

from MenuBar import *
from preferences.fenetrePreferences import *
from preferences.themes.themeLoader import *
from dataManager.data import *
from dataManager.ProfilManager import *
from dataManager.BindingManager import *

CHARGERPRECONFIG = False

# CECI est la CORRECTION d'un BUG :
style = Style()

def fixed_map(option):
    """
    Returns the style map for 'option' with any styles starting with
    ("!disabled", "!selected", ...) filtered out

    style.map() returns an empty list for missing options, so this should
    be future-safe
    """
    return [elm for elm in style.map("Treeview", query_opt=option)
            if elm[:2] != ("!disabled", "!selected")]

style.map("Treeview",
          foreground=fixed_map("foreground"),
          background=fixed_map("background"))


class Application(Frame):
    """
    Application Globale.
    """
    def __init__(self, master = None, **kwargs):
        """
        Constructeur de l'application.
        @param master: master du tkinter.Frame() que cet objet est.
        @param **kwargs: paramètre de configurations du tkinter.Frame() que cet objet est.
        """
        super().__init__(master, **kwargs)

        # Liste de clés qui permettent de référé à une tache précise
        self.listKey = []
        os.makedirs(os.path.expanduser("~/.taskManager/"), exist_ok = True)

        self.__data = Data()

        # Début de l'instanciation
        self.winfo_toplevel().title("Gestionnaire de calendrier")
        self.periodManager = PeriodManager(self)

        ## Preferences
        # À mettre près la création de la fenêtre car le ProfilManagera besoin de la fenêtre pour en changer le titre
        self.__profilManager  = ProfilManager(self)
        self.__BindingManager = BindingManager(self) # À mettre après le ProfilManager car il faut savoir quel fichier de binding charger
        self.menu = MenuBar(self.winfo_toplevel(), self) # Il faut le mettre après le BindingManagerpour les accelerator
        self.prefFen = FenetrePreferences(self)

        # Continuation de l'instanciation
        self.taskEditor = TaskEditor(self, self.menu, self.periodManager)
        self.taskEditor.pack(side=LEFT, fill = BOTH, expand = NO)
        self.calendar = CalendarZone(self, self.periodManager)
        self.calendar.pack(side=LEFT, fill = BOTH, expand = YES)

        ## Bindings
        self.bind_all("<<preferences>>", lambda e=None:self.preferences())
        self.bind_all("<<save-file>>"  , lambda e=None:self.save())
        self.bind_all("<<restart>>"    , lambda e=None:self.restart())
        self.bind_all("<<open-file>>"  , lambda e=None:self.open())
        self.bind_all("<<quit>>"       , lambda e=None:self.quitter())

        # Set des bindings mécanique en lien avec le bindingManager

        #self.bind_all("<Control-r>", lambda e : self.event_generate("<<restart>>"))

        for binding in self.getBindingIn("Application"):
            for key in self.getBindingIn("Application")[binding]["bindings"]:
                self.bind_all(key, lambda e, binding = binding : self.event_generate("<<" + binding + ">>"), add=1)
        if not CHARGERPRECONFIG:
            self.__load()


    "" # Marque pour que le repli de code fasse ce que je veux
    #############
    # Getters : #
    #############
    ""
    def getBindingManager(self):
        """ Retourne le Binding Manager """
        return self.__BindingManager

    def getBindingIn(self, categorie):
        """
        Permet d'obtenir les combinaisons
        @param categorie : <str> nom de la catégorie dont on veux les bindings
                          exemple : "Application"
        @return <dict> contenant tous les bindings
        """
        return self.getBindingManager().getBindings()[categorie]

    def getData(self):
        """ Retourne le Gestionnaire des données """
        return self.__data

    def getDonneeCalendrier(self):
        """
        Permet d'obtenir le DonneeCalendrier.
        @return le DonneeCalendrier.
        """
        return self.calendar.getDonneeCalendrier()

    def getPanneauActif(self):
        """
        Permet d'obtenir le panneau actif dans les affichages de calendrier.
        @return le panneau actif dans les affichages de calendrier.
        """
        return self.calendar.getPanneauActif()
    def getPeriodManager(self):
        """
        Permet d'obtenir le PeriodManager.
        @return le periodeManager.
        """
        return self.periodManager

    def getProfilManager(self):
        """ Retourne le Profil Manager """
        return self.__profilManager

    def getTaskEditor(self):
        """
        Permet d'obtenir le TaskEditor.
        @return le TaskEditor.
        """
        return self.taskEditor

    ""
    ######################################
    # Redéfinition de certaines méthodes #
    # Pour une meilleure expérience      #
    ######################################
    ""
    def destroy(self):
        """
        Redéfinition de la méthode pour supprimer aussi la fenêtre parente
        """
        super().destroy()
        try:
            self.winfo_toplevel().destroy() # Pour détruire aussi la fenêtre parente
        except:pass

    ""
    ###########################
    # Traitement des fichiers #
    ###########################
    ""
    def __load(self):
        """
        Permet de charger les périodes enregistrées dans periode.json
        """
        ## Si le fichier n'existe pas, on ne fait rien. Il sera créé lors de la prochaine sauvegarde.
        if not os.path.exists(self.getData().getProfilFolder() + "periodes.json"):
            return

        ## Chargement du fichier
        with open(self.getData().getProfilFolder() + "periodes.json", "r", encoding="utf-8") as f:
            data = load(f)

        ## Création des périodes
        for periode in data["periodes"]:
            dataPeriode = data["periodes"][periode]
            # On crée la période
            p = Periode.load(dataPeriode, self.getPeriodManager())
            # On l'ajoute
            self.getPeriodManager().ajouter(p)
        
        ## On active une période.
        self.getDonneeCalendrier().switchPeriode()

    def save(self):
        """
        Fonction qui va enregistrer toutes les données
        """
        d = {}
        d["periodes"] = {}
        for periode in self.getPeriodManager().getPeriodes():
            d["periodes"][periode.getNom()] = periode.saveByDict()

        with open(self.getData().getProfilFolder() + "periodes.json", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4)

    ""
    #####################
    # Autres méthodes : #
    #####################
    ""
    def preferences(self):
        self.prefFen.activateandwait()

    def restart(self):
        """
        Restarter de l'application.
        """
        try:
            self.save() # Pour être sûr, même si c'est fait dans le finally du main aussi.
        except BaseException as e:
            showerror("Erreur Fatale", "Erreur Fatale de lors de l'enregistrement :\n%s : %s"%(e.__class__.__name__, e))
        else:
            if sys.platform.startswith("win"):
                command = "start pyw -3.8 "
            else:
                command = "pythonw3 " # À tester sur mac ou linux (mais bon mac ne supporte pas l'application de toutes façon...).
            command += sys.argv[0]
            os.system(command)
            raise SystemExit(0)

    def setModeEditionPeriode(self, enEdition):
        """
        Permet de switcher entre le mode période et le mode normal.
        @param enEdition: True pour période, False sinon.
        """
        self.calendar.setBarreOutilPeriode(enEdition)
        if enEdition:
            self.taskEditor.filter(type = ("Période", "Tâche indépendante"))
            self.taskEditor.setEditionPeriode(True)
            pass
        else:
            self.taskEditor.filter(type = ("Tâche", "Tâche indépendante"))
            self.taskEditor.setEditionPeriode(False)
            pass

## Main :
def main():
    """Fonction main, principale du programme."""
    app = Application()


    w = app.winfo_toplevel().winfo_screenwidth()
    h = app.winfo_toplevel().winfo_screenheight()
    app.winfo_toplevel().geometry("%sx%s+%s+%s"%(int(0.9*w), int(0.8*h), int(0.05*w), int(0.05*h)))
    app.update()
    try:
        app.winfo_toplevel().state("zoomed")
    except:
        pass
    app.pack(expand = YES, fill = BOTH)
    
    if CHARGERPRECONFIG:
        # Création d'une période préfaite
        periodeSemaine = Periode(app.getPeriodManager(),
                                 "semaine",
                                 datetime.date(2020, 7, 4),
                                 datetime.date(2020, 7, 27),
                                 "semaine pour faciliter les calculs",
                                 color = "#7FFF7F")
        app.getPeriodManager().ajouter(periodeSemaine)

        # Création de tâches préfaites (c'est du lore)
        periodeSemaine.addPrimitiveSchedulable(Task("B",  periodeSemaine, "", "#7CF0F7", datetime.datetime(2020, 7,  8,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
        periodeSemaine.addPrimitiveSchedulable(Task("C",  periodeSemaine, "", "#C2F77C", datetime.datetime(2020, 7,  8, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
        periodeSemaine.addPrimitiveSchedulable(Task("E",  periodeSemaine, "", "#5D7CDC", datetime.datetime(2020, 7, 12, 10, 0, 0), datetime.timedelta(3,0,0, 0, 0, 1)))
        periodeSemaine.addPrimitiveSchedulable(Task("F",  periodeSemaine, "", "#FA6FFF", datetime.datetime(2020, 7,  8, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))
        periodeSemaine.addPrimitiveSchedulable(Task("Joyeux anniversaire", periodeSemaine,
                                    "Gâteau au chocolat et ne pas oublier la crême anglaise", "#85FAB7",
                                    datetime.datetime(2020, 7, 26, 12, 0, 0), datetime.timedelta(0,0,0, 0, 0, 5)))

        # Création d'un groupe préfait
        tacheA1 = Task("A1", periodeSemaine, "", "#F77CAA", datetime.datetime(2020, 7,  6,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1))
        tacheA2 = Task("A2", periodeSemaine, "", "#42A69A", datetime.datetime(2020, 7,  6, 10, 0, 0), datetime.timedelta(0,0,0, 0, 0, 2))
        group = Groupe("Mon Groupe", periodeSemaine, "description", "#FF88FF")
        group.addTask(tacheA1)
        group.addTask(tacheA2)
        periodeSemaine.addPrimitiveSchedulable(group)

        # Et une autre tâche
        periodeSemaine.addPrimitiveSchedulable(Task("D",  periodeSemaine, "", "#B97CF7", datetime.datetime(2020, 7, 12,  8, 0, 0), datetime.timedelta(0,0,0, 0, 0, 1)))

        # Update :
        app.getTaskEditor().redessiner()
        app.getDonneeCalendrier().switchPeriode()
    
    
    try:
        app.mainloop()
        try:
            app.destroy()
        except:
            pass
    except SystemExit:
        raise
    except BaseException as e:
        Frame().winfo_toplevel().withdraw()
        app._report_exception()
        showerror("Erreur Fatale", "Erreur Fatale de l'application.\nL'application va essayer d'enregistrer.\n%s : %s"%(e.__class__.__name__, e))
    finally:
        try:
            app.save()
        except BaseException as e:
            Frame().winfo_toplevel().withdraw()
            app._report_exception()
            showerror("Erreur Fatale", "Erreur Fatale de lors de l'enregistrement :\n%s : %s"%(e.__class__.__name__, e))
