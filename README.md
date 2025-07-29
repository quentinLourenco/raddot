# Raddot - Documentation du Projet

Ce document fournit une documentation complète du projet Raddot, incluant l'architecture, les routes disponibles et les fonctionnalités principales.

## Architecture du Projet

Raddot est structuré selon une architecture Django classique, avec quelques personnalisations pour améliorer la maintenabilité et la séparation des préoccupations :

### Structure des Applications

1. **raddot** - Application principale du projet (configuration Django)
   - `settings.py` - Configuration générale du projet
   - `urls.py` - Routage principal

2. **user_manager** - Gestion des utilisateurs et de l'authentification
   - `models/` - Modèles liés aux utilisateurs
   - `views/` - Vues pour l'authentification et la gestion des profils
   - `forms/` - Formulaires pour l'inscription, la connexion et la modification du profil
   - `middleware/` - Middleware personnalisé pour la protection des routes

3. **social_app** - Fonctionnalités sociales principales
   - `models/` - Définition des modèles de données (Subraddot, Post, Comment, Vote)
   - `views/` - Logique des vues séparées par fonctionnalité
   - `forms/` - Formulaires pour la création et modification de contenu
   - `templates/` - Templates organisés par fonctionnalité
   - `components/` - Templates réutilisables (cartes, listes, etc.)

### Organisation des Fichiers Statiques
Les fichiers CSS sont organisés par composant ou par page pour faciliter la maintenance :
- `base.css` - Styles globaux
- `discover.css`, `subraddot_card.css`, `subraddot_card_list.css` - Styles spécifiques aux composants

### Approche Modulaire
- **Séparation des modèles** : Chaque modèle est dans son propre fichier pour une meilleure lisibilité
- **Vues organisées par fonctionnalité** : Séparation des vues dans différents fichiers selon leur fonction
- **Composants réutilisables** : Les composants d'UI (comme subraddot_card) sont créés de façon modulaire

## Routes Disponibles

### Routes d'Authentification (`/auth/`)

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/auth/login/` | `login` | `user_manager:login` | Page de connexion |
| `/auth/logout/` | `logout` | `user_manager:logout` | Déconnexion de l'utilisateur |
| `/auth/register/` | `register` | `user_manager:register` | Page d'inscription |

### Routes de Contenu Social (`/home/`)

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/home/` | `homepage` | `social_app:homepage` | Page d'accueil de l'application |
| `/home/discover/` | `discover_subraddots` | `social_app:discover_subraddots` | Découverte des communautés disponibles |
| `/home/r/create/` | `subraddot_create` | `social_app:subraddot_create` | Création d'une nouvelle communauté |
| `/home/r/<nom>/` | `subraddot_home` | `social_app:subraddot_home` | Affichage d'une communauté spécifique |
| `/home/r/<nom>/update/` | `subraddot_update` | `social_app:update_subraddot` | Modification d'une communauté (réservé au créateur) |
| `/home/r/<nom>/join/` | `join_subraddot` | `social_app:join_subraddot` | Rejoindre une communauté |
| `/home/r/<nom>/leave/` | `leave_subraddot` | `social_app:leave_subraddot` | Quitter une communauté |
| `/home/my_subraddots/` | `user_subraddots` | `social_app:user_subraddots` | Liste des communautés créées par l'utilisateur connecté |

### Routes de Profil

| URL | Vue | Nom | Description |
|-----|-----|-----|-------------|
| `/profile/` | `profile` | `profile` | Affiche le profil de l'utilisateur connecté |
| `/profile/edit/` | `update_profile` | `update_profile` | Permet à l'utilisateur de modifier son profil |

## Protection des Routes

L'application utilise un middleware personnalisé (`ProtectRoutesMiddleware`) qui protège toutes les routes sauf celles commençant par:
- `/auth/` (authentification)
- `/admin/` (administration)
- `/static/` (fichiers statiques)
- `/media/` (fichiers média)

Les utilisateurs non authentifiés qui tentent d'accéder à des routes protégées sont automatiquement redirigés vers la page de connexion.

## Composants Réutilisables

### Subraddot Card
Un composant qui affiche un aperçu d'un subraddot avec:
- Son icône (ou une icône par défaut)
- Son nom et sa description
- Le nombre de membres
- Des boutons d'action qui s'adaptent en fonction du statut de l'utilisateur (créateur, membre, non membre)

### Subraddot Card List
Un composant qui affiche une liste de cartes subraddot avec:
- Options de filtrage (tous les subraddots, mes créations, mes abonnements)
- Gestion des cas sans résultat
- Affichage responsive des résultats
