"""
donnees.py - Constantes et chargement des données de configuration
pour le calculateur Starlink Education (Groupe 3 - PPP EC2LT).

Certaines valeurs sont provisoires (voir data/couts_materiel.json,
champ "_note") en attendant les données réelles remontées par
LOT3 (prix matériel réseau) et LOT4 (dimensionnement solaire).
"""

import json
from pathlib import Path

# Racine du projet : app/utils/donnees.py -> app/utils -> app -> racine
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def _charger_json(nom_fichier: str) -> dict:
    """Charge un fichier JSON depuis le dossier data/."""
    chemin = DATA_DIR / nom_fichier
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Offres Starlink (cahier des charges + état de l'art LOT1) ---

OFFRES_STARLINK = {
    "Lite": {
        "prix_kit_fcfa": 117000,
        "abonnement_mensuel_fcfa": 22000,
    },
    "Résidentiel": {
        "prix_kit_fcfa": 146000,
        "abonnement_mensuel_fcfa": 30000,
    },
}

CAPACITE_DOWN_MBPS = 305
CAPACITE_UP_MBPS = 40

# --- Profils d'usage pédagogique (débit / utilisateur en Mbps) ---
# Source : recommandations Zoom / Teams / BigBlueButton + doc Moodle (état de l'art LOT1)

PROFILS_USAGE = {
    "LMS / OER": 1.5,
    "Classe virtuelle": 2.0,
    "Visio + IA pédagogique": 3.0,
}

# Débit MONTANT par utilisateur (Mbps) - HYPOTHÈSE de groupe à sourcer :
# la majorité des élèves reçoivent sans émettre (caméra coupée), d'où des
# valeurs bien inférieures au débit descendant.
PROFILS_USAGE_UP = {
    "LMS / OER": 0.2,
    "Classe virtuelle": 0.3,
    "Visio + IA pédagogique": 0.5,
}

# --- Énergie ---

PUISSANCE_STARLINK_W = 75
PUISSANCE_ROUTEUR_W = 15
PUISSANCE_SWITCH_W = 10
PUISSANCE_TOTALE_W = PUISSANCE_STARLINK_W + PUISSANCE_ROUTEUR_W + PUISSANCE_SWITCH_W  # 100 W

# --- TCO ---

TAUX_MAINTENANCE_ANNUEL = 0.05
DUREE_ABONNEMENT_MOIS = 60
DUREE_TCO_ANS = 5


def charger_couts_materiel() -> dict:
    """
    Retourne les coûts matériel (routeur, switch, panneau, batterie).
    Chargés depuis data/couts_materiel.json.
    Valeurs provisoires tant que LOT3/LOT4 n'ont pas transmis les prix réels.
    """
    return _charger_json("couts_materiel.json")


def charger_parametres_ecole() -> dict:
    """
    Retourne les paramètres par défaut de l'école (curseurs, hypothèses solaires).
    Chargés depuis data/parametres_ecole.json.
    """
    return _charger_json("parametres_ecole.json")
