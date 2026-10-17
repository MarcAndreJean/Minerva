#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 01-Vue.py

    Identification  : 01-Vue
    Titre           : GUI principal
    Auteurs         : Marc-André Jean
    Date            : 13-04-2017
    Description     : GUI principal de l'application.


    Le module ``Vue``
    ================================

    Ce module s'occupe de l'affichage de la vue global de l'application
    avec la librairie Tkinter de Python. Elle contient une classe VueGlobal
    qui s'occupe des deux sous-vues (Ordinateur et Editeur).


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"


# Importation des modules nécessaires.
try:
    modOrdinateur = __import__("01-01-Ordinateur")
    modEditeur = __import__("01-02-Editeur")
except ImportError:
    import importlib
    modOrdinateur = importlib.import_module("Modules.01-01-Ordinateur")
    modEditeur = importlib.import_module("Modules.01-02-Editeur")

# Importation de Tkinter selon le version de Python.
# Python 2 seulement:
try:
    from Tkinter import *
    import ttk as ttk
# Python 2 et 3 (Python 2 après ''pip install future''):
except ImportError:
    from tkinter import *
    import tkinter.ttk as ttk


class VueGlobal(Frame):
    """
        class VueGlobal
        ========================

        Cette classe hérite d'un Widget Frame. Ce Frame va inclure un
        gestionnaire d'onglet qui contient une collection de vue (classe
        Notebook de Tk). Ce widget Notebook permet la sélection entre les
        deux vues principales du programme : la vue « Ordinateur » et la
        vue « Editeur ». Pour d'amples informations, se référer au document
        de spécifications avec le croquis des interfaces.

        :example:
        >>> test = VueGlobal()
        >>> test = VueGlobal(Tk())


    """

    # Constructeur.
    def __init__(self, parent=None):
        """
            Constructeur de VueGlobal.

            Le constructeur initialise son Frame avec le parent qui est
            donné en argument. Il initialise un gestionnaire d'onglet
            (Widget Notebook) et l'ajoute dans le Frame. Il initialise
            ensuite les deux sous-vues et les ajoute dans le gestionnaire
            d'onglet.

            :example:
            >>> test = VueGlobal(None)
            >>> test = VueGlobal(Tk())

            :param parent: Widget Parent de la classe.
            :type parent: Widget (Tk)

            .. warning:: Cette classe a besoin d'avoir le module
              « 01-01-Ordinateur » et le module « 01-02-Editeur »
              accessible.


        """
        # Initialise le Frame de l'instance.
        Frame.__init__(self, parent)

        # Crée la composante graphique qui va controler le gui Ordinateur
        # et Editeur avec un tabs.
        self.vueTabs = ttk.Notebook(self)

        # Crée les deux sous-vues.
        self.vueOrdinateur = modOrdinateur.VueOrdinateur(self.vueTabs)
        self.vueEditeur = modEditeur.VueEditeur(self.vueTabs,
                                                self.vueOrdinateur)

        # Pack les vues dans le gestionnaire d'onglet (Tab) et Pack le
        # gestionnaire d'onglet dans le parent.
        self.vueTabs.pack(fill=BOTH, padx=2, pady=3, expand=True)
        self.vueOrdinateur.pack(fill=BOTH, expand=True)
        self.vueEditeur.pack(fill=BOTH, expand=True)

        # Ajoute les deux sous-vues dans le gestionnaire d'onglet.
        self.vueTabs.add(self.vueOrdinateur, text="Ordinateur")
        self.vueTabs.add(self.vueEditeur, text="Editeur")
        # Fin de __init__.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
