import streamlit as st
import random

st.set_page_config(page_title="Cyber-Opéra — Générative", layout="centered")

# ---------- STYLES ----------
st.markdown(
    """
    <style>
    .cyber-title {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #ff6ec7, #00f5ff);
        -webkit-background-clip: text;
        color: transparent;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .cyber-subtitle {
        text-align: center;
        font-size: 0.9rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }
    .card {
        padding: 1rem 1.2rem;
        border-radius: 0.9rem;
        border: 1px solid rgba(255,255,255,0.06);
        background: radial-gradient(circle at top left, rgba(255,255,255,0.06), rgba(0,0,0,0.7));
        box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        margin-bottom: 0.6rem;
    }
    .mini-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        opacity: 0.7;
        letter-spacing: 0.12em;
        margin-bottom: 0.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='cyber-title'>Cyber-Opéra</div>", unsafe_allow_html=True)
st.markdown("<div class='cyber-subtitle'>Système personnel de navigation symbolique</div>", unsafe_allow_html=True)

# ---------- DONNÉES DU SYSTÈME ----------

triades = [
    {"name": "Gémeaux", "clair": "Clair", "ombre": "Dispersion", "pouvoir": "Compréhension", "emoji": "🌀"},
    {"name": "Verseau", "clair": "Vision", "ombre": "Froideur", "pouvoir": "Vision du futur", "emoji": "⚡️"},
    {"name": "Poissons", "clair": "Intuition", "ombre": "Confusion", "pouvoir": "Synchronicités", "emoji": "🌊"},
]

spheres = [
    "Amour 💗",
    "Boulot 🛰️",
    "Corps 🦴",
    "Développement 📚",
    "Expression 🎙️",
    "Flow Créatif 🎨",
    "Générosité 🎁",
    "Habitat 🏠",
    "Intelligence ♟️",
    "Joie 🌞",
    "Karma 🜃",
    "Lien social 🤝",
]

feux = [
    "Étincelle ✨",
    "Flamme 🔥",
    "Brasier 🔥🔥",
    "Cendre 🕯️",
    "Phoenix 🐦‍🔥",
]

familles = [
    {"name": "Action", "motto": "produire", "hint": "Fais avancer quelque chose, même en version brouillon.", "emoji": "⚙️"},
    {"name": "Pause", "motto": "ressentir", "hint": "Fais silence 3 minutes et écoute ce qui se passe en toi.", "emoji": "🌫️"},
    {"name": "Combat", "motto": "trancher", "hint": "Choisis une chose à arrêter ou une limite à poser aujourd'hui.", "emoji": "🗡️"},
    {"name": "Initiation", "motto": "transformer", "hint": "Fais une petite chose nouvelle qui te met légèrement mal à l'aise.", "emoji": "🜇"},
    {"name": "Chaos", "motto": "brouiller pour révéler", "hint": "Bouscule un automatisme : change l'ordre, le chemin, la forme habituelle.", "emoji": "☄️"},
]

# Défauts possibles pour la 5e carte de la scène opératique
defauts = [
    "dispersion", "anxiété",
    "froideur", "procrastination",
    "confusion", "fatigue",
    "jalousie", "pression",
    "fatigue du corps", "surcharge",
    "blocage d'expression", "chaos créatif",
    "fuite", "désordre",
    "suranalyse", "vide intérieur",
    "errance", "isolement",
    "brûler trop vite",
    "feu sans direction",
    "étouffé par émotions",
    "dispersé par mental",
    "refroidi par détachement",
]

# ---------- FONCTIONS UTILITAIRES ----------

def pick_random(lst):
    return random.choice(lst)

def generate_scene():
    """Génère une scène opératique = 5 cartes."""
    return {
        "triade": pick_random(triades),
        "sphere": pick_random(spheres),
        "feu": pick_random(feux),
        "famille": pick_random(familles),
        "defaut": pick_random(defauts),
    }

def build_markdown_for_scene(scene, intention, synchro, micro):
    tri = scene["triade"]
    fam = scene["famille"]
    md = f"""# Scène opératique — Cyber-Opéra

## Tirage

- **Triade** : {tri['emoji']} {tri['name']}  
  - Pouvoir : {tri['pouvoir']}  
  - Clair : {tri['clair']} · Ombre : {tri['ombre']}

- **Feu** : {scene['feu']}

- **Sphère** : {scene['sphere']}

- **Famille du grimoire** : {fam['emoji']} {fam['name']}  
  - Motto : {fam['motto']}  
  - Suggestion : {fam['hint']}

- **Défaut à transmuter** : {scene['defaut']}

---

## Journal Opéra

- **Intention** : {intention or "_(non renseignée)_"}
- **Synchronicité** : {synchro or "_(non renseignée)_"}
- **Micro-victoire** : {micro or "_(non renseignée)_"}
"""
    return md

# ---------- SESSION STATE ----------

for key in ["triade", "sphere", "feu", "famille", "scene",
            "journal_intention", "journal_synchro", "journal_micro"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key.startswith("journal_") else None

# ---------- SIDEBAR (COMMANDES) ----------

st.sidebar.header("🎛️ Contrôle de la scène")

if st.sidebar.button("✨ Tirage quotidien"):
    st.session_state.triade = pick_random(triades)
    st.session_state.sphere = pick_random(spheres)
    st.session_state.feu = pick_random(feux)
    st.session_state.famille = pick_random(familles)

if st.sidebar.button("🎭 Générer une Scène opératique"):
    st.session_state.scene = generate_scene()
    # reset journal quand on génère une nouvelle scène
    st.session_state.journal_intention = ""
    st.session_state.journal_synchro = ""
    st.session_state.journal_micro = ""

st.sidebar.markdown("---")
st.sidebar.caption("Chaque tirage est une scène. Tu choisis comment la jouer dans la matière.")

# ---------- CONTENU PRINCIPAL : TABS ----------

tab1, tab2 = st.tabs(["🌓 Tirage quotidien", "🎭 Scène opératique"])

# --- Onglet 1 : Tirage quotidien ---
with tab1:
    st.subheader("🌓 Tirage quotidien")

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.triade:
            tri = st.session_state.triade
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">TRIADE</div>
                    <h3>{tri['emoji']} {tri['name']}</h3>
                    <p><b>Pouvoir :</b> {tri['pouvoir']}</p>
                    <p><b>Clair :</b> {tri['clair']} · <b>Ombre :</b> {tri['ombre']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.session_state.feu:
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FEU INTÉRIEUR</div>
                    <h3>{st.session_state.feu}</h3>
                    <p>Intensité / température énergétique du jour.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col2:
        if st.session_state.sphere:
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SPHÈRE</div>
                    <h3>{st.session_state.sphere}</h3>
                    <p>Zone de vie impactée par le tirage.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.session_state.famille:
            fam = st.session_state.famille
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FAMILLE DU GRIMOIRE</div>
                    <h3>{fam['emoji']} {fam['name']}</h3>
                    <p><b>Motto :</b> {fam['motto']}</p>
                    <p style="font-size:0.85rem;opacity:0.85;"><i>Suggestion :</i> {fam['hint']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- Onglet 2 : Scène opératique ---
with tab2:
    st.subheader("🎭 Scène opératique — 5 cartes")

    if st.session_state.scene is None:
        st.info("Utilise le bouton **« 🎭 Générer une Scène opératique »** dans la sidebar pour créer une scène.")
    else:
        scene = st.session_state.scene

        col1, col2 = st.columns(2)

        # Carte 1 : Rôle intérieur (Triade)
        with col1:
            tri = scene["triade"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">CARTE 1 — RÔLE INTÉRIEUR</div>
                    <h3>{tri['emoji']} {tri['name']}</h3>
                    <p><b>Pouvoir :</b> {tri['pouvoir']}</p>
                    <p><b>Clair :</b> {tri['clair']} · <b>Ombre :</b> {tri['ombre']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Carte 2 : Feu
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">CARTE 2 — FEU DE LA SCÈNE</div>
                    <h3>{scene['feu']}</h3>
                    <p>Qualité d'intensité qui colore toute la scène.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Carte 3 : Sphère + Carte 4 : Famille + Carte 5 : Défaut
        with col2:
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">CARTE 3 — DÉCOR / SPHÈRE</div>
                    <h3>{scene['sphere']}</h3>
                    <p>Le théâtre concret où la scène se joue aujourd'hui.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            fam = scene["famille"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">CARTE 4 — ÉNERGIE OPÉRATIQUE</div>
                    <h3>{fam['emoji']} {fam['name']}</h3>
                    <p><b>Motto :</b> {fam['motto']}</p>
                    <p style="font-size:0.85rem;opacity:0.85;"><i>Suggestion :</i> {fam['hint']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">CARTE 5 — DÉFAUT À TRANSMUTER</div>
                    <h3>🜁 {scene['defaut']}</h3>
                    <p>Aspect à observer, non à juger. Matériau brut pour l'alchimie du jour.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ---------- JOURNAL OPÉRA ----------
        st.markdown("### 📓 Journal Opéra")

        col_j1, col_j2 = st.columns(2)
        with col_j1:
            st.session_state.journal_intention = st.text_area(
                "Intention",
                value=st.session_state.journal_intention,
                placeholder="Quel geste intérieur ou extérieur veux-tu poser dans cette scène ?",
            )
        with col_j2:
            st.session_state.journal_synchro = st.text_area(
                "Synchronicité",
                value=st.session_state.journal_synchro,
                placeholder="Signes, coïncidences, résonances remarquées...",
            )

        st.session_state.journal_micro = st.text_area(
            "Micro-victoire",
            value=st.session_state.journal_micro,
            placeholder="Quel petit mouvement, même minuscule, honore la scène aujourd'hui ?",
        )

        # ---------- EXPORT MARKDOWN ----------
        st.markdown("### 📤 Exporter")

        md_content = build_markdown_for_scene(
            scene,
            st.session_state.journal_intention,
            st.session_state.journal_synchro,
            st.session_state.journal_micro,
        )

        st.download_button(
            label="📥 Exporter la scène en Markdown",
            data=md_content,
            file_name="scene-opera.md",
            mime="text/markdown",
        )

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🕯️ Chaque tirage est une scène. À toi de jouer l'opéra dans la matière.")
