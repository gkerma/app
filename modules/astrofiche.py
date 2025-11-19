"""
AstroFiche — Module autonome pour Cyber-Opéra
Version tolérante : fonctionne même sans flatlib/swisseph.

- 12 signes astrodynamiques
- Profil natal par défaut
- Si flatlib + swisseph sont installés : calcul automatique Soleil/Lune/Ascendant
- Sinon : calcul automatique désactivé proprement.
"""

# ============================================================
# 1. IMPORT OPTIONNEL DE FLATLIB / SWISSEPH
# ============================================================

try:
    from flatlib.chart import Chart
    from flatlib import const
    HAS_ASTRO_LIB = True
except Exception:
    Chart = None
    const = None
    HAS_ASTRO_LIB = False

# ============================================================
# 2. BASE DE DONNÉES — 12 SIGNES
# ============================================================

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

# ============================================================
# 3. PROFIL NATAL PAR DÉFAUT
# ============================================================

DEFAULT_NATAL = {
    "soleil": "Gémeaux",
    "lune": "Verseau",
    "ascendant": "Sagittaire",
}

# ============================================================
# 4. CALCUL AUTOMATIQUE DU THÈME NATAL
# ============================================================

def compute_birth_chart(date, time, lat, lon):
    """
    Calcule Soleil / Lune / Ascendant via flatlib si disponible.
    Si la librairie astro n'est pas disponible, renvoie le profil par défaut.
    """
    if not HAS_ASTRO_LIB:
        # Fallback : on retourne juste le profil par défaut
        return DEFAULT_NATAL.copy()

    chart = Chart(date, time, lat, lon)
    return {
        "soleil": chart.get(const.SUN).sign.capitalize(),
        "lune": chart.get(const.MOON).sign.capitalize(),
        "ascendant": chart.get(const.ASC).sign.capitalize(),
    }

# ============================================================
# 5. ACCÈS À UN SIGNE
# ============================================================

def get_sign_data(sign_name):
    return next(s for s in ASTRO_SIGNS if s["name"] == sign_name)

# ============================================================
# 6. RÉSONANCE SUJET ↔ PERSONNAGE
# ============================================================

def compute_resonance(personnage, profil_natal):
    sun = get_sign_data(profil_natal["soleil"])
    moon = get_sign_data(profil_natal["lune"])
    asc  = get_sign_data(profil_natal["ascendant"])

    natal_signs = [sun, moon, asc]

    score = 0
    notes = []

    if personnage["name"] in [s["name"] for s in natal_signs]:
        score += 3
        notes.append("Résonance directe (Soleil, Lune ou Ascendant)")

    if personnage["element"] in [s["element"] for s in natal_signs]:
        score += 2
        notes.append(f"Affinité élémentaire ({personnage['element']})")

    if personnage["mode"] in [s["mode"] for s in natal_signs]:
        score += 1
        notes.append(f"Harmonie modale ({personnage['mode']})")

    oppositions = {"Feu": "Eau", "Eau": "Feu", "Terre": "Air", "Air": "Terre"}
    if oppositions[personnage["element"]] in [s["element"] for s in natal_signs]:
        score -= 1
        notes.append("Tension élémentaire (axe opposé)")

    return score, notes

# ============================================================
# 7. INTERPRÉTATION NARRATIVE
# ============================================================

def interpret_character(personnage, profil_natal, mode="Space Opera total"):
    score, notes = compute_resonance(personnage, profil_natal)

    if mode == "Sobre":
        txt = f"Le personnage du jour est **{personnage['emoji']} {personnage['name']}**.\n\n"
        txt += "Résonances avec ton thème natal :\n"
        for n in notes:
            txt += f"- {n}\n"
        txt += (
            f"\nPouvoir : **{personnage['pouvoir']}**\n"
            f"Fragilité : **{personnage['fragilite']}**"
        )
        return txt

    txt = (
        f"Le **{personnage['emoji']} {personnage['name']}** traverse la scène de ton Opéra intérieur. "
        "Ses signaux résonnent avec ta triade natale :\n\n"
    )
    for n in notes:
        txt += f"- {n}\n"
    txt += "\n"
    txt += (
        f"L’artefact activé est **{personnage['pouvoir']}**, "
        f"tandis que l’ombre **{personnage['fragilite']}** indique la zone d’alchimie du moment."
    )
    return txt
