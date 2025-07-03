# TeamBrains - Plateforme Collaborative Étudiante

![TeamBrains Logo](src/assets/logo_teambrains.svg)

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/teambrains/teambrains)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/teambrains/teambrains/actions)

## À propos

**TeamBrains** est une plateforme collaborative moderne conçue pour faciliter la gestion de projets étudiants. Elle combine des outils de gestion de tâches, de communication en temps réel, et de suivi de progression, avec un système de facturation hybride adapté aux établissements scolaires.

### Fonctionnalités principales

- **Gestion de projets** collaborative avec suivi en temps réel
- **Gestion de tâches** avec sprints et validation par les pairs
- **Chat intégré** avec partage de fichiers
- **CV digital** pour valoriser les projets réalisés
- **Interface école** avec gestion d'étudiants
- **Système d'abonnement** hybride avec intégration Stripe
- **Tableaux de bord** avec statistiques et analytics

---

## Documentation complète

### Documentation principale
- **[Documentation technique complète](DOCUMENTATION.md)** - Guide complet du projet
- **[Architecture système](docs/ARCHITECTURE.md)** - Description détaillée de l'architecture
- **[Guide de déploiement](docs/DEPLOYMENT_GUIDE.md)** - Instructions de déploiement
- **[API Documentation](docs/API_ENDPOINTS.md)** - Documentation des endpoints
- **[Schéma de base de données](docs/DATABASE_SCHEMA.md)** - Structure et relations

### Guides techniques
- **[Installation locale](#installation-rapide)** - Démarrage rapide avec Docker
- **[Configuration](#configuration)** - Variables d'environnement
- **[Tests](#tests)** - Guide des tests et CI/CD
- **[Contribution](#contribution)** - Comment contribuer au projet

---

## Installation rapide

### Prérequis
- Docker et Docker Compose
- Git

### 1. Cloner le projet
```bash
git clone https://github.com/your-org/teambrains.git
cd teambrains
```

### 2. Configuration environnement
```bash
# Backend
cp servers/teambrains-backend/.env.example servers/teambrains-backend/.env

# Frontend
cp servers/teambrains-frontend/.env.example servers/teambrains-frontend/.env
```

### 3. Lancement avec Docker
```bash
docker-compose up -d --build
```

### 4. Accès aux services
- **Frontend** : http://localhost:5173
- **Backend API** : http://localhost:5001
- **Base de données** : localhost:5432
- **Mailpit** (emails dev) : http://localhost:8025

---

## Architecture

### Stack technique

#### Backend
- **Flask** (Python 3.8+) - Framework web
- **PostgreSQL** - Base de données relationnelle
- **SQLAlchemy** - ORM et migrations
- **JWT** - Authentification stateless
- **Stripe** - Système de paiements

#### Frontend
- **React 18** - Interface utilisateur
- **Vite** - Build tool moderne
- **TailwindCSS** - Framework CSS
- **React Router** - Navigation
- **Axios** - Client HTTP

#### Infrastructure
- **Docker** - Conteneurisation
- **Nginx** - Proxy inverse (production)
- **GitHub Actions** - CI/CD

### Diagramme d'architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Client  │◄──►│   Flask API     │◄──►│   PostgreSQL    │
│   (Port 5173)   │    │   (Port 5001)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Stripe API    │
                       │   (Paiements)   │
                       └─────────────────┘
```

---

## Fonctionnalités détaillées

### Authentification et rôles
- **Étudiants** : Création de projets, collaboration, CV digital
- **Écoles** : Gestion d'étudiants, tableaux de bord, facturation
- **Administrateurs** : Gestion globale, analytics, configuration

### Gestion de projets
- Création et configuration de projets
- Gestion des membres avec rôles spécifiques
- Suivi de progression en temps réel
- Organisation par statuts et priorités

### Système de tâches
- Création et assignation de tâches
- Pourcentage de complétion
- Système de priorités (haute, moyenne, basse)
- Organisation par sprints
- Validation par les pairs avec commentaires

### Facturation hybride
- **Plan Étudiant** : 2€/mois
- **Plan École** : 120€/an de base + 2€/mois par étudiant
- Calcul automatique selon le nombre d'étudiants
- Intégration Stripe complète avec webhooks

---

## Configuration

### Variables d'environnement backend (.env)

```env
# Base de données
SQLALCHEMY_DATABASE_URI=postgresql://user:password@localhost:5432/teambrains

# JWT
JWT_SECRET_KEY=your-super-secret-key

# Stripe
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key

# Email
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_USE_TLS=False

# Upload
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Variables d'environnement frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:5001
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
```

---

## Tests

### Backend (Python)
```bash
cd servers/teambrains-backend
python -m pytest tests/ -v
```

### Frontend (React)
```bash
cd servers/teambrains-frontend
npm test
```

### Tests d'intégration
```bash
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## Déploiement

### Développement
```bash
docker-compose up -d
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud (Heroku + Vercel)
Voir le [guide de déploiement détaillé](docs/DEPLOYMENT_GUIDE.md).

---

## 📈 Monitoring

### Métriques disponibles
- Performance des APIs
- Utilisation de la base de données
- Statistiques de paiements Stripe
- Analytics utilisateurs

### Outils recommandés
- **Logs** : ELK Stack, Grafana Loki
- **Métriques** : Prometheus + Grafana
- **Uptime** : Pingdom, UptimeRobot
- **Erreurs** : Sentry

---

## 🤝 Contribution

### Processus de contribution
1. **Fork** le repository
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commit** les modifications (`git commit -m 'feat: add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir** une Pull Request

### Standards de code
- **Python** : PEP 8, docstrings, type hints
- **JavaScript** : ESLint, fonctions fléchées, composants fonctionnels
- **Commits** : Convention Conventional Commits
- **Tests** : Couverture minimum 80%

---

## 📄 Structure du projet

```
TeamBrains/
├── 📁 src/
│   ├── 📁 servers/
│   │   ├── 🐍 teambrains-backend/     # API Flask
│   │   │   ├── 📁 routes/             # Routes organisées
│   │   │   ├── 📄 models.py           # Modèles SQLAlchemy
│   │   │   ├── 📄 app.py              # Application principale
│   │   │   └── 📄 requirements.txt    # Dépendances Python
│   │   └── teambrains-frontend/    # Application React
│   │       ├── 📁 src/components/     # Composants React
│   │       ├── 📁 src/context/        # Contextes
│   │       ├── 📄 package.json        # Dépendances Node.js
│   │       └── 📄 vite.config.js      # Configuration Vite
│   └── 📁 assets/                     # Assets globaux
├── 📁 docs/                           # Documentation
│   ├── 📄 ARCHITECTURE.md             # Architecture système
│   ├── 📄 API_ENDPOINTS.md            # Documentation API
│   ├── 📄 DATABASE_SCHEMA.md          # Schéma BDD
│   └── 📄 DEPLOYMENT_GUIDE.md         # Guide déploiement
├── 📄 DOCUMENTATION.md                # Documentation complète
├── 📄 README.md                       # Ce fichier
├── 📄 docker-compose.yml              # Configuration Docker
└── 📄 .github/workflows/              # CI/CD GitHub Actions
```

---

## Roadmap

### Phase 1 (Actuelle)
- [x] Gestion de projets et tâches
- [x] Chat en temps réel
- [x] Système d'authentification
- [x] Interface école
- [x] Facturation hybride Stripe

### Phase 2 (Q1 2025)
- [ ] Application mobile (React Native)
- [ ] Notifications push
- [ ] Système de templates de projets
- [ ] Analytics avancés

### Phase 3 (Q2 2025) 📋
- [ ] Intégration Git/GitHub
- [ ] Système de review de code
- [ ] Marketplace de plugins
- [ ] API publique

---

## 📞 Support et communauté

### 🐛 Signaler un bug
Créez une [issue](https://github.com/teambrains/teambrains/issues) avec :
- Description détaillée
- Étapes de reproduction
- Environnement (OS, navigateur)
- Screenshots si applicable

### Proposer une fonctionnalité
Ouvrez une [discussion](https://github.com/teambrains/teambrains/discussions) pour échanger sur vos idées.

### 📧 Contact
- **Email** : contact@teambrains.dev
- **Discord** : [Serveur TeamBrains](https://discord.gg/teambrains)
- **Twitter** : [@TeamBrainsDev](https://twitter.com/TeamBrainsDev)

---

## 📜 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🏆 Équipe

### Core Team
- **Lead Developer** : [Yanis](https://github.com/yanis-username)
- **Backend Developer** : [Nom](https://github.com/username)
- **Frontend Developer** : [Nom](https://github.com/username)
- **DevOps Engineer** : [Nom](https://github.com/username)

### Contributeurs
Merci à tous nos [contributeurs](https://github.com/teambrains/teambrains/contributors) !

---

## Remerciements

- **Stripe** pour l'excellent système de paiements
- **React** et **Flask** pour les frameworks robustes
- **TailwindCSS** pour le système de design
- **PostgreSQL** pour la base de données fiable
- La communauté open-source pour l'inspiration

---

<div align="center">

**Fait avec passion par l'équipe TeamBrains**

[Star ce repo](https://github.com/teambrains/teambrains/stargazers) | [Signaler un bug](https://github.com/teambrains/teambrains/issues) | [Proposer une fonctionnalité](https://github.com/teambrains/teambrains/discussions)

</div> 