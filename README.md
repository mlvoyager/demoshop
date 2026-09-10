# ShopDemo — Application e-commerce (Flask)

Application e-commerce simple et basique, pensee comme support pour un projet DevOps
(Dockerfile, pipeline CI/CD, Kubernetes, ArgoCD).

## Fonctionnalites

- Catalogue de produits (page d'accueil)
- Page de detail produit
- Panier (stocke en session Flask)
- Ajout / suppression d'articles
- Validation de commande (simulee, sans paiement reel)
- Endpoint `/healthz` pour les health checks (utile pour Kubernetes)

## Stack technique

- Python 3 / Flask
- Flask-SQLAlchemy (base SQLite embarquee, creee et remplie automatiquement au demarrage)
- Gunicorn (serveur WSGI pour la production / conteneur)

## Lancer en local

```bash
python -m venv venv
source venv/bin/activate       # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

L'application est disponible sur http://localhost:5000

## Lancer les tests

```bash
pip install pytest
pytest
```

## Variables d'environnement

| Variable        | Description                              | Defaut                      |
|-----------------|-------------------------------------------|------------------------------|
| `SECRET_KEY`    | Cle secrete Flask (sessions)              | `dev-secret-key-change-me`  |
| `DATABASE_URL`  | URI de connexion base de donnees          | SQLite local `shop.db`      |

## Notes pour la partie DevOps

- L'app expose `/healthz` -> a utiliser pour les probes `livenessProbe` / `readinessProbe` Kubernetes.
- Le port par defaut est **5000**.
- Pour la production, lancer plutot avec Gunicorn, par exemple :
  ```bash
  gunicorn -w 2 -b 0.0.0.0:5000 app:app
  ```
- Penser a externaliser `SECRET_KEY` et `DATABASE_URL` via des Secrets/ConfigMaps Kubernetes.
- La base SQLite est stockee en fichier local : pour un vrai deploiement K8s multi-replica,
  il faudra migrer vers une base externe (PostgreSQL, MySQL) ou un volume persistant partage.
