#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Projet          : Editeur, Compilateur et Micro-Ordinateur pour
                      un langage assembleur.
    Nom du fichier  : 05-Enum.py

    Identification  : 05-Enum
    Titre           : Enum
    Auteurs         : Marc-André Jean
    Date            : 14-04-2017
    Description     : Enum pour les OPCODE's, REGISTRE's, ADRESSAGE's
                      et MODE's.


    Le module ``Enum``
    ================================

    Ce module contient une fonction pour créer des types Enum's. Ce
    module contient aussi des énumérations pour les OPCODE's, les
    REGISTRE's et pour les ADRESSAGE's.


"""

# Dictionnaire Whitelist du code ASCII permit.


def intTOascii(code):
    """
        Convertit code en lettre ascii.

        Cette fonction convertit le nombre code en une lettre ascii.

        :example:
        >>> intTOascii(65)
        'A'
        >>> intTOascii(0xFFFF)
        '.'

        :param code: Nombre représentant une lettre ascii.
        :type code: int
        :return: Lettre ascii.
        :rtype: str

    """
    # Contrôle des types.
    try:
        if isinstance(code, str):
            if len(code) == 0:
                return '.'
            elif len(code) > 1:
                code = ord(code[-1])
            else:
                code = ord(code)
        elif isinstance(code, unicode):
            return '.'
    except NameError:
        pass

    # Retourne un ' ' si c'est une code non permit.
    if code < 0x20 or code > 0x7E:
        return '.'
    # Sinon retourne le code ascii normal.
    else:
        return chr(code)


def asciiTOint(code):
    """
        Convertit lettre ascii en int.

        Cette fonction convertit une lettre ascii en code.

        :example:
        >>> asciiTOint('a')
        97
        >>> asciiTOint('è')
        0

        :param code: Une lettre ascii.
        :type code: str
        :return: code ascii.
        :rtype: int

    """
    # Contrôle des types.
    try:
        if isinstance(code, str):
            if len(code) == 0:
                return 0
            elif len(code) > 1:
                if code[-1] < 0x0000 or code[-1] > 0x007E:
                    return 0
                return ord(code[-1])
            else:
                return ord(code)
        elif isinstance(code, unicode):
            return 0
    except NameError:
        pass

    # Retourne 0 si c'est une lettre non permise.
    if code < 0x0000 or code > 0x007E:
        return 0
    # Sinon retourne le code ascii normal.
    else:
        return ord(code)


def enum(**enums):
    """
        Création du type Enum pour le besoin de l'application.

        :return: Un type Enum
        :rtype: Enum

        >>> ENUMTEST = enum(VRAI = True, FAUX = False)
        >>> ENUMTEST.VRAI
        True
        >>> ENUMTEST.FAUX
        False

    """
    return type('Enum', (), enums)

# Énumération pour la vue 01-01-Ordinateur.
TYPEUSE = enum(NORMAL=1, LIGNECOMMANDE=2)

# Énumération pour le mode du bus.
MODE = enum(INERTE=0x0000,
            READ=0x0001,
            WRITE=0x0002,
            END=0x0004,  # Fin instruction
            RESET=0x0008,
            HALT=0x0009)

# Enumération pour les opérateurs.
OPCODE = enum(NOP=0x0000,
              JMP=0x0100,
              JMZ=0x0200,
              JMO=0x0300,
              JMC=0x0400,
              SET=0x0500,
              LD=0x0600,
              ST=0x0700,
              MV=0x0800,
              HLT=0x0F00,
              # Commande pour l'ALU.
              ADD=0x1100,
              SUB=0x1200,
              MUL=0x1300,
              DIV=0x1400,
              OR=0x2100,
              AND=0x2200,
              XOR=0x2300,
              NOT=0x2400,
              # Comparateurs.
              LT=0x3100,
              GT=0x3200,
              LE=0x3300,
              GE=0x3400,
              EQ=0x3500,
              EZ=0x3600,
              NZ=0x3700,
              # --Chaine de caractères.
              DTA=0xFFFF)

# Enumération pour le registre.
REGISTRE = enum(A=0x0001, B=0x0002, C=0x0003, D=0x0004)

# Enumeration pour le type d'adressage.
# 1. L'argument est l'adresse d'un registre.
# 2. L'argument est l'adresse d'un registre qui pointe vers une adresse.
# 3. L'argument est une adresse.
# 4. L'argument est une adresse qui pointe vers une adresse.
ADRESSAGE = enum(ADDR_OF_REG=0x0010,
                 ADDR_FROM_REG=0x0020,
                 ADDR=0x0030,
                 ADDR_FROM_ADDR=0x0040)


# Activation des doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()
