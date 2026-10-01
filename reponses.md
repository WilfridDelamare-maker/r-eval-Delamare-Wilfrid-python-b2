# j'ai mis la partie 2 du Controle dans un fichier exercice2.txt car après j'ai remplacé par la db SQLite !

1. Une route GET /stations crée une station. Quel verbe et quel code HTTP faut-il utiliser pour cette création ?
il faut faire app.post('/stations', status_code=201)

2. GET /stations/999 demande une station inexistante. Quel code HTTP et quel type de réponse faut-il renvoyer ?
Il faut envoyer une 404 Ressource Not found de type raise HTTPexception.


3. Quelle est la différence entre les codes 401 et 403 ? Donnez un exemple de chaque cas.
401 c'est non autorisé car pas connecté avec le token ou session expirée...
403 c'est interdit meme si authentifié, l'utilisateur n'a pas droit d'accéder. exemple: un simple user veut accéder à une partie admin 



Après avoir créé une station, puis arrêté et relancé l'application, la station est toujours présente dans eval.db. Le post a réussi dans le /docs.
Conclusion : les données sont bien persistées dans la base SQLite et ne dépendent plus d'une liste en mémoire.

## Tests pytest

Première exécution :

`python -m pytest -q`

python -m pytest -q
........                                                                                                          [100%]
=================================================== warnings summary ===================================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\lloyd\Desktop\r-eval-Delamare-Wilfrid-python-b2\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
8 passed, 1 warning in 0.33s
(.venv) 

Tous les tests passent.

Deuxième exécution :

`python -m pytest -q`

python -m pytest -q
........                                                                                                          [100%]
=================================================== warnings summary ===================================================
.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\lloyd\Desktop\r-eval-Delamare-Wilfrid-python-b2\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
8 passed, 1 warning in 0.16s
(.venv)

Tous les tests passent également.

Les tests sont indépendants et utilisent une base SQLite de test vide pour chaque test.