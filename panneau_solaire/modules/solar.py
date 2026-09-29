"""
Module de génération des graphiques pour la partie Alimentation Solaire.
Projet PPP Starlink au Service de l'Éducation.
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# DONNÉES
# ============================================================

# Scénarios
scenarios = ['14h/jour', '24h/24']
consommation = [1050, 1800]          # Wh/jour
panneaux = [269, 462]                # Wc
batteries = [1706, 2925]             # Wh
couts = [1242837, 2131350]           # FCFA

# Répartition des coûts (scénario 14h/jour)
postes = ['Panneaux solaires', 'Batteries lithium']
couts_repartition = [48461, 1194375]  # FCFA

# Évolution de la consommation selon les heures d'usage
heures = [8, 10, 12, 14, 16, 18, 20, 22, 24]
conso_heures = [600, 750, 900, 1050, 1200, 1350, 1500, 1650, 1800]


# ============================================================
# GRAPHIQUE 1 : Comparaison des scénarios (coûts)
# ============================================================

def graphique_comparaison_couts():
    plt.figure(figsize=(8, 5))
    bars = plt.bar(scenarios, couts, color=['#2E86AB', '#E63946'])
    plt.title('Comparaison des coûts des scénarios', fontsize=14, fontweight='bold')
    plt.xlabel('Scénario', fontsize=12)
    plt.ylabel('Coût (FCFA)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajouter les valeurs sur les barres
    for bar, cout in zip(bars, couts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50000,
                 f'{cout:,.0f} FCFA', ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('graphique_comparaison_couts.png', dpi=150)
    plt.show()


# ============================================================
# GRAPHIQUE 2 : Répartition des coûts (camembert)
# ============================================================

def graphique_repartition_couts():
    plt.figure(figsize=(8, 6))
    colors = ['#F4A261', '#2A9D8F']
    explode = (0.05, 0.05)

    plt.pie(couts_repartition, labels=postes, autopct='%1.1f%%',
            colors=colors, explode=explode, shadow=True, startangle=90)
    plt.title('Répartition des coûts de l\'installation solaire\n(Scénario 14h/jour)',
              fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('graphique_repartition_couts.png', dpi=150)
    plt.show()


# ============================================================
# GRAPHIQUE 3 : Évolution de la consommation
# ============================================================

def graphique_evolution_consommation():
    plt.figure(figsize=(10, 5))
    plt.plot(heures, conso_heures, marker='o', color='#2E86AB',
             linewidth=2, markersize=8, markerfacecolor='#E63946')
    plt.title('Évolution de la consommation selon les heures d\'usage',
              fontsize=14, fontweight='bold')
    plt.xlabel('Heures d\'utilisation par jour', fontsize=12)
    plt.ylabel('Consommation (Wh/jour)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(heures)

    # Ajouter les valeurs sur les points
    for h, c in zip(heures, conso_heures):
        plt.annotate(f'{c} Wh', (h, c), textcoords="offset points",
                     xytext=(0, 10), ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig('graphique_evolution_consommation.png', dpi=150)
    plt.show()


# ============================================================
# GRAPHIQUE 4 : Dimensionnement des panneaux
# ============================================================

def graphique_dimensionnement_panneaux():
    plt.figure(figsize=(8, 5))
    bars = plt.bar(scenarios, panneaux, color=['#2A9D8F', '#E76F51'])
    plt.title('Dimensionnement des panneaux solaires selon les scénarios',
              fontsize=14, fontweight='bold')
    plt.xlabel('Scénario', fontsize=12)
    plt.ylabel('Puissance panneau (Wc)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, p in zip(bars, panneaux):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 10,
                 f'{p} Wc', ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('graphique_dimensionnement_panneaux.png', dpi=150)
    plt.show()


# ============================================================
# GRAPHIQUE 5 : Dimensionnement des batteries
# ============================================================

def graphique_dimensionnement_batteries():
    plt.figure(figsize=(8, 5))
    bars = plt.bar(scenarios, batteries, color=['#264653', '#E9C46A'])
    plt.title('Dimensionnement des batteries selon les scénarios',
              fontsize=14, fontweight='bold')
    plt.xlabel('Scénario', fontsize=12)
    plt.ylabel('Capacité batterie (Wh)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar, b in zip(bars, batteries):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50,
                 f'{b} Wh', ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('graphique_dimensionnement_batteries.png', dpi=150)
    plt.show()


# ============================================================
# EXÉCUTION DE TOUS LES GRAPHIQUES
# ============================================================

if __name__ == "__main__":
    print("Génération des graphiques...")
    graphique_comparaison_couts()
    graphique_repartition_couts()
    graphique_evolution_consommation()
    graphique_dimensionnement_panneaux()
    graphique_dimensionnement_batteries()
    print("Graphiques générés avec succès !")