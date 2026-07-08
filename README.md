

# MiniCat

MiniCat és un petit llenguatge de programació inspirat en **Lisp** implementat íntegrament en **Python**.

L'objectiu del projecte és mostrar, de manera senzilla i educativa, com es pot construir un intèrpret complet format per:

* Lexer (tokenitzador)
* Parser
* AST (Arbre de Sintaxi Abstracta)
* Entorn de variables
* Funcions definides per l'usuari
* Avaluador
* Biblioteca estàndard
* REPL interactiu

El llenguatge utilitza sintaxi basada en expressions entre parèntesis, molt semblant a Scheme o Lisp, però amb paraules clau en català.

---

# Característiques

MiniCat inclou:

* Sintaxi tipus Lisp
* Variables globals
* Funcions definides per l'usuari
* Funcions anònimes
* Funcions recursives
* Condicionals
* Bucles
* Gestió d'errors
* Llistes
* Diccionaris
* Operacions matemàtiques
* Funcions trigonomètriques
* Nombres enters i decimals
* Cadenes de text
* Booleans
* Comentaris
* REPL interactiu

---

# Arquitectura

El projecte està dividit en diverses parts.

```
Codi font
│
├── Lexer
│     Converteix text en tokens
│
├── Parser
│     Converteix tokens en AST
│
├── Entorn
│     Guarda variables i funcions
│
├── Biblioteca estàndard
│     Funcions incorporades
│
├── Avaluador
│     Executa l'AST
│
└── REPL
      Consola interactiva
```

---

# Instal·lació

Només cal Python 3.

```bash
python3 minicat.py
```

No necessita cap dependència externa.

Només utilitza:

* math
* random
* re (actualment no utilitzat)

---

# Sintaxi

Les expressions tenen la forma:

```lisp
(funció argument1 argument2 ...)
```

Exemple:

```lisp
(+ 2 3)
```

Resultat

```
5
```

---

# Comentaris

Tot el que segueix un punt i coma és un comentari.

```lisp
; això és un comentari
(+ 2 3)
```

---

# Variables

Es creen amb **definir**.

```lisp
(definir x 10)

(definir y 20)

(+ x y)
```

Resultat

```
30
```

---

# Operacions matemàtiques

## Suma

```lisp
(+ 3 5)
```

## Resta

```lisp
(- 8 2)
```

## Multiplicació

```lisp
(* 4 5)
```

## Divisió

```lisp
(/ 20 4)
```

---

# Comparacions

```lisp
(< 3 5)

(> 5 2)

(= 10 10)

(<= 5 8)

(>= 4 4)
```

---

# Booleans

Existeixen dos valors:

```lisp
cert

fals
```

---

# Operadors lògics

```lisp
(i cert cert)

(o fals cert)

(no fals)
```

---

# Condicionals

```lisp
(si (> 10 5)

    "gran"

    "petit")
```

Resultat

```
gran
```

---

# Bucles

```lisp
(definir x 0)

(mentre (< x 5)

    (definir x (+ x 1)))
```

---

# Funcions

## Funció anònima

```lisp
(funció (x)

    (* x x))
```

---

## Definir funcions

```lisp
(definir-funció quadrat (x)

    (* x x))
```

Ús

```lisp
(quadrat 8)
```

Resultat

```
64
```

---

# Funcions recursives

Exemple factorial.

```lisp
(definir-funció factorial (n)

    (si (= n 0)

        1

        (* n
           (factorial (- n 1)))))
```

Després

```lisp
(factorial 5)
```

Resultat

```
120
```

---

# Llistes

Crear

```lisp
(llista 1 2 3 4)
```

Primer element

```lisp
(car (llista 1 2 3))
```

Resultat

```
1
```

Resta de la llista

```lisp
(cdr (llista 1 2 3))
```

Resultat

```
(2 3)
```

Longitud

```lisp
(longitud (llista 1 2 3))
```

---

# Cadenes

```lisp
"Hola món"
```

Concatenació

```lisp
(concat "Hola " "MiniCat")
```

Conversió

```lisp
(cadena 123)
```

---

# Conversió numèrica

```lisp
(numero "123")
```

```lisp
(numero "5.4")
```

---

# Diccionaris

Crear

```lisp
(definir d (diccionari))
```

Assignar

```lisp
(assigna d "nom" "MiniCat")
```

Llegir

```lisp
(obté d "nom")
```

---

# Funcions matemàtiques

Valor de π

```lisp
pi
```

Arrel quadrada

```lisp
(arrel 81)
```

Sinus

```lisp
(sin pi)
```

Cosinus

```lisp
(cos pi)
```

Tangents

```lisp
(tan pi)
```

---

# Nombres aleatoris

```lisp
(aleatori)
```

Retorna un nombre entre

```
0.0

i

1.0
```

---

# Escriure per pantalla

```lisp
(escriure "Hola")
```

També

```lisp
(escriure 1 2 3)
```

---

# Gestió d'errors

MiniCat incorpora una construcció senzilla.

```lisp
(provar

    (/ 5 0)

    "Error")
```

Si hi ha una excepció, retorna el segon valor.

---

# Quote

És possible evitar l'avaluació amb `'`.

```lisp
'(1 2 3)
```

Equivalent a

```lisp
(citar (1 2 3))
```

---

# REPL

En executar el programa apareix:

```
MiniCat v5

minicat>
```

Per sortir:

```
sortir
```

El REPL detecta automàticament quan els parèntesis estan equilibrats.

---

# Exemple complet

```lisp
(definir-funció factorial (n)

    (si (= n 0)

        1

        (* n (factorial (- n 1)))))

(escriure (factorial 6))
```

Sortida

```
720
```

---

# Estructura interna

```
minicat.py

├── Lexer
├── Parser
├── Entorn
├── Funcions MiniCat
├── Biblioteca estàndard
├── Avaluador
├── Execució
└── REPL
```

---

# Limitacions actuals

Actualment MiniCat no disposa de:

* Macros
* Tail Call Optimization
* Fitxers
* Imports
* Mòduls
* Classes
* Objectes
* Lambda variàdica
* Col·lecció d'escombraries pròpia
* Optimitzador
* Compilador

---

# Possibles millores

* Sistema de paquets
* Mòduls
* Excepcions pròpies
* Iteradors
* Funcions d'ordre superior
* map
* filter
* reduce
* JSON
* Entrada/sortida de fitxers
* Expressions regulars
* Biblioteca estàndard ampliada
* Tipus nous (sets, tuples...)
* Compilació a bytecode

---

# Llicència

Aquest projecte és de codi obert i es pot utilitzar amb finalitats educatives, d'aprenentatge i experimentació.

---

# Autor

MiniCat v5 és un intèrpret minimalista inspirat en Lisp, desenvolupat íntegrament en Python amb l'objectiu d'explicar el funcionament intern d'un llenguatge de programació: des de la tokenització fins a l'execució de codi.

