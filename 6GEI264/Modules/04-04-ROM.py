#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 04-04-ROM.py

    Identification  : 04-04-ROM
    Titre           : Mémoire ROM
    Auteurs         : Marc-André Jean
    Date            : 15-04-2017
    Description     : Mémoire ROM du Micro-Ordinateur.


    Le module ``ROM``
    ================================

    Ce module présente la classe ROM qui est la représentation de la
    mémoire ROM du micro-ordinateur. C'est elle qui lit ou écrit en mémoire
    selon l'adresse indiqué dans le bus. Si c'est une lecture, la mémoire
    renvoit la valeur sur la ligne Data du bus.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"


# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
    modBus = __import__("04-01-Bus")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
    modBus = importlib.import_module("Modules.04-01-Bus")
# Redéfinition.
MODE = modEnum.MODE


class ROM:
    """
        class ROM
        ========================

        Cette classe représente la mémoire du micro-ordinateur. Elle
        contient une fonction qui permet d'uploader le code dans la
        mémoire ROM (un peu comme nous pourrions le faire avec certains
        micro-controlleur USB). À chaque coup d'horloge (clock/event),
        la classe vérifie si elle doit effectuer une lecture ou
        écriture en mémoire.

        :example:
        >>> test = ROM(modBus.Bus())


    """

    # Constructeur.
    def __init__(self, bus):
        """
            Constructeur de la classe ROM.

            Le constructeur s'occupe d'initialiser la mémoire et lie
            ce composant avec le bus.

            :example:
            >>> test = ROM(modBus.Bus())

            :param bus: Composant Bus du Micro-Ordinateur.
            :type bus: Bus

        """
        self.clock = False
        # Bus.
        self.bus = bus
        self.bus.register(self)

        # Tableau de int pour représenter la mémoire.
        self._data = [0] * (0x40FB + 1)
        return

    def event(self):
        """
            Récepteur pour le signal event.

            Cette fonction est appelé lorsqu'un event est émit
            sur le bus. Elle gère l'écriture et la lecture en mémoire.

            :example:
            >>> bus = modBus.Bus()
            >>> test = ROM(bus)
            >>> test.event()
            >>> bus.event()

        """
        # Si ce n'est pas de la mémoire ROM on quitte.
        if self.bus.address > 0x40FB:
            return
        # Si en mode LECTURE:
        if self.bus.mode == MODE.READ:
            # On mets la valeur de la case mémoire à l'adresse bus.address
            # dans le bus.data.
            self.bus.data = self._data[self.bus.address]
        # Si en mode ÉCRITURE:
        elif self.bus.mode == MODE.WRITE:
            # On mets la valeur de bus.data dans la case mémoire
            # à l'adresse bus.address.
            self._data[self.bus.address] = self.bus.data
        return

    def uploadProgram(self, bytecode):
        """
            Fonction pour charger bytecode dans la ROM.

            Cette fonction charge un programme (celui dans bytecode) dans
            la mémoire ROM.

            :example:
            >>> bus = modBus.Bus()
            >>> test = ROM(bus)
            >>> test.uploadProgram([0xFAFA, 0xAFAF, 0x0000, 0xFFFF])

            :param bytecode: Tableau de int (16 bits) d'un programme
                             exécutable.
            :type bytecode: int[]


        """
        # On parcourt toutes les adresses de la mémoire ROM.
        for address in range(min(len(bytecode), 0x40FB + 1)):
            # On transfert le bytecode[address] à l'adresse.
            self._data[address] = bytecode[address]
        # Si le bytecode est plus petit que la taille max de la mémoire
        # ROM, on mets dans zéro pour le reste des cases.
        if len(bytecode) < 0x40FB + 1:
            # On attribut des zéros pour ces cases.
            for address in range(len(bytecode), 0x40FB + 1):
                self._data[address] = 0x0000
        # Fin.
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
