# 🤖 Restaurant Chatbot - Telegram Bot avec Django & n8n

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![n8n](https://img.shields.io/badge/n8n-Workflow-orange.svg)](https://n8n.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Chatbot Telegram complet pour la gestion de restaurant avec backend Django REST API, orchestration n8n et système de paiement intégré.

---

## 🎯 Vue d'Ensemble

### Qu'est-ce que ce projet?

Un système complet de chatbot Telegram pour restaurant permettant:
- 🤖 Interaction client via Telegram (boutons cliquables)
- 🍽️ Gestion de menu dynamique
- 🛒 Système de panier intelligent
- 💰 Portefeuille virtuel et paiements
- 📦 Gestion des commandes avec notifications
- 🔄 Automatisation complète via n8n

### Architecture

```
┌─────────────────┐
│  Telegram Bot   │  ← Interface utilisateur
└────────┬────────┘
         │
┌────────▼────────┐
│   n8n Workflow  │  ← Orchestration & Logique
└────────┬────────┘
         │
┌────────▼────────┐
│   Django API    │  ← Backend & Base de données
└─────────────────┘
```

---

## ✨ Fonctionnalités Principales

### 🔐 Authentification
- Connexion automatique via Telegram ID
- Cache de tokens (24h)
- Système sécurisé par token Bearer

### 🍕 Menu & Commandes
- Menu par catégories
- Panier persistant
- Commandes avec suivi de statut
- Notifications automatiques (Cron 30s)

### 💰 Portefeuille & Paiements
- Portefeuille virtuel par utilisateur
- Rechargement fictif (pour tests)
- Paiement de commandes depuis le wallet
- Historique des transactions

### 🤖 Bot Telegram
- Boutons inline cliquables
- Workflow organisé en 4 sections

---

## 🚀 Quick Start (2 Options)

### Option 1: Script Automatique (Recommandé)

**Windows:**
```bash
# Lancer le gestionnaire principal
scripts\manage.bat

# Puis choisir:
# [1] Quick Start - Installation complète automatique
```

**Linux/Mac:**
```bash
# Lancer le gestionnaire principal
./scripts/manage.sh

# Puis choisir:
# [1] Quick Start - Installation complète automatique
```

### Option 2: Manuel

**Windows:**
```bash
# 1. Créer environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer .env
copy .env.example .env
# Éditer .env avec votre TELEGRAM_BOT_TOKEN

# 4. Base de données
python manage.py migrate

# 5. Créer superuser
python manage.py createsuperuser

# 6. Démarrer serveur
python manage.py runserver
```

**Linux/Mac:**
```bash
# 1. Créer environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer .env
cp .env.example .env
# Éditer .env avec votre TELEGRAM_BOT_TOKEN

# 4. Base de données
python manage.py migrate

# 5. Créer superuser
python manage.py createsuperuser

# 6. Démarrer serveur
python manage.py runserver
```

---

## 📋 Prérequis

### Obligatoire
- ✅ Python 3.11+
- ✅ Bot Telegram créé via @BotFather
- ✅ Docker & Docker Compose (pour n8n)

### Recommandé
- PostgreSQL (production)
- Git

---

## 🔧 Configuration

### 1. Créer un Bot Telegram

```
1. Ouvrir Telegram
2. Chercher @BotFather
3. Envoyer /newbot
4. Suivre les instructions
5. Copier le TOKEN reçu
```

### 2. Configurer .env

```bash
# Créer depuis l'exemple
copy .env.example .env
```

Éditer `.env`:
```env
# Django
SECRET_KEY=votre_secret_key_unique_50_caracteres
DEBUG=True  # False en production
ALLOWED_HOSTS=localhost,127.0.0.1

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Base de données (optionnel - SQLite par défaut)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=restaurant_db
DB_USER=restaurant_user
DB_PASSWORD=mot_de_passe_securise
```

### 3. Importer le Workflow n8n

```bash
# 1. Démarrer n8n avec Docker
docker-compose up -d

# 2. Accéder à n8n
http://localhost:5678
Login: admin / admin123

# 3. Importer
Workflows → Import → Sélectionner:
n8n_workflows/Restaurant Bot - Version Optimisée v3.json

# 4. Configurer credentials Telegram
Settings → Credentials → New → Telegram API
Token: [Votre token bot]

# 5. Activer le workflow
Toggle "Active" en haut à droite
```

---

## 📂 Structure du Projet

```
Chatbot_gestion_restaurant/
│
├── 📄 README.md                        # ⭐ Ce fichier
│
├── 📂 apps/                            # Backend Django
│   ├── core/          # Modèles communs
│   ├── users/         # Authentification
│   ├── menu/          # Produits & catégories
│   ├── orders/        # Commandes
│   └── wallet/        # Portefeuille + paiements
│
├── 📂 config/                          # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📂 n8n_workflows/                   # Workflows n8n
│   └── Restaurant Bot - Version Optimisée v3.json  # ⭐ 
│
├── 📂 scripts/                         # Scripts utilitaires
│   ├── manage.bat                     # ⭐ Gestionnaire (Windows)
│   ├── manage.sh                      # ⭐ Gestionnaire (Linux/Mac)
│   └── start.sh                       # Quick start (Linux/Mac)
│
├── 📄 docker-compose.yml               # Docker config
├── 📄 requirements.txt
└── 📄 .env.example

Légende:
⭐ = Fichiers principaux
```

---

## 🎮 Utilisation

### Avec le Gestionnaire (Recommandé)

**Windows:**
```bash
# Lancer le menu principal
scripts\manage.bat
```

**Linux/Mac:**
```bash
# Lancer le menu principal
./scripts/manage.sh
```

**Menu disponible:**
- [1] 🚀 Quick Start (installation)
- [2] 🐳 Docker - Démarrer
- [3] 🛑 Docker - Arrêter
- [4] 📊 Docker - Logs
- [5] 🗄️ Base de données - Setup
- [6] 🔄 Base de données - Reset
- [7] 🔧 Django - Runserver
- [8] 📝 Django - Shell
- [9] 👤 Django - Créer superuser

### Quick Start Simple

**Linux/Mac uniquement:**
```bash
# Démarrage rapide avec choix Docker/Local
./scripts/start.sh
```

### Commandes Manuelles

```bash
# Démarrer Django (local)
python manage.py runserver

# Démarrer Docker (n8n + Django)
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter Docker
docker-compose down

# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell Django
python manage.py shell
```

---

## 🧪 Tests

### Via Telegram

```
/start        → Message de bienvenue
/menu         → Menu avec boutons cliquables
/cart         → Voir le panier
/orders       → Liste des commandes
/wallet       → Solde du portefeuille
/transactions → Historique
/recharge     → Recharger le portefeuille (fictif)
```

### Checklist Complète

- [ ] Bot répond au `/start`
- [ ] `/menu` affiche des boutons cliquables
- [ ] Clic sur bouton ajoute au panier
- [ ] `/cart` affiche le panier
- [ ] Checkout crée une commande
- [ ] `/orders` liste les commandes séparément
- [ ] `/wallet` affiche le solde
- [ ] `/recharge` permet de recharger
- [ ] Paiement débite le wallet
- [ ] Notifications reçues après ~30s

---

## 📚 Documentation Complète


### Documentation Spécifique

- [n8n_workflows/README.md](n8n_workflows/README.md) - Vue d'ensemble workflows
- [n8n_workflows/V3_NEW_FEATURES.md](n8n_workflows/V3_NEW_FEATURES.md) - Nouvelles fonctionnalités v3
- [n8n_workflows/V3_FIXES.md](n8n_workflows/V3_FIXES.md) - Corrections appliquées
- [n8n_workflows/REORGANISATION_V3.md](n8n_workflows/REORGANISATION_V3.md) - Détails réorganisation

---

## 🌐 URLs & Accès

### Django API (Local)
```
API:      http://localhost:8000
Admin:    http://localhost:8000/admin/
Swagger:  http://localhost:8000/api/docs/
ReDoc:    http://localhost:8000/api/redoc/

Login Admin: admin / admin123
```

### n8n (Docker)
```
n8n:      http://localhost:5678

Login: admin / admin123
```

---

## 📊 Endpoints API Principaux

### Authentification
```http
POST /api/auth/users/login_or_register/
POST /api/auth/users/login/
```

### Menu
```http
GET  /api/menu/products/menu/
GET  /api/menu/products/
GET  /api/menu/categories/
```

### Commandes
```http
GET  /api/orders/my_orders/
POST /api/orders/orders/
GET  /api/orders/orders/{id}/
```

### Portefeuille
```http
GET  /api/wallet/wallets/my_wallet/
POST /api/wallet/wallets/recharge_fictif/
POST /api/wallet/wallets/pay_order/
GET  /api/wallet/transactions/
```

**Documentation complète:** http://localhost:8000/api/docs/

---

## 🐛 Dépannage

### Problème: Bot ne répond pas

```bash
# 1. Vérifier que n8n est actif
docker-compose ps

# 2. Vérifier le workflow est activé
# n8n → Workflow → Toggle "Active"

# 3. Vérifier les logs
docker-compose logs -f n8n
```

### Problème: Erreur de base de données

```bash
# Reset complet de la DB
scripts\manage.bat
# Choisir [6] Base de données - Reset
```

### Problème: Boutons non cliquables

```bash
# Vérifier TELEGRAM_BOT_TOKEN dans .env
# Puis redémarrer:
docker-compose restart n8n
```


---

## 🚀 Production

### Checklist de Déploiement

- [ ] `DEBUG=False` dans `.env`
- [ ] `SECRET_KEY` unique et sécurisée (50+ caractères)
- [ ] PostgreSQL au lieu de SQLite
- [ ] HTTPS configuré (Nginx/Caddy)
- [ ] Backups automatiques configurés
- [ ] Tous les tests passés
- [ ] Documentation à jour

---

## 🛠️ Technologies Utilisées

- **Backend:** Python 3.11, Django 5.0, Django REST Framework
- **Orchestration:** n8n Workflow Automation
- **Interface:** Telegram Bot API
- **Base de données:** SQLite (dev) / PostgreSQL (prod)
- **Conteneurisation:** Docker & Docker Compose
- **Documentation:** Swagger / ReDoc

---

## 📞 Support & Ressources


### Liens Externes
- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation n8n](https://docs.n8n.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

## 🎯 Démarrage Rapide (Résumé)

```bash
# 1. Configuration initiale
scripts\manage.bat
# → Choisir [1] Quick Start

# 2. Configurer .env avec TELEGRAM_BOT_TOKEN

# 3. Démarrer Docker
scripts\manage.bat
# → Choisir [2] Docker - Démarrer

# 4. Importer workflow dans n8n
# http://localhost:5678
# Import → Restaurant Bot - Version Optimisée v3.json

# 5. Tester le bot
# Telegram → Votre bot → /start
```

---

## 📄 Licence

Ce projet est fourni tel quel pour usage personnel et éducatif.

---

## 🎉 Contributeurs

Merci à tous ceux qui ont contribué à ce projet!

---

## 📝 Changelog

### v3.0 (2024-12-06) - ACTUEL
- ✅ Réorganisation complète du workflow
- ✅ Système de portefeuille complet
- ✅ Paiement de commandes
- ✅ Rechargement fictif
- ✅ Messages séparés pour meilleure UX
- ✅ Documentation consolidée

### v2.0 (2024-12)
- ✅ Boutons inline cliquables
- ✅ Cache de tokens (24h)
- ✅ Système de panier

### v1.0 (2024-11)
- ✅ Version basique fonctionnelle

---

**Version:** 3.0
**Date:** 2024-12-06
**Statut:** ✅ **Production Ready**

---