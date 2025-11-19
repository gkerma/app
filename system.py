# ============================================================
# CYBER-OPERA — VERSION ASTROFICHE (Code optimisé)
# Fichier principal : app.py
# Dépendance externe : modules/astrofiche.py
# ============================================================

import streamlit as st
import random
from datetime import datetime
from collections import Counter
import pandas as pd
from modules.astrofiche import HAS_ASTRO_LIB

# Import du module astrofiche
from modules.astrofiche import (
    ASTRO_SIGNS,
    DEFAULT_NATAL,
    compute_birth_chart,
    get_sign_data,
    compute_resonance,
    interpret_character
)

# ============================================================
# CONFIG STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Cyber-Opéra — Génératif",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# UI STYLES
# ============================================================

st.markdown(
    """
    <style>
    body {
        font-family: 'Inter', sans-serif;
    }
    .cyber-title {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ff6ec7, #00f5ff);
        -webkit-background-clip: text;
        color: transparent;
        letter-spacing: 0.08em;
        margin-top: 0rem;
        margin-bottom: 0.25rem;
    }
    .cyber-subtitle {
        text-align: center;
        font-size: 0.95rem;
        opacity: 0.75;
        margin-bottom: 1.8rem;
    }
    .card {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        border: 1px solid rgba(255,255,255,0.08);
        background: radial-gradient(circle at top left, rgba(255,255,255,0.05), rgba(0,0,0,0.65));
        box-shadow: 0 12px 36px rgba(0,0,0,0.25);
        margin-bottom: 0.8rem;
    }
    .mini-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        opacity: 0.6;
        letter-spacing: 0.18em;
        margin-bottom: 0.35rem;
    }

@media (max-width: 900px) {

    /* Réduction des titres */
    .cyber-title {
        font-size: 1.8rem !important;
    }

    .cyber-subtitle {
        font-size: 0.8rem !important;
    }

    /* Cartes : marges adaptées */
    .card {
        padding: 0.8rem !important;
        margin-bottom: 1rem !important;
    }

    /* Colonnes empilées automatiquement */
    .block-container {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Scroll horizontal pour large tableaux */
    .dataframe {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }

    /* Inputs compactés */
    input, select, textarea {
        font-size: 0.9rem !important;
    }

    /* Réduction des espacements */
    h3 {
        font-size: 1.2rem !important;
    }
}

</style>

    """,
    unsafe_allow_html=True,
)

# HEADER
st.markdown("<div class='cyber-title'>Cyber-Opéra</div>", unsafe_allow_html=True)
st.markdown("<div class='cyber-subtitle'>Navigation symbolique + Moteur astrologique</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# 1. SYSTÈME CYBER-OPÉRA (hors astrologie)
# ------------------------------------------------------------

SPHERES = [
    "Amour 💗", "Boulot 🛰️", "Corps 🦴", "Développement 📚",
    "Expression 🎙️", "Flow Créatif 🎨", "Générosité 🎁",
    "Habitat 🏠", "Intelligence ♟️", "Joie 🌞",
    "Karma 🜃", "Lien social 🤝"
]

FEUX = [
    "Étincelle ✨",
    "Flamme 🔥",
    "Brasier 🔥🔥",
    "Cendre 🕯️",
    "Phoenix 🐦‍🔥"
]

FAMILLES = [
    {"name": "Action", "motto": "produire", "hint": "Fais avancer quelque chose aujourd’hui.", "emoji": "⚙️"},
    {"name": "Pause", "motto": "ressentir", "hint": "Quelques minutes de silence changent la scène.", "emoji": "🌫️"},
    {"name": "Combat", "motto": "trancher", "hint": "Une limite. Une décision.", "emoji": "🗡️"},
    {"name": "Initiation", "motto": "transformer", "hint": "Fais une petite chose nouvelle.", "emoji": "🜇"},
    {"name": "Chaos", "motto": "bousculer", "hint": "Inverse l’ordre, casse la routine.", "emoji": "☄️"}
]

DEFAUTS = [
    "dispersion", "anxiété", "froideur", "procrastination",
    "confusion", "fatigue", "jalousie", "pression",
    "fatigue du corps", "surcharge", "blocage d'expression",
    "chaos créatif", "fuite", "désordre", "suranalyse",
    "vide intérieur", "errance", "isolement",
    "brûler trop vite", "feu sans direction",
    "étouffé par émotions", "dispersé par mental",
    "refroidi par détachement"
]

# ------------------------------------------------------------
# 2. ARCANES OPÉRATIQUES (Cycle mensuel)
# ------------------------------------------------------------

ARCANES = [
    {"name": "Le Portail", "emoji": "🜄", "theme": "passage, seuil, nouvelle phase"},
    {"name": "Le Miroir", "emoji": "🪞", "theme": "reflet, conscience de soi"},
    {"name": "La Tour Data", "emoji": "🛰️", "theme": "structure, réseau, système"},
    {"name": "Le Flux", "emoji": "🌊", "theme": "mouvement, lâcher-prise"},
    {"name": "L’Astre Noir", "emoji": "🌑", "theme": "inconscient, incubation"},
    {"name": "Le Pont", "emoji": "🌉", "theme": "liaison, médiation"},
    {"name": "Le Masque", "emoji": "🎭", "theme": "persona, jeu social"},
    {"name": "Le Grimoire", "emoji": "📜", "theme": "mémoire, archives"},
    {"name": "La Spirale", "emoji": "🌀", "theme": "cycles, répétition créatrice"},
    {"name": "Le Cœur Quantique", "emoji": "💗", "theme": "lien profond, amour"},
]

# ------------------------------------------------------------
# 3. SESSION STATE — INITIALISATION
# ------------------------------------------------------------

STATE_DEFAULTS = {
    "tone_mode": "Space Opera total",
    "triade": None,
    "sphere": None,
    "feu": None,
    "famille": None,
    "scene": None,
    "journal_intention": "",
    "journal_synchro": "",
    "journal_micro": "",
    "scene_interpretation": "",
    "space_history": [],
    "month_cycle": None,
    "month_cycle_notes": {},
    "natal_profile": DEFAULT_NATAL.copy()
}

for key, val in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ------------------------------------------------------------
# 4. FONCTIONS UTILITAIRES
# ------------------------------------------------------------

def pick(lst):
    return random.choice(lst)

def generate_scene():
    """Scène = Personnage astro + Sphère + Feu + Famille + Défaut."""
    return {
        "personnage": pick(ASTRO_SIGNS),
        "sphere": pick(SPHERES),
        "feu": pick(FEUX),
        "famille": pick(FAMILLES),
        "defaut": pick(DEFAUTS)
    }

def generate_month_cycle(days=30):
    """Cycle mensuel = arcane + sphère + feu + défaut + personnage du jour."""
    cycle = []
    for i in range(days):
        cycle.append({
            "jour": i + 1,
            "arcane": pick(ARCANES),
            "sphere": pick(SPHERES),
            "feu": pick(FEUX),
            "defaut": pick(DEFAUTS),
            "personnage": pick(ASTRO_SIGNS)
        })
    return cycle

# ------------------------------------------------------------
# 5. INTERPRÉTATIONS CYBER-OPÉRA
# ------------------------------------------------------------

def interpret_daily(tri, sphere, feu, fam, mode):
    """Interprétation non-astro du tirage quotidien."""
    if mode == "Sobre":
        return (
            f"Ton fonctionnement du jour s'appuie sur **{tri}**.\n"
            f"Sphère clé : **{sphere}**.\n"
            f"Feu : **{feu}**.\n"
            f"Famille : **{fam['name']}** (motto : {fam['motto']})."
        )
    return (
        f"Le Cyber-Opéra ouvre un acte où **{tri}** joue en toi. "
        f"Le décor énergétique s'installe dans **{sphere}**, projeté sous la lumière du feu **{feu}**. "
        f"La famille **{fam['emoji']} {fam['name']}** orchestre la vibration du jour."
    )

def interpret_cycle_day(day):
    """Interprétation non-astro d'un jour du cycle."""
    arc = day["arcane"]
    return (
        f"L'arcane du jour est **{arc['emoji']} {arc['name']}** (*{arc['theme']}*).\n"
        f"Sphère active : **{day['sphere']}**.\n"
        f"Feu : **{day['feu']}**.\n"
        f"Défaut : **{day['defaut']}**."
    )

# ============================================================
# BLOC 3 — ONGLET PROFIL NATAL & TRIADE SUJET
# ============================================================

# Onglets généraux
tab_profile, tab_daily, tab_scene, tab_history, tab_cycle, tab_stats = st.tabs([
    "♒ Profil natal & Triade Sujet",
    "🌓 Tirage quotidien",
    "🎭 Scène opératique",
    "📚 Historique",
    "🗓️ Cycle mensuel",
    "📊 Stats & Grimoire"
])

# ============================================================
# ONGLET PROFIL NATAL
# ============================================================
with tab_profile:

    st.subheader("♒ Profil natal — Sujet de l’Opéra intérieur")

    natal = st.session_state.natal_profile
    sign_names = [s["name"] for s in ASTRO_SIGNS]

    # --------------------------------------------------------
    # 1. AFFICHAGE
    # --------------------------------------------------------
    colA, colB, colC = st.columns(3)

    with colA:
        sun = get_sign_data(natal["soleil"])
        st.markdown(
            f"""
            <div class="card">
                <div class="mini-label">SOLEIL</div>
                <h3>{sun['emoji']} {sun['name']}</h3>
                <p><b>Élément :</b> {sun['element']}</p>
                <p><b>Mode :</b> {sun['mode']}</p>
                <p><b>Pouvoir :</b> {sun['pouvoir']}</p>
                <p><b>Fragilité :</b> {sun['fragilite']}</p>
            </div>
            """, unsafe_allow_html=True
        )

    with colB:
        moon = get_sign_data(natal["lune"])
        st.markdown(
            f"""
            <div class="card">
                <div class="mini-label">LUNE</div>
                <h3>{moon['emoji']} {moon['name']}</h3>
                <p><b>Élément :</b> {moon['element']}</p>
                <p><b>Mode :</b> {moon['mode']}</p>
                <p><b>Pouvoir :</b> {moon['pouvoir']}</p>
                <p><b>Fragilité :</b> {moon['fragilite']}</p>
            </div>
            """, unsafe_allow_html=True
        )

    with colC:
        asc = get_sign_data(natal["ascendant"])
        st.markdown(
            f"""
            <div class="card">
                <div class="mini-label">ASCENDANT</div>
                <h3>{asc['emoji']} {asc['name']}</h3>
                <p><b>Élément :</b> {asc['element']}</p>
                <p><b>Mode :</b> {asc['mode']}</p>
                <p><b>Pouvoir :</b> {asc['pouvoir']}</p>
                <p><b>Fragilité :</b> {asc['fragilite']}</p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # 2. FORMULAIRE — MISE À JOUR MANUELLE
    # --------------------------------------------------------
    st.markdown("### Modifier ton profil natal")

    col1, col2, col3 = st.columns(3)

    with col1:
        new_sun = st.selectbox(
            "Signe solaire",
            sign_names,
            index=sign_names.index(natal["soleil"])
        )

    with col2:
        new_moon = st.selectbox(
            "Signe lunaire",
            sign_names,
            index=sign_names.index(natal["lune"])
        )

    with col3:
        new_asc = st.selectbox(
            "Ascendant",
            sign_names,
            index=sign_names.index(natal["ascendant"])
        )

    if st.button("Enregistrer ce profil natal"):
        st.session_state.natal_profile = {
            "soleil": new_sun,
            "lune": new_moon,
            "ascendant": new_asc
        }
        st.success("Profil mis à jour.")

    st.markdown("---")

    # --------------------------------------------------------
    # 3. FORMULAIRE — CALCUL AUTOMATIQUE
    # --------------------------------------------------------
    st.markdown("### Calcul automatique (date, heure, lieu)")

    colD, colE, colF = st.columns(3)

    with colD:
        date_naiss = st.date_input("Date de naissance")

    with colE:
        heure_naiss = st.time_input("Heure de naissance")

    with colF:
        st.write("Coordonnées du lieu :")
        lat = st.number_input("Latitude", value=48.8566, format="%.6f")
        lon = st.number_input("Longitude", value=2.3522, format="%.6f")

    if st.button("Calculer thème natal"):
        nat = compute_birth_chart(
            date_naiss.strftime("%Y/%m/%d"),
            heure_naiss.strftime("%H:%M"),
            str(lat),
            str(lon)
        )
        st.session_state.natal_profile = nat
        st.success("Profil natal automatiquement calculé.")

    st.markdown("---")

    # --------------------------------------------------------
    # 4. SYNTHÈSE "FICHE SUJET"
    # --------------------------------------------------------

    st.markdown("## Fiche Sujet — Synthèse opératique")

    def synthese_sujet():
        e = [sun["element"], moon["element"], asc["element"]]
        m = [sun["mode"], moon["mode"], asc["mode"]]

        elem_dom = max(set(e), key=e.count)
        mode_dom  = max(set(m), key=m.count)

        return (
            f"Ton sujet intérieur est structuré autour de l’élément **{elem_dom}** "
            f"et du mode **{mode_dom}**. "
            "C’est la signature essentielle de ta triade natale."
        )

    st.markdown(
        f"""
        <div class="card">
            <p>{synthese_sujet()}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# Fin du Bloc 3
# ============================================================
# ============================================================
# BLOC 4 — TIRAGE QUOTIDIEN + SCÈNE OPÉRATIQUE
# ============================================================

# ========================
# TIRAGE QUOTIDIEN
# ========================
with tab_daily:

    st.subheader("🌓 Tirage quotidien")

    # Bouton
    if st.button("✨ Effectuer le tirage quotidien"):
        triade = pick([s["name"] for s in ASTRO_SIGNS])
        st.session_state.triade = triade
        st.session_state.sphere = pick(SPHERES)
        st.session_state.feu = pick(FEUX)
        st.session_state.famille = pick(FAMILLES)

        # Personnage astrodynamique (signe du jour)
        st.session_state.personnage_q = next(
            s for s in ASTRO_SIGNS if s["name"] == triade
        )

        # Interprétation classique
        interp = interpret_daily(
            triade,
            st.session_state.sphere,
            st.session_state.feu,
            st.session_state.famille,
            st.session_state.tone_mode
        )
        st.session_state.daily_interpretation = interp

        # Interprétation Sujet ↔ Personnage
        interp_astro = interpret_character(
            st.session_state.personnage_q,
            st.session_state.natal_profile,
            mode=st.session_state.tone_mode
        )
        st.session_state.daily_interpretation_astro = interp_astro

    # Affichage
    if st.session_state.triade:

        col1, col2 = st.columns(2)

        with col1:
            p = st.session_state.personnage_q
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">PERSONNAGE ASTRO</div>
                    <h3>{p['emoji']} {p['name']}</h3>
                    <p><b>Élément :</b> {p['element']}</p>
                    <p><b>Mode :</b> {p['mode']}</p>
                    <p><b>Pouvoir :</b> {p['pouvoir']}</p>
                    <p><b>Fragilité :</b> {p['fragilite']}</p>
                </div>
                """, unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FEU</div>
                    <h3>{st.session_state.feu}</h3>
                </div>
                """, unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SPHÈRE</div>
                    <h3>{st.session_state.sphere}</h3>
                </div>
                """, unsafe_allow_html=True
            )

            fam = st.session_state.famille
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FAMILLE</div>
                    <h3>{fam['emoji']} {fam['name']}</h3>
                    <p>Motto : {fam['motto']}</p>
                    <p>{fam['hint']}</p>
                </div>
                """, unsafe_allow_html=True
            )

        st.markdown("### 🧠 Interprétation (Cyber-Opéra)")
        st.markdown(st.session_state.daily_interpretation)

        st.markdown("### ✧ Résonance Sujet ↔ Personnage")
        st.markdown(st.session_state.daily_interpretation_astro)

# ========================
# SCÈNE OPÉRATIQUE
# ========================
with tab_scene:

    st.subheader("🎭 Scène opératique — 5 cartes")

    if st.button("🎭 Générer une Scène"):
        scene = generate_scene()
        st.session_state.scene = scene

        # Interprétation Sujet ↔ Personnage
        st.session_state.scene_astro = interpret_character(
            scene["personnage"],
            st.session_state.natal_profile,
            mode=st.session_state.tone_mode
        )

        # Interprétation classique
        base = (
            f"Rôle intérieur : {scene['personnage']['emoji']} {scene['personnage']['name']}.\n"
            f"Sphère dominante : {scene['sphere']}.\n"
            f"Feu : {scene['feu']}.\n"
            f"Famille : {scene['famille']['emoji']} {scene['famille']['name']}.\n"
            f"Défaut à transmuter : {scene['defaut']}."
        )
        st.session_state.scene_interpretation = base

        # Historique automatique
        st.session_state.space_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "scene": scene,
            "interp": base,
            "interp_astro": st.session_state.scene_astro,
            "tone": st.session_state.tone_mode
        })

        # Reset journal
        st.session_state.journal_intention = ""
        st.session_state.journal_synchro = ""
        st.session_state.journal_micro = ""

    # Affichage
    if st.session_state.scene:

        scene = st.session_state.scene
        p = scene["personnage"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">PERSONNAGE</div>
                    <h3>{p['emoji']} {p['name']}</h3>
                    <p>Élément : {p['element']}</p>
                    <p>Mode : {p['mode']}</p>
                    <p>Pouvoir : {p['pouvoir']}</p>
                    <p>Fragilité : {p['fragilite']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FEU</div>
                    <h3>{scene['feu']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SPHÈRE</div>
                    <h3>{scene['sphere']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            fam = scene["famille"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FAMILLE</div>
                    <h3>{fam['emoji']} {fam['name']}</h3>
                    <p>Motto : {fam['motto']}</p>
                    <p>{fam['hint']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">DÉFAUT À TRANSMUTER</div>
                    <h3>🜁 {scene['defaut']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------
        # Journal
        # -------------------------
        st.markdown("### 📓 Journal Opéra")

        st.session_state.journal_intention = st.text_area(
            "Intention",
            value=st.session_state.journal_intention
        )
        st.session_state.journal_synchro = st.text_area(
            "Synchronicité",
            value=st.session_state.journal_synchro
        )
        st.session_state.journal_micro = st.text_area(
            "Micro-victoire",
            value=st.session_state.journal_micro
        )

        # -------------------------
        # Interprétations
        # -------------------------
        st.markdown("### 🧠 Interprétation (Cyber-Opéra)")
        st.markdown(st.session_state.scene_interpretation)

        st.markdown("### ✧ Résonance Sujet ↔ Personnage")
        st.markdown(st.session_state.scene_astro)

# ============================================================
# Fin du Bloc 4
# ============================================================
# ============================================================
# BLOC 5 — CYCLE MENSUEL + MICRO-ORACLES + EXPORTS
# ============================================================

with tab_cycle:

    st.subheader("🗓️ Cycle mensuel — 30 jours opératiques")

    # ------------------------------
    # 1. Génération du cycle
    # ------------------------------
    if st.button("🜂 Générer un cycle mensuel complet"):
        cycle = generate_month_cycle(days=30)
        st.session_state.month_cycle = cycle

        # Interprétations automatiques (classique + astro)
        notes = {}
        for day in cycle:
            interp_classic = interpret_cycle_day(day)
            interp_astro = interpret_character(
                day["personnage"],
                st.session_state.natal_profile,
                mode=st.session_state.tone_mode
            )
            notes[day["jour"]] = {
                "classic": interp_classic,
                "astro": interp_astro
            }
        st.session_state.month_cycle_notes = notes

        st.success("Cycle mensuel généré.")

    # ------------------------------
    # 2. Affichage du cycle
    # ------------------------------
    if st.session_state.month_cycle:

        cycle = st.session_state.month_cycle
        notes = st.session_state.month_cycle_notes

        jours = [d["jour"] for d in cycle]
        choix = st.selectbox("Sélectionner un jour :", jours)

        day = next(d for d in cycle if d["jour"] == choix)
        n = notes[choix]

        colA, colB = st.columns(2)

        # Affichage du signe + triade
        with colA:
            p = day["personnage"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">PERSONNAGE DU JOUR</div>
                    <h3>{p['emoji']} {p['name']}</h3>
                    <p>Élément : {p['element']}</p>
                    <p>Mode : {p['mode']}</p>
                    <p>Pouvoir : {p['pouvoir']}</p>
                    <p>Fragilité : {p['fragilite']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Affichage du reste
        with colB:
            arc = day["arcane"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">ARCANE</div>
                    <h3>{arc['emoji']} {arc['name']}</h3>
                    <p>{arc['theme']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SPHÈRE</div>
                    <h3>{day['sphere']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FEU</div>
                    <h3>{day['feu']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">DÉFAUT</div>
                    <h3>🜁 {day['defaut']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 🧠 Interprétation (Cyber-Opéra)")
        st.markdown(n["classic"])

        st.markdown("### ✧ Résonance Sujet ↔ Personnage")
        st.markdown(n["astro"])

        # ------------------------------
        # 3. Export Markdown du jour
        # ------------------------------
        md_day = f"""# Jour {day['jour']} — Cyber-Opéra
## Personnage : {p['emoji']} {p['name']}
### Interprétation Sujet ↔ Personnage
{n['astro']}

### Interprétation Cyber-Opéra
{n['classic']}

### Sphère
{day['sphere']}

### Feu
{day['feu']}

### Défaut
{day['defaut']}

### Arcane
{arc['emoji']} {arc['name']} — {arc['theme']}
"""

        st.download_button(
            "📄 Exporter ce jour en Markdown",
            md_day,
            file_name=f"cyber-opera-jour-{day['jour']}.md"
        )

    st.markdown("---")

    # ------------------------------
    # 4. Export du cycle complet
    # ------------------------------
    if st.session_state.month_cycle:

        cycle = st.session_state.month_cycle
        notes = st.session_state.month_cycle_notes

        md_cycle = "# Cycle mensuel Cyber-Opéra\n\n"

        for day in cycle:
            d = day["jour"]
            arc = day["arcane"]
            p = day["personnage"]
            n = notes[d]

            md_cycle += f"""
## Jour {d}
### {p['emoji']} {p['name']}
**Interprétation Sujet ↔ Personnage :**  
{n['astro']}

**Interprétation Cyber-Opéra :**  
{n['classic']}

- Sphère : {day['sphere']}
- Feu : {day['feu']}
- Défaut : {day['defaut']}
- Arcane : {arc['emoji']} {arc['name']} (*{arc['theme']}*)

---
"""

        st.download_button(
            "📘 Exporter le cycle complet",
            md_cycle,
            file_name="cycle-complet-cyberopera.md"
        )

    st.markdown("---")

    # ------------------------------
    # 5. Générer 30 micro-oracles d’un coup
    # ------------------------------

    st.subheader("🔮 Micro-oracles (génération automatique)")

    if st.button("Générer 30 micro-oracles pour la saison"):
        micro = []

        for i in range(1, 31):
            p = pick(ASTRO_SIGNS)
            interp = interpret_character(
                p,
                st.session_state.natal_profile,
                mode=st.session_state.tone_mode
            )
            micro.append(
                f"### Jour {i} — {p['emoji']} {p['name']}\n{interp}\n"
            )

        st.session_state.micro_oracles = micro
        st.success("Micro-oracles générés.")

    # Affichage
    if "micro_oracles" in st.session_state:
        for m in st.session_state.micro_oracles:
            st.markdown(m)

        # Export micro-oracles
        md_micro = "# Micro-oracles — Saison complète\n\n" + "\n".join(st.session_state.micro_oracles)

        st.download_button(
            "📘 Exporter les micro-oracles",
            md_micro,
            file_name="micro-oracles-cyberopera.md"
        )

# ============================================================
# Fin du Bloc 5
# ============================================================
# ============================================================
# BLOC 6 — STATS, PORTRAIT DE SAISON, IMPORT, GRIMOIRE
# ============================================================

with tab_stats:

    st.subheader("📊 Statistiques & Grimoire de Saison")

    # ------------------------------------------------------
    # 1. STATISTIQUES GLOBALES
    # ------------------------------------------------------
    st.markdown("## Statistiques générales")

    if not st.session_state.space_history and not st.session_state.month_cycle:
        st.info("Aucune donnée encore. Générez des scènes et/ou un cycle pour alimenter les statistiques.")
    else:

        # Extraction des données
        sph_list = []
        feu_list = []
        def_list = []
        astro_list = []

        # Récupération depuis l'historique des scènes
        for entry in st.session_state.space_history:
            scene = entry["scene"]
            sph_list.append(scene["sphere"])
            feu_list.append(scene["feu"])
            def_list.append(scene["defaut"])
            astro_list.append(scene["personnage"]["name"])

        # Depuis le cycle mensuel
        if st.session_state.month_cycle:
            for day in st.session_state.month_cycle:
                sph_list.append(day["sphere"])
                feu_list.append(day["feu"])
                def_list.append(day["defaut"])
                astro_list.append(day["personnage"]["name"])

        # Calcul des fréquences
        sph_count = Counter(sph_list)
        feu_count = Counter(feu_list)
        def_count = Counter(def_list)
        astro_count = Counter(astro_list)

        # Stats affichées
        st.markdown("### 🔹 Fréquences des Sphères")
        st.write(pd.DataFrame.from_dict(sph_count, orient='index', columns=["Occurrences"]))

        st.markdown("### 🔹 Fréquences des Feux")
        st.write(pd.DataFrame.from_dict(feu_count, orient='index', columns=["Occurrences"]))

        st.markdown("### 🔹 Fréquences des Défauts")
        st.write(pd.DataFrame.from_dict(def_count, orient='index', columns=["Occurrences"]))

        st.markdown("### 🔹 Fréquences des Personnages astrologiques")
        st.write(pd.DataFrame.from_dict(astro_count, orient='index', columns=["Occurrences"]))

        # ------------------------------------------------------
        # 2. TOP 1 & POURCENTAGES
        # ------------------------------------------------------
        st.markdown("## Top 1 & Pourcentages")

        def top_and_percent(counter):
            if not counter:
                return None, 0
            total = sum(counter.values())
            top = counter.most_common(1)[0]
            pct = round((top[1] / total) * 100, 1)
            return top[0], pct

        top_sphere, pct_sphere = top_and_percent(sph_count)
        top_feu, pct_feu = top_and_percent(feu_count)
        top_def, pct_def = top_and_percent(def_count)
        top_astro, pct_astro = top_and_percent(astro_count)

        st.write(f"**Sphère dominante :** {top_sphere} ({pct_sphere} %)")
        st.write(f"**Feu dominant :** {top_feu} ({pct_feu} %)")
        st.write(f"**Défaut récurrent :** {top_def} ({pct_def} %)")
        st.write(f"**Personnage astro dominant :** {top_astro} ({pct_astro} %)")

        # ------------------------------------------------------
        # 3. PORTRAIT DE SAISON (synthèse)
        # ------------------------------------------------------
        st.markdown("## 🌀 Portrait de saison")

        def build_portrait():
            text = ""

            # Sphère dominante
            if top_sphere:
                text += f"La saison s'est structurée autour de la sphère **{top_sphere}**, pivot récurrent du théâtre intérieur.\n"

            # Feu dominant
            if top_feu:
                text += f"L'énergie principale fut le feu **{top_feu}**, moteur des dynamiques et des bascules.\n"

            # Défaut récurrent
            if top_def:
                text += f"Le défaut le plus fréquent fut **{top_def}**, agissant comme un fil rouge à transmuter.\n"

            # Personnage astro dominant
            if top_astro:
                sign = next(s for s in ASTRO_SIGNS if s["name"] == top_astro)
                text += (
                    f"Le personnage cosmique dominant fut **{sign['emoji']} {top_astro}**, "
                    f"porteur de **{sign['pouvoir']}** mais aussi du risque de **{sign['fragilite']}**.\n"
                )

            # Synthèse finale
            text += (
                "\nEn résumé, cette saison révèle un thème central mêlant "
                f"**{top_sphere}**, **{top_feu}**, et les dynamiques de **{top_astro}** — "
                "un paysage intérieur riche en transitions symboliques."
            )

            return text

        portrait = build_portrait()
        st.markdown(f"<div class='card'>{portrait}</div>", unsafe_allow_html=True)

        # Export portrait seul
        st.download_button(
            "📄 Exporter le portrait de saison",
            portrait,
            file_name="portrait-de-saison.md"
        )

        st.markdown("---")

        # ------------------------------------------------------
        # 4. IMPORT D’UN .MD
        # ------------------------------------------------------
        st.subheader("📥 Importer un fichier Markdown (.md)")

        md_file = st.file_uploader("Importer un fichier .md", type=["md"])

        if md_file:
            md_text = md_file.read().decode("utf-8")
            st.markdown("### Contenu importé :")
            st.markdown(md_text)

        st.markdown("---")

        # ------------------------------------------------------
        # 5. GRIMOIRE DE SAISON (export global)
        # ------------------------------------------------------
        st.subheader("📘 Export : Grimoire de Saison (global)")

        cycle = st.session_state.month_cycle
        notes = st.session_state.month_cycle_notes

        # Construction du grimoire
        grimoire = "# Grimoire de Saison — Cyber-Opéra\n\n"

        # Profil natal
        nat = st.session_state.natal_profile
        grimoire += "## Profil natal\n"
        grimoire += f"- Soleil : {nat['soleil']}\n"
        grimoire += f"- Lune : {nat['lune']}\n"
        grimoire += f"- Ascendant : {nat['ascendant']}\n\n"

        # Portrait
        grimoire += "## Portrait de saison\n"
        grimoire += portrait + "\n\n"

        # Cycle complet
        if cycle:
            grimoire += "## Cycle mensuel\n"
            for day in cycle:
                d = day["jour"]
                p = day["personnage"]
                arc = day["arcane"]
                inter = notes[d]

                grimoire += f"""
### Jour {d}
**{p['emoji']} {p['name']}**

**Résonance Sujet ↔ Personnage :**  
{inter['astro']}

**Interprétation Cyber-Opéra :**  
{inter['classic']}

- Sphère : {day['sphere']}
- Feu : {day['feu']}
- Défaut : {day['defaut']}
- Arcane : {arc['emoji']} {arc['name']} (*{arc['theme']}*)

---
"""

        # Micro-oracles
        if "micro_oracles" in st.session_state:
            grimoire += "## Micro-oracles\n\n"
            grimoire += "\n".join(st.session_state.micro_oracles)

        # Export
        st.download_button(
            "📘 Exporter le Grimoire de Saison",
            grimoire,
            file_name="grimoire-cyberopera.md"
        )

# ============================================================
# Fin du Bloc 6
# ============================================================
