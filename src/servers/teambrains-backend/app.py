from flask import Flask
from flask_cors import CORS
import logging
from models import db, User, Project
from routes.auth import auth
from routes.users import users
from routes.projects import projects
from routes.cv import cv_bp
from dotenv import load_dotenv
import os
from extensions import bcrypt, mail
from flask_jwt_extended import JWTManager
from routes.contact import contact_bp
from routes.chat import chat_bp
from routes.planification import planification_bp
from flask_migrate import Migrate
from routes.uploadFile import upload_bp
from routes.sprint import sprint_bp
from routes.validation import validation_bp
from routes.schools import schools_bp
from routes.school_partnership import school_partnership_bp
from routes.stripe_partnership import stripe_partnership_bp
from routes.search import search_bp
from routes.subtasks import subtasks_bp
from routes.skills import skills_bp
from routes.visibility import visibility_bp
from models import School, Task, SubTask, TaskValidation, SubTaskValidation, CVProject, project_members
from datetime import datetime, timedelta


load_dotenv()

# Configuration du logging avec fichier
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
bcrypt.init_app(app)
#CORS(app, supports_credentials=True, origins=["http://localhost:5173/"])


app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(projects, url_prefix='/projects')
app.register_blueprint(cv_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(planification_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(sprint_bp)
app.register_blueprint(validation_bp)
app.register_blueprint(schools_bp)
app.register_blueprint(school_partnership_bp)
app.register_blueprint(stripe_partnership_bp)
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(subtasks_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(visibility_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = 'mailpit'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite la taille des fichiers à 16 Mo

db.init_app(app)

# Initialiser Flask-Migrate
migrate = Migrate(app, db)

jwt = JWTManager(app)

mail.init_app(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

with app.app_context():
    db.create_all()


def insert_test_data():
    """Insérer les données de test après les migrations"""
    try:
        # Vérifier si des données existent déjà
        if User.query.first() is not None:
            print("ℹ️  Les données de test existent déjà, pas d'insertion nécessaire.")
            return
        
        print("🌱 Insertion des données de test...")
        
        # Créer les écoles
        school1 = School(
            name='École Polytechnique',
            description='Grande école d\'ingénieurs',
            contact_email='contact@polytechnique.fr',
            website='https://polytechnique.fr',
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        school2 = School(
            name='HEC Paris',
            description='École de commerce',
            contact_email='contact@hec.fr',
            website='https://hec.fr',
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.session.add(school1)
        db.session.add(school2)
        db.session.commit()
        
        # Créer les utilisateurs avec mots de passe hashés
        users_data = [
            {
                'id': 'u1', 'role': 'student', 'nom': 'Dupont', 'prenom': 'Alice',
                'email': 'alice@polytechnique.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': 'FullStack', 'technologies': 'Python,React,SQL',
                'etudes': 'École Polytechnique - Informatique', 'ambitions': 'Devenir CTO',
                'linkedin_url': 'https://linkedin.com/in/alice-dupont',
                'portfolio_url': 'https://portfolio.alice.com',
                'github_url': 'https://github.com/alice-dupont', 'school_id': 1
            },
            {
                'id': 'u2', 'role': 'student', 'nom': 'Martin', 'prenom': 'Bob',
                'email': 'bob@polytechnique.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': 'BackEnd', 'technologies': 'Python,Django,PostgreSQL',
                'etudes': 'École Polytechnique - Génie Logiciel', 'ambitions': 'Expert en architecture backend',
                'linkedin_url': 'https://linkedin.com/in/bob-martin',
                'portfolio_url': 'https://portfolio.bob.com',
                'github_url': 'https://github.com/bob-martin', 'school_id': 1
            },
            {
                'id': 'u3', 'role': 'student', 'nom': 'Durand', 'prenom': 'Chloé',
                'email': 'chloe@hec.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': 'FrontEnd', 'technologies': 'JavaScript,React,Vue.js',
                'etudes': 'HEC Paris - Digital Business', 'ambitions': 'Lead Frontend Developer',
                'linkedin_url': 'https://linkedin.com/in/chloe-durand',
                'portfolio_url': 'https://portfolio.chloe.com',
                'github_url': 'https://github.com/chloe-durand', 'school_id': 2
            },
            {
                'id': 'u4', 'role': 'admin', 'nom': 'Admin', 'prenom': 'Super',
                'email': 'admin@teambrains.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': None, 'technologies': None, 'etudes': None,
                'ambitions': None, 'linkedin_url': None, 'portfolio_url': None,
                'github_url': None, 'school_id': None
            },
            {
                'id': 'u5', 'role': 'school_admin', 'nom': 'Admin', 'prenom': 'Polytechnique',
                'email': 'admin.polytechnique@polytechnique.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': None, 'technologies': None, 'etudes': None,
                'ambitions': None, 'linkedin_url': None, 'portfolio_url': None,
                'github_url': None, 'school_id': 1
            },
            {
                'id': 'u6', 'role': 'school_admin', 'nom': 'Admin', 'prenom': 'HEC',
                'email': 'admin.hec@hec.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': None, 'technologies': None, 'etudes': None,
                'ambitions': None, 'linkedin_url': None, 'portfolio_url': None,
                'github_url': None, 'school_id': 2
            },
            {
                'id': 'u7', 'role': 'businessman', 'nom': 'Dubois', 'prenom': 'Thomas',
                'email': 'thomas@startup.fr', 'password': bcrypt.generate_password_hash('password123').decode('utf-8'),
                'typeDeveloppeur': None, 'technologies': None, 'etudes': None,
                'ambitions': None, 'linkedin_url': None, 'portfolio_url': None,
                'github_url': None, 'school_id': None
            }
        ]
        
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
        
        db.session.commit()
        
        # Créer les projets (créés par l'entrepreneur)
        project1 = Project(
            name='Projet IA', project_slug='projet-ia',
            creation_date=datetime.utcnow(), status='in_progress',
            description='Projet d\'intelligence artificielle',
            creator_id='u7', progress=50
        )
        
        project2 = Project(
            name='Plateforme Web', project_slug='plateforme-web',
            creation_date=datetime.utcnow(), status='in_progress',
            description='Développement d\'une plateforme web',
            creator_id='u7', progress=100
        )
        
        project3 = Project(
            name='App Mobile', project_slug='app-mobile',
            creation_date=datetime.utcnow(), status='in_progress',
            description='Application mobile React Native',
            creator_id='u7', progress=25
        )
        
        db.session.add(project1)
        db.session.add(project2)
        db.session.add(project3)
        db.session.commit()
        
        # Ajouter les membres de projet (avec les bonnes combinaisons pour pouvoir lancer)
        members_data = [
            # Projet 1: FullStack (Alice) - peut être lancé
            {'project_id': 1, 'user_id': 'u1', 'role': 'FullStack'},
            # Projet 2: BackEnd (Bob) + FrontEnd (Chloé) - peut être lancé
            {'project_id': 2, 'user_id': 'u2', 'role': 'BackEnd'},
            {'project_id': 2, 'user_id': 'u3', 'role': 'FrontEnd'},
            # Projet 3: Seulement BackEnd (Bob) - ne peut PAS être lancé (manque FrontEnd)
            {'project_id': 3, 'user_id': 'u2', 'role': 'BackEnd'}
        ]
        
        for member_data in members_data:
            stmt = project_members.insert().values(**member_data)
            db.session.execute(stmt)
        
        db.session.commit()
        
        # Créer les tâches
        task1 = Task(
            title='Collecte de données', description='Rassembler les datasets',
            due_date=datetime.utcnow() + timedelta(days=7), percent_completion=20,
            assignee_id='u2', project_id=1, priority='haute', sprint='Sprint 1'
        )
        
        task2 = Task(
            title='Déploiement', description='Déployer sur le cloud',
            due_date=datetime.utcnow() + timedelta(days=14), percent_completion=100,
            assignee_id='u3', project_id=2, priority='moyenne', sprint='Sprint 2'
        )
        
        task3 = Task(
            title='Design UI/UX', description='Créer les maquettes de l\'app',
            due_date=datetime.utcnow() + timedelta(days=10), percent_completion=0,
            assignee_id='u3', project_id=3, priority='haute', sprint='Sprint 1'
        )
        
        db.session.add(task1)
        db.session.add(task2)
        db.session.add(task3)
        db.session.commit()
        
        # Créer les sous-tâches
        subtask1 = SubTask(
            title='Télécharger dataset', description='Télécharger depuis Kaggle',
            due_date=datetime.utcnow() + timedelta(days=2), percent_completion=100,
            priority='haute', status='done', task_id=1, assigned_student_id='u2',
            created_date=datetime.utcnow()
        )
        
        subtask2 = SubTask(
            title='Nettoyer données', description='Supprimer les valeurs manquantes',
            due_date=datetime.utcnow() + timedelta(days=4), percent_completion=0,
            priority='moyenne', status='pending', task_id=1, assigned_student_id='u1',
            created_date=datetime.utcnow()
        )
        
        db.session.add(subtask1)
        db.session.add(subtask2)
        db.session.commit()
        
        # Créer les validations
        task_validation = TaskValidation(
            task_id=1, status='validated', comment='OK',
            validator_id='u1', timestamp=datetime.utcnow()
        )
        
        subtask_validation = SubTaskValidation(
            subtask_id=1, status='validated', feedback='Bien joué',
            validator_id='u1', timestamp=datetime.utcnow()
        )
        
        db.session.add(task_validation)
        db.session.add(subtask_validation)
        db.session.commit()
        
        # Créer les CV projects (sans ID fixe pour éviter les conflits)
        cv_projects_data = [
            {
                'user_id': 'u1', 'project_id': 1, 'role': 'FullStack Developer',
                'start_date': datetime.utcnow() - timedelta(days=30),
                'end_date': datetime.utcnow(), 'team_size': 1,
                'description': 'Développement full-stack du projet IA'
            },
            {
                'user_id': 'u2', 'project_id': 2, 'role': 'Backend Developer',
                'start_date': datetime.utcnow() - timedelta(days=45),
                'end_date': datetime.utcnow(), 'team_size': 2,
                'description': 'Développement des APIs de la plateforme'
            },
            {
                'user_id': 'u3', 'project_id': 2, 'role': 'Frontend Developer',
                'start_date': datetime.utcnow() - timedelta(days=45),
                'end_date': datetime.utcnow(), 'team_size': 2,
                'description': 'Développement de l\'interface utilisateur'
            },
            {
                'user_id': 'u2', 'project_id': 3, 'role': 'Backend Developer',
                'start_date': datetime.utcnow() - timedelta(days=15),
                'end_date': datetime.utcnow(), 'team_size': 1,
                'description': 'Développement des APIs de l\'application mobile'
            }
        ]
        
        for cv_project_data in cv_projects_data:
            cv_project = CVProject(**cv_project_data)
            db.session.add(cv_project)
        
        db.session.commit()
        
        print("✅ Données de test insérées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données de test: {e}")
        db.session.rollback()


# Insérer les données de test après la création des tables
with app.app_context():
    insert_test_data()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
