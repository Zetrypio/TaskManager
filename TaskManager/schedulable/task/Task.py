# -*- coding:utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame, Button as TkButton
from tkinter.colorchooser import askcolor
import datetime
import random

from ..AbstractSchedulableObject import *

from util.util import *
from .dialog.datetimeDialog import *
from .dialog.askEditTask import *
from .TaskInDnd import *

from affichages.items.DatetimeItemPart import *
from affichages.items.content.DisplayableTask import *

class Task(AbstractSchedulableObject):
    """Classe définissant une tâche."""
    def __init__(self, nom, periode, desc="", color="white",
                 debut=None, duree=None,
                 rep=-1, nbrep = 0,
                 parent = None,
                 done = False,
                 dependances = None, dependantes = None,
                 id = None):
        """
        @param nom         : nom de la tâche.
        @param periode     : Période de la tâche, peut être None.
        @param desc        : description.
        @param color       : couleur avec un nom compatible avec les noms de couleurs tkinter.
        @param debut       : datetime. du début.
        @param duree       : datetime.
        @param rep         : temps entre répétition.
        @param nbrep       : nombre de répétitions.
        @param dependances : <list Task>
        @param dependantes : <list Task>
        @param id          : <str> contient l'id de la tache
        """
        # Constructeur parent :
        super().__init__(nom, periode, desc, color)
        
        # Informations temporelles :
        self.__debut = (debut + datetime.timedelta()) if debut is not None else None # Faire une copie et check nonNull
        self.__duree = (duree + datetime.timedelta()) if duree is not None else None
        
        # Informations des répétitions :

        self.__rep   = rep    # répétition
        self.__nbrep = nbrep  # nombre de répétitions
        
        # Parent : L'utilise-t-on pour les groupes aussi ?
        self.__parent = parent

        # Est-ce que la tâche est faite ?
        self.__done = done or False

        # Pour reconnaitre une task parmi toutes
        self.__uniqueID = id if id is not None else self.setUniqueID()

        # Liste des dépendances pour les liens
        self.__dependances = dependances if dependances else []
        self.__dependantes = dependantes if dependantes else []

        self.updateStatut()

        if self.isContainer():
            # Attribut présent que quand on est un conteneur : est-ce une bonne idée ?
            self.__subtasks = []

    def __str__(self):
        """Return a nice string representation of this object."""
        return "Task: %s, from %s to %s, %s"%(self.getNom(), self.getDebut() or "Unknown", self.getFin() or "Unknown", self.getStatut())

    "" # Marque pour repli de code
    ###############################
    # Constructeurs alternatifs : #
    ###############################
    ""
    @staticmethod
    def load(d, p):
        """
        Constructeur alternatif (en tant que méthode statique) qui crée une tache
        à partir des informations d'enregistrement que cette tâche aurait pu produire.
        @param d : dictionnaire qu'aurait créé cette tâche si on lui demandait d'enregistrer...
        @param p : période de la tâche.
        @return la tâche nouvellement créée.
        """
        t = Task(nom     = d["nom"],
            periode = p,
            desc    = d["desc"],
            color   = d["color"],
            debut   = strToDatetime(d["debut"]),
            duree   = strToTimedelta(d["duree"]),
            rep     = strToTimedelta(d["rep"]),
            nbrep   = d["nbrep"],
            done    = d["done"],
            id      = d["id"])
        # On crée les sous tâches si elles existent :
        if d["subtasks"] is not None:
            for dataSubTask in d["subtasks"]:
                subTask = Task.load(dataSubTask, p)
                t.addSubTask(subTask)
        return t
    ""
    #######################################################
    # Méthode de l'interface ITaskEditorDisplayableObject #
    # implémentée par la superclasse de cette classe :    #
    #######################################################
    ""
    def getHeader(self):
        """
        Permet de donner la ligne d'entête de cet objet dans l'affichage du Treeview() du TaskEditor().
        @return Le nom suivi du statut
        @specified by getHeader() in ITaskEditorDisplayableObject().
        """
        return self.getNom(), self._statut

    def iterateDisplayContent(self, displayDependances = True, displayDependantes = True):
        """
        Permet de donner les lignes de contenu de cet objet dans l'affichage du Treeview() du TaskEditor().
        @yield les informations à afficher (y en a pas mal et elles sont parfois conditionnelles).
        @specified by iterateDisplayContent() in ITaskEditorDisplayableObject().
        """
        # Note : on yield par paires.
        if not self.isContainer():
            yield "Début :",           self.getDebut()
            yield "Durée :",           self.getDuree()
            yield "Fin :",             self.getFin()
            yield "Nombre rep :",      self.__nbrep
            yield "Temps entre rep :", self.__rep
            if displayDependances:
                a = {
                    "displayDependances": True,
                    "displayDependantes": False
                }
                yield "Dépendances :", len(self.__dependances)
                yield a
                yield from self.__dependances
            if displayDependantes:
                a = {
                    "displayDependances": False,
                    "displayDependantes": True
                }
                yield "Dépendantes :", len(self.__dependantes)
                yield a
                yield from self.__dependantes
        if (self.__parent is None           # Ne pas répéter les descriptions identiques dans les sous-tâches.
        and self.getDescription().strip()): # Ne pas afficher les descriptions vides.
            yield "Description :", self.getDescription()
        if self.isContainer():
            a = {
                "displayDependances": displayDependances,
                "displayDependantes": displayDependantes
            }
            yield "Instances :", len(self.getSubTasks())
            yield a
            yield from self.getSubTasks()

    def setRMenuContent(self, taskEditor, rmenu):
        """
        Permet de rajouter les commandes au RMenu() de cet objet si il est présent.
        Si cet objet n'a pas besoin de RMenu() dans le TaskEditor(), il faut simplement
        que cette méthode retourne False
        @param taskEditor : permet de faire des interactions avec le TaskEditor().
        @param rmenu : le RMenu() sur lequel rajouter les commandes et tout et tout.
        @return True car le RMenu() existe.
        @specified by getRMenuContent() in ITaskEditorDisplayableObject().
        """
        # Ajout des menus :
        # Si c'est un conteneur :
        if not self.isContainer() and self.__parent is None:
            rmenu.add_command(label="Transformer en une tâche déplaçable", command=lambda: self.transformToDnd(taskEditor, rmenu))
            rmenu.add_separator()
        # Dans tout les cas :
        rmenu.add_command(label = "Éditer %s"%self.getNom(), command = lambda : askEditTask(self))
        rmenu.add_command(label = "Supprimer %s"%self, command=lambda: self.delete(taskEditor.getApplication()))
        return True

    ""
    ########################################
    # Définition des méthodes abstraites : #
    # de la superclasse.                   #
    ########################################
    ""
    def acceptLink(self):
        """
        Permet de savoir si l'objet peut être à l'origine d'un lien, sans se soucier
        de la destination pour le moment encore inconnu.
        @return True si l'objet est en capacité de faire des liens, False sinon.
        """
        return self._statut != "Inconnu" # and self.getParent() is None

    def acceptLinkTo(self, schedulable):
        """
        Permet de savoir si un lien est possible entre cet objet et l'objet reçu, peu importe le sens,
        peu importe si le lien existe déjà.
        @param schedulable: l'autre objet dont on doit faire le lien avec cet objet.
        """
        return isinstance(schedulable, Task) and not self.intersectWith(schedulable)

    def createDisplayableInstance(self, frame, part):
        """
        Permet de créer une instance de la version affichable d'une tâche.
        @param frame: master du tkinter.Frame() qu'est l'objet créé par cette méthode.
        @param part: DatetimeItemPart() nécessaire pour savoir quelle partie de la tâche à afficher.
        """
        # Ici, on s'en fiche de la part.
        return DisplayableTask(frame, self, part)

    def copy(self):
        """
        Permet d'obtenir une copie de la tâche
        @return une copie de la tâche.
        """
        t = Task(self.getNom(), self.getPeriode(), self.getDescription(), self.getColor(),
                 self.getDebut(), self.getDuree(), self.__rep, self.__nbrep, self.getParent())
        # Doit-on copier les dépendances et le statut ?
        t.__dependances = self.__dependances[:]
        t.updateStatut()
        # On retourne la copie :
        return t

    def delete(self, app):
        """
        Permet de supprimer définitivement cette tâche.
        @param app: Application(), nécessaire pour la suppression d'une tâche.
        """
        if self.__parent is None and not self.isContainer():
            app.getTaskEditor().supprimer(self)
            app.getPeriodManager().getActivePeriode().removeInstanciatedSchedulable(self)
        elif self.isContainer():
            app.getTaskEditor().supprimer(self)
            for t in self.getSubTasks():
                app.getPeriodManager().getActivePeriode().removeInstanciatedSchedulable(t)
        else:
            self.__parent.removeSubTask(self)
            app.getTaskEditor().redessiner()
            app.getPeriodManager().getActivePeriode().removeInstanciatedSchedulable(self)

    def getRawRepartition(self, displayedCalendar):
        """
        @see AbstractSchedulableObject#getRawRepartition(displayedCalendar)
        @override AbstractSchedulableObject#getRawRepartition(displayedCalendar)
        """
        return self.getRepartition(displayedCalendar)

    def getRepartition(self, displayedCalendar):
        """
        TODO : Gère également les tâches à répétition. 
        @see AbstractSchedulableObject#getRepartition(displayedCalendar)
        @override AbstractSchedulableObject#getRepartition(displayedCalendar)
        """
        def addRepartition(instance):
            if not instance.isContainer():
                if instance.getDebut().date() == instance.getFin().date():
                    yield DatetimeItemPart(instance.getDebut().date(),
                                           instance.getDebut().time(),
                                           instance.getFin().time(),
                                           self)
                else:
                    debutJour = datetime.time(0, 0, 0)
                    finJour   = datetime.time(23, 59, 59)
        
                    date = instance.getDebut().date()
                    heure1 = instance.getDebut().time()
                    heure2 = finJour
        
                    while date < instance.getFin().date():
                        yield DatetimeItemPart(date, heure1, heure2, self)
                        heure1 = debutJour
                        date += datetime.timedelta(days = 1)
        
                    heure2 = instance.getFin().time()
        
                    yield DatetimeItemPart(date, heure1, heure2, self)

        # Permet de gérer les tâches à répétitions différemment de celles qui sont normales :
        if self.__nbrep > 0:
            instance = self.copy()
            count = self.__nbrep
            while count > 0 and instance.getDebut().date() < self.getPeriode().getFin():
                yield from addRepartition(instance)
                instance.setDebut(instance.getDebut() + instance.__rep)
                count -= 1
        else:
            yield from addRepartition(self)

    def instantiate(self):
        periode = self.getPeriode()
        
        # Si on est une tâche container:
        if self.isContainer():
            for subTask in self.__subtasks:
                subTask.instantiate()
        else:
            periode.addInstanciatedSchedulable(self)

    def updateStatut(self):
        """
        Permet de mettre à jour le statut de la tâche.
        """
        self._statut = "Inconnu" if self.getDebut() == None\
                  else "Répétition" if self.__nbrep != 0\
                  else "Fait" if self.__done\
                  else "En retard" if self.getFin() < datetime.datetime.now()\
                  else "En cours" if self.getDebut() < datetime.datetime.now()\
                  else "À faire"

    ""
    ##############
    # Container: #
    ##############
    ""
    def addSubTask(self, task):
        """
        Permet d'ajouter une sous-tâche si cette tâche est une tâche conteneur.
        Il est impératif de gérer la suppression de la tâche dans TaskEditor depuis l'extérieur.
        @param task: la sous-tâche à ajouter.
        @raise RuntimeError: si ce n'est pas une tâche conteneur.
        @raise RuntimeError: si c'est une tâche conteneur mais qu'on rajoute une sous-tâche déjà conteneur.
        @raise RuntimeError: si la tâche à rajouter est déjà dans une tâche conteneur (peut être celle-ci ou non).
        """
        if not self.isContainer():
            raise RuntimeError("Impossible de rajouter une tâche dans une tâche non conteneur.")
        if task.isContainer():
            raise RuntimeError("Impossible de rajouter une tâche conteneur dans une autre tâche conteneur")
        if task.__parent is not None:
            raise RuntimeError("Impossible de rajouter une tâche dans un conteneur, sachant qu'elle est déjà présente dans un autre conteneur")
        try:
            self.__subtasks.append(task)
        except:
            self.__subtasks = [task]
        task.__parent = self    # Accès private possible, au vu que ce sont des objets de même type.

    def getParent(self):
        """
        Retourne la tâche conteneur qui contient cette tâche (si ce conteneur existe).
        @return la tâche parente, ou None le cas échéant.
        """
        return self.__parent

    def getSubTasks(self):
        """
        Permet d'obtenir les sous-tâches de cette tâche conteneur.
        @return une copie de la liste des sous-tâches de cette tâche conteneur.
        @raise RuntimeError: si cette tâche n'est pas une tâche conteneur.
        """
        if not self.isContainer():
            raise RuntimeError("Impossible d'obtenir les sous-tâches d'une tâche non conteneur.")
        return self.__subtasks[:]

    def isContainer(self):
        """
        Permet de savoir si cette tâche est une tâche conteneur.
        @return True si la tâche est une tâche conteneur, False sinon.
        """
        self.updateStatut()
        return self._statut == "Inconnu"

    def removeSubTask(self, task):
        """
        Permet d'enlever une sous-tâche de cette tâche conteneur.
        @param task: la sous-tâche à enlever.
        @raise RuntimeError: si cette tâche n'est pas conteneur.
        @raise RuntimeError: si la sous-tâche à enlever n'est pas dans ce conteneur.
        """
        if not self.isContainer():
            raise RuntimeError("Impossible d'enlever une tâche d'une tâche non conteneur.")
        if task.__parent != self:
            raise RuntimeError("Impossible d'enlever une tâche d'un conteneur où cette tâche n'est pas présente.")
        self.__subtasks.remove(task)

    ""
    #################
    # Dépendances : #
    #################
    def addDependance(self, task):
        """
        Permet d'ajouter une dépendance à cette tâche,
        c'est-à-dire que notre tâche (self) dépendra de
        cette nouvelle task.
        @param task: la tâche dont celle-ci va dépendre.
        """
        self.__dependances.append(task)
        task.__dependantes.append(self)

    def getDependances(self):
        """
        Permet d'obtenir une copie de la liste des tâches
        dont dépend cette tâche.
        @return: une copie de cette liste.
        """
        return self.__dependances[:]

    def getDependantes(self):
        """
        Permet d'obtenir une copie de la liste des tâches
        dépendant de cette tâche.
        @return une copie de la liste des tâches dépendantes.
        """
        return self.__dependantes[:]

    def removeDependance(self, task):
        """
        Permet d'enlever une dépendance à cette tâche,
        c'est-à-dire que notre tâche (self) dépendra de
        cette nouvelle task.
        @param task: la tâche dont celle-ci dépendait.
        """
        self.__dependances.remove(task)
        task.__dependantes.remove(self)

    ""
    ###########################
    # Méthode "temporelles" : #
    ###########################

    def getDebut(self):
        """
        Getter pour le début de la tâche.
        @return un datetime.datetime() correspondant au début de cette tâche si elle en a un.
        @return None si cette tâche n'a pas de début.
        """
        return self.__debut + datetime.timedelta() if self.__debut is not None else None # Faire une copie et vérifier les trucs

    def getDuree(self):
        """
        Getter pour la Durée de la tâche.
        @return un datetime.timedelta() correspondant à la durée de la tâche.
        """
        return self.__duree + datetime.timedelta() # Faire une copie

    def getFin(self):
        """
        Getter pour la fin de la tâche.
        @return un datetime.datetime() correspondant à la fin de la tâche si il existe.
        @return None si la tâche n'as pas de début (en vrai c'est qu'elle n'as pas de fin).
        """
        return (self.__debut + self.__duree) if self.__debut is not None else None

    def getNbRep(self):
        """
        Getter pour le nombre de répétition de la tache
        @return <int>
        """
        return self.__nbrep

    def getRep(self):
        """
        Getter pour la durée entre 2 répétitions
        @return <datetime.timedelta>
        """
        return self.__rep

    def setDebut(self, debut, change = "fin"):
        """
        Permet de mettre le début de la période.
        @param debut: Le datetime.date du début de la période.
        @param change: Si "duree": change la durée mais pas la fin,
                       Si "fin": change la fin mais pas la durée.
                       Sinon : raise ValueError
        """
        if change == "duree":
            fin = self.getFin()
            self.__debut = debut + datetime.timedelta() # Faire une copie de la date
            self.__duree = fin - self.getFin()
        elif change == "fin":
            self.__debut = debut + datetime.timedelta() # Faire une copie de la date
        else:
            raise ValueError('Mauvaise valeur à changer : %s, seulement "duree" et "fin" sont possibles.'%change)

    def setDuree(self, duree):
        """
        Setter de la duree de la tache
        @param duree : <datetime.timedelta> celui qu'il faut mettre
        """
        self.__duree = duree
        self.setDebut(self.getDebut(), change = "fin")

    def intersectWith(self, task):
        """
        Permet de savoir si cette tâche s'intersectionne avec une autre.
        @param task: la tâche dont on teste l'intersection avec celle-ci.
        @return True si les 2 tâches s'intersectionnent, False sinon.
        """
        return not (self.getFin() < task.getDebut() or self.getDebut() > task.getFin())

    ""
    ####################
    # Autre méthodes : #
    ####################
    ""
    #def getFilterStateWith(self, filter):
        #Si non autorisé par le filtre :
        #if ("name" in filter and self.nom.lower().count(filter["name"]) == 0)\
        #or ("type" in filter and not "Tâche" in filter["type"]): # TODO : Ajouter tâches indépendantes.
            #return -1
         #Filtre prioritaire ?
        #if "name" in filter and self.nom.lower().startswith(filter["name"].lower()):
            #return 1
         #Sinon : autorisé par le filtre, mais pas prioritaire.
       #return 0

    def getUniqueID(self):
        """
        Permet d'obtenir l'ID de la tache
        @return : <str> self.__uniqueID
        """
        return self.__uniqueID

    def isDone(self):
        """
        Getter pour savoir si la tâche est validée.
        @return True si la tâche est validé, False sinon.
        """
        return self.__done

    def setDone(self, value):
        """
        Setter pour dire si la tâche est validée.
        @param value: True si la tâche est validée, False sinon.
        """
        self.__done = value
        self.updateStatut()

    def setUniqueID(self):
        """
        Permet d'ajouter un uniqueID à la tache et de le mettre dans la liste
        qui vérifie s'il est bien unique
        """
        ID = id(self)
        if self.getPeriode():
            while str(ID) in self.getPeriode().getApplication().listKey:
                ID += 1
        return str(ID)

    def transformToDnd(self, taskEditor, rmenu):
        """
        Permet de transformer cette tâche en une tâche déplaçable,
        c'est-à-dire une tâche conteneur. En vrai, ce sera une
        nouvelle tâche, avec comme contenu cette tâche ici présente.
        
        @param taskEditor: Référence vers le TaskEditor pour pouvoir
        faire les opérations.
        @param rmenu: référence vers le RMenu de cet tâche en tant
        qu'item du TaskEditor. Nécessaire pour l'opération.
        """
        # On supprime le RMenu pour le recréer après
        # dans le TaskEditor via notre méthode getRMenuContent()
        # car il va être différent.
        rmenu.destroy()
        del rmenu
        
        # On s'enlève du TaskEditor, mais on ne se supprime pas
        # attention. On va juste se réajouter ailleurs...
#        taskEditor.supprimer(self)
        self.getPeriode().removePrimitiveSchedulable(self) # N'enlève pas des instanciées.
        
        # On crée une tâche qui nous ressemble, mais dont le début
        # n'est pas présent. Et pour cause : c'est ce qui fait que
        # ça devient une tâche conteneur. On peut alors s'y ajouter.
        newTask = self.copy()
        newTask.__debut = None
        newTask.updateStatut()
        newTask.addSubTask(self)
        
        # Le fait de rajouter cette nouvelle tâche va nous rajouter
        # indirectement. Je vous avais bien dit qu'on ne se supprimait pas !
#        taskEditor.ajouter(newTask)
        self.getPeriode().addPrimitiveSchedulable(newTask)
        taskEditor.redessiner()

    ""
    #######################################
    # Méthodes liées à l'enregistrement : #
    #######################################
    ""
    def saveByDict(self):
        """
        Méthode qui sauvegarde les attributs présent (ici)

        @save debut      : <datetime>  ou None
        @save duree      : <timedelta> ou None
        @save rep        : <?> répétition
        @save nbrep      : <int> nombre de répérition
        @save parent     : <str> nom du conteneur
        @save done       : <?>
        @save depencance : <list str> liste des noms des taches
        @save dependante : <list str> liste des noms des taches

        @return dico : <dict> contient les couples clé-valeur ci-dessus
        """
        # On va chercher les attributs de la superclasse
        dico = super().saveByDict()
        # Si on est conteneur, il y a des attributs qu'on a pas

        dico["debut"] = datetimeToStr(self.getDebut())
        dico["duree"] = timedeltaToStr(self.getDuree())

        dico["rep"] = timedeltaToStr(self.__rep)
        dico["nbrep"] = self.__nbrep

        dico["subtasks"] = [st.saveByDict() for st in self.getSubTasks()] if self.isContainer() else None
        dico["parent"] = self.getParent().getNom() if self.getParent() else None
        dico["done"] = self.__done

        dico["id"] = self.getUniqueID()


        dico["dependance"] = []
        for dep in self.getDependances():
            dico["dependance"].append(dep.getUniqueID())

        dico["dependante"] = []
        for dep in self.getDependantes():
            dico["dependante"].append(dep.getUniqueID())

        return dico
