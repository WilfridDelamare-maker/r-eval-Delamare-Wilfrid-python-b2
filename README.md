# API Stations

API FastAPI de gestion de stations avec validation Pydantic, persistance SQLite via SQLAlchemy et tests avec pytest.

## Structure du projet

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── db_models.py
│   └── db.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_stations.py
├── README.md
├── requirements.txt
├── reponses.md
└── .gitignore
```

## Prérequis

- Python 3
- pip

## Installation

Se placer à la racine du projet.

Créer un environnement virtuel :

```bash
python -m venv .venv
```

Activer l'environnement sous Git Bash :

```bash
source .venv/Scripts/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

## Lancer l'API

Depuis la racine du projet :

```bash
uvicorn app.main:app --reload
```

L'API est disponible à l'adresse :

```text
http://127.0.0.1:8000
```

La documentation Swagger est disponible à l'adresse :

```text
http://127.0.0.1:8000/docs
```

## Routes principales

### Vérification de l'état de l'API

```text
GET /health
```

Réponse attendue :

```json
{
  "status": "ok"
}
```

### Création d'une station

```text
POST /stations
```

Exemple de body :

```json
{
  "code": "ST-01",
  "name": "Centre",
  "capacity": 10,
  "status": "open"
}
```

La station est créée avec un identifiant généré automatiquement.

Une création réussie renvoie le code HTTP `201`.

### Liste des stations

```text
GET /stations
```

Cette route renvoie toutes les stations présentes dans la base.

### Filtre par statut

```text
GET /stations?status=open
```

Cette route renvoie uniquement les stations dont le statut correspond à la valeur demandée.

Les statuts autorisés sont :

```text
open
closed
maintenance
```

### Lecture d'une station par identifiant

```text
GET /stations/{station_id}
```

Exemple :

```text
GET /stations/1
```

Si la station existe, la route renvoie le code HTTP `200`.

Si la station n'existe pas, la route renvoie le code HTTP `404`.

### Modification partielle d'une station

```text
PATCH /stations/{station_id}
```

Le PATCH permet de modifier uniquement `name` ou `status`.

Exemple :

```json
{
  "name": "Nouvelle gare"
}
```

Les champs absents restent inchangés.

Si la station n'existe pas, la route renvoie le code HTTP `404`.

## Validation des données

Les données reçues sont validées avec Pydantic.

Contraintes principales :

- `code` doit être une chaîne non vide
- `code` doit être unique
- `name` doit être une chaîne non vide
- `capacity` doit être un entier supérieur ou égal à `1`
- `status` doit être égal à `open`, `closed` ou `maintenance`
- `status` vaut `open` par défaut

Une donnée invalide produit automatiquement une réponse HTTP `422`.

Exemples invalides :

```json
{
  "code": "ST-01",
  "name": "Centre",
  "capacity": 0,
  "status": "open"
}
```

ou :

```json
{
  "code": "ST-01",
  "name": "Centre",
  "capacity": 10,
  "status": "flying"
}
```

## Base de données

L'application utilise SQLite avec SQLAlchemy.

Les stations sont stockées dans une base SQLite locale.

Contrairement à une simple liste Python en mémoire, les données restent disponibles après un redémarrage de l'application.

La table `stations` contient notamment :

- `id` : clé primaire générée
- `code` : valeur unique
- `name`
- `capacity`
- `status`

Les sessions SQLAlchemy sont fournies aux routes avec :

```python
Depends(get_db)
```

La session est fermée automatiquement après utilisation.

En cas de doublon sur `code`, SQLAlchemy peut déclencher une `IntegrityError`.

Dans ce cas :

- la transaction est annulée avec `rollback()`
- l'API renvoie le code HTTP `409`

## Tests

Les tests utilisent :

- pytest
- FastAPI TestClient
- une base SQLite de test distincte de la base principale

Chaque test démarre avec une base vide.

Les tests sont donc indépendants les uns des autres et ne dépendent pas de leur ordre d'exécution.

## Lancer les tests

Depuis la racine du projet :

```bash
python -m pytest -q
```

Lancer la commande deux fois de suite pour vérifier que les tests restent indépendants :

```bash
python -m pytest -q
python -m pytest -q
```

## Cas testés

Les tests vérifient notamment :

- `GET /health` renvoie `200` et `status = ok`
- création d'une station avec `POST /stations`
- lecture de la station créée avec `GET /stations/{id}`
- filtre `status=open`
- modification du `name` avec `PATCH`
- conservation de `code`, `capacity` et `status` après un PATCH du nom
- lecture d'un identifiant inexistant
- erreur `422` pour `capacity=0`
- erreur `422` pour `status="flying"`
- absence de création après une entrée invalide
- erreur `409` en cas de code déjà existant
- une seule station présente après une tentative de doublon

## Persistance après redémarrage

Pour vérifier la persistance :

1. créer une station avec `POST /stations`
2. vérifier sa présence avec `GET /stations`
3. arrêter Uvicorn avec `Ctrl + C`
4. relancer l'API
5. refaire `GET /stations`

La station doit toujours être présente après le redémarrage.

