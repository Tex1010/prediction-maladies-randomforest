import os  # <--- INDISPENSABLE pour utiliser os.path
from flask import Flask
from flask_cors import CORS
from models import db

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION DU CHEMIN ---
# On s'assure que le dossier 'instance' existe à la racine du projet
instance_path = os.path.join(app.root_path, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# On force le chemin vers le dossier instance pour maladies.db
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "maladies.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

# --- INITIALISATION ---
db.init_app(app)

with app.app_context():
    # SQLAlchemy va scanner tes fichiers dans le dossier /models 
    # et créer les tables s'il trouve les classes
    db.create_all()
    print(f"✅ Succès ! Base de données créée ici : {app.config['SQLALCHEMY_DATABASE_URI']}")

if __name__ == '__main__':
    app.run(debug=True)