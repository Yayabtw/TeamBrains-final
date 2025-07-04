#!/bin/bash

# Script pour pousser les données de test dans la base de données TeamBrains
# Usage: ./seed_database.sh

set -e

echo "🌱 Début du seeding de la base de données TeamBrains..."

# Vérifier que Docker est en cours d'exécution
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker n'est pas en cours d'exécution"
    exit 1
fi

# Vérifier que le conteneur de base de données est en cours d'exécution
if ! docker ps | grep -q "teambrains-database"; then
    echo "❌ Le conteneur teambrains-database n'est pas en cours d'exécution"
    echo "💡 Démarrez d'abord vos conteneurs avec: docker-compose up -d"
    exit 1
fi

# Attendre que PostgreSQL soit prêt
echo "⏳ Attente que PostgreSQL soit prêt..."
until docker exec teambrains-database pg_isready -U teambrains -d teambrains > /dev/null 2>&1; do
    echo "   PostgreSQL n'est pas encore prêt, attente..."
    sleep 2
done

echo "✅ PostgreSQL est prêt"

# Vider les tables existantes (optionnel - décommentez si nécessaire)
# echo "🗑️  Nettoyage des tables existantes..."
# docker exec teambrains-database psql -U teambrains -d teambrains -c "
#   TRUNCATE TABLE subtask_validations, task_validations, subtasks, tasks, project_members, cv_projects, projects, users, schools CASCADE;
# "

# Pousser les données de test
echo "📊 Insertion des données de test..."
docker exec -i teambrains-database psql -U teambrains -d teambrains < infrastructure/db-init/init_teambrains.sql

# Vérifier que les données ont été insérées
echo "🔍 Vérification des données insérées..."
docker exec teambrains-database psql -U teambrains -d teambrains -c "
SELECT 
    'Schools' as table_name, COUNT(*) as count FROM schools
UNION ALL
SELECT 'Users', COUNT(*) FROM users
UNION ALL
SELECT 'Projects', COUNT(*) FROM projects
UNION ALL
SELECT 'Project Members', COUNT(*) FROM project_members
UNION ALL
SELECT 'Tasks', COUNT(*) FROM tasks
UNION ALL
SELECT 'Subtasks', COUNT(*) FROM subtasks
UNION ALL
SELECT 'Task Validations', COUNT(*) FROM task_validations
UNION ALL
SELECT 'Subtask Validations', COUNT(*) FROM subtask_validations
UNION ALL
SELECT 'CV Projects', COUNT(*) FROM cv_projects;
"

echo "✅ Seeding terminé avec succès!"
echo ""
echo "📋 Résumé des données insérées:"
echo "   - Écoles: 2"
echo "   - Utilisateurs: 6 (avec typeDeveloppeur)"
echo "   - Projets: 2"
echo "   - Membres de projet: 4"
echo "   - Tâches: 2"
echo "   - Sous-tâches: 2"
echo "   - Validations: 2"
echo "   - CV Projects: 3"
echo ""
echo "🌐 Accès à pgAdmin: http://localhost:5050"
echo "   Email: admin@admin.com"
echo "   Mot de passe: teambrains" 