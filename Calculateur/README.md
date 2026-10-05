# Calculateur Starlink Education - Groupe 3 (EC2LT)

Calculateur interactif de dimensionnement (bande passante + TCO sur 5 ans en FCFA)
pour un pilote de déploiement Starlink dans une école rurale sénégalaise.

Projet PPP - *Starlink au Service de l'Éducation et de l'Enseignement Supérieur*.

## Installation

**Prérequis : Python 3.12** (les dépendances ne sont pas garanties compatibles avec 3.13+)

```bash
py -3.12 -m venv .venv

# Windows
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

python --version   # doit afficher 3.12.x
pip install -r requirements.txt
```

## Lancer l'application

```bash
streamlit run app/app.py
```

L'application est accessible sur http://localhost:8501

## Lancer les tests

```bash
pytest tests/test_calculs.py
```

## Structure du projet

```
Projet_Starlink_Education/
├── app/
│   ├── app.py                  # Interface Streamlit
│   └── utils/
│       ├── calculs.py          # Moteur de calcul (débit, énergie, TCO)
│       └── donnees.py          # Constantes et chargement des données
├── data/
│   ├── couts_materiel.json     # Prix matériel (provisoires, voir champ _note)
│   └── parametres_ecole.json   # Paramètres par défaut de l'école
├── tests/
│   └── test_calculs.py
├── config.yaml
└── requirements.txt
```

## Formules

| Grandeur | Formule |
|---|---|
| Utilisateurs simultanés | `inscrits x taux de contention` |
| Débit requis (↓ et ↑) | `simultanés x débit par utilisateur (profil)` |
| Capacité effective | `capacité max annoncée x coefficient de débit réel` |
| Volume mensuel (Go) | `débit x 3600 x h/jour x jours/mois x facteur d'activité / 8 / 1000` |
| Énergie / jour | `puissance totale (W) x heures d'utilisation` |
| Panneaux | `ceil(énergie x 1,2 / (puissance panneau x heures de soleil))` |
| Batterie (Ah) | `énergie x jours d'autonomie / (tension x profondeur de décharge)` |
| Nb batteries | `ceil(Ah requis / Ah par batterie)` |
| TCO 5 ans | `matériel + abonnement x 60 + 5 % x 5 ans x matériel + installation + formation` |

## Hypothèses et sources (à compléter avant le rendu)

| Hypothèse | Valeur | Source / statut |
|---|---|---|
| Offres, kits, abonnements, 305 / 40 Mbps | Lite 22 000 / Rés. 30 000 FCFA/mois ; kits 117 000 / 146 000 | Cahier des charges du projet |
| Débit par profil (↓) | 1,5 / 2,0 / 3,0 Mbps | Recommandations Zoom, Teams, BigBlueButton, Moodle : **ajouter les liens** |
| Débit par profil (↑) | 0,2 / 0,3 / 0,5 Mbps | **Hypothèse de groupe, à sourcer ou justifier** |
| Coefficient de débit réel | 70 % | **Hypothèse prudente**, modifiable dans l'interface |
| Consommation | Starlink 75 W + routeur 15 W + switch 10 W | **À sourcer** (fiche technique Starlink, fiches équipements LOT3) |
| Maintenance | 5 % du matériel par an | **Hypothèse à justifier** |
| Facteur d'activité moyen | 50 % | **Hypothèse** (le débit requis est un pic) |
| Jours d'école par mois | 22 | Hypothèse |

## ⚠️ Données provisoires

Les prix routeur (80 000 FCFA) et switch (160 000 FCFA) sont réels. Les
constantes panneau solaire, batterie (prix, capacité en Ah), installation et
formation sont provisoires en attendant les données réelles remontées par LOT3 (maquette
réseau) et LOT4 (alimentation solaire). Elles sont modifiables directement
dans `data/couts_materiel.json`, marquées par le champ `_note`.
