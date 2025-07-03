# Configuration Stripe - TeamBrains

## Table des matières
- [Configuration Développement](#configuration-développement)
- [Configuration Production](#configuration-production)
- [Webhooks](#webhooks)
- [Tests et Debug](#tests-et-debug)
- [Troubleshooting](#troubleshooting)

---

## Configuration Développement

### 1. Variables d'environnement

Créez un fichier `.env` dans `teambrains-backend/` :

```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...  # Clé secrète de test
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Clé publique de test

# Webhooks (optionnel en dev - utilise des secrets fixes)
STRIPE_WEBHOOK_SECRET=whsec_...  # Pour webhook principal (si utilisé)
STRIPE_PARTNERSHIP_WEBHOOK_SECRET=whsec_...  # Pour webhook partenariat
```

### 2. Stripe CLI Setup

#### Installation
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Ou téléchargement direct
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
sudo apt update && sudo apt install stripe
```

#### Connexion
```bash
stripe login
```

#### Lancer le webhook listener
```bash
# Pour le webhook partenariat (recommandé)
stripe listen --forward-to localhost:5001/api/partnership/stripe/webhook

# Pour le webhook principal (si utilisé)
stripe listen --forward-to localhost:5001/api/stripe/webhook
```

**Note :** Le CLI affichera un secret webhook. Copiez-le et mettez-le à jour dans le code si nécessaire.

### 3. Secrets Webhook Fixes

En développement, le code utilise des secrets fixes pour éviter la configuration :

```python
# Dans stripe_partnership.py
endpoint_secret = 'whsec_b016ddbd5e1935ad4341f95c1ac10d848b86d1b2c4c3555a1971bc473f761e71'
```

**Important :** Ce secret doit correspondre à celui affiché par `stripe listen`

---

## Configuration Production

### 1. Variables d'environnement Production

```bash
# Stripe Production
STRIPE_SECRET_KEY=sk_live_...  # Clé secrète de production
STRIPE_PUBLISHABLE_KEY=pk_live_...  # Clé publique de production

# Webhooks Production (OBLIGATOIRE)
STRIPE_WEBHOOK_SECRET=whsec_...  # Secret du webhook principal
STRIPE_PARTNERSHIP_WEBHOOK_SECRET=whsec_...  # Secret du webhook partenariat
```

### 2. Configuration Webhook Production

#### Via Dashboard Stripe

1. **Allez sur** : https://dashboard.stripe.com/webhooks
2. **Cliquez sur "Add endpoint"**
3. **URL de production** :
   ```
   https://votre-domaine.com/api/partnership/stripe/webhook
   ```
4. **Événements à activer** :
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_action_required`

#### Via API Stripe

```bash
curl -X POST https://api.stripe.com/v1/webhook_endpoints \
  -H "Authorization: Bearer sk_live_..." \
  -H "Content-Type: application/json" \
  --data '{
    "url": "https://votre-domaine.com/api/partnership/stripe/webhook",
    "enabled_events": [
      "checkout.session.completed",
      "invoice.payment_succeeded",
      "invoice.payment_failed",
      "customer.subscription.updated",
      "customer.subscription.deleted",
      "invoice.payment_action_required"
    ]
  }'
```

### 3. Récupération du Secret Webhook

Après création du webhook, récupérez le secret :

```bash
curl -X GET https://api.stripe.com/v1/webhook_endpoints/we_... \
  -H "Authorization: Bearer sk_live_..."
```

Copiez le `secret` dans vos variables d'environnement.

---

## Webhooks

### Structure des Webhooks

```
/api/partnership/stripe/webhook  # Webhook principal (recommandé)
/api/stripe/webhook              # Webhook de redirection (vers partenariat)
```

### Événements Traités

| Événement | Description | Action |
|-----------|-------------|---------|
| `checkout.session.completed` | Paiement réussi | Créer/mettre à jour abonnement |
| `invoice.payment_succeeded` | Facture payée | Enregistrer facture |
| `invoice.payment_failed` | Échec paiement | Incrémenter compteur échecs |
| `customer.subscription.updated` | Abonnement modifié | Mettre à jour statut |
| `customer.subscription.deleted` | Abonnement supprimé | Marquer comme annulé |

### Gestion des Erreurs

- **Signature invalide** : Vérifier le secret webhook
- **Payload invalide** : Vérifier le format JSON
- **Erreur de traitement** : Logs détaillés dans les fichiers

---

## Tests et Debug

### 1. Test de Connexion Stripe

```bash
# Test API Stripe
curl -X GET https://api.stripe.com/v1/customers \
  -H "Authorization: Bearer sk_test_..." \
  -H "Content-Type: application/json"
```

### 2. Test Webhook Local

```bash
# Lancer le listener
stripe listen --forward-to localhost:5001/api/partnership/stripe/webhook

# Dans un autre terminal, déclencher un événement
stripe trigger checkout.session.completed
```

### 3. Endpoints de Debug

```bash
# Test configuration webhook
GET http://localhost:5001/api/partnership/stripe/webhook/test

# Debug abonnements utilisateur
GET http://localhost:5001/api/partnership/stripe/debug-user-subscriptions

# Synchronisation forcée
POST http://localhost:5001/api/partnership/stripe/force-sync-all
```

### 4. Logs de Debug

Les logs incluent des identifiants pour faciliter le debug :

- [WEBHOOK] : Événements webhook
- [SUCCESS] : Succès
- [ERROR] : Erreurs
- [REDIRECT] : Redirections
- [DOCKER] : Mode Docker
- [SYNC] : Synchronisation rapide

---

## Troubleshooting

### Problèmes Courants

#### 1. "Signature webhook invalide"

**Cause :** Secret webhook incorrect
**Solution :**
```bash
# Vérifier le secret affiché par stripe listen
stripe listen --print-secret

# Mettre à jour dans le code ou .env
```

#### 2. "Webhook non reçu"

**Cause :** URL incorrecte ou serveur inaccessible
**Solution :**
```bash
# Vérifier l'URL dans Stripe Dashboard
# Tester l'accessibilité
curl -X POST https://votre-domaine.com/api/partnership/stripe/webhook
```

#### 3. "Abonnement non créé"

**Cause :** Erreur dans le traitement webhook
**Solution :**
```bash
# Vérifier les logs
docker-compose logs teambrains-backend

# Synchroniser manuellement
POST /api/partnership/stripe/sync-subscription
```

#### 4. "Erreur de base de données"

**Cause :** Problème de connexion DB ou migration
**Solution :**
```bash
# Vérifier la connexion DB
docker-compose exec teambrains-backend python -c "from models import db; print(db.engine.execute('SELECT 1').fetchone())"

# Appliquer les migrations
docker-compose exec teambrains-backend flask db upgrade
```

### Commandes Utiles

```bash
# Redémarrer le serveur
docker-compose restart teambrains-backend

# Voir les logs en temps réel
docker-compose logs -f teambrains-backend

# Tester l'API
curl -X GET http://localhost:5001/api/partnership/stripe/subscription/status \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Lister les webhooks Stripe
stripe webhook_endpoints list
```

---

## Monitoring Production

### Métriques à Surveiller

1. **Taux de succès webhook** : > 99%
2. **Temps de réponse** : < 2s
3. **Erreurs de signature** : 0
4. **Abonnements créés** : Correspond aux paiements

### Alertes Recommandées

- Webhook échec > 5%
- Temps de réponse > 5s
- Erreurs de base de données
- Abonnements orphelins

### Logs Production

```bash
# Logs structurés
docker-compose logs teambrains-backend | grep "PARTNERSHIP WEBHOOK"

# Logs d'erreur
docker-compose logs teambrains-backend | grep "ERROR"
```

---

## Sécurité

### Bonnes Pratiques

1. **Ne jamais commiter** les clés Stripe
2. **Utiliser des secrets** différents dev/prod
3. **Valider les signatures** webhook
4. **Limiter les permissions** des clés API
5. **Monitorer les accès** API

### Permissions Stripe Recommandées

- **Lecture** : customers, subscriptions, invoices
- **Écriture** : customers, subscriptions
- **Webhooks** : Événements spécifiques uniquement

---

## Support

### Ressources Utiles

- [Documentation Stripe](https://stripe.com/docs)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Webhooks Guide](https://stripe.com/docs/webhooks)
- [API Reference](https://stripe.com/docs/api)

### Contact

Pour les problèmes spécifiques à TeamBrains :
- Vérifier les logs d'abord
- Utiliser les endpoints de debug
- Consulter cette documentation

---

*Dernière mise à jour : Juillet 2025* 