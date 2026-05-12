## Installation du Backend
1. Aller dans le dossier backend : `cd backend`
2. Créer l'environnement virtuel : `python -m venv venv`
3. Activer l'environnement en Linux ou Mac : `source venv/bin/activate`
4. Activer l'environnement en Windows : `.\venv\Scripts\activate`
5. Installer les dépendances : `pip install -r requirements.txt`
6. Initialiser la base de données (Migration) : `flask db upgrade`
7. Lancer le serveur : `python app.py`