import os  # <--- INDISPENSABLE pour utiliser os.path
from flask import Flask
from flask_cors import CORS
from models import db
from flask_migrate import Migrate
from routes.patient_routes import patient_bp
from routes.full_routes import full_bp

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
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(patient_bp)
app.register_blueprint(full_bp)

if __name__ == '__main__':
    app.run(debug=True)