"""
calculs.py - Moteur de calcul du calculateur Starlink Education.

Contient : dimensionnement du débit (descendant + montant), alerte de
saturation, volume de données mensuel, dimensionnement énergie/solaire/
batteries, et calcul du TCO sur 5 ans.
"""

import math

from utils.donnees import (
    PROFILS_USAGE,
    PROFILS_USAGE_UP,
    CAPACITE_DOWN_MBPS,
    CAPACITE_UP_MBPS,
    PUISSANCE_TOTALE_W,
    TAUX_MAINTENANCE_ANNUEL,
    DUREE_ABONNEMENT_MOIS,
    DUREE_TCO_ANS,
)


def calculer_utilisateurs_simultanes(nb_eleves: int, taux_contention: float) -> int:
    """
    Calcule le nombre d'utilisateurs simultanés à partir du nombre
    total d'élèves et du taux de contention (ex : 0.20 pour 20 %).
    """
    return max(1, round(nb_eleves * taux_contention))


def calculer_debit_requis(nb_simultanes: int, profil: str) -> float:
    """Débit descendant total requis (Mbps) selon le profil d'usage."""
    debit_par_utilisateur = PROFILS_USAGE.get(profil)
    if debit_par_utilisateur is None:
        raise ValueError(f"Profil d'usage inconnu : {profil}")
    return nb_simultanes * debit_par_utilisateur


def calculer_debit_montant_requis(nb_simultanes: int, profil: str) -> float:
    """Débit montant total requis (Mbps) selon le profil d'usage."""
    debit_par_utilisateur = PROFILS_USAGE_UP.get(profil)
    if debit_par_utilisateur is None:
        raise ValueError(f"Profil d'usage inconnu : {profil}")
    return nb_simultanes * debit_par_utilisateur


def calculer_capacite_effective(capacite_max_mbps: float, coefficient_reel: float = 1.0) -> float:
    """
    Capacité réellement exploitable = capacité maximale annoncée x coefficient
    de débit réel (0 < coefficient <= 1). Le débit annoncé est un maximum.
    """
    if not 0 < coefficient_reel <= 1:
        raise ValueError("Le coefficient de débit réel doit être dans ]0 ; 1]")
    return capacite_max_mbps * coefficient_reel


def verifier_saturation(debit_requis_mbps: float, capacite_mbps: float = CAPACITE_DOWN_MBPS) -> dict:
    """
    Compare le débit requis à la capacité.
    Retourne un statut ("OK" / "SATURE") et la marge disponible.
    """
    sature = debit_requis_mbps > capacite_mbps
    return {
        "statut": "SATURE" if sature else "OK",
        "debit_requis_mbps": round(debit_requis_mbps, 1),
        "capacite_mbps": round(capacite_mbps, 1),
        "marge_mbps": round(capacite_mbps - debit_requis_mbps, 1),
    }


def calculer_volume_mensuel_go(
    debit_requis_mbps: float,
    heures_par_jour: float,
    jours_par_mois: float = 22,
    facteur_activite: float = 0.5,
) -> float:
    """
    Estime le volume de données descendant mensuel (Go).
    Le débit requis est un pic : on applique un facteur d'activité moyen
    (part du temps où le pic est réellement atteint).
    Mbps -> Go : débit x 3600 s x heures x jours x facteur / 8 / 1000.
    """
    megabits = debit_requis_mbps * 3600 * heures_par_jour * jours_par_mois * facteur_activite
    return round(megabits / 8 / 1000, 1)


def calculer_energie_journaliere(heures_utilisation: float, puissance_w: float = PUISSANCE_TOTALE_W) -> float:
    """
    Énergie consommée par jour (Wh).
    Puissance par défaut = Starlink + routeur + switch (100 W).
    """
    return puissance_w * heures_utilisation


def calculer_nombre_panneaux(
    energie_wh_jour: float,
    puissance_panneau_w: float,
    heures_ensoleillement: float,
    marge_securite: float = 1.2,
) -> int:
    """
    Nombre de panneaux solaires nécessaires (arrondi au supérieur).
    Marge de sécurité de 20 % par défaut (pertes, nébulosité).
    """
    production_panneau_wh_jour = puissance_panneau_w * heures_ensoleillement
    return max(1, math.ceil(energie_wh_jour * marge_securite / production_panneau_wh_jour))


def calculer_capacite_batterie_ah(
    energie_wh_jour: float,
    jours_autonomie: float,
    tension_batterie_v: float,
    profondeur_decharge: float = 0.8,
) -> float:
    """
    Capacité totale de batterie nécessaire (Ah) pour l'autonomie souhaitée
    (par défaut 2 jours en cas de nébulosité).
    """
    energie_totale_wh = energie_wh_jour * jours_autonomie
    capacite_ah = energie_totale_wh / (tension_batterie_v * profondeur_decharge)
    return round(capacite_ah, 1)


def calculer_nombre_batteries(capacite_requise_ah: float, capacite_unitaire_ah: float) -> int:
    """Nombre de batteries (en parallèle, même tension) pour couvrir la capacité requise."""
    return max(1, math.ceil(capacite_requise_ah / capacite_unitaire_ah))


def calculer_tco(
    prix_kit_fcfa: float,
    abonnement_mensuel_fcfa: float,
    prix_routeur_fcfa: float,
    prix_switch_fcfa: float,
    cout_panneaux_fcfa: float,
    cout_batteries_fcfa: float,
    cout_installation_fcfa: float = 0,
    cout_formation_fcfa: float = 0,
    duree_mois: int = DUREE_ABONNEMENT_MOIS,
    taux_maintenance: float = TAUX_MAINTENANCE_ANNUEL,
    duree_ans: int = DUREE_TCO_ANS,
) -> dict:
    """
    TCO sur 5 ans en FCFA : matériel, abonnement, maintenance (% annuel du
    matériel), installation et formation (coûts uniques).
    """
    cout_materiel = (
        prix_kit_fcfa + prix_routeur_fcfa + prix_switch_fcfa + cout_panneaux_fcfa + cout_batteries_fcfa
    )
    cout_abonnement = abonnement_mensuel_fcfa * duree_mois
    cout_maintenance = cout_materiel * taux_maintenance * duree_ans
    total = (
        cout_materiel + cout_abonnement + cout_maintenance
        + cout_installation_fcfa + cout_formation_fcfa
    )
    return {
        "materiel_fcfa": round(cout_materiel),
        "abonnement_fcfa": round(cout_abonnement),
        "maintenance_fcfa": round(cout_maintenance),
        "installation_fcfa": round(cout_installation_fcfa),
        "formation_fcfa": round(cout_formation_fcfa),
        "total_fcfa": round(total),
    }
