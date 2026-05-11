from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .patient import Patient
from .parametre import Parametre
from .resultat import Resultat