# 🐱 MiniCat — Llenguatge minimalista en català

MiniCat és un petit llenguatge de programació inspirat en Lisp, implementat íntegrament en Python.

Està pensat per ser simple, didàctic i transparent, ideal per aprendre com funciona un intèrpret real.

MiniCat utilitza sintaxi basada en expressions entre parèntesis, amb paraules clau en català:

```lisp
(funció argument1 argument2 ...)
```

---

# 🎯 Objectius del projecte

MiniCat mostra com es construeix un intèrpret complet:

- Lexer (tokenitzador)
- Parser
- Representació interna del programa (AST basat en llistes)
- Entorn de variables
- Funcions definides per l’usuari
- Avaluador
- Biblioteca estàndard
- REPL interactiu

Tot en un únic fitxer Python, fàcil de llegir i modificar.

---

# ✨ Característiques

MiniCat inclou:

- Sintaxi tipus Lisp
- Variables i funcions definides per l’usuari
- Funcions recursives
- Condicionals (`si`)
- Bucles (`mentre`)
- Gestió d’errors (`provar`)
- Llistes i diccionaris
- Operacions matemàtiques i trigonomètriques
- Nombres enters i decimals
- Cadenes de text
- Booleans (`cert`, `fals`)
- Comentaris (`;`)
- REPL interactiu

---

# 🧱 Arquitectura del projecte

```text
Codi font
│
├── Lexer
│     Converteix text en tokens
│
├── Parser
│     Converteix tokens en llistes (AST)
│
├── Entorn
│     Guarda variables i funcions
│
├── Biblioteca estàndard
│     Funcions incorporades
│
├── Avaluador
│     Executa l’AST
│
└── REPL
      Consola interactiva
```

---

# 🚀 Instal·lació i execució

Només cal Python 3.

Executa MiniCat:

```bash
python3 minicat.py
```

No necessita cap dependència externa.

Utilitza únicament:

- `math`
- `random`
- `re` (actualment no utilitzat)

---

# 📘 Sintaxi bàsica

Les expressions tenen la forma:

```lisp
(funció argument1 argument2 ...)
```

Exemple:

```lisp
(+ 2 3)
```

Resultat:

```text
5
```

---

# 🧩 Exemples bàsics

## 🔢 Suma

```lisp
(+ 10 20)
```

## 📦 Llistes

```lisp
(llista 1 2 3 4)
```

## 🔍 Accedir al primer element

```lisp
(car (llista 10 20 30))
```

## 🔁 Bucle `mentre`

```lisp
(definir x 0)

(mentre (< x 5)
    (escriure x)
    (definir x (+ x 1))
)
```

## 🧠 Condicional `si`

```lisp
(si (> 10 5)
    "És més gran"
    "No és més gran"
)
```

## 🧮 Funció definida per l’usuari

```lisp
(definir-funció quadrat (n)
    (* n n)
)

(quadrat 7)
```

## 🔁 Recursió

```lisp
(definir-funció factorial (n)
    (si (= n 0)
        1
        (* n (factorial (- n 1)))
    )
)

(factorial 5)
```

---

# 🧪 Exemple complet: suma d’una llista

```lisp
(definir-funció suma (l)
    (si (= (longitud l) 0)
        0
        (+ (car l) (suma (cdr l)))
    )
)

(suma (llista 3 4 5))
```

---

# 🎓 Per què MiniCat és educatiu?

- La sintaxi és mínima → menys soroll, més conceptes.
- Tot és una expressió → com Scheme, ideal per aprendre.
- El codi Python és curt i llegible → perfecte per estudiar intèrprets.
- Les funcions en català ajuden a l’aprenentatge inicial.

---

## 📚 Resum

MiniCat és un llenguatge minimalista inspirat en Lisp que permet explorar els fonaments dels llenguatges de programació i la construcció d’intèrprets. Amb una sintaxi senzilla, funcions en català i una implementació compacta en Python, és una eina ideal tant per a estudiants com per a docents que vulguin entendre el funcionament intern d’un llenguatge de programació.
