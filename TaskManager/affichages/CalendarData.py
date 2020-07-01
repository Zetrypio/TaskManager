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
    affichages auront ces données dans la même instance de cette classe.
    """
    def __init__(self):
        """
        Constructeur de CalendarData.
        Voir CalendarData.__doc__ pour la raison de cette classe.
        """
        pass