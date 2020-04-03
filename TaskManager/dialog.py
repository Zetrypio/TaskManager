# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *

def noCommand(*_,**__):pass

class Dialog(Frame):
    """Boîte de dialogue usuelle"""
    def __init__(self, master = None, title = 'Dialogue',
                 buttons = ('Ok', 'Appliquer', 'Annuler', 'Aide'),
                 defaultbutton = 'Ok',
                 command = noCommand,
                 exitButton = ('Ok', 'Annuler')):

        #if master is None:
        #    master = _default_root = Tk()

        self.dialog = Toplevel(master)
        self.dialog.transient(self.dialog.master)
        self.dialog.title(title)
        self.dialog.protocol("WM_DELETE_WINDOW", lambda : self.execute("WM_DELETE_WINDOW"))
        self.dialog.withdraw()

        self.parent = self.dialog.master

        self.command = command
        self.exitButton = exitButton
        Frame.__init__(self, self.dialog)

        self.__buttons_extraframe = Frame(self.dialog)
        self.__buttons_extraframe.pack(side = BOTTOM, fill = X)
        self.__buttons_frame = Frame(self.__buttons_extraframe)
        self.__buttons_frame.pack(side = BOTTOM)
        self.__separator = Separator(self.dialog, orient = HORIZONTAL)
        self.__separator.pack(side = BOTTOM, fill = X)
        self.__bouton_appuyer = None
        self.pack(side = TOP, expand = YES, fill = BOTH)

        self.__buttons = []
        for i in buttons:
            self.__buttons.append(Button(self.__buttons_frame, text = i, command = lambda x = i: self.execute(x)))
            self.__buttons[-1].pack(side = LEFT, padx = 4, pady = 4)
            if i == defaultbutton:
                self.__buttons[-1].config(default = ACTIVE)


    def activate(self):
        self.parent.winfo_toplevel().attributes("-disabled", True)
        self.dialog.focus_set()
        self.dialog.state("normal")
        self.geometry("+%s+%s"%(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.update()
        self.centerscreenalways()

    def activateandwait(self):
        self.activate()
        while self.__bouton_appuyer is None:
            self.mainloop()
        return self.__bouton_appuyer

    def deactivate(self):
        self.parent.winfo_toplevel().attributes("-disabled", False)
        try:
            self.dialog.withdraw()
        except:
            pass
        self.parent.winfo_toplevel().focus_set()

    def destroy(self):
        self.deactivate()
        Frame.destroy(self)
        self.dialog.destroy()

    def execute(self, button):
        self.__bouton_appuyer = button
        self.command(button)
        if button in self.exitButton :
            self.deactivate()
            self.quit()

    def geometry(self, *a):
        return self.dialog.geometry(*a)

    def centerscreenalways(self):
        xy = self.geometry().split("+")[0]
        x, y = xy.split("x")
        x = int(x)
        y = int(y)
        sx = self.winfo_screenwidth()
        sy = self.winfo_screenheight()
        npx = sx/2 - x/2
        npy = sy/2 - y/2
        self.geometry("+%s+%s"%(int(npx), int(npy)))
        self.update()


def askString(master, nom, question):
    # Créer l'espace du dialogue :
    dialogue = Dialog(master, nom, ("Ok", "Annuler"))
    dialogue.bind_all("<Return>", lambda e: dialogue.execute("Ok"))
    dialogue.bind_all("<Escape>", lambda e: dialogue.execute("Annuler"))

    # Mettre des composants dessus :
    lbl = Label(dialogue, text = question)
    etr = Entry(dialogue)
    lbl.pack(side = LEFT, expand =YES, fill = BOTH)
    etr.pack(side = LEFT, expand =YES, fill = BOTH, padx = 5, pady = 5)

    # Activer puis récupérer le résultat pour le renvoyer
    bouton = dialogue.activateandwait()
    result = etr.get()
    result = result if bouton == "Ok" and result else None
    dialogue.destroy()
    return result


