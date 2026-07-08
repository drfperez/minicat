#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniCat v4 – Llenguatge funcional complet en català amb compilació nativa.
Novetats:
- `(compila expr)` retorna una funció Python compilada a bytecode.
- Suport per compilar condicionals, bucles, llistes, crides, etc.
"""

import re, math, random, sys, io

# ---------- Traça ----------
traça_activa = False
prof_traça = 0

def traça_log(entrant, expr, res=None):
    if not traça_activa:
        return
    indent = "  " * prof_traça
    if entrant:
        print(f"{indent}-> {expr}")
    else:
        print(f"{indent}<- {res}")

# ---------- Lèxic ----------
def tokenitza(codi):
    tokens = []
    pos, linia = 0, 1
    while pos < len(codi):
        while pos < len(codi) and codi[pos].isspace():
            if codi[pos] == '\n': linia += 1
            pos += 1
        if pos >= len(codi): break
        if codi[pos] == ';':
            while pos < len(codi) and codi[pos] != '\n': pos += 1
            continue
        if codi[pos] == '(':
            tokens.append(('PAR_ESQ','(',linia)); pos+=1; continue
        if codi[pos] == ')':
            tokens.append(('PAR_DRET',')',linia)); pos+=1; continue
        if codi[pos] == '"':
            fi = codi.find('"', pos+1)
            if fi==-1: raise SyntaxError(f"Línia {linia}: falta tancar \"")
            tokens.append(('CADENA',codi[pos+1:fi],linia)); pos=fi+1; continue
        if codi[pos] == "'":
            tokens.append(('CITA',"'",linia)); pos+=1; continue
        m = re.match(r'\d+\.?\d*', codi[pos:])
        if m:
            val = m.group(0)
            tokens.append(('NUMERO', float(val) if '.' in val else int(val), linia))
            pos += m.end(); continue
        m = re.match(r'[^\s()"\';]+', codi[pos:])
        if m:
            tokens.append(('SIMBOL',m.group(0),linia)); pos+=m.end(); continue
        raise SyntaxError(f"Línia {linia}: caràcter inesperat '{codi[pos]}'")
    return tokens

# ---------- Sintaxi ----------
def analitza(tokens):
    if not tokens: raise SyntaxError("Expressió incompleta")
    tipus, valor, linia = tokens.pop(0)
    if tipus == 'PAR_DRET': raise SyntaxError(f"Línia {linia}: ')' inesperat")
    if tipus == 'CITA':
        if not tokens: raise SyntaxError(f"Línia {linia}: falta expressió després de '")
        return ['citar', analitza(tokens)]
    if tipus != 'PAR_ESQ': return valor
    ast = []
    while tokens and tokens[0][0] != 'PAR_DRET':
        ast.append(analitza(tokens))
    if not tokens: raise SyntaxError(f"Línia {linia}: falta ')'")
    tokens.pop(0)
    return ast

def analitza_programa(codi):
    tokens = tokenitza(codi)
    return analitza(tokens) if tokens else None

# ---------- Entorn ----------
class Entorn(dict):
    def __init__(self, pare=None):
        super().__init__()
        self.pare = pare
    def buscar(self, clau):
        if clau in self: return self[clau]
        if self.pare: return self.pare.buscar(clau)
        raise NameError(f"Símbol no definit: {clau}")

entorn_global = None

def entorn_inicial():
    e = Entorn()
    e.update({
        'cert': True, 'fals': False, 'pi': math.pi, 'e': math.e,
        '+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b,
        '/': lambda a,b: a/b, 'modul': lambda a,b: a%b,
        'expon': lambda a,b: a**b, 'arrel': lambda a: math.sqrt(a),
        'sin': lambda a: math.sin(a), 'cos': lambda a: math.cos(a),
        'tan': lambda a: math.tan(a), 'abs': lambda a: abs(a),
        'aleatori': lambda: random.random(),
        '=': lambda a,b: a==b, '<': lambda a,b: a<b, '>': lambda a,b: a>b,
        '<=': lambda a,b: a<=b, '>=': lambda a,b: a>=b,
        'i': lambda a,b: a and b, 'o': lambda a,b: a or b, 'no': lambda a: not a,
        'llista': lambda *a: list(a), 'vector': lambda *a: list(a),
        'cons': lambda a,b: [a]+b if isinstance(b,list) else [a,b],
        'car': lambda l: l[0] if l else None,
        'cdr': lambda l: l[1:] if isinstance(l,list) and len(l)>1 else [],
        'buit?': lambda l: len(l)==0 if isinstance(l,list) else True,
        'llista?': lambda x: isinstance(x,list),
        'vector?': lambda x: isinstance(x,list),
        'longitud': lambda x: len(x),
        'concat': lambda *a: ''.join(str(x) for x in a),
        'subcadena': lambda s,i,j: s[i:j],
        'cadena': lambda x: str(x), 'numero': lambda x: float(x) if '.' in str(x) else int(x),
        'escriure': lambda *a: print(*a),
        'llegir': lambda: input(), 'llegir-numero': lambda: float(input()),
        'carrega-fitxer': lambda fitxer: executa_fitxer(fitxer),
        'prova': lambda *a: a[-1] if a else None,
        'diccionari': lambda **kv: kv,
        'assigna': lambda d,k,v: d.update({k:v}),
        'obté': lambda d,k,defecte=None: d.get(k,defecte),
        'claus': lambda d: list(d.keys()), 'valors': lambda d: list(d.values()),
        'activar-traça': lambda: activa_traça(),
        'desactivar-traça': lambda: desactiva_traça(),
    })
    return e

# ---------- Macros ----------
macro_taula = {}
def definir_macro(nom, fn):
    macro_taula[nom] = fn

def expandir_macros(expr):
    if not isinstance(expr, list): return expr
    if not expr: return expr
    cap = expr[0]
    if isinstance(cap, str) and cap in macro_taula:
        macro_fn = macro_taula[cap]
        expansio = macro_fn(*expr[1:])
        return expandir_macros(expansio)
    return [expandir_macros(sub) for sub in expr]

# ---------- TCO (trampolí) ----------
class Cua:
    __slots__ = ('expr', 'entorn')
    def __init__(self, expr, entorn):
        self.expr = expr
        self.entorn = entorn

# ---------- Avaluació interpretada ----------
def avalua(expr, entorn):
    global prof_traça
    expr = expandir_macros(expr)
    traça_log(True, expr)
    prof_traça += 1
    try:
        while True:
            if not isinstance(expr, list):
                res = expr if not isinstance(expr, str) else entorn.buscar(expr)
                break
            if not expr:
                res = None; break
            cap = expr[0]

            # --- Formes especials ---
            if cap == 'definir':
                _, nom, val_expr = expr
                entorn[nom] = avalua(val_expr, entorn)
                res = entorn[nom]; break
            elif cap == 'definir-funció':
                _, nom, params, cos = expr
                if not isinstance(params, list):
                    raise SyntaxError("Paràmetres han de ser llista")
                child = Entorn(entorn)
                def func(*args):
                    local = dict(zip(params, args))
                    local['pare'] = child
                    resultat = avalua(cos, local)
                    while isinstance(resultat, Cua):
                        f, *args2 = resultat.expr
                        resultat = f(*args2)
                    return resultat
                child[nom] = func
                entorn[nom] = func
                res = func; break
            elif cap == 'funció':
                _, params, cos = expr
                if not isinstance(params, list):
                    raise SyntaxError("Paràmetres han de ser llista")
                child = Entorn(entorn)
                def lambda_func(*args, p=params, c=cos, e=child):
                    local = dict(zip(p, args))
                    local['pare'] = e
                    resultat = avalua(c, local)
                    while isinstance(resultat, Cua):
                        f, *args2 = resultat.expr
                        resultat = f(*args2)
                    return resultat
                res = lambda_func; break
            elif cap == 'si':
                if len(expr)==3: _, cond_expr, si_br = expr; no_br = None
                elif len(expr)==4: _, cond_expr, si_br, no_br = expr
                else: raise SyntaxError("si requereix 2 o 3 arguments")
                if avalua(cond_expr, entorn):
                    expr = si_br
                elif no_br is not None:
                    expr = no_br
                else:
                    res = None; break
            elif cap == 'mentre':
                _, cond_expr, cos_expr = expr
                res = None
                while avalua(cond_expr, entorn):
                    res = avalua(cos_expr, entorn)
                break
            elif cap == 'provar':
                _, cos_expr, rec_expr = expr
                try:
                    res = avalua(cos_expr, entorn)
                except Exception:
                    res = avalua(rec_expr, entorn)
                break
            elif cap == 'citar':
                res = expr[1]; break
            elif cap == 'definir-macro':
                _, nom, fn_expr = expr
                fn = avalua(fn_expr, entorn)
                definir_macro(nom, fn)
                res = fn; break
            elif cap == 'compila':
                # NOVA: compilació potent
                if len(expr) != 2:
                    raise SyntaxError("compila requereix 1 argument (expressió)")
                ast_a_compilar = expr[1]
                res = _compila_ast(ast_a_compilar, entorn)
                break
            else:
                funcio = avalua(cap, entorn)
                args = [avalua(arg, entorn) for arg in expr[1:]]
                if callable(funcio):
                    resultat = funcio(*args)
                    if isinstance(resultat, Cua):
                        expr = resultat.expr
                        entorn = resultat.entorn
                        continue
                    res = resultat
                    break
                else:
                    raise TypeError(f"{cap} no és cridable")
        prof_traça -= 1
        traça_log(False, expr, res)
        return res
    finally:
        prof_traça -= 1

# ---------- COMPILADOR A PYTHON (NOU) ----------
OPS_DIRECTES = {
    '+': '({} + {})', '-': '({} - {})', '*': '({} * {})', '/': '({} / {})',
    'modul': '({} % {})', 'expon': '({} ** {})',
    '=': '({} == {})', '<': '({} < {})', '>': '({} > {})',
    '<=': '({} <= {})', '>=': '({} >= {})',
    'i': '({} and {})', 'o': '({} or {})', 'no': '(not {})',
    'arrel': '(math.sqrt({}))', 'sin': '(math.sin({}))',
    'cos': '(math.cos({}))', 'tan': '(math.tan({}))',
    'abs': '(abs({}))',
    'concat': '("".join(str(x) for x in ({})))',
}

def _tradueix_ast(ast, entorn_capturat, profunditat=0):
    if not isinstance(ast, list):
        if isinstance(ast, str):
            return f"entorn_capturat['{ast}']"
        else:
            return repr(ast)
    if not ast:
        return 'None'
    cap = ast[0]
    if cap == 'si':
        if len(ast) == 3: _, cond, si_br = ast; no_br = None
        elif len(ast) == 4: _, cond, si_br, no_br = ast
        else: raise SyntaxError("si mal format")
        cond_py = _tradueix_ast(cond, entorn_capturat)
        si_py = _tradueix_ast(si_br, entorn_capturat)
        if no_br is not None:
            no_py = _tradueix_ast(no_br, entorn_capturat)
            return f"({si_py} if {cond_py} else {no_py})"
        else:
            return f"({si_py} if {cond_py} else None)"
    elif cap == 'mentre':
        _, cond, cos = ast
        cond_py = _tradueix_ast(cond, entorn_capturat)
        cos_py = _tradueix_ast(cos, entorn_capturat)
        return f"(None, exec('''while {cond_py}:\\n    {cos_py}'''))[0]"
    elif cap == 'provar':
        _, cos, rec = ast
        cos_py = _tradueix_ast(cos, entorn_capturat)
        rec_py = _tradueix_ast(rec, entorn_capturat)
        return f"((lambda: {cos_py})() if True else None) or {rec_py}"
    elif cap == 'llista':
        elems = ', '.join(_tradueix_ast(e, entorn_capturat) for e in ast[1:])
        return f"[{elems}]"
    elif cap == 'vector':
        elems = ', '.join(_tradueix_ast(e, entorn_capturat) for e in ast[1:])
        return f"[{elems}]"
    elif cap == 'cons':
        a = _tradueix_ast(ast[1], entorn_capturat)
        b = _tradueix_ast(ast[2], entorn_capturat)
        return f"([{a}] + {b} if isinstance({b}, list) else [{a}, {b}])"
    elif cap == 'car':
        l = _tradueix_ast(ast[1], entorn_capturat)
        return f"({l}[0] if {l} else None)"
    elif cap == 'cdr':
        l = _tradueix_ast(ast[1], entorn_capturat)
        return f"({l}[1:] if isinstance({l}, list) and len({l})>1 else [])"
    elif cap == 'definir-funció':
        _, nom, params, cos = ast
        param_list = ', '.join(params)
        cos_py = _tradueix_ast(cos, entorn_capturat)
        codi_funcio = f"""
def {nom}(entorn_capturat, {param_list}):
    return {cos_py}
"""
        return codi_funcio
    elif cap == 'funció':
        _, params, cos = ast
        param_list = ', '.join(params)
        cos_py = _tradueix_ast(cos, entorn_capturat)
        codi = f"lambda entorn_capturat, {param_list}: {cos_py}"
        return f"({codi})"
    if isinstance(cap, str) and cap in OPS_DIRECTES:
        plantilla = OPS_DIRECTES[cap]
        if cap in ('no', 'arrel', 'sin', 'cos', 'tan', 'abs'):
            arg = _tradueix_ast(ast[1], entorn_capturat)
            return plantilla.format(arg)
        elif cap == 'concat':
            args_py = ', '.join(_tradueix_ast(a, entorn_capturat) for a in ast[1:])
            return f'"".join(str(x) for x in ({args_py}))'
        else:
            a = _tradueix_ast(ast[1], entorn_capturat)
            b = _tradueix_ast(ast[2], entorn_capturat)
            return plantilla.format(a, b)
    funcio_py = _tradueix_ast(cap, entorn_capturat)
    args_py = ', '.join(f"entorn_capturat, {_tradueix_ast(a, entorn_capturat)}" for a in ast[1:])
    return f"{funcio_py}({args_py})"

def _compila_ast(ast, entorn):
    entorn_capturat = dict(entorn)
    try:
        codi_generat = _tradueix_ast(ast, entorn_capturat)
    except Exception as e:
        raise RuntimeError(f"Error en compilació: {e}")
    if isinstance(codi_generat, str) and codi_generat.strip().startswith('def '):
        capçalera = "import math\n"
        codi_complet = capçalera + codi_generat
        namespace = {}
        exec(codi_complet, namespace)
        nom_funcio = codi_generat.split()[1].split('(')[0]
        funcio_python = namespace[nom_funcio]
        def embolcall_def(*args):
            return funcio_python(entorn_capturat, *args)
        return embolcall_def
    else:
        codi_lambda = f"lambda entorn_capturat: {codi_generat}"
        namespace = {}
        exec(f"import math\n_f = {codi_lambda}", namespace)
        funcio_python = namespace['_f']
        def embolcall_expr():
            return funcio_python(entorn_capturat)
        return embolcall_expr

# ---------- Execució global ----------
def executa(codi):
    global entorn_global
    if entorn_global is None:
        entorn_global = entorn_inicial()
    ast = analitza_programa(codi)
    return avalua(ast, entorn_global) if ast is not None else None

def executa_fitxer(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        codi = f.read()
    return executa(codi)

def activa_traça():
    global traça_activa
    traça_activa = True
    return "traça activada"

def desactiva_traça():
    global traça_activa
    traça_activa = False
    return "traça desactivada"

# ---------- REPL ----------
def parentesi_equilibrat(codi):
    oberts = 0
    for c in codi:
        if c == '(': oberts += 1
        elif c == ')': oberts -= 1
        if oberts < 0: return False
    return oberts == 0

def repl():
    print("MiniCat v4 REPL. Escriu 'sortir' per acabar.")
    acumulat, prompt = "", "minicat> "
    while True:
        try:
            linia = input(prompt)
            if linia.strip() == 'sortir': break
            acumulat += linia + "\n"
            if parentesi_equilibrat(acumulat):
                resultat = executa(acumulat)
                if resultat is not None:
                    print(resultat)
                acumulat, prompt = "", "minicat> "
            else:
                prompt = "... "
        except Exception as e:
            print(f"Error: {e}")
            acumulat, prompt = "", "minicat> "

if __name__ == "__main__":
    if len(sys.argv) > 1:
        executa_fitxer(sys.argv[1])
    else:
        repl()
