# -*- coding:utf-8 -*-

def askHeureExacte(master, region):
    """
    Permet de faire un dialogue à l'utilisateur
    lui demandant de confirmer l'heure exacte à laquelle
    la tâche rajoutée via Drag&Drop doit-être rajoutée.
    @param region: L'heure auparavant calculée.
    @return la nouvelle heure calculée.
    """
    heure1 = region.hour
    minute1 = region.minute
    def onClose(bouton):
        nonlocal region
        if bouton == "Reset":
            h.set(heure1)
            m.set(minute1)
            return
        if bouton == "Ok":
            heure2 = int(h.get())
            minute2 = int(m.get())
            region += datetime.timedelta(minutes = heure2*60 - heure1 * 60 + minute2 - minute1)
        else:
            region = None
        fen.destroy()
    def minutePres():
        if var.get():
            m.config(increment = 1)
        else:
            m.config(increment = 5)
    def adapteHeure():
        """Adapte les heures quand on augmente (ou diminue) trop les minutes."""
        minutes = int(m.get())
        heures = int(h.get())
        while minutes < 0:
            minutes += 60
            heures -= 1
        while minutes >= 60:
            minutes -= 60
            heures += 1
        heures += 24
        heures %= 24
        m.set(minutes)
        h.set(heures)

    fen = Dialog(self, "Confirmez l'heure exacte", ("Ok", "Annuler", "Reset"), command = onClose)
    Label(fen, text = "Veuillez entrer l'heure exacte").pack(side = TOP, expand = YES, fill = BOTH)
    var = BooleanVar(value = False)
    c = Checkbutton(fen, text = "Précision à la minute près ?", command = minutePres, variable = var)
    c.pack(side = TOP, fill = X)
    Label(fen, text = "Heure :").pack(side = LEFT)
    h = Spinbox(fen, from_ = -1, to = 24, increment = 1, command = adapteHeure)
    h.pack(side = LEFT, fill = X, expand = YES)
    m = Spinbox(fen, from_ = -5, to = 64, increment = 5, command = adapteHeure)
    m.pack(side = RIGHT, fill = X, expand = YES)
    Label(fen, text = "Minute :").pack(side = RIGHT)
    onClose("Reset")
    fen.activateandwait()
    return region
