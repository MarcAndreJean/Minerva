#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 02-FonctionEditeur.py

    Identification  : 02-FonctionEditeur.py
    Titre           : Fonction Editeur
    Auteurs         : Marc-André Jean
    Date            : 13-04-2017
    Description     : Interface de sauvegarde/chargement de fichier.


    Le module ``FonctionEditeur``
    ================================

    Ce module contient des fonctions pour permettre la sauvegarde et le
    chargement de fichier *.asm en format texte. Le
    module contient aussi des fonctions pour permettre la sauvegarde et le
    chargement de fichier *.exeb en format binaire.


"""

__author__ = "Marc-Andre Jean"
__version__ = "1.0"
__status__ = "Production"

import os
import struct


def saveTextCode(path, code):
    """
        Sauvegarde du code en version texte.

        Cette fonction sauvegarde l'argument « code » dans le chemin
        argument « path ».

        :example:
        >>> saveTextCode("C:/test.asm", "mov 10 acc")
        >>> os.remove("C:/test.asm")

        :param path: Chemin du fichier.
        :type path: str
        :param code: Données.
        :type code: str

    """
    # On ouvre le fichier et nous écrivons à les données à l'intérieur.
    fichier = open(path, "w")
    fichier.write(code)
    # Nous fermons le fichier et quittons la fonction.
    fichier.close()
    return


def loadTextCode(path):
    """
        Charge du code en version texte.

        Cette fonction charge le texte du fichier situer à
        l'emplacement de l'argument « path ». La fonction retourne
        ensuite le texte.

        :example:
        >>> saveTextCode("C:/test.asm", "mov 10 acc")
        >>> loadTextCode("C:/test.asm")
        'mov 10 acc'
        >>> os.remove("C:/test.asm")

        :param path: Chemin du fichier
        :type path: str
        :return: Texte du fichier.
        :rtype: str

    """
    # On ouvre le fichier
    fichier = open(path, "r")
    # Nous lisons le texte et le transfèrons dans notre variable.
    code = fichier.read()
    # On ferme le fichier et on retourne le code.
    fichier.close()
    return code


def saveByteCode(path, bytecode):
    """
        Sauvegarde du bytecode en version binaire.

        Cette fonction sauvegarde le bytecode en argument dans un
        fichier binaire.

        :example:
        >>> saveByteCode("C:/test.exeb", [0x0200, 0x0001])
        >>> os.remove("C:/test.exeb")

        :param path: Chemin du fichier.
        :type path: str
        :param code: Bytecodes.
        :type code: int[]

    """
    # On ouvre le fichier et nous écrivons les données à l'intérieur.
    fichier = open(path, "wb")
    try:
        # Nous écrivons les bytes (16 bits) en argument.
        for i in range(len(bytecode)):
            # On écrit les 16 bits
            fichier.write(struct.pack('>H', bytecode[i]))
        # Nous finnisons de remplir le fichier avec des NOP (0x0000)
        if (len(bytecode) < 0x40FB):
            for i in range(len(bytecode), 0x40FB + 1):
                fichier.write(struct.pack('>H', 0))
    # Si une erreur survient
    except Exception as e:
        fichier.close()
        os.remove(path)
        raise e
    # Nous fermons le fichier et quittons la fonction.
    fichier.close()
    return


def loadByteCode(path):
    """
        Chargement du bytecode en version binaire.

        Cette fonction charge le bytecode d'un fichier binaire et
        retourne une liste de int représentant le bytecode.

        :example:
        >>> saveByteCode("C:/test.exeb", [0x0200, 0xFFFF])
        >>> loadByteCode("C:/test.exeb")[0:2]
        [512, 65535]
        >>> os.remove("C:/test.exeb")

        :param path: Chemin du fichier.
        :type path: str
        :return: Bytecodes.
        :rtype: int[]

    """
    # On ouvre le fichier et nous écrivons à les données à l'intérieur.
    fichier = open(path, "rb")
    bytecode = []
    try:
        # Nous écrivons les bytes (16 bits) en argument.
        for i in range(0, 0x40FB + 1):
            bytecode.append(int(struct.unpack('>H', fichier.read(2))[0]))
    # Si une erreur survient
    except Exception as e:
        fichier.close()
        raise e
    # On ferme le fichier et on revoie le résultat.
    fichier.close()
    return bytecode


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
