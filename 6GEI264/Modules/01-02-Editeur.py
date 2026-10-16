#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 01-02-Editeur.py

    Identification  : 01-02-Editeur
    Titre           : Interface Éditeur
    Auteurs         : Marc-André Jean
    Date            : 13-04-2017
    Description     : Interface éditeur de l'application.


    Le module ``VueEditeur``
    ================================

    Ce module contient la vue « Éditeur » telle que présentée dans le
    document de spécification. La classe nommée « VueEditeur » gère
    la création des composantes de cette vue. La classe hérite du widget
    Frame pour permettre un placement plus polyvalent et une réutilisation
    plus aisée de cette vue.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"

# Importation des modules nécessaires.
try:
    modFunctEditor = __import__("02-FonctionEditeur")
    modCompiler = __import__("03-Compileur")
    modStatusBar = __import__("01-03-StatusBar")
    modCST = __import__("01-04-CodeScrolledText")
except ImportError:
    import importlib
    modFunctEditor = importlib.import_module("Modules.02-FonctionEditeur")
    modCompiler = importlib.import_module("Modules.03-Compileur")
    modStatusBar = importlib.import_module("Modules.01-03-StatusBar")
    modCST = importlib.import_module("Modules.01-04-CodeScrolledText")


# Importation de Tkinter selon la version de Python.
# Python 2 seulement:
try:
    from Tkinter import *
    import ttk as ttk
    from ttk import Frame
    import ScrolledText as tkst
    import tkFileDialog as fileDialog
    import tkMessageBox as messageBox
# Python 2 et 3 (Python 2 après ''pip install future''):
except ImportError:
    from tkinter import *
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as tkst
    import tkinter.filedialog as fileDialog
    import tkinter.messagebox as messageBox


class VueEditeur(Frame):
    """
        class VueEditeur
        ========================

        Cette classe hérite d'un Frame. Elle représente la vue « Editeur »
        telle que présentée dans le document de spécification. Le Frame
        inclut les boutons et autres Widgets nécessaires pour la vue.

        :example:
        >>> test = VueEditeur()

    """

    # Constructeur.
    def __init__(self, parent=None, attachOrdinateurGUI=None):
        """
            Constructeur de la classe VueEditeur.

            Le constructeur initialise le Frame de la classe avec le Widget
            parent donné en argument. Il initialise ensuite les Widgets
            nécessaires de la vue (comme décrit dans le document de
            spécification). Les fonctions du module « 02-FonctionEditeur »
            et du module « 03-Compileur » seront liés aux évènements
            associés (par exemple les boutons de la vue).

            :param parent: Parent Widget de la classe.
            :type parent: Widget (Tk)
            :param attachOrdinateurGUI: Interface ordinateur.
            :type attachOrdinateurGUI: Widget (Tk)

            :example:
            >>> test1 = VueEditeur()
            >>> test2 = VueEditeur(Tk())

            .. warning:: Cette classe a besoin d'avoir accès aux modules
                         « 02-FonctionEditeur » et « 03-Compileur ».


        """
        self.guiOrdinateur = attachOrdinateurGUI
        # Initialise le Frame de l'instance.
        Frame.__init__(self, parent)

        # Création des widgets nécessaires.
        # --Frame(Text + Button).
        self.globalFrame = Frame(self)

        # ----Text.
        self.frameCin = Frame(self.globalFrame)
        self.labelCin = ttk.Label(self.frameCin,
                                  text="Code", anchor=SW)

        self.innerFrameCin = Frame(self.frameCin, relief=SUNKEN)
        self.txtConsoleInput = modCST.CodeScrolledText(self.innerFrameCin)
        self.txtConsoleInput.configure(width=0, relief=FLAT)
        self.labelCin.pack(fill=X, padx=3, ipady=5)
        self.innerFrameCin.pack(fill=BOTH,
                                padx=3, pady=5, expand=True)
        self.txtConsoleInput.pack(fill=BOTH, padx=3, pady=3, expand=True)
        self.frameCin.grid(column=0, row=0, sticky="NSWE")
        # ----Button.
        self.frameBut = Frame(self.globalFrame)
        if self.guiOrdinateur is not None:
            self.butTransfer = ttk.Button(
                self.frameBut, text="Compiler et Transfèrer dans Ordinateur")
        self.butCompile = ttk.Button(
            self.frameBut, text="Compiler et Sauvegarder")
        self.butSave = ttk.Button(self.frameBut, text="Sauvegarder Code")
        self.butLoad = ttk.Button(self.frameBut,
                                  text="Ouvrir Code")
        if self.guiOrdinateur is not None:
            self.butTransfer.pack(fill=X, padx=20, pady=35, ipady=15)
            self.butCompile.pack(fill=X, padx=20, ipady=15)
        else:
            self.butCompile.pack(fill=X, padx=20, pady=35, ipady=15)
        self.butSave.pack(fill=X, padx=20, pady=3, ipady=10)
        self.butLoad.pack(fill=X, padx=20, pady=3, ipady=10)
        self.frameBut.grid(column=1, row=0, sticky="NWE")
        # ----Grid Configure
        self.globalFrame.grid_rowconfigure(0, weight=1)
        self.globalFrame.grid_columnconfigure(0, minsize=400, weight=4)
        self.globalFrame.grid_columnconfigure(1, minsize=100, weight=1)
        # --StatusBar.
        self.statusBar = modStatusBar.StatusBar(self)
        # Pack
        self.globalFrame.pack(fill=BOTH, expand=True)
        self.statusBar.pack(fill=X)

        # Liaison des évènements.
        if self.guiOrdinateur is not None:
            self.butTransfer.configure(command=self.__callbackCompileTransfer)
        self.butCompile.configure(command=self.__callbackCompile)
        self.butSave.configure(command=self.__callbackSave)
        self.butLoad.configure(command=self.__callbackLoad)

        # Fin de __init__.
        return

    def __callbackCompileTransfer(self):
        """
            Callback pour le bouton «Compiler et Transfert».

            Cette fonction appelle la fonction appropriée du module
            03-Compiler. Si la compilation est un échec, cette fonction
            avertie l'utilisateur via une boite système l'erreur
            (l'information est aussi inscrite sur la barre de statut).
            Si la compilation est un succès on transfère le code dans
            l'interface «Ordinateur».

            ..note: Cette fonction est interne à la classe.


        """
        # On compile le code inscrit dans le widget Text.
        result = modCompiler.compile(self.txtConsoleInput.get("1.0", END))
        # Si la compilation est un succès.
        if result[0]:
            self.statusBar.setText("La compilation est un succès.")
            # On Transfère le code.
            self.guiOrdinateur.transfert(result[1])
            self.statusBar.setText(
                "La compilation est un succès. Transfert effectué.")
        # Si la compilation est un échec.
        else:
            # On informe l'utilisateur.
            self.statusBar.setText(result[1])
            messageBox.showerror(title="Erreur de compilation",
                                 message=result[1])
        # Fin callbackCompile.
        return

    def __callbackCompile(self):
        """
            Callback pour le bouton «Compiler».

            Cette fonction appelle la fonction appropriée du module
            03-Compiler. Si la compilation est un échec, cette fonction
            avertie l'utilisateur via une boite système l'erreur
            (l'information est aussi inscrite sur la barre de statut).
            Si la compilation est un succès, on ouvre une boite système
            pour faire choisir l'emplacement où sauvegarder le fichier
            compilé. Nous appelons ensuite la fonction pour sauvegarder
            ce fichier.

            ..note: Cette fonction est interne à la classe.


        """
        # On compile le code inscrit dans le widget Text.
        result = modCompiler.compile(self.txtConsoleInput.get("1.0", END))
        # Si la compilation est un succès.
        if result[0]:
            self.statusBar.setText("La compilation est un succès.")
            # On demande le chemin du fichier à sauvegarder.
            info = fileDialog.asksaveasfilename(
                defaultextension=".exeb",
                filetypes=[("Executable byte code", ".exeb")],
                title="Sauvegarder l'exécutable sous...")
            # --Si l'utilisateur annule.
            if info is "":
                return
            # On sauvegarde ce fichier.
            modFunctEditor.saveByteCode(info, result[1])
            self.statusBar.setText(
                "La compilation est un succès. L'exécutable a été sauvegardé.")
        # Si la compilation est un échec.
        else:
            # On informe l'utilisateur.
            self.statusBar.setText(result[1])
            messageBox.showerror(title="Erreur de compilation",
                                 message=result[1])
        # Fin callbackCompile.
        return

    def __callbackSave(self):
        """
            Fonction «callback» pour le bouton «Sauvegarder».

            Cette fonction appelle la fonction appropriée du module
            02-FonctionEditeur. On ouvre une boite système pour faire
            choisir l'emplacement où sauvegarder le fichier du code
            non-compilé. Nous appelons ensuite la fonction pour
            sauvegarder ce fichier.

            ..note: Cette fonction est interne à la classe.
        """
        # On demande le chemin du fichier à sauvegarder.
        info = fileDialog.asksaveasfilename(
            defaultextension=".asm",
            filetypes=[("Assembler", ".asm"),
                       ("Texte", ".txt")],
            title="Sauvegarder le code sous...")
        # --Si l'utilisateur annule.
        if info is "":
            return
        # On sauvegarde ce fichier.
        modFunctEditor.saveTextCode(
            info, self.txtConsoleInput.get(
                "1.0", END)[
                0:-1])
        self.statusBar.setText("Code sauvegarder.")
        # Fin callbackSave.
        return

    def __callbackLoad(self):
        """
            Fonction «callback» pour le bouton «Charger».

            Cette fonction appelle la fonction appropriée du module
            02-FonctionEditeur. On ouvre une boite système pour faire
            choisir l'emplacement du fichier code à charger. Nous appelons
            ensuite la fonction pour charger ce fichier.

            ..note: Cette fonction est interne à la classe.
        """
        # On demande le chemin du fichier à charger.
        info = fileDialog.askopenfilename(
            defaultextension=".asm",
            filetypes=[("Assembler", ".asm"),
                       ("Texte", ".txt")],
            title="Ouvrir le code...")
        # --Si l'utilisateur annule.
        if info is "":
            return
        # On charge ce fichier.
        code = modFunctEditor.loadTextCode(info)
        self.txtConsoleInput.delete("1.0", END)
        self.txtConsoleInput.insert(END, code)
        self.statusBar.setText("Code charger.")
        # Fin callbackLoad.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
