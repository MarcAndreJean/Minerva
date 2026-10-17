# Travail 1 : Tests unitaires de `DaysUntilDeadline`

Tests unitaires et fuzzing de la fonction `DaysUntilDeadline`, qui calcule le nombre de jours entre la date courante et une échéance. Les tests ont révélé un bogue dans le code fourni : au-delà d'environ 292 ans d'écart, `time.Duration` sature et la fonction retourne 106 751 jours. Il est corrigé en comptant à partir des secondes Unix.

## Contenu

| Fichier | Description |
| --- | --- |
| [rapport.md](rapport.md) | Rapport : choix des cas de test, défis, bogue et correction, déclaration d'utilisation de l'IA |
| [deadline.go](deadline.go) | Fonction `DaysUntilDeadline` (avec la correction) |
| [deadline_test.go](deadline_test.go) | Tests unitaires et fuzzing |
| [go.mod](go.mod) | Module Go |

## Utilisation

```text
go test -cover
go test -fuzz=FuzzDaysUntilDeadline -fuzztime=30s
```

## Outils

Go

---

Fichier généré à l'aide de ChatGPT-6 Luna.
