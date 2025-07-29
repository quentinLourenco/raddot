# Raddot - Documentation des Routes

Cette documentation liste toutes les routes disponibles dans l'application Raddot, organisées par catégorie.

## Routes Principales

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/` | `root_redirect` | `root_redirect` | Redirige vers la page d'accueil (utilisateurs connectés) ou la page de connexion (utilisateurs non connectés) |
| `/profile/` | `profile` | `profile` | Affiche le profil de l'utilisateur connecté |
| `/profile/edit/` | `update_profile` | `update_profile` | Permet à l'utilisateur de modifier son profil |

## Routes d'Authentification (`/auth/`)

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/auth/login/` | `login` | `user_manager:login` | Page de connexion |
| `/auth/logout/` | `logout` | `user_manager:logout` | Déconnexion de l'utilisateur |
| `/auth/register/` | `register` | `user_manager:register` | Page d'inscription |

## Routes de Contenu Social (`/home/`)

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/home/` | `homepage` | `social_app:homepage` | Page d'accueil de l'application |
| `/home/r/discover/` | `discover_subraddots` | `social_app:discover_subraddots` | Découverte des communautés disponibles |
| `/home/r/create/` | `create_subraddot` | `social_app:create_subraddot` | Création d'une nouvelle communauté |
| `/home/r/<nom>/` | `homepage` | `social_app:subraddot_detail` | Affichage d'une communauté spécifique |
| `/home/r/<nom>/update/` | `update_subraddot` | `social_app:update_subraddot` | Modification d'une communauté (réservé au créateur) |
| `/home/my_subraddots/` | `my_subraddots` | `social_app:my_subraddots` | Liste des communautés créées par l'utilisateur connecté |

## Routes pour les fichiers média

En mode développement (DEBUG=True), les fichiers média sont servis à partir de l'URL `/media/` et sont stockés dans le dossier `MEDIA_ROOT` configuré dans les paramètres Django.

## Protection des Routes

L'application utilise un middleware personnalisé (`ProtectRoutesMiddleware`) qui protège toutes les routes sauf celles commençant par:
- `/auth/` (authentification)
- `/admin/` (administration)
- `/static/` (fichiers statiques)
- `/media/` (fichiers média)

Les utilisateurs non authentifiés qui tentent d'accéder à des routes protégées sont automatiquement redirigés vers la page de connexion.
