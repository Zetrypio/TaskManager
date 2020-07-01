# -*- coding:utf-8 -*-

class CalendarData:
    """
    Cette classe va regrouper les informations de période,
    d'heures, des objets planifiables mis dans les calendriers.
    
    L'objectif est que modifier la date de début/fin de la période
    en cours par exemple, n'ai pas besoin d'être exécuté sur tout
    les modes d'affichages comme on faisait jusqu'à maintenant
    via la classe DonneeCalendrier. Modifier quelque part
    sera de facto une modification de partout, car tout les
    affichages auront ces données dans la m�me instance de cette classe.
    """
    def __init__(self):
        """
        Constructeur de CalendarData.
        Voir CalendarData.__doc__ pour la raison de cette classe.
        """

        # infos des heures :
        self.heureDebut = datetime.time(8, 0, 0)
        self.heureFin = datetime.time(17, 59, 0)

        # infos des jours :
        self.jourDebut = self.getDebutPeriode()
        self.jourFin   = self.getFinPeriode()

        # liste des objets planifiables :
        self.schedulables = []

    ""
    ########################################
    # Getter pour les infos des périodes : #
    ########################################
    def getDebutPeriode(self):
        """
        Permet d'obtenir le jour du début de la période active si elle existe.
        @return datetime.date() correspondant au début de la période active si elle existe.
        @return None si elle n'existe pas.
        """
        return self.getPeriodeActive().getDebut() if self.getPeriodeActive() is not None else None

    def getLongueurPeriode(self):
        """
        Permet d'obtenir la longueur de la période.
        @return un datetime.timedelta, de la longueur de la période
        (seulement les jours comptent). Le début autant que la fin sont pris en compte (Est-ce une bonne idée ?)
        @return datetime.timedelta(0) si la période active n'existe pas.
        """
        return (self.getFinPeriode() - self.getDebutPeriode() + datetime.timedelta(days=1)) if self.getPeriodeActive() is not None else datetime.timedelta()

    def getFinPeriode(self):
        """
        Permet d'obtenir le jour de fin de la période active si elle existe.
        @return datetime.date() correspondant à la fin de la période active si elle existe.
        @return None si elle n'existe pas.
        """
        return self.getPeriodeActive().getFin()   if self.getPeriodeActive() is not None else None

    def getPeriodeActive(self):
        """
        Getter pour la période active.
        Nécessaire pour savoir quelle période afficher.
        @return la période active.
        """
        return self.getApplication().getPeriodManager().getActivePeriode()

    ""
    #####################################################
    # Méthodes pour les infos des heures d'affichages : #
    #####################################################
    def getHeureDebut(self):
        """
        Getter pour l'heure du début de l'affichage.
        @return datetime.time() de l'heure du début de l'affichage.
        """
        return self.heureDebut

    def setHeureDebut(self, valeur):
        """
        Setter pour l'heure du début de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure du début de l'affichage.
        """
        self.heureDebut = valeur
        self.updateAffichage()
        
    def getNbheure(self):
        """
        Permet de savoir le nombre d'heures affichés dans ce calendrier.
        @return un nombre entier correspondant au nombre d'heures affichées.
        """
        return self.getHeureFin().hour - self.getHeureFin().hour

    def getHeureFin(self):
        """
        Getter pour l'heure de fin de l'affichage.
        @return datetime.time() de l'heure de fin de l'affichage.
        """
        return self.heureFin

    def setHeureFin(self, valeur):
        """
        Setter pour l'heure de fin de l'affichage.
        Ne concerne pas tout les calendriers (à voir ?).
        @param valeur: datetime.time() de l'heure de fin de l'affichage.
        """
        self.heureFin = valeur
        self.updateAffichage()

    ""
    ####################################################
    # Méthodes pour les infos des jours d'affichages : #
    ####################################################
    def getJourDebut(self):
        """
        Permet d'avoir le jour du début de l'affichage.
        @return datetime.date() du début de l'affichage.
        """
        return self.jourDebut

    def setJourDebut(self, valeur):
        """
        Permet de modifier le jour de début de l'affichage.
        @param valeur: Le datetime.time() à mettre 
        """
        self.jourDebut = valeur + datetime.timedelta()
        self.updateAffichage()

    def getNbJour(self):
        """
        Permet d'obtenir le nombre de jours affichés dans le calendrier.
        @return un int correspondant au nombre de jours affichés.
        """
        return self.getDureeJour().days

    def setNbJour(self, valeur):
        """
        Setter pour le nombre de jours affichés, via un nombre entier.
        Change la position du jour de fin afin d'y parvenir.
        @param valeur : int correspondant au nombre de jours à afficher.
        """
        # TODO : Rajouter le check de dépassement de fin de période -> nouvelle méthode.
        self.jourFin = (self.jourDebut + datetime.timedelta(days=valeur-1)) if self.jourDebut is not None else None
        self.updateAffichage()

    def getDureeJour(self):
        """
        Permet d'obtenir un timedelta correspondant au nombre de jours affichés dans le calendrier.
        @return un datetime.timedelta() correspondant au nombre de jours affichés.
        """
        return (self.jourFin - self.jourDebut + datetime.timedelta(days=1)) if self.jourDebut is not None and self.jourFin is not None else datetime.timedelta()

    def setDureeJour(self, valeur):
        """
        Setter pour le nombre de jours affichés, via un timedelta.
        Change la position de la fin de la période pour y arriver.
        @param valeur: datetime.timedelta() correspondant au nombre de
        jours à afficher.
        """
        # XXX : Pourquoi faire "valeur - datetime.timedelta(days=1)" ?
        # Ne serait-ce pas en dehors de la fonction de faire cette vérification ?
        self.jourFin = (self.jourDebut + valeur - datetime.timedelta(days=1)) if self.jourDebut is not None else None
        
        # TODO : À revoir. -> utiliser une nouvelle méthode.
        if self.getJourFin() > self.getFinPeriode():
            self.setJourFin(self.getFinPeriode())

        self.updateAffichage()

    def getJourFin(self):
        """
        Getter pour le jour de fin de l'affichage.
        @return le datetime.date() correspondant au jour de fin
        de l'affichage.
        """
        return self.jourFin

    def setJourFin(self, valeur):
        """
        Setter pour le jour de fin de l'affichage.
        @param valeur: le datetime.date() du jour de fin de l'affichage.
        """
        self.jourFin = valeur