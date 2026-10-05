"""
Tests unitaires pour le moteur de calcul (app/utils/calculs.py).
Lancer avec : pytest tests/test_calculs.py
"""

import sys
from pathlib import Path

# Ajoute app/ au path pour retrouver le package "utils" (même logique que Streamlit)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))

from utils.calculs import (
    calculer_utilisateurs_simultanes,
    calculer_debit_requis,
    calculer_debit_montant_requis,
    calculer_capacite_effective,
    calculer_volume_mensuel_go,
    calculer_nombre_batteries,
    verifier_saturation,
    calculer_energie_journaliere,
    calculer_nombre_panneaux,
    calculer_capacite_batterie_ah,
    calculer_tco,
)


def test_utilisateurs_simultanes():
    assert calculer_utilisateurs_simultanes(500, 0.20) == 100


def test_utilisateurs_simultanes_minimum():
    assert calculer_utilisateurs_simultanes(10, 0.01) >= 1


def test_debit_requis():
    assert calculer_debit_requis(100, "Classe virtuelle") == 200.0


def test_debit_requis_profil_invalide():
    try:
        calculer_debit_requis(100, "Inconnu")
        assert False, "Une erreur aurait du etre levee"
    except ValueError:
        pass


def test_saturation_ok():
    resultat = verifier_saturation(200, capacite_mbps=305)
    assert resultat["statut"] == "OK"


def test_saturation_depassee():
    resultat = verifier_saturation(400, capacite_mbps=305)
    assert resultat["statut"] == "SATURE"


def test_energie_journaliere():
    assert calculer_energie_journaliere(8, puissance_w=100) == 800


def test_nombre_panneaux():
    # 800 Wh x 1.2 = 960 Wh ; un panneau 150 W x 5 h = 750 Wh -> 2 panneaux
    assert calculer_nombre_panneaux(800, 150, 5) == 2


def test_capacite_batterie():
    ah = calculer_capacite_batterie_ah(
        energie_wh_jour=800, jours_autonomie=2, tension_batterie_v=12, profondeur_decharge=0.8
    )
    assert ah == 166.7  # 1600 Wh / (12 V x 0.8)


def test_nombre_batteries():
    assert calculer_nombre_batteries(166.7, 100) == 2
    assert calculer_nombre_batteries(100, 100) == 1


def test_debit_montant():
    assert calculer_debit_montant_requis(100, "Classe virtuelle") == 30.0


def test_capacite_effective():
    assert calculer_capacite_effective(305, 0.7) == 213.5


def test_capacite_effective_invalide():
    try:
        calculer_capacite_effective(305, 1.5)
        assert False, "Une erreur aurait du etre levee"
    except ValueError:
        pass


def test_volume_mensuel():
    # 100 Mbps x 3600 s x 8 h x 22 j x 0.5 / 8 / 1000 = 3960 Go
    assert calculer_volume_mensuel_go(100, 8, 22, 0.5) == 3960.0


def test_tco():
    resultat = calculer_tco(
        prix_kit_fcfa=117000,
        abonnement_mensuel_fcfa=22000,
        prix_routeur_fcfa=80000,
        prix_switch_fcfa=50000,
        cout_panneaux_fcfa=45000,
        cout_batteries_fcfa=60000,
    )
    assert resultat["total_fcfa"] > 0
    assert resultat["abonnement_fcfa"] == 22000 * 60


def test_tco_valeur_exacte():
    # materiel = 117000+80000+160000+90000+120000 = 567000
    # abonnement = 22000 x 60 = 1 320 000 ; maintenance = 567000 x 5 % x 5 = 141750
    r = calculer_tco(117000, 22000, 80000, 160000, 90000, 120000, cout_installation_fcfa=100000, cout_formation_fcfa=150000)
    assert r["materiel_fcfa"] == 567000
    assert r["maintenance_fcfa"] == 141750
    assert r["total_fcfa"] == 567000 + 1320000 + 141750 + 100000 + 150000
