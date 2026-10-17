#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : LigneCommande.py

    Identification  : LigneCommande
    Titre           : Programme «ligne de commande» du projet
    Auteurs         : Marc-André Jean
    Date            : 13-04-2017
    Description     : Démmarrage de l'application en interpréteur.


    Le module ``LigneCommande``
    ================================

    Ce module s'occupe de démarrer l'application en mode «ligne de
    commande» et de rassembler tous les modules. Les lignes de code
    ci-dessous s'occupent de démarrer l'interface après que tous les
    modules soient chargés.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"

# Importation des modules nécessaires.
try:
    modVue = __import__("01-01-Ordinateur")
    modEnum = __import__("05-Enum")
except ImportError:
    import importlib
    modVue = importlib.import_module("Modules.01-01-Ordinateur")
    modEnum = importlib.import_module("Modules.05-Enum")


# Importation de Tkinter selon la version de Python.
# Python 2 seulement:
try:
    from Tkinter import *
# Python 2 et 3 (Python 2 après ''pip install future''):
except ImportError:
    from tkinter import *

# Si "LigneCommande.pyw" est lancé comme étant le programme principal
# (donc non importé, mais exécuter), on crée l'application.
if __name__ == '__main__':
    # Création de la fenêtre avec une taille initiale.
    root = Tk()

    # Création de la vue globale dans le root.
    vueGlobal = modVue.VueOrdinateur(root, modEnum.TYPEUSE.LIGNECOMMANDE)
    vueGlobal.pack(fill=BOTH, expand=True)

    # Définition des paramètres pour le root.
    root.wm_minsize(800, 600)
    root.wm_title("Projet Conception - Ligne de commande - v" + __version__)

    # Démarrage de l'application.
    root.mainloop()
