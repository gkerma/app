"""
AstroFiche — Module autonome pour Cyber-Opéra
Gestion du profil natal, calcul automatique du thème natal,
résonance Sujet ↔ Personnage, et interprétations opératiques.

Dépendances :
    pip install flatlib
"""

from flatlib.chart import Chart
from flatlib import const

# ==============================================
# 1. DONNÉES — 12 SIGNES ASTRODYNAMIQUES
# ==============================================

ASTRO_SIGNS = [
    {
        "name": "Bélier", "emoji": "🔥",
        "element": "Feu", "mode": "Cardinal",
        "clair": "Élan", "ombre": "Impulsivité",
        "pouvoir": "Activation", "fragilite": "Feu trop vite"
    },
    {
        "name": "Taureau", "emoji": "🌿",
        "element": "Terre", "mode": "Fixe",
        "clair": "Stabilité", "ombre": "Inertie",
        "pouvoir": "Ancrage", "fragilite": "Blocage"
    },
    {
        "name": "Gémeaux", "emoji": "🌀",
        "element": "Air", "mode": "Mutable",
        "clair": "Clarté", "ombre": "Dispersion",
        "pouvoir": "Compréhension", "fragilite": "Doute"
    },
    {
        "name": "Cancer", "emoji": "🌙",
        "element": "Eau", "mode": "Cardinal",
        "clair": "Sensibilité", "ombre": "Hypersensibilité",
        "pouvoir": "Protection", "fragilite": "Retrait"
    },
    {
        "name": "Lion", "emoji": "☀️",
        "element": "Feu", "mode": "Fixe",
        "clair": "Rayonnement", "ombre": "Orgueil",
        "pouvoir": "Création", "fragilite": "Besoin de validation"
    },
    {
        "name": "Vierge", "emoji": "🌾",
        "element": "Terre", "mode": "Mutable",
        "clair": "Précision", "ombre": "Suranalyse",
        "pouvoir": "Optimisation", "fragilite": "Perfectionnisme"
    },
    {
        "name": "Balance", "emoji": "⚖️",
        "element": "Air", "mode": "Cardinal",
        "clair": "Harmonie", "ombre": "Indécision",
        "pouvoir": "Diplomatie", "fragilite": "Évitement"
    },
    {
        "name": "Scorpion", "emoji": "🦂",
        "element": "Eau", "mode": "Fixe",
        "clair": "Intensité", "ombre": "Obsession",
        "pouvoir": "Transmutation", "fragilite": "Autodestruction"
    },
    {
        "name": "Sagittaire", "emoji": "🏹",
        "element": "Feu", "mode": "Mutable",
        "clair": "Vision", "ombre": "Exagération",
        "pouvoir": "Expansion", "fragilite": "Fuite"
    },
    {
        "name": "Capricorne", "emoji": "⛰️",
        "element": "Terre", "mode": "Cardinal",
        "clair": "Structure", "ombre": "Rigidité",
        "pouvoir": "Ascension", "fragilite": "Durcissement"
    },
    {
        "name": "Verseau", "emoji": "⚡️",
        "element": "Air", "mode": "Fixe",
        "clair": "Innovation", "ombre": "Froideur",
        "pouvoir": "Projection", "fragilite": "Dissociation"
    },
    {
        "name": "Poissons", "emoji": "🌊",
        "element": "Eau", "mode": "Mutable",
        "clair": "Intuition", "ombre": "Confusion",
        "pouvoir": "Synchronicité", "fragilite": "Brouillard"
    },
]


# =====================================================
# 2. PROFIL NATAL (par défaut, manuel, ou automatique)
# =====================================================

DEFAULT_NATAL = {
    "soleil": "Gémeaux",
    "lune": "Verseau",
    "ascendant": "Sagittaire",
}

def compute_birth_chart(date, time, lat, lon):
    """Calcule Soleil / Lune / Ascendant via Flatlib."""
    chart = Chart(date, time, lat, lon)
    return {
        "soleil": chart.get(const.SUN).sign.capitalize(),
        "lune": chart.get(const.MOON).sign.capitalize(),
        "ascendant": chart.get(const.ASC).sign.capitalize(),
    }


# =====================================================
# 3. ACCÈS AUX SIGNES
# =====================================================

def get_sign_data(sign_name):
    """Retourne la fiche complète d’un signe."""
    return next(s for s in ASTRO_SIGNS if s["name"] == sign_name)


# =====================================================
# 4. RÉSONANCE SUJET ↔ PERSONNAGE
# =====================================================

def compute_resonance(personnage, profil_natal):
    """Analyse la résonance entre le personnage tiré et le thème natal."""
    sun = get_sign_data(profil_natal["soleil"])
    moon = get_sign_data(profil_natal["lune"])
    asc = get_sign_data(profil_natal["ascendant"])

    natal_signs = [sun, moon, asc]

    score = 0
    notes = []

    # Résonance directe
    if personnage["name"] in [s["name"] for s in natal_signs]:
        score += 3
        notes.append("Résonance directe avec ton Soleil, ta Lune ou ton Ascendant")

    # Résonance élémentaire
    if personnage["element"] in [s["element"] for s in natal_signs]:
        score += 2
        notes.append(f"Résonance élémentaire ({personnage['element']})")

    # Résonance modale
    if personnage["mode"] in [s["mode"] for s in natal_signs]:
        score += 1
        notes.append(f"Résonance modale ({personnage['mode']})")

    # Opposition élémentaire
    oppositions = {"Feu": "Eau", "Eau": "Feu", "Terre": "Air", "Air": "Terre"}
    if oppositions[personnage["element"]] in [s["element"] for s in natal_signs]:
        score -= 1
        notes.append("Tension élémentaire (activation par contraste)")

    return score, notes


# =====================================================
# 5. INTERPRÉTATION SUJET ↔ PERSONNAGE
# =====================================================

def interpret_character(personnage, profil_natal, mode="Sobre"):
    """Interprétation narrative selon tonalité."""
    score, notes = compute_resonance(personnage, profil_natal)

    if mode == "Sobre":
        txt = (
            f"Le personnage du jour est **{personnage['emoji']} {personnage['name']}**.\n\n"
            f"Résonances avec ton thème natal :\n"
        )
        for n in notes:
            txt += f"- {n}\n"
        txt += "\n"
        txt += (
            f"Pouvoir activé : **{personnage['pouvoir']}**.\n"
            f"Fragilité sollicitée : **{personnage['fragilite']}**.\n"
        )
        return txt

    # Mode Space Opera total
    txt = (
        f"Le **{personnage['emoji']} {personnage['name']}** traverse aujourd’hui la scène cosmique intérieure. "
        "Il projette ses résonances dans les fibres secrètes de ton thème natal :\n\n"
    )
    for n in notes:
        txt += f"- {n}\n"
    txt += "\n"
    txt += (
        f"L’artefact qu'il t’offre est **{personnage['pouvoir']}**. "
        f"Dans son ombre danse **{personnage['fragilite']}**, fragment à alchimiser.\n"
    )
    return txt
