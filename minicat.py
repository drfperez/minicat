#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniCat: un mini-llenguatge de programació funcional en català.
Sintaxi Lisp amb paraules clau catalanes.
Autor: Francesc Pérez García 
"""

import re

# ---------- 1. Anàlisi lèxica ----------
def tokenitza(codi):
    """Converteix el codi font en una llista de tokens."""
    patrons = [
        (r'\(', 'PAR_ESQ'),
        (r'\)', 'PAR_DRET'),
        (r'"[^"]*"', 'CADENA'),
        (r'\d+\.?\d*', 'NUMERO'),
        (r'[^\s()"]+', 'SIMBOL')
    ]
    tokens = []
    pos = 0
    while pos < len(codi):
        if codi[pos].isspace():
            pos += 1
            continue
        for patro, tipus in patrons:
            m = re.match(patro, codi[pos:])
            if m:
                valor = m.group(0)
                if tipus == 'CADENA':
                    valor = valor[1:-1]   # treure cometes
                elif tipus == 'NUMERO':
                    valor = float(valor) if '.' in valor else int(valor)
                tokens.append((tipus, valor))
                pos += m.end()
                break
        else:
            raise SyntaxError(f"Caràcter inesperat: {codi[pos]}")
    return tokens


# ---------- 2. Anàlisi sintàctica ----------
def analitza(tokens):
    """Converteix tokens en una estructura de llistes niades (AST)."""
    if not tokens:
        raise SyntaxError("Expressió incompleta")
    token = tokens.pop(0)
    tipus, valor = token
    if tipus == 'PAR_DRET':
        raise SyntaxError("Parèntesi inesperat")
    if tipus != 'PAR_ESQ':
        return valor   # àtom (nombre, cadena, símbol)

    # Llista d'expressions
    ast = []
    while tokens and tokens[0][0] != 'PAR_DRET':
        ast.append(analitza(tokens))
    if not tokens:
        raise SyntaxError("Falta tancar parèntesi")
    tokens.pop(0)  # descartar ')'
    return ast


def analitza_programa(codi):
    """Retorna l'AST del programa complet."""
    tokens = tokenitza(codi)
    if not tokens:
        return None
    return analitza(tokens)


# ---------- 3. Entorn i avaluació ----------
class Entorn(dict):
    """Diccionari amb enllaç a l'entorn pare (àmbit lèxic)."""
    def __init__(self, pare=None):
        super().__init__()
        self.pare = pare

    def buscar(self, clau):
        if clau in self:
            return self[clau]
        if self.pare:
            return self.pare.buscar(clau)
        raise NameError(f"Símbol no definit: {clau}")


def entorn_inicial():
    """Crea l'entorn global amb totes les primitives."""
    env = Entorn()
    env.update({
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '=': lambda a, b: a == b,
        '<': lambda a, b: a < b,
        '>': lambda a, b: a > b,
        '<=': lambda a, b: a <= b,
        '>=': lambda a, b: a >= b,
        'i': lambda a, b: a and b,
        'o': lambda a, b: a or b,
        'no': lambda a: not a,
        'llista': lambda *args: list(args),
        'escriure': lambda *args: print(*args),
        'prova': lambda *args: args[-1] if args else None,
        'carrega': lambda modul: __import__(modul),
    })
    return env


def avalua(expr, entorn):
    """Avalua una expressió en l'entorn donat."""
    # Àtom: nombre, cadena, o símbol
    if not isinstance(expr, list):
        if isinstance(expr, str):       # símbol -> buscar-lo a l'entorn
            return entorn.buscar(expr)
        return expr                     # literal (nombre, cadena)

    # Llista buida
    if not expr:
        return None

    cap = expr[0]

    # Formes especials (no avaluen tots els arguments immediatament)
    if cap == 'definir':
        if len(expr) != 3:
            raise SyntaxError("definir requereix 2 arguments (nom valor)")
        _, nom, valor_expr = expr
        entorn[nom] = avalua(valor_expr, entorn)
        return entorn[nom]

    if cap == 'funció':
        if len(expr) != 3:
            raise SyntaxError("funció requereix 2 arguments (paràmetres cos)")
        _, params, cos = expr
        return lambda *args, p=params, c=cos, e=Entorn(entorn): (
            avalua(c, dict(zip(p, args), pare=e))
        )

    if cap == 'si':
        if len(expr) == 3:
            _, cond, branca_si = expr
            branca_no = None
        elif len(expr) == 4:
            _, cond, branca_si, branca_no = expr
        else:
            raise SyntaxError("si requereix 2 o 3 arguments (cond conseqüent [alternatiu])")
        if avalua(cond, entorn):
            return avalua(branca_si, entorn)
        elif branca_no is not None:
            return avalua(branca_no, entorn)
        else:
            return None

    # Crida a funció (primitiva o definida per l'usuari)
    funcio = avalua(cap, entorn)
    args = [avalua(arg, entorn) for arg in expr[1:]]
    return funcio(*args)


# ---------- 4. Intèrpret principal ----------
entorn_global = entorn_inicial()

def executa(codi):
    """Executa un string de codi en MiniCat."""
    ast = analitza_programa(codi)
    if ast is None:
        return None
    return avalua(ast, entorn_global)


def executa_fitxer(ruta):
    """Executa un fitxer .cat."""
    with open(ruta, 'r', encoding='utf-8') as f:
        codi = f.read()
    return executa(codi)


def repl():
    """Bucle interactiu (Read-Eval-Print Loop)."""
    print("MiniCat REPL. Escriu 'sortir' per acabar.")
    while True:
        try:
            codi = input("minicat> ")
            if codi.strip() == 'sortir':
                break
            resultat = executa(codi)
            if resultat is not None:
                print(resultat)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        executa_fitxer(sys.argv[1])
    else:
        repl()
