#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-01-Bus.py

    Identification  : 04-01-Bus
    Titre           : Bus
    Auteurs         : Marc-André Jean
    Date            : 15-04-2017
    Description     : Bus de données du Micro-Ordinateur.


    Le module ``Bus``
    ================================

    Ce module contient le Bus tel que présentée dans le document de
    spécification. Le Bus contrôle le flux des diverses données et
    état de l'ordinateur. C'est lui qui propage les coups d'horloge
    aux autres composantes de l'ordinateur.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "production"

# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
# Redéfinition.
MODE = modEnum.MODE


class Bus:
    """
        class Bus
        ========================

        Le bus système du Micro-Ordinateur a un total de 49 lignes de
        communications. Ce bus système a trois sous-bus:
        - Un bus Data (16 bits)
        - Un bus Address (16 bits)
        - Un bus Control (16 bits) (aussi appelée Mode)
        En addition de ces trois sous-bus (total de 48 lignes), le bus
        système a aussi une ligne (un bit) pour l'horloge du système.

        :example:
        >>> test = Bus()


    """

    def __init__(self):
        """
            Constructeur de la classe Bus.

            Le constructeur initialise les attributs de la classe bus.

            :example:
            >>> test = Bus()

        """
        self._component = []  # liste des composantes de la machine
        self.data = 0x0000        # valeur sur le bus
        self.address = 0x0000      # adresse d'operation
        self.mode = MODE.END   # 0:inerte, 1:write, 2:read,
        # 4:END, 8:RESET, 9:HALT
        # Fin.
        return

    def register(self, component):
        """
            Fonction pour ajouter un composant.

            Cette fonction permet d'ajouter des elements dans la liste des
            composantes de l'ordinateur elle possede comme parametre le
            composant a ajouter dans la liste «component ».

            :example:
            >>> test = Bus()
            >>> test.register(Bus())

            :param component: Composant du Micro-Ordinateur à lié.
            :type component: class

        """
        # On ajoute le composant dans la liste.
        self._component.append(component)
        return

    def event(self):
        """
            Fonction qui appelle la fonction event() des composantes.

            Cette fonction appelle la fonction event() de chaque
            composante (si elle existe).

            :example:
            >>> test = Bus()
            >>> test.register(Bus())
            >>> test.event()

        """
        # Si la liste de composant n'est pas vide.
        if self._component:
            # Pour chaque composant.
            for i in self._component:
                # Si le composant a une fonction event, nous l'appelons.
                if i.event:
                    i.event()
        return

    def clock(self):
        """
            Fonction qui appelle la fonction clock() des composantes.

            Cette fonction contrôle le traitement et l'exécution des
            instructions en agissant particulièrement sur le cpu. Elle
            appelle les fonctions clock() des composantes se trouvant
            dans la liste de composante.

            :example:
            >>> test = Bus()
            >>> test.register(Bus())
            >>> test.clock()

        """
        # On quitte la fonction si le bus n'est pas prêt à recevoir un
        # coup d'horloge.
        if self.mode == MODE.HALT:
            return

        # En mode RESET ou END on propage le coup d'horloge.
        if self.mode == MODE.RESET or self.mode == MODE.END:
            # Si la fonction est en mode END, nous la réinitialisons en
            # mode INERTE.
            if self.mode == MODE.END:
                self.mode = MODE.INERTE
            # Si la liste de composante n'est pas vide.
            if self._component:
                # Pour chaque composante dans la liste.
                for i in self._component:
                    # Si la composante a une fonction clock, nous l'appelons.
                    if i.clock:
                        i.clock()
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
