# CSV Analyzer

Application web Django permettant d'importer des fichiers CSV et d'en obtenir une analyse statistique complète avec visualisations interactives.

## Fonctionnalités

- **Import CSV** — téléversement et nommage de datasets
- **Analyse automatique** — statistiques descriptives (moyenne, médiane, écart-type, quartiles, valeurs manquantes) pour chaque colonne
- **Visualisations** — histogrammes pour les variables numériques, diagrammes en barres pour les variables catégorielles (Chart.js)
- **Mes datasets** — bibliothèque personnelle pour retrouver et supprimer les analyses
- **Authentification** — inscription, connexion, déconnexion
- **Profil utilisateur** — changement de nom, e-mail, mot de passe, photo de profil (avatar rond redimensionné à 300×300 px)
- **API REST** — endpoints documentés via Swagger / Redoc (`/api/docs/`)

## Stack technique

| Couche | Technologie |
|---|---|
| Backend | Django 6, Django REST Framework |
| Analyse | pandas, numpy |
| Documentation API | drf-spectacular (OpenAPI 3) |
| CORS | django-cors-headers |
| Config | python-decouple (`.env`) |
| Images | Pillow |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js 4 |
| Base de données | SQLite (dev) |

## Structure du projet

```
rendu/
├── accounts/          # App authentification & profil
│   ├── models.py      # Modèle Profile (OneToOne → User, avatar)
│   ├── views.py       # register, login, logout, profile
│   └── forms.py       # RegisterForm, LoginForm, UsernameForm…
├── datasets/          # App datasets & analyse
│   ├── models.py      # Modèle Dataset (fichier, métadonnées)
│   ├── utils.py       # analyze_csv() — stats + données graphiques
│   ├── views.py       # list, upload, detail, delete
│   └── api_views.py   # API REST (list/create/retrieve/destroy/analyze)
├── config/            # Paramètres Django (settings, urls, wsgi)
├── templates/         # Templates HTML (base.html + par app)
├── static/            # chart.umd.min.js, favicon.svg
├── .env.example       # Variables d'environnement à renseigner
├── requirements.txt
└── manage.py
```

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/AurelienAllenic/exo1-django.git
cd exo1-django
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
```

Éditer `.env` :

```env
SECRET_KEY=remplacez-par-une-vraie-cle-secrete
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

### 6. Lancer le serveur

```bash
python manage.py runserver
```

L'application est disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API REST

L'API est accessible sous `/api/` et protégée par authentification de session.

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/datasets/` | Liste des datasets de l'utilisateur |
| POST | `/api/datasets/` | Créer un dataset (upload CSV) |
| GET | `/api/datasets/<id>/` | Détail d'un dataset |
| DELETE | `/api/datasets/<id>/` | Supprimer un dataset |
| GET | `/api/datasets/<id>/analyze/` | Analyse complète (stats + graphiques) |

Documentation interactive :
- Swagger UI : [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- Redoc : [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

## Modèle MVT

Le projet suit strictement le patron **Model – View – Template** de Django :

- **Model** — `Dataset`, `Profile` définissent la structure des données et la logique métier
- **View** — les vues (`views.py`) récupèrent les données et les passent aux templates
- **Template** — les fichiers HTML (`templates/`) assurent le rendu final

## Variables d'environnement

| Variable | Description | Exemple |
|---|---|---|
| `SECRET_KEY` | Clé secrète Django | `django-insecure-...` |
| `DEBUG` | Mode debug | `True` / `False` |
| `ALLOWED_HOSTS` | Hôtes autorisés (séparés par `,`) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Origines CORS autorisées | `http://localhost:3000` |

## Fichiers ignorés par Git

`.env`, `.venv/`, `db.sqlite3`, `media/` (avatars & datasets uploadés), `staticfiles/` — voir `.gitignore`.
