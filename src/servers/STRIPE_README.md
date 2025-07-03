# Stripe - TeamBrains

## Quick Start

### Développement
```bash
# 1. Setup automatique
./setup_stripe.sh dev

# 2. Lancer le webhook listener
stripe listen --forward-to localhost:5001/api/partnership/stripe/webhook

# 3. Démarrer le serveur
docker-compose up

# 4. Tester
stripe trigger checkout.session.completed
```

### Production
```bash
# 1. Setup automatique
./setup_stripe.sh prod

# 2. Configurer le webhook dans Stripe Dashboard
# URL: https://votre-domaine.com/api/partnership/stripe/webhook

# 3. Déployer
docker-compose -f docker-compose.prod.yml up -d
```

## Fichiers Importants

- `STRIPE_SETUP.md` - Documentation complète
- `setup_stripe.sh` - Script de setup automatique
- `teambrains-backend/env.example` - Variables d'environnement
- `teambrains-backend/routes/stripe_partnership.py` - Routes principales

## URLs Webhook

- **Développement** : `http://localhost:5001/api/partnership/stripe/webhook`
- **Production** : `https://votre-domaine.com/api/partnership/stripe/webhook`

## Tests

```bash
# Test de connexion
curl -H "Authorization: Bearer sk_test_..." https://api.stripe.com/v1/customers

# Test webhook local
stripe trigger checkout.session.completed

# Debug abonnements
curl -H "Authorization: Bearer JWT_TOKEN" http://localhost:5001/api/partnership/stripe/debug-user-subscriptions
```

## Troubleshooting

### Signature webhook invalide
```bash
# Vérifier le secret
stripe listen --print-secret

# Mettre à jour dans le code si nécessaire
```

### Webhook non reçu
```bash
# Vérifier l'URL
curl -X POST http://localhost:5001/api/partnership/stripe/webhook

# Vérifier les logs
docker-compose logs teambrains-backend
```

## Support

- **Documentation complète** : `STRIPE_SETUP.md`
- **Logs** : `docker-compose logs teambrains-backend`
- **Debug** : Endpoints `/api/partnership/stripe/debug-*`

---

*Configuration simplifiée pour TeamBrains* 