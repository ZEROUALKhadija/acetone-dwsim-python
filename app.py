import math
import matplotlib.pyplot as plt


# ============================================================
# SIMULATION D'UN PROCEDE DE VAPORISATION DE L'ACETONE
# Modèle : Loi de Raoult
# ============================================================


# ============================================================
# 1. DONNEES D'ENTREE
# ============================================================

debit_entree = 38.0              # kg/h
temperature_entree = 10.0        # °C
pression_entree = 1.0            # atm

fraction_haut = 0.40             # 40 %
fraction_chauffe = 0.60          # 60 %


# ============================================================
# 2. PROPRIETES APPROXIMATIVES DE L'ACETONE
# ============================================================

Cp_liquide = 2.15                # kJ/(kg.K)
delta_H_vap = 518.0              # kJ/kg


# ============================================================
# 3. CONSTANTES D'ANTOINE POUR L'ACETONE
#
# log10(Psat) = A - B / (T + C)
#
# Psat : mmHg
# T    : °C
# ============================================================

A = 7.02447
B = 1161.0
C = 224.0


# ============================================================
# 4. FONCTION DE PRESSION DE VAPEUR SATURANTE
# ============================================================

def pression_saturation(T_C):

    Psat_mmhg = 10 ** (
        A - B / (T_C + C)
    )

    Psat_atm = Psat_mmhg / 760.0

    return Psat_atm


# ============================================================
# 5. FONCTION DE TEMPERATURE D'EBULLITION
#
# Loi de Raoult :
#
# P = x * Psat
#
# Pour l'acétone pure :
#
# x = 1
#
# donc :
#
# P = Psat
# ============================================================

def temperature_ebullition(pression_atm):

    # Fraction molaire de l'acétone
    x_acetone = 1.0

    # Pression de vapeur saturante nécessaire
    Psat_atm = pression_atm / x_acetone

    # Conversion atm -> mmHg
    Psat_mmhg = Psat_atm * 760.0

    # Equation d'Antoine inversée
    T_C = B / (
        A - math.log10(Psat_mmhg)
    ) - C

    # Conversion °C -> K
    T_K = T_C + 273.15

    return T_C, T_K


# ============================================================
# 6. SEPARATION DU DEBIT
# ============================================================

debit_haut = debit_entree * fraction_haut

debit_chauffe = debit_entree * fraction_chauffe


# ============================================================
# 7. TEMPERATURE D'EBULLITION A 1 ATM
# ============================================================

T_eb_C, T_eb_K = temperature_ebullition(
    pression_entree
)


# ============================================================
# 8. CALCUL DE L'ENERGIE
# ============================================================

# Energie nécessaire pour chauffer le liquide

delta_T = T_eb_C - temperature_entree

Q_chauffage = (
    debit_chauffe
    * Cp_liquide
    * delta_T
)


# Energie nécessaire pour vaporiser

Q_vaporisation = (
    debit_chauffe
    * delta_H_vap
)


# Energie totale

Q_total = (
    Q_chauffage
    + Q_vaporisation
)


# Conversion kJ/h -> kW

Q_kW = Q_total / 3600.0


# ============================================================
# 9. AFFICHAGE DES RESULTATS PRINCIPAUX
# ============================================================

print()

print("=" * 70)
print("          SIMULATION DU PROCEDE - ACETONE")
print("             MODELE : LOI DE RAOULT")
print("=" * 70)


# ------------------------------------------------------------
# CONDITIONS D'ENTREE
# ------------------------------------------------------------

print()
print("1. CONDITIONS D'ENTREE")
print("-" * 70)

print(
    f"Débit d'entrée              : "
    f"{debit_entree:.2f} kg/h"
)

print(
    f"Température d'entrée        : "
    f"{temperature_entree:.2f} °C"
)

print(
    f"Pression d'entrée           : "
    f"{pression_entree:.2f} atm"
)


# ------------------------------------------------------------
# SEPARATION
# ------------------------------------------------------------

print()
print("2. SEPARATION")
print("-" * 70)

print(
    f"Fraction supérieure         : "
    f"{fraction_haut * 100:.0f} %"
)

print(
    f"Débit supérieur             : "
    f"{debit_haut:.2f} kg/h"
)

print(
    f"Fraction vers le heater     : "
    f"{fraction_chauffe * 100:.0f} %"
)

print(
    f"Débit vers le heater        : "
    f"{debit_chauffe:.2f} kg/h"
)


# ------------------------------------------------------------
# EQUILIBRE LIQUIDE-VAPEUR
# ------------------------------------------------------------

print()
print("3. EQUILIBRE LIQUIDE-VAPEUR")
print("-" * 70)

print(
    "Modèle thermodynamique     : Loi de Raoult"
)

print(
    "Composé                    : Acétone"
)

print(
    "Fraction molaire acétone   : 1.000"
)

print(
    f"Température d'ébullition   : "
    f"{T_eb_C:.2f} °C"
)

print(
    f"Température d'ébullition   : "
    f"{T_eb_K:.2f} K"
)


# ------------------------------------------------------------
# BILAN ENERGETIQUE
# ------------------------------------------------------------

print()
print("4. BILAN ENERGETIQUE DU HEATER")
print("-" * 70)

print(
    f"Chauffage du liquide       : "
    f"{Q_chauffage:.2f} kJ/h"
)

print(
    f"Vaporisation               : "
    f"{Q_vaporisation:.2f} kJ/h"
)

print(
    f"Energie totale             : "
    f"{Q_total:.2f} kJ/h"
)

print(
    f"Puissance thermique        : "
    f"{Q_kW:.2f} kW"
)


# ============================================================
# 10. TABLEAU DES 25 POINTS
# ============================================================

nombre_points = 25

pression_min = 0.1
pression_max = 3.0


# Création des pressions

pressions = []

for i in range(nombre_points):

    P = (
        pression_min
        + i * (
            pression_max - pression_min
        )
        / (nombre_points - 1)
    )

    pressions.append(P)


# ============================================================
# 11. CALCUL DES TEMPERATURES
# ============================================================

temperatures_C = []
temperatures_K = []


for P in pressions:

    T_C, T_K = temperature_ebullition(P)

    temperatures_C.append(T_C)
    temperatures_K.append(T_K)


# ============================================================
# 12. AFFICHAGE DU TABLEAU
# ============================================================

print()

print("=" * 75)
print("       TABLEAU PRESSION - TEMPERATURE D'EBULLITION")
print("=" * 75)

print(
    f"{'Point':<8}"
    f"{'Pression (atm)':<20}"
    f"{'T (°C)':<18}"
    f"{'T (K)':<18}"
)

print("-" * 75)


for i in range(nombre_points):

    P = pressions[i]

    T_C = temperatures_C[i]

    T_K = temperatures_K[i]

    print(
        f"{i + 1:<8}"
        f"{P:<20.4f}"
        f"{T_C:<18.2f}"
        f"{T_K:<18.2f}"
    )


print("=" * 75)


# ============================================================
# 13. SAUVEGARDE DU TABLEAU
# ============================================================

with open(
    "tableau_pression_temperature.txt",
    "w",
    encoding="utf-8"
) as fichier:

    fichier.write(
        "TABLEAU PRESSION - TEMPERATURE D'EBULLITION\n"
    )

    fichier.write(
        "Acétone - Loi de Raoult\n"
    )

    fichier.write(
        "=" * 70 + "\n"
    )

    fichier.write(
        f"{'Point':<8}"
        f"{'Pression (atm)':<20}"
        f"{'T (°C)':<18}"
        f"{'T (K)':<18}\n"
    )

    fichier.write(
        "-" * 70 + "\n"
    )

    for i in range(nombre_points):

        P = pressions[i]

        T_C = temperatures_C[i]

        T_K = temperatures_K[i]

        fichier.write(
            f"{i + 1:<8}"
            f"{P:<20.4f}"
            f"{T_C:<18.2f}"
            f"{T_K:<18.2f}\n"
        )


# ============================================================
# 14. TRACE DE LA COURBE EN KELVIN
# ============================================================

plt.figure(figsize=(9, 6))


plt.plot(
    pressions,
    temperatures_K,
    marker="o",
    linewidth=1.5
)


# Point à 1 atm

plt.scatter(
    [pression_entree],
    [T_eb_K],
    s=80,
    zorder=5,
    label=f"1 atm : {T_eb_K:.2f} K"
)


# Axes

plt.xlabel(
    "Pression (atm)"
)

plt.ylabel(
    "Température d'ébullition (K)"
)


# Titre

plt.title(
    "Température d'ébullition de l'acétone\n"
    "en fonction de la pression"
)


# Grille

plt.grid(True)


# Légende

plt.legend()


# Mise en page

plt.tight_layout()


# Sauvegarde

plt.savefig(
    "courbe_temperature_pression_K.png",
    dpi=300
)


# Affichage

plt.show()


# ============================================================
# 15. SCHEMA DU PROCEDE
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 6)
)

ax.set_xlim(0, 12)
ax.set_ylim(0, 6)

ax.axis("off")


# ------------------------------------------------------------
# ALIMENTATION
# ------------------------------------------------------------

ax.text(
    1,
    3,
    "ALIMENTATION\n\n"
    "Acétone\n"
    "38 kg/h\n"
    "10 °C\n"
    "1 atm",
    ha="center",
    va="center",
    fontsize=10,
    bbox=dict(
        boxstyle="round,pad=0.5",
        fill=False
    )
)


# ------------------------------------------------------------
# FLECHE ALIMENTATION
# ------------------------------------------------------------

ax.annotate(
    "",
    xy=(3, 3),
    xytext=(1.7, 3),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)


# ------------------------------------------------------------
# SEPARATEUR
# ------------------------------------------------------------

ax.add_patch(
    plt.Rectangle(
        (3, 2),
        2,
        2,
        fill=False,
        linewidth=2
    )
)

ax.text(
    4,
    3,
    "SÉPARATEUR",
    ha="center",
    va="center",
    fontsize=10
)


# ------------------------------------------------------------
# FLUX 40 %
# ------------------------------------------------------------

ax.annotate(
    "",
    xy=(6.5, 4.7),
    xytext=(5, 3.5),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

ax.text(
    5.7,
    4.5,
    "40 %\n15.2 kg/h",
    ha="center",
    va="center"
)


# ------------------------------------------------------------
# FLUX 60 %
# ------------------------------------------------------------

ax.annotate(
    "",
    xy=(6.5, 1.5),
    xytext=(5, 2.5),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

ax.text(
    5.7,
    1.5,
    "60 %\n22.8 kg/h",
    ha="center",
    va="center"
)


# ------------------------------------------------------------
# HEATER
# ------------------------------------------------------------

ax.add_patch(
    plt.Rectangle(
        (6.5, 0.7),
        2.2,
        1.6,
        fill=False,
        linewidth=2
    )
)

ax.text(
    7.6,
    1.5,
    f"HEATER\n"
    f"Q = {Q_kW:.2f} kW",
    ha="center",
    va="center",
    fontsize=10
)


# ------------------------------------------------------------
# SORTIE VAPEUR
# ------------------------------------------------------------

ax.annotate(
    "",
    xy=(10.8, 1.5),
    xytext=(8.7, 1.5),
    arrowprops=dict(
        arrowstyle="->",
        linewidth=2
    )
)

ax.text(
    9.8,
    2.1,
    f"VAPEUR D'ACÉTONE\n"
    f"T = {T_eb_K:.2f} K",
    ha="center",
    va="center",
    fontsize=10
)


# ------------------------------------------------------------
# TITRE
# ------------------------------------------------------------

ax.set_title(
    "Schéma simplifié du procédé de séparation "
    "et vaporisation",
    fontsize=14
)


plt.tight_layout()


# Sauvegarde du schéma

plt.savefig(
    "schema_procede_acetone.png",
    dpi=300
)


plt.show()


# ============================================================
# 16. FICHIER RECAPITULATIF
# ============================================================

with open(
    "resultats.txt",
    "w",
    encoding="utf-8"
) as fichier:

    fichier.write(
        "SIMULATION DU PROCEDE - ACETONE\n"
    )

    fichier.write(
        "Modèle : Loi de Raoult\n\n"
    )

    fichier.write(
        f"Débit entrée : "
        f"{debit_entree:.2f} kg/h\n"
    )

    fichier.write(
        f"T entrée : "
        f"{temperature_entree:.2f} °C\n"
    )

    fichier.write(
        f"P entrée : "
        f"{pression_entree:.2f} atm\n\n"
    )

    fichier.write(
        f"Débit 40 % : "
        f"{debit_haut:.2f} kg/h\n"
    )

    fichier.write(
        f"Débit 60 % : "
        f"{debit_chauffe:.2f} kg/h\n\n"
    )

    fichier.write(
        f"T ébullition : "
        f"{T_eb_C:.2f} °C\n"
    )

    fichier.write(
        f"T ébullition : "
        f"{T_eb_K:.2f} K\n\n"
    )

    fichier.write(
        f"Q chauffage : "
        f"{Q_chauffage:.2f} kJ/h\n"
    )

    fichier.write(
        f"Q vaporisation : "
        f"{Q_vaporisation:.2f} kJ/h\n"
    )

    fichier.write(
        f"Q total : "
        f"{Q_total:.2f} kJ/h\n"
    )

    fichier.write(
        f"Puissance thermique : "
        f"{Q_kW:.2f} kW\n"
    )


# ============================================================
# 17. FIN
# ============================================================

print()

print("=" * 70)
print("                    FIN DE LA SIMULATION")
print("=" * 70)

print()

print("Fichiers créés :")

print(
    "  1. tableau_pression_temperature.txt"
)

print(
    "  2. courbe_temperature_pression_K.png"
)

print(
    "  3. schema_procede_acetone.png"
)

print(
    "  4. resultats.txt"
)

print()

print(
    "La température de la courbe est exprimée en Kelvin."
)