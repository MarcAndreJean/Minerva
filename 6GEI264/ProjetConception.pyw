#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : ProjetConception.py

    Identification  : ProjetConception
    Titre           : Programme principal du projet
    Auteurs         : Marc-André Jean
    Date            : 27-04-2017
    Description     : Démmarrage de l'application.


    Le module ``ProjetConception``
    ================================

    Ce module s'occupe tout simplement de démarrer l'application et de
    rassembler tous les modules. Les lignes de code ci-dessous s'occupent
    de démarrer l'interface après que tous les modules soient chargés.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"


# Importation des modules nécessaires.
try:
    modVue = __import__("01-Vue")
except ImportError:
    import importlib
    modVue = importlib.import_module("Modules.01-Vue")


# Importation de Tkinter selon la version de Python.
# Python 2 seulement:
try:
    from Tkinter import *
# Python 2 et 3 (Python 2 après ''pip install future''):
except ImportError:
    from tkinter import *

# Si "ProjetConception.pyw" est lancé comme étant le programme principal
# (donc non importé, mais exécuter), on crée l'application.
if __name__ == '__main__':
    # Création de la fenêtre avec une taille initiale.
    root = Tk()

    # Création de la vue globale dans le root.
    vueGlobal = modVue.VueGlobal(root)
    vueGlobal.pack(fill=BOTH, expand=True)

    # Définition des paramètres pour le root.
    root.wm_minsize(800, 600)
    root.wm_title("Projet Conception - v" + __version__)

    # Démarrage de l'application.
    root.mainloop()
