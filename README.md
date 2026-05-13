## Installation du Backend
1. Aller dans le dossier backend : `cd backend`
2. Créer l'environnement virtuel : `python -m venv venv`
3. Activer l'environnement en Linux ou Mac : `source venv/bin/activate`
4. Activer l'environnement en Windows : `.\venv\Scripts\activate`
5. Installer les dépendances : `pip install -r requirements.txt`
6. Initialiser la base de données (Migration) : `flask db upgrade`
7. Lancer le serveur : `python app.py`

## 🧠 Modèle d'Intelligence Artificielle

Le projet utilise un modèle **Random Forest** pour prédire les risques de maladies.

### Entraînement du modèle
Si le fichier `random_forest_model.pkl` est manquant ou si vous modifiez le dataset, vous devez réentraîner le modèle :

1. Assurez-vous que l'environnement virtuel est activé.
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez le script d'entraînement :
   ```bash
   python train_model.py