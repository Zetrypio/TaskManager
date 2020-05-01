# -*- coding:utf-8 -*-
from tkinter.messagebox import *
from dialog import *
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
import datetime

JOUR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
class SuperTache(Frame):
    def __init__(self, master, task, **kwargs):
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est une référence vers AffichageCalendrier ou AffichageGantt, héritant de SuperCalendrier
        
        self.task = task

        self.texte = Text(self, wrap = "word", state = "normal", bg = self.task.getDisplayColor(), width=0, height=0)
        
        self.texte.insert(INSERT, task.nom) # On met le nom dedans
        self.texte.tag_add("titre", "1.0", "1.%s"%int(len(task.nom)))
        self.texte.tag_config("titre", font="Arial 12 bold") 
        
        self.texte.insert(END, "\n"+task.desc)
        self.texte.tag_add("corps", "2.0", "2.%s"%int(len(task.desc)))
        self.texte.tag_config("corps", font="Arial 10") 
        
        self.texte.config(state = "disabled") # Pour ne pas changer le texte dedans
        self.texte.pack(fill=BOTH, expand=YES)# On l'affiche une fois qu'il est tout beau.
        self.pack_propagate(False)

        #La selection des taches
        self.texte.bind("<Button-1>", self._clique)
        self.texte.bind("<Control-Button-1>", self.multiSelection)

    def getCalendrier(self):
        return self.master

    def multiSelection(self, e):
        """Permet d'envoyer l'objet à la methode dans SuperCalendrier"""
        self.getCalendrier().multiSelection(self.task)

    def _clique(self, e):
        self.getCalendrier().deselect()
        self.getCalendrier().select(self.task)

    def updateColor(self): # fonction pour mettre à jour la couleur
        try:
            self.texte.config(bg=self.task.getDisplayColor())
        except:
            self._report_exception()


class SuperCalendrier(Frame):
    def __init__(self, master = None, **kwargs):
        assert self.__class__ != SuperCalendrier # interdire instanciation direct (classe abstraite version simple)
        kwargs["bg"] = "light gray"
        Frame.__init__(self, master, **kwargs)
        # Note : self.master est référence vers DonneeCalendrier.

        # infos des heures :
        self.heureDebut = datetime.time(8, 0, 0)
        self.heureFin = datetime.time(17, 59, 0)

        # infos des jours :
        self.jourDebut = self.getDebutPeriode()
        self.nbJour = self.getLongueurPeriode()

        # liste des tâches :
        self.listeTask = []
        self.listeTaskAffichees = []


    def mouseClicked(self, event):
        self.deselect()

    def escapePressed(self, event):
        self.deselect()
    
    def updateTaskColor(self):
        for tache in self.listeTaskAffichees:
            tache.updateColor()

    def onIntervertir(self):pass # Juste pour qu'elle existe

    def multiSelection(self, task):
        task.inverseSelection()
        self.getDonneeCalendrier().updateTaskColor()

    def select(self, tache):
        """gere la selection"""
        tache.setSelected(True)
        self.getDonneeCalendrier().updateTaskColor()

    def deselect(self):
        self.getDonneeCalendrier().clearJourSelectionnes()
        for tache in self.getSelectedTask():
            tache.setSelected(False)
        self.getDonneeCalendrier().updateTaskColor()

    def getSelectedTask(self):
        return [task for task in self.listeTask if task.isSelected()]

    def selectTaskJour(self, jour, control=False):
        if not control:
            self.deselect()

        self.getDonneeCalendrier().addJourSelectionnes(jour)

        for task in self.listeTask:
            # Si on commence avant ou on est sur le jour et qu'on fini après ou sur le jour
            if task.getDebut().date() <= jour and task.getFin().date() >= jour:
                task.setSelected(True)
        self.updateTaskColor()

    def getDonneeCalendrier(self):
        return self.master.master

    def getApplication(self):
        return self.master.master.getApplication() # Skip le NoteBook

    def getLongueurPeriode(self):
        return 8 # TODO : À mettre à la longueur de la période.
    def getDebutPeriode(self):
        return datetime.date(2020, 4, 6); # TODO : À mettre au début de la période.
    def getFinPeriode(self):
        return self.getDebutPeriode() + datetime.timedelta(days = self.getLongueurPeriode())
        
    def getHeureDebut(self):
        return self.heureDebut
    def setHeureDebut(self, valeur):
        self.heureDebut = valeur
        self.updateAffichage()
        
    def getNbheure(self): # Retourne un int
        return self.getHeureFin().hour - self.getHeureFin().hour

    def getHeureFin(self):
        return self.heureFin
    def setHeureFin(self, valeur):
        self.heureFin = valeur
        self.updateAffichage()

    def getJourDebut(self):
        return self.jourDebut
    def setJourDebut(self, valeur):
        self.jourDebut = valeur + datetime.timedelta()
        self.updateAffichage()

    def getNbJour(self):
        return self.nbJour
    def setNbJour(self, valeur):
        self.nbJour = valeur
        self.updateAffichage()
    
    def getJourFin(self):
        return self.jourDebut + datetime.timedelta(days = self.nbJour)
    
    def rangeDate(self, jourA, jourB, last = True):
        jour = jourA + datetime.timedelta()
        while jour <= jourB:
            if jour == jourB and not last: break
            yield jour
            jour += datetime.timedelta(days = 1)

    def identify_region(self, x, y):
        """
        Renvoie la région à la position X et Y.
        X et Y sont relatifs à ce widget.

        La région doit être quelque chose qui doit permettre de
        savoir où ajouter une tâche si celle-ci n'a pas de début/période
        prédéfinie. (voir #addTask(tache, REGION = ...))

        Cela doit donc correspondre à un ensemble avec une date/heure
        de début, on utilisera pour cela la classe datetime.datetime().

        Méthode à redéfinir dans les sous-classes.
        """
        raise NotImplementedError

    def addTask(self, tache, region = None):
        """
      - Permet d'ajouter une tâche sur le panneau d'affichage.

      - Méthode à redéfinir dans les sous-classes, en appelant
        la variante parent (celle de SuperCalendrier), car celle-ci
        s'occuppe de mettre la tâche dans la liste et de demander la durée
        à l'utilisateur quand celle-ci n'est pas définie (càd: elle est de 0).

      - Cependant, la suite doit être redéfinie dans les sous-classes pour gérer
        l'affichage de la tâche.

      - Et le plus important : la méthode doit renvoyer la tâche avec sa durée prédéfinie.

      - Dans les sous-classes, ça donne :

        def addTask(self, tache, region = None):
            '''Permet d'ajouter une tâche, region correspond au début de la tâche si celle-ci n'en a pas.'''
            if (tache := SuperCalendrier.addTask(self, tache, region)) == None: # region est géré dans la variante parent : on ne s'en occupe plus ici.
                return

            ####################
            # Ajout graphique. #
            ####################
            ... # Note : on utilisera très probablement une liste, non ?
            ... # et peut-être une classe particulière, défini dans le même fichier ?
            ... # Quand je dis une liste, c'est une liste différente de self.listeTask,
                # car celle-ci existe déjà, mais qui contiendrait les cadres/panneaux des classes
                # que l'on va créer pour cette représentation. Cependant, on pourrais dire, si
                # c'est possible, que cette classe pourrait être utilisée pour plusieurs dispositions
                # si celles-cis sont similaires. Mais chaque disposition pourra aussi avoir sa classe
                # d'affichage d'une tâche custom.

            return tache # on revoie la tache avec son début et sa duree. TRÈS IMPORTANT.
        """
        if self.__class__ == SuperCalendrier:
            raise NotImplementedError
        if tache is None : return
        self.listeTask.append(tache)
        if region and tache.debut is None:
            # Important pour ne pas altérer l'originelle :
            # Cela permet de pouvoir Drag&Drop une même tâche
            # plusieurs fois.
            tache = tache.copy()
            tache.debut = region
        if tache.duree <= datetime.timedelta():
            tache.duree = self.askDureeTache()
            if not tache.duree:
                return None
        # SUITE À FAIRE DANS LES SOUS-CLASSES.
        return tache

    def askDureeTache(self):
        # Fonction quand on ferme le dialogue :
        duree = None
        def onClose(bouton):
            nonlocal duree
            if bouton == "Ok":
                duree = datetime.timedelta(days = int(d.get()), hours = int(h.get()), minutes = int(m.get()))
                if duree > datetime.timedelta():
                    fen.quit()
                    fen.destroy()
                else:
                    showerror("Durée invalide", "Veuillez mettre une durée plus grande que 0.")
            else:
                fen.destroy()
        def adapteHeureJour():
            """Adaptation des heures et des jours quand on augmente ou diminue trop les heures ou les minutes."""
            minutes = int(m.get())
            heures  = int(h.get())
            jours   = int(d.get())
            
            while minutes >= 60:
                minutes -= 60
                heures += 1
            while minutes < 0:
                minutes += 60
                heures -= 1
            while heures >= 24:
                heures -= 24
                jours += 1
            while heures < 0:
                heures += 24
                jours -= 1
            jours = max(0, min(jours, self.getLongueurPeriode()))
            
            m.set(minutes)
            h.set(heures)
            d.set(jours)
            
        # Création du dialogue :
        fen = Dialog(self, title = "Choix de la duree de la tâche",
                   buttons = ("Ok", "Annuler"), command = onClose, exitButton = ('Annuler',))
        # Widgets du dialogue :
        Label(fen, text = "Choisissez la durée de la Tâche").pack(side = TOP, fill = X)
        d = Spinbox(fen, from_ = 0, to = self.getLongueurPeriode(), increment = 1, width = 4)
        d.pack(side = LEFT)
        Label(fen, text = "Jours").pack(side = LEFT)
        h = Spinbox(fen, from_ = -1, to = 24, increment = 1, width = 4, command = adapteHeureJour)
        h.pack(side = LEFT)
        Label(fen, text = "Heures").pack(side = LEFT)
        m = Spinbox(fen, from_ = -1, to = 60, increment = 1, width = 4, command = adapteHeureJour)
        m.pack(side = LEFT)
        Label(fen, text = "Minutes").pack(side = LEFT)
        d.set(0)
        h.set(1)
        m.set(0)
        # lancement du dialogue:
        fen.activateandwait()
        return duree

    def updateAffichage(self):
        """
        Méthode pour mettre à jour l'affichage.
        Appelée lors de chaque changements avec
        setHeureDebut, setHeureFin, setJourDebut et setNbJour
        """
        raise NotImplementedError

    def doConfiguration(self, paramAffichage):
        """
        Méthode pour éventuellement changer la barre d'outil
        secondaire quand ce panneau est actif.
        
        Par défaut, fait un reset normal de cette barre.
        """
        self.getApplication().setModeEditionPeriode(False)
        paramAffichage.setStateListe(NORMAL)
        if self.getNbJour() == self.getLongueurPeriode():
            paramAffichage.setModeListe("Période")
        elif self.getNbJour() == 7:
            paramAffichage.setModeListe("1 semaine")
        elif self.getNbJour() == 1:
            paramAffichage.setModeListe("1 jour")
        else:
            paramAffichage.setModeListe("%s jours"%self.getNbJour())

if __name__=='__main__':
    import Application
    Application.main()
