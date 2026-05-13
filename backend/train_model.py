import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# 1. Génération de données fictives réalistes
def generate_medical_data(n=1000):
    np.random.seed(42)
    data = []
    for _ in range(n):
        age = np.random.randint(1, 90)
        temp = np.random.uniform(36.0, 41.0)
        tension = np.random.randint(90, 160)
        toux = np.random.choice([0, 1])
        frissons = np.random.choice([0, 1])
        fatigue = np.random.choice([0, 1])
        maux_tete = np.random.choice([0, 1])
        vomissement = np.random.choice([0, 1])

        # Règles logiques pour les tables (ce que l'IA doit apprendre)
        fievre = 1 if temp > 38.5 else 0
        paludisme = 1 if (temp > 39 and frissons == 1 and maux_tete == 1) else 0
        grippe = 1 if (toux == 1 and fatigue == 1 and temp > 37.5) else 0
        anemie = 1 if (fatigue == 1 and age > 60) else 0 # Exemple simplifié

        data.append([age, temp, tension, fatigue, frissons, toux, maux_tete, vomissement, 
             fievre, paludisme, grippe, anemie])
        
    columns = ['age', 'temperature', 'tension', 'fatigue', 'frissons', 'toux', 
               'maux_tete', 'vomissement', 'fievre', 'paludisme', 'grippe', 'anemie']
    return pd.DataFrame(data, columns=columns)

# 2. Entraînement
df = generate_medical_data()
X = df[['age', 'temperature', 'tension', 'fatigue', 'frissons', 'toux', 'maux_tete', 'vomissement']]
y = df[['fievre', 'paludisme', 'grippe', 'anemie']]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 3. Sauvegarde
if not os.path.exists('model_data'): os.makedirs('model_data')
joblib.dump(model, 'model_data/random_forest_model.pkl')
print("Modèle entraîné et sauvegardé dans model_data/random_forest_model.pkl")