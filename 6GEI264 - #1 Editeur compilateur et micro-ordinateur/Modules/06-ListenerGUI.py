#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 06-ListenerGUI.py

    Identification  : 06-ListenerGUI
    Titre           : Micro-Ordinateur
    Auteurs         : Marc-André Jean
    Date            : 17-04-2017
    Description     : Composant supplémentaire pour le micro-ordinateur.


    Le module ``ListenerGUI``
    ================================

    Ce module présente la classe ListenerGUI qui est un composant
    supplémentaire pour le micro-ordinateur. Il s'agit d'un
    « Listener » qui écoute les communications sur le bus pour mettre à
    jour la GUI s'il y a des changements de valeur dans la mémoire ou dans
    les registres.

"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"


# Importation des modules nécessaires.
try:
    modEnum = __import__("05-Enum")
    __import__("04-01-Bus")
    __import__("04-02-CPU")
    __import__("04-05-IO")
except ImportError:
    import importlib
    modEnum = importlib.import_module("Modules.05-Enum")
    importlib.import_module("Modules.04-01-Bus")
    importlib.import_module("Modules.04-02-CPU")
    importlib.import_module("Modules.04-05-IO")
# Redéfinition.
MODE = modEnum.MODE
asciiTOint = modEnum.asciiTOint


class ListenerGUI:
    """
        class ListenerGUI
        ========================

        Il s'agit d'un « Listener » qui écoute les communications sur le
        bus pour mettre à jour la GUI s'il y a des changements de valeur
        dans la mémoire ou dans les registres.

        :example:
        >>> modGUI = __import__("01-01-Ordinateur")
        >>> gui = modGUI.VueOrdinateur()
        >>> test = ListenerGUI(gui)

    """

    # Constructeur.
    def __init__(self, GUI):
        """
            Constructeur de la classe ListenerGUI.

            Le constructeur s'occupe de lié ce composant avec la GUI.

            :example:
            >>> modGUI = __import__("01-01-Ordinateur")
            >>> gui = modGUI.VueOrdinateur()
            >>> test = ListenerGUI(gui)

        """
        # À attacher.
        self.bus = None
        self.cpu = None
        self.io = None
        # GUI.
        self.gui = GUI
        # Variable de comparaisons pour le CPU.
        self.prevRegA = 0
        self.prevRegB = 0
        self.prevRegC = 0
        self.prevRegD = 0
        self.prevRegP = 0
        self.prevRegI = 0
        self.prevRegS = 0
        # Fin.
        return

    def attachBus(self, bus):
        """
            Attache le bus au composant.

            Cette fonction s'occupe de lié ce composant avec le bus.

            :param bus: Composant Bus du Micro-Ordinateur.
            :type bus: Bus

            .. note:: La gui Ordinateur l'attache automatiquement.

        """
        # On attache le Bus.
        self.bus = bus
        self.bus.register(self)
        # Fin.
        return

    def attachCPU(self, CPU):
        """
            Attache le cpu au composant.

            Cette fonction s'occupe de lié ce composant avec le cpu.

            :param bus: Composant CPU du Micro-Ordinateur.
            :type bus: CPU

            .. note:: La gui Ordinateur l'attache automatiquement.

        """
        # Attache le CPU.
        self.cpu = CPU
        # Variable de comparaisons pour le CPU.
        self.prevRegA = CPU.regA
        self.prevRegB = CPU.regB
        self.prevRegC = CPU.regC
        self.prevRegD = CPU.regD
        self.prevRegP = CPU.regP
        self.prevRegI = CPU.regI
        self.prevRegS = CPU.regS
        # Fin.
        return

    def attachIO(self, io):
        """
            Attache le module I/O au composant.

            Cette fonction s'occupe de lié ce composant avec le module IO.

            :param bus: Composant IO du Micro-Ordinateur.
            :type bus: IO

            .. note:: La gui Ordinateur l'attache automatiquement.

        """
        # On attache le module IO.
        self.io = io
        # Fin.
        return

    def event(self):
        """
            Récepteur pour le signal event.

            Cette fonction est appelé lorsqu'un event est émit
            sur le bus.

        """
        # On vérifie s'il y a un changement de le registre.
        self._verifierRegistre()
        # Si en mode Écriture:
        if self.bus.mode == MODE.WRITE:
            # On avertit la GUI.
            self.gui.updateMemory(self.bus.address, self.bus.data)
        # Fin.
        return

    def clock(self):
        """
            Récepteur pour le signal clock.

            Cette fonction est appelé lorsqu'un coup d'horloge est émit
            sur le bus. Elle envoie un signal à la GUI s'il y a un
            changement de valeur pour une adresse (écriture).

        """
        # On vérifie s'il y a un changement de le registre.
        self._verifierRegistre()
        # Fin de la fonction.
        return

    def _verifierRegistre(self):
        """
            Vérifie un changement dans un registre.

            Cette fonction vérifie s'il y a un changement dans un registre.
            Si c'est le cas, nous avertisons la GUI.

        """
        # RegA.
        if self.prevRegA != self.cpu.regA:
            self.prevRegA = self.cpu.regA
            self.gui.updateMemory("RegA", self.prevRegA)

        # RegB.
        if self.prevRegB != self.cpu.regB:
            self.prevRegB = self.cpu.regB
            self.gui.updateMemory("RegB", self.prevRegB)

        # RegC.
        if self.prevRegC != self.cpu.regC:
            self.prevRegC = self.cpu.regC
            self.gui.updateMemory("RegC", self.prevRegC)

        # RegD.
        if self.prevRegD != self.cpu.regD:
            self.prevRegD = self.cpu.regD
            self.gui.updateMemory("RegD", self.prevRegD)

        # RegP.
        if self.prevRegP != self.cpu.regP:
            self.prevRegP = self.cpu.regP
            self.gui.updateMemory("RegP", self.prevRegP)

        # RegI.
        if self.prevRegI != self.cpu.regI:
            self.prevRegI = self.cpu.regI
            self.gui.updateMemory("RegI", self.prevRegI)

        # RegS.
        if self.prevRegS != self.cpu.regS:
            self.prevRegS = self.cpu.regS
            self.gui.updateMemory("RegS", self.prevRegS)

        # Fin.
        return

    def writeKeyboardBuffer(self, key):
        """
            Mets à jour le tampon du clavier.

            Cette fonction mets à jour la mémoire tampon du clavier en
            transfèrant directement le tout dans la mémoire IO.

            :param keysBuffer: Tabeau mémoire tampon du clavier.
            :type keysbuffer: str

        """
        self.io.lockIO.acquire()
        for i in range(255, 0, -1):
            self.io.data[i] = self.io.data[i - 1]
        self.io.data[0] = asciiTOint(key)
        self.io.lockIO.release()
        return


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
