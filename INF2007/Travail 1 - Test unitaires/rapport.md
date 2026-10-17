# INF 2007 Travail 1 : Tests unitaires de `DaysUntilDeadline`

Marc-André Jean

# Choix des cas de test

Chaque cas vérifie un comportement différent de `DaysUntilDeadline`.

## Tests positifs

### Dates valides

Trois cas :

- une échéance future, du 26 mai au 1er juin 2025, qui doit donner 6 jours;
- le même jour, qui doit donner 0. C'est le plus petit résultat possible;
- le plus grand écart possible, du 1er janvier 0000 au 31 décembre 9999, qui doit donner 3 652 424 jours.

Le dernier cas traverse tous les changements d'année et toutes les années bissextiles. Une erreur dans le compte des jours changerait le total. Il n'y a donc pas de cas séparé pour ces situations.

## Tests négatifs

### Dates invalides

Quatre sortes de dates invalides sont testées :

- une date avec un mois qui n'existe pas (« 2025-13-01 », le mois 13);
- une date avec un jour qui n'existe pas dans le mois (« 2025-04-31 », avril n'a que 30 jours);
- une date mal formatée (« 2025/05/26 »);
- une chaîne vide.

Chacune est testée dans la date courante, puis dans l'échéance, parce que la fonction retourne un message d'erreur différent pour chaque paramètre. Un neuvième cas met les deux dates invalides en même temps. La fonction valide la date courante en premier, donc c'est son message qui doit sortir.

### Échéance antérieure

Un cas, avec une échéance en 1999 et une date courante en 2025. La fonction doit retourner une erreur et 0.

## Fuzzing

Le fuzzing génère des entrées automatiquement et cherche celle qui brise une propriété. `FuzzDaysUntilDeadline` vérifie trois propriétés :

- la fonction ne panique jamais;
- une erreur est toujours accompagnée de 0;
- quand il n'y a pas d'erreur, la date courante plus le nombre de jours retourné redonne l'échéance.

La recherche peut se lancer avec `go test -fuzz=FuzzDaysUntilDeadline -fuzztime=30s`. La durée est limitée pour que la commande se termine dans un temps raisonnable.

## Ce qui a été écarté

Les autres façons d'écrire une date invalide n'ont pas de cas écrit à la main : espaces autour de la date, mois sans zéro (« 2025-5-26 »), mois 00, 29 février d'une année non bissextile. Elles sont toutes rejetées par `time.Parse` et passent par la même ligne `if err != nil` que le mois 13. Leur donner chacune un cas reviendrait à tester la bibliothèque standard de Go, pas la fonction. Le fuzzing couvre quand même ce genre d'entrées : il vérifie, sur des millions d'entrées générées, qu'une date invalide n'est pas acceptée avec un mauvais résultat.

# Garantie de bon fonctionnement de la fonction par les tests

## Valeur et erreur vérifiées

Chaque cas vérifie la valeur retournée et l'erreur. Pour une date valide, l'erreur doit être nulle et le nombre de jours exact. Pour un cas d'erreur, le message doit être exactement celui attendu et la valeur doit être 0. Les erreurs attendues sont créées avec `errors.New`, et les tests comparent leurs messages avec ceux des erreurs retournées. Comparer le message permet de savoir que la fonction signale la bonne date, ce qu'un simple `err != nil` ne dirait pas.

Les messages d'échec donnent l'entrée, la valeur obtenue et la valeur attendue. Par exemple, si la fonction retournait 5 au lieu de 6 :

```
DaysUntilDeadline("2025-05-26", "2025-06-01") = 5; expected 6
```

## Couverture

`go test -cover` donne une couverture de 100 %. Toutes les lignes de la fonction sont exécutées par les tests. Une ligne exécutée n'est pas forcément une ligne vérifiée, donc ce sont les valeurs comparées dans chaque test qui comptent.

```
$ go test -cover
PASS
coverage: 100.0% of statements
ok      tn1     0.434s
```

# Les défis rencontrés

## Cas limites

Dans le code fourni, la ligne `int(due.Sub(current).Hours() / 24)` donne le bon résultat pour les dates habituelles. Elle donne un mauvais résultat seulement quand l'écart entre les deux dates dépasse environ 292 ans. Ce bogue a été corrigé (voir la section « Bogue trouvé et correction »).

## Trouver une propriété pour le fuzzing

Le fuzzing demande une propriété qui est vraie pour toutes les entrées. Pour cette fonction, on ne peut pas connaître le bon nombre de jours sans le recalculer. La propriété utilisée fait le chemin inverse : elle ajoute le résultat à la date courante et compare avec l'échéance.

# Bogue trouvé et correction

## Le bogue

Le code fourni donne un mauvais résultat quand l'écart entre les deux dates dépasse environ 292 ans. `due.Sub(current)` retourne un `time.Duration`, qui est un `int64` de nanosecondes. Sa valeur maximale correspond à environ 292 ans. Au-delà, `Sub` retourne cette valeur maximale. La fonction retourne alors 106 751 jours, sans erreur, peu importe l'écart réel.

Avec le code fourni, le cas du plus grand écart échoue :

```
--- FAIL: TestDaysUntilDeadlineValid/largest_gap (0.00s)
    deadline_test.go:37: DaysUntilDeadline("0000-01-01", "9999-12-31") = 106751; expected 3652424
```

## La correction

L'écart est calculé en secondes plutôt qu'en nanosecondes. La ligne :

```go
days := int(due.Sub(current).Hours() / 24)
```

est remplacée par :

```go
// Count from Unix seconds rather than due.Sub(current): a time.Duration
// (int64 nanoseconds) saturates at about 292 years.
// 86400 = 60 seconds x 60 minutes x 24 hours = number of seconds in a day.
days := int((due.Unix() - current.Unix()) / 86400)
```

## Pourquoi la correction fonctionne

`Unix()` donne le nombre de secondes depuis le 1er janvier 1970. Pour les années 0000 à 9999, l'écart maximal est d'environ 3.2 * 10^11 secondes. La limite d'un `int64` est d'environ 9.2 * 10^18, donc la valeur maximale n'est plus atteinte. La division par 86 400 est exacte, parce que les deux dates sont toujours à minuit (00:00:00).

Le résultat attendu pour le plus grand écart se vérifie à la main. Le calendrier grégorien se répète tous les 400 ans, soit 146 097 jours. Dix mille ans divisé par 400 donne 25. Ainsi, dix mille ans font 146 097 * 25 = 3 652 425 jours. Il faut en enlever un, puisqu'on compte l'écart entre le premier et le dernier jour : 3 652 424. C'est la valeur que retourne la fonction corrigée.

# Déclaration d'utilisation de l'IA

Auto-complétion de Copilot utilisée dans Visual Studio Code.

Avec Gemini :

1.
```
Quelles sont les limitations de time.Parse en Go?
```

2.
```
Si on divise la valeur maximale d'un float64 par 24, le résultat serait-il supérieur aux valeurs maximales d'un int32 et d'un int64?
```

3.
```
Combien d'années peut-on représenter avec un int64 exprimé en nanosecondes?
```

4.
```
Combien de jours entre "0000-01-01" et "9999-12-31" et pourquoi?
````

5.
```
Combien d'années le cycle complet du calendrier grégorien fait-il? Et combien de jours cela représente-t-il?
```

6.
```
Est-ce que "time.Parse" de Go attribue une heure?
```

Avec ChatGPT-6 Luna :
1.
```
Fais une liste des fautes à corriger.
Pour chaque point, indique l’ancienne phrase, suivie de la phrase proposée. Utilise le format suivant :
1. `old` => `new`. [Raison de la correction.]
```
Le fichier du rapport a été joint à la conversation avec ChatGPT.
