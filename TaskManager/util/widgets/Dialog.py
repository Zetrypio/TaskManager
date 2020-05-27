# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from tkinter import Label, Frame
from tkinter.messagebox import WARNING, YESNO, YES
from tkinter.messagebox import _show

def noCommand(*_,**__):pass

class Dialog(Frame):
    """
    Boîte de dialogue usuelle.
    """
    def __init__(self, master = None, title = 'Dialogue',
                 buttons = ('Ok', 'Appliquer', 'Annuler', 'Aide'),
                 defaultbutton = 'Ok',
                 command = noCommand,
                 exitButton = ('Ok', 'Annuler')):
        """
        Constructeur d'un dialogue.
        @param master: parent du dialogue.
        @param title: Titre de la fenêtre du dialogue.
        @param buttons: Liste des textes à mettre sur les boutons à mettre.
        @param defaultbutton: Le boutons par défaut.
        @param command: la fonction à exécuter lors de l'appuie sur l'un des boutons.
        @param exitButton: Liste des boutons qui vont automatiquement désactiver le dialogue
        quand ils seront pressés. Désactivé ne veut pas dire détruit, simplement caché.
        """

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
        """
        Permet d'activer le dialogue.
        @bug: lors de la fermeture, ferme aussi la fenêtre
        principale en sortant de la mainloop de tkinter.
        Utilisez Dialog#activateandwait() à la place.
        """
        self.parent.winfo_toplevel().attributes("-disabled", True)
        self.dialog.focus_set()
        self.dialog.state("normal")
        self.geometry("+%s+%s"%(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.update()
        self.centerscreenalways()

    def activateandwait(self):
        """
        Permet d'activer le dialogue et d'attendre sa sortie.
        @return le bouton appuyé.
        """
        self.activate()
        while self.__bouton_appuyer is None:
            self.mainloop()
        return self.__bouton_appuyer

    def deactivate(self):
        """
        Permet de fermer le dialogue sans le détruire.
        Il est réactivable par la suite.
        """
        self.parent.winfo_toplevel().attributes("-disabled", False)
        try:
            self.dialog.withdraw()
        except:
            pass
        self.parent.winfo_toplevel().focus_set()

    def destroy(self):
        """
        Permet de détruire le dialogue entièrement,
        il n'est plus réactivable par la suite.
        """
        self.deactivate()
        Frame.destroy(self)
        self.dialog.destroy()

    def execute(self, button):
        """
        Méthode permettant de simuler l'appuie sur un bouton du dialogue.
        Notez que les vrais boutons passent aussi par cette méthode,
        ainsi que la croix de fermeture de fenêtre (alors avec le texte
        "WM_DELETE_WINDOW").
        @param button: le texte du bouton qui aurait été appuyé.
        """
        self.__bouton_appuyer = button
        try:
            self.command(button)
        except SystemExit:
            raise
        except:
            sys.stderr.write("Exception in Dialog callback\nfrom ")
            self._report_exception()
        else:
            if button in self.exitButton :
                self.deactivate()
                self.quit()

    def geometry(self, *a):
        """
        Permet de configurer la géométrie de la fenêtre du dialogue,
        voir Toplevel#geometry() pour plus d'information.
        """
        return self.dialog.geometry(*a)

    def centerscreenalways(self):
        """
        Permet de rencentrer la fenêtre du dialogue au
        centre de l'écran dans tout les cas.
        """
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
    """
    Pose une question à l'utilisateur dans un dialogue,
    il doit répondre dans un champ d'entrée.
    @param master: master du dialogue.
    @param nom: titre du dialogue.
    @param question: question posée à l'utilisateur.
    @note: Cela sert aussi d'exemple quant à l'utilisation
    de la classe Dialog().
    """
    # Créer l'espace du dialogue :
    dialogue = Dialog(master, nom, ("Ok", "Annuler"))
    # Il y a des problèmes avec ces bindings...
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


def askyesnowarning(title=None, message=None, **options):
    "Ask a question with a warning; return true if the answer is yes."
    s = _show(title, message, WARNING, YESNO, **options)
    return s == YES
