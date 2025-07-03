#!/bin/bash

# Script de Setup Stripe - TeamBrains
# Usage: ./setup_stripe.sh [dev|prod]

set -e

echo "Configuration Stripe TeamBrains"
echo "================================"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les messages
print_info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

print_success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

print_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Vérifier l'environnement
ENV=${1:-dev}
if [[ "$ENV" != "dev" && "$ENV" != "prod" ]]; then
    print_error "Usage: $0 [dev|prod]"
    exit 1
fi

print_info "Configuration pour l'environnement: $ENV"

# Vérifier si Stripe CLI est installé
if ! command -v stripe &> /dev/null; then
    print_warning "Stripe CLI non trouvé. Installation..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install stripe/stripe-cli/stripe
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg
        echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list
        sudo apt update && sudo apt install stripe
    else
        print_error "Système d'exploitation non supporté. Installez Stripe CLI manuellement."
        exit 1
    fi
fi

print_success "Stripe CLI installé"

# Configuration selon l'environnement
if [[ "$ENV" == "dev" ]]; then
    print_info "Configuration Développement"
    echo "================================"
    
    # Vérifier si l'utilisateur est connecté
    if ! stripe config --list &> /dev/null; then
        print_warning "Connexion Stripe requise"
        stripe login
    fi
    
    print_success "Stripe CLI connecté"
    
    # Créer le fichier .env s'il n'existe pas
    if [[ ! -f "teambrains-backend/.env" ]]; then
        print_info "Création du fichier .env"
        cat > teambrains-backend/.env << EOF
# Stripe Configuration - Développement
STRIPE_SECRET_KEY=sk_test_...  # Remplacez par votre clé de test
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Remplacez par votre clé publique de test

# Webhooks (optionnel en dev - utilise des secrets fixes)
STRIPE_WEBHOOK_SECRET=whsec_...  # Pour webhook principal (si utilisé)
STRIPE_PARTNERSHIP_WEBHOOK_SECRET=whsec_...  # Pour webhook partenariat
EOF
        print_success "Fichier .env créé"
        print_warning "N'oubliez pas de remplacer les clés Stripe par vos vraies clés de test"
    else
        print_info "Fichier .env existe déjà"
    fi
    
    # Instructions pour le webhook listener
    echo ""
    print_info "Pour lancer le webhook listener en développement :"
    echo "stripe listen --forward-to localhost:5001/api/partnership/stripe/webhook"
    echo ""
    print_warning "Copiez le secret webhook affiché et mettez-le à jour dans le code si nécessaire"
    
elif [[ "$ENV" == "prod" ]]; then
    print_info "Configuration Production"
    echo "============================"
    
    # Vérifier les variables d'environnement
    if [[ -z "$STRIPE_SECRET_KEY" || -z "$STRIPE_PUBLISHABLE_KEY" ]]; then
        print_error "Variables d'environnement Stripe manquantes"
        echo "Définissez :"
        echo "  STRIPE_SECRET_KEY=sk_live_..."
        echo "  STRIPE_PUBLISHABLE_KEY=pk_live_..."
        exit 1
    fi
    
    if [[ -z "$STRIPE_PARTNERSHIP_WEBHOOK_SECRET" ]]; then
        print_error "Secret webhook partenariat manquant"
        echo "Définissez :"
        echo "  STRIPE_PARTNERSHIP_WEBHOOK_SECRET=whsec_..."
        exit 1
    fi
    
    print_success "Variables d'environnement configurées"
    
    # Instructions pour la configuration webhook
    echo ""
    print_info "Configuration webhook production :"
    echo "1. Allez sur https://dashboard.stripe.com/webhooks"
    echo "2. Créez un endpoint avec l'URL :"
    echo "   https://votre-domaine.com/api/partnership/stripe/webhook"
    echo "3. Activez les événements :"
    echo "   - checkout.session.completed"
    echo "   - invoice.payment_succeeded"
    echo "   - invoice.payment_failed"
    echo "   - customer.subscription.updated"
    echo "   - customer.subscription.deleted"
    echo "   - invoice.payment_action_required"
    echo "4. Copiez le secret dans STRIPE_PARTNERSHIP_WEBHOOK_SECRET"
fi

# Test de connexion Stripe
print_info "Test de connexion Stripe..."
if curl -s -H "Authorization: Bearer $STRIPE_SECRET_KEY" https://api.stripe.com/v1/customers &> /dev/null; then
    print_success "Connexion Stripe OK"
else
    print_warning "Impossible de tester la connexion Stripe (clés non configurées ou invalides)"
fi

# Instructions finales
echo ""
print_success "Setup terminé !"
echo ""
print_info "Prochaines étapes :"
if [[ "$ENV" == "dev" ]]; then
    echo "1. Remplacez les clés Stripe dans teambrains-backend/.env"
    echo "2. Lancez le webhook listener :"
    echo "   stripe listen --forward-to localhost:5001/api/partnership/stripe/webhook"
    echo "3. Démarrez le serveur :"
    echo "   docker-compose up"
    echo "4. Testez avec :"
    echo "   stripe trigger checkout.session.completed"
else
    echo "1. Configurez le webhook dans le Dashboard Stripe"
    echo "2. Déployez votre application"
    echo "3. Testez les webhooks"
    echo "4. Monitorer les logs"
fi

echo ""
print_info "Documentation complète : STRIPE_SETUP.md" 