"""
app.py - Interface Streamlit du calculateur Starlink Education
(LOT 2 - Groupe 3, PPP EC2LT).

Lancer avec : streamlit run app/app.py
"""

import streamlit as st
import pandas as pd

from utils import donnees
from utils.calculs import (
    calculer_utilisateurs_simultanes,
    calculer_debit_requis,
    calculer_debit_montant_requis,
    calculer_capacite_effective,
    verifier_saturation,
    calculer_volume_mensuel_go,
    calculer_energie_journaliere,
    calculer_nombre_panneaux,
    calculer_capacite_batterie_ah,
    calculer_nombre_batteries,
    calculer_tco,
)

st.set_page_config(page_title="Calculateur Starlink Education", layout="wide")

st.title(":material/satellite_alt: Calculateur Starlink - École Rurale Sénégal")
st.caption("Dimensionnement bande passante + TCO sur 5 ans (FCFA)")

parametres = donnees.charger_parametres_ecole()
couts = donnees.charger_couts_materiel()

# ----------------- SIDEBAR -----------------
st.sidebar.header("Paramètres de l'école")

nb_eleves = st.sidebar.slider(
    "Nombre total d'élèves",
    min_value=100, max_value=1000,
    value=parametres.get("nb_eleves_defaut", 500), step=10,
)

taux_contention_pct = st.sidebar.slider(
    "Taux de contention (%)",
    min_value=5, max_value=50,
    value=parametres.get("taux_contention_defaut_pct", 20), step=1,
)

profil = st.sidebar.selectbox("Profil d'usage", list(donnees.PROFILS_USAGE.keys()))

offre = st.sidebar.selectbox("Offre Starlink", list(donnees.OFFRES_STARLINK.keys()))

coef_reel_pct = st.sidebar.slider(
    "Débit réel exploitable (% du max annoncé)",
    min_value=30, max_value=100,
    value=parametres.get("coefficient_debit_reel_pct", 70), step=5,
    help="Les 305 / 40 Mbps sont des maxima « jusqu'à ». Hypothèse de dimensionnement prudente.",
)

plafond_go = st.sidebar.number_input(
    "Plafond de données mensuel (Go, 0 = illimité)",
    min_value=0, value=0, step=100,
)

st.sidebar.divider()
heures_utilisation = st.sidebar.slider(
    "Heures d'utilisation / jour",
    min_value=1, max_value=12,
    value=parametres.get("heures_utilisation_par_jour", 8),
)

# ----------------- DÉBIT & SATURATION -----------------
taux_contention = taux_contention_pct / 100
coef_reel = coef_reel_pct / 100
nb_simultanes = calculer_utilisateurs_simultanes(nb_eleves, taux_contention)

debit_requis = calculer_debit_requis(nb_simultanes, profil)
capacite_down = calculer_capacite_effective(donnees.CAPACITE_DOWN_MBPS, coef_reel)
saturation = verifier_saturation(debit_requis, capacite_down)

debit_up_requis = calculer_debit_montant_requis(nb_simultanes, profil)
capacite_up = calculer_capacite_effective(donnees.CAPACITE_UP_MBPS, coef_reel)
saturation_up = verifier_saturation(debit_up_requis, capacite_up)

col1, col2, col3 = st.columns(3)
col1.metric("Utilisateurs simultanés", nb_simultanes)
col2.metric("Débit descendant requis", f"{saturation['debit_requis_mbps']} Mbps")
col3.metric("Capacité descendante effective", f"{saturation['capacite_mbps']} Mbps")

col1b, col2b = st.columns(2)
col1b.metric("Débit montant requis", f"{saturation_up['debit_requis_mbps']} Mbps")
col2b.metric("Capacité montante effective", f"{saturation_up['capacite_mbps']} Mbps")

if saturation["statut"] == "OK":
    st.success(f":material/check_circle: Descendant OK - marge : {saturation['marge_mbps']} Mbps")
else:
    st.error(f":material/error: Descendant SATURÉ - dépassement de {-saturation['marge_mbps']} Mbps")

if saturation_up["statut"] == "OK":
    st.success(f":material/check_circle: Montant OK - marge : {saturation_up['marge_mbps']} Mbps")
else:
    st.error(f":material/error: Montant SATURÉ - dépassement de {-saturation_up['marge_mbps']} Mbps")

# ----------------- VOLUME MENSUEL -----------------
volume_go = calculer_volume_mensuel_go(
    debit_requis,
    heures_utilisation,
    parametres.get("jours_ecole_par_mois", 22),
    parametres.get("facteur_activite_moyen", 0.5),
)
st.metric("Volume descendant estimé / mois", f"{volume_go:,.0f} Go".replace(",", " "))
if plafond_go > 0:
    if volume_go > plafond_go:
        st.error(f":material/error: Plafond de {plafond_go} Go dépassé de {volume_go - plafond_go:,.0f} Go".replace(",", " "))
    else:
        st.success(f":material/check_circle: Sous le plafond de {plafond_go} Go")

# ----------------- ÉNERGIE / SOLAIRE -----------------
st.header(":material/bolt: Alimentation solaire")

energie_jour = calculer_energie_journaliere(heures_utilisation, donnees.PUISSANCE_TOTALE_W)

nb_panneaux = calculer_nombre_panneaux(
    energie_jour,
    couts.get("puissance_panneau_w", 150),
    parametres.get("heures_ensoleillement_moyen", 5),
)

capacite_batterie_ah = calculer_capacite_batterie_ah(
    energie_jour,
    parametres.get("jours_autonomie", 2),
    couts.get("tension_batterie_v", 12),
    parametres.get("profondeur_decharge_batterie", 0.8),
)

col4, col5, col6 = st.columns(3)
col4.metric("Consommation totale", f"{donnees.PUISSANCE_TOTALE_W} W")
col5.metric("Énergie / jour", f"{energie_jour:.0f} Wh")
col6.metric("Panneaux nécessaires", nb_panneaux)

nb_batteries = calculer_nombre_batteries(capacite_batterie_ah, couts.get("capacite_batterie_ah", 100))
col7, col8 = st.columns(2)
col7.metric("Capacité batterie requise", f"{capacite_batterie_ah} Ah")
col8.metric("Batteries nécessaires", nb_batteries)

# ----------------- TCO -----------------
st.header(":material/payments: TCO sur 5 ans (FCFA)")

offre_data = donnees.OFFRES_STARLINK[offre]
cout_panneaux = nb_panneaux * couts.get("prix_panneau_fcfa", 45000)
cout_batteries = nb_batteries * couts.get("prix_batterie_fcfa", 60000)

tco = calculer_tco(
    prix_kit_fcfa=offre_data["prix_kit_fcfa"],
    abonnement_mensuel_fcfa=offre_data["abonnement_mensuel_fcfa"],
    prix_routeur_fcfa=couts.get("prix_routeur_fcfa", 80000),
    prix_switch_fcfa=couts.get("prix_switch_fcfa", 160000),
    cout_panneaux_fcfa=cout_panneaux,
    cout_batteries_fcfa=cout_batteries,
    cout_installation_fcfa=couts.get("cout_installation_fcfa", 0),
    cout_formation_fcfa=couts.get("cout_formation_fcfa", 0),
)

df_tco = pd.DataFrame({
    "Poste": ["Matériel", "Abonnement (60 mois)", "Maintenance (5%/an)", "Installation", "Formation"],
    "Coût (FCFA)": [
        tco["materiel_fcfa"], tco["abonnement_fcfa"], tco["maintenance_fcfa"],
        tco["installation_fcfa"], tco["formation_fcfa"],
    ],
})

st.bar_chart(df_tco.set_index("Poste"))
st.metric("TCO Total sur 5 ans", f"{tco['total_fcfa']:,} FCFA".replace(",", " "))

# st.caption(
#     ":material/warning: Certaines valeurs (prix routeur/switch/panneau/batterie) sont provisoires "
#     "en attendant les données réelles de LOT3 (maquette réseau) et LOT4 (solaire). "
#     "Voir data/couts_materiel.json pour les modifier."
# )