import streamlit as st
import random
from datetime import datetime
from collections import Counter
import pandas as pd

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

# Arcanes pour le Cycle mensuel
arcanes = [
    {"name": "Le Portail", "emoji": "🜄", "theme": "passage, seuil, nouvelle phase"},
    {"name": "Le Miroir", "emoji": "🪞", "theme": "reflet, conscience de soi"},
    {"name": "La Tour Data", "emoji": "🛰️", "theme": "structure, système, réseau"},
    {"name": "Le Flux", "emoji": "🌊", "theme": "mouvement, lâcher-prise"},
    {"name": "L’Astre Noir", "emoji": "🌑", "theme": "inconscient, incubation"},
    {"name": "Le Pont", "emoji": "🌉", "theme": "lien, médiation, passage entre mondes"},
    {"name": "Le Masque", "emoji": "🎭", "theme": "rôle, persona, jeu social"},
    {"name": "Le Grimoire", "emoji": "📜", "theme": "connaissance, mémoire, trace"},
    {"name": "La Spirale", "emoji": "🌀", "theme": "répétition créatrice, cycle"},
    {"name": "Le Cœur Quantique", "emoji": "💗", "theme": "lien profond, amour, résonance"},
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

def generate_month_cycle(days=30):
    """Génère un cycle mensuel (30 jours) : Arcane + Sphère + Défaut + Feu."""
    cycle = []
    for i in range(days):
        cycle.append(
            {
                "jour": i + 1,
                "arcane": pick_random(arcanes),
                "sphere": pick_random(spheres),
                "feu": pick_random(feux),
                "defaut": pick_random(defauts),
            }
        )
    return cycle

def interpret_scene(scene, mode="Sobre"):
    """Produit une interprétation narrative de la scène en deux tonalités."""
    tri = scene["triade"]
    fam = scene["famille"]
    sphere = scene["sphere"]
    feu = scene["feu"]
    defaut = scene["defaut"]

    if mode == "Sobre":
        texte = (
            f"Aujourd'hui, ton fonctionnement dominant est placé sous l'archétype **{tri['emoji']} {tri['name']}** : "
            f"ton pouvoir clé est la *{tri['pouvoir']}*, avec une tension entre le clair (*{tri['clair']}*) "
            f"et l'ombre (*{tri['ombre']}*).\n\n"
            f"La zone de vie la plus concernée est **{sphere}**, où ton attention est invitée à se poser.\n\n"
            f"Le niveau d'intensité globale est **{feu}**, ce qui peut te servir de repère pour ajuster ton rythme.\n\n"
            f"La dynamique recommandée par le système est **{fam['emoji']} {fam['name']}** "
            f"(motto : *{fam['motto']}*), avec une proposition concrète : {fam['hint']}\n\n"
            f"Le défaut du jour, **{defaut}**, n'est pas une faute mais un signal : un endroit à observer pour "
            f"mieux comprendre comment tu fonctionnes."
        )
    else:
        # Mode Space Opera total
        texte = (
            f"Les rideaux s'ouvrent sur la scène intérieure : **{tri['emoji']} {tri['name']}** prend le rôle principal. "
            f"Tu entres dans l'acte du jour avec le pouvoir de *{tri['pouvoir']}* comme artefact central, tandis que "
            f"le clair (*{tri['clair']}*) et l'ombre (*{tri['ombre']}*) dansent comme deux satellites autour de ton esprit.\n\n"
            f"Le théâtre choisi par le Cyber-Opéra est **{sphere}** : c'est là que les projecteurs se braquent, là "
            f"où les dialogues et les gestes auront un poids particulier.\n\n"
            f"Dans les coulisses énergétiques, le feu actif est **{feu}**. Il définit la température cosmique de ta journée : "
            f"soit une étincelle à nourrir, soit un brasier à canaliser, soit des cendres à remuer pour réveiller le Phoenix.\n\n"
            f"La Famille du Grimoire qui orchestre la vibration de la scène est **{fam['emoji']} {fam['name']}** "
            f"(motto : *{fam['motto']}*). C'est l'esprit qui te murmure : {fam['hint']}\n\n"
            f"Dans l'ombre des décors se cache **{defaut}**, non comme un monstre à abattre mais comme un "
            f"fragment d'étoile brute. En l'acceptant dans le champ de ta conscience, tu ajoutes une nouvelle "
            f"note à la partition de ton Space Opera intérieur."
        )
    return texte

def build_markdown_for_scene(scene, intention, synchro, micro, interpretation):
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

## Interprétation

{interpretation}

---

## Journal Opéra

- **Intention** : {intention or "_(non renseignée)_"}
- **Synchronicité** : {synchro or "_(non renseignée)_"}
- **Micro-victoire** : {micro or "_(non renseignée)_"}
"""
    return md

def build_markdown_for_cycle(cycle, notes, title="Cycle mensuel — Cyber-Opéra"):
    lines = [f"# {title}", ""]
    for day in cycle:
        idx = day["jour"]
        arc = day["arcane"]
        key = str(idx)
        note = notes.get(key, {})
        synchro = note.get("synchro", "")
        micro = note.get("micro", "")
        lines.append(f"## Jour {idx} — {arc['emoji']} {arc['name']}")
        lines.append("")
        lines.append(f"- **Arcane** : {arc['emoji']} {arc['name']} — *{arc['theme']}*")
        lines.append(f"- **Sphère** : {day['sphere']}")
        lines.append(f"- **Feu** : {day['feu']}")
        lines.append(f"- **Défaut à observer** : {day['defaut']}")
        lines.append("")
        lines.append("**Notes :**")
        lines.append(f"- Synchronicité : {synchro or '_(non renseignée)_'}")
        lines.append(f"- Micro-geste : {micro or '_(non renseignée)_'}")
        lines.append("")
    return "\n".join(lines)

# ---------- SESSION STATE ----------

for key in [
    "triade", "sphere", "feu", "famille", "scene",
    "journal_intention", "journal_synchro", "journal_micro",
    "scene_interpretation", "space_history",
    "month_cycle", "month_cycle_notes", "tone_mode"
]:
    if key not in st.session_state:
        if key == "space_history":
            st.session_state[key] = []
        elif key == "month_cycle":
            st.session_state[key] = None
        elif key == "month_cycle_notes":
            st.session_state[key] = {}
        elif key == "tone_mode":
            st.session_state[key] = "Space Opera total"
        elif key.startswith("journal_") or key.endswith("interpretation"):
            st.session_state[key] = ""
        else:
            st.session_state[key] = None

# ---------- SIDEBAR (COMMANDES) ----------

st.sidebar.header("🎛️ Contrôle")

st.sidebar.write("### Tonalité des interprétations")
st.session_state.tone_mode = st.sidebar.radio(
    "Tonalité",
    options=["Sobre", "Space Opera total"],
    index=1,
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.header("🎲 Tirages")

if st.sidebar.button("✨ Tirage quotidien"):
    st.session_state.triade = pick_random(triades)
    st.session_state.sphere = pick_random(spheres)
    st.session_state.feu = pick_random(feux)
    st.session_state.famille = pick_random(familles)

if st.sidebar.button("🎭 Générer une Scène opératique"):
    scene = generate_scene()
    st.session_state.scene = scene
    # reset journal
    st.session_state.journal_intention = ""
    st.session_state.journal_synchro = ""
    st.session_state.journal_micro = ""
    # nouvelle interprétation selon le mode
    interp = interpret_scene(scene, mode=st.session_state.tone_mode)
    st.session_state.scene_interpretation = interp
    # entrée historique automatique
    st.session_state.space_history.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "scene": scene,
            "interpretation": interp,
            "tone": st.session_state.tone_mode,
        }
    )

st.sidebar.markdown("---")
if st.sidebar.button("🗓️ Générer un cycle mensuel (30 jours)"):
    st.session_state.month_cycle = generate_month_cycle(days=30)
    st.session_state.month_cycle_notes = {}

st.sidebar.caption("Chaque tirage est une scène. Chaque cycle est une saison de ton Space Opera.")

# ---------- CONTENU PRINCIPAL : TABS ----------

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🌓 Tirage quotidien", "🎭 Scène opératique", "📚 Historique", "🗓️ Cycle mensuel", "📊 Stats & Grimoire"]
)

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
            st.session_state.scene_interpretation,
        )

        st.download_button(
            label="📥 Exporter la scène en Markdown",
            data=md_content,
            file_name="scene-opera.md",
            mime="text/markdown",
        )

        # ---------- INTERPRÉTATION AFFICHÉE ----------
        st.markdown("### 🧠 Interprétation automatique")
        st.markdown(st.session_state.scene_interpretation)

# --- Onglet 3 : Historique Space Opera ---
with tab3:
    st.subheader("📚 Historique Space Opera")

    if not st.session_state.space_history:
        st.info("Aucune scène enregistrée pour l’instant. Génère une scène opératique pour commencer l’historique.")
    else:
        for entry in reversed(st.session_state.space_history):
            s = entry["scene"]
            tri = s["triade"]
            fam = s["famille"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SCÈNE DU {entry['timestamp']} — Tonalité : {entry['tone']}</div>
                    <p><b>Triade</b> : {tri['emoji']} {tri['name']} · <b>Feu</b> : {s['feu']}</p>
                    <p><b>Sphère</b> : {s['sphere']} · <b>Famille</b> : {fam['emoji']} {fam['name']}</p>
                    <p><b>Défaut</b> : {s['defaut']}</p>
                    <hr/>
                    <p style="font-size:0.85rem;opacity:0.9;">{entry['interpretation']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- Onglet 4 : Cycle mensuel ---
with tab4:
    st.subheader("🗓️ Cycle mensuel — Arcane + Sphère + Défaut + Feu")

    if st.session_state.month_cycle is None:
        st.info("Clique sur **« 🗓️ Générer un cycle mensuel (30 jours) »** dans la sidebar pour créer un cycle.")
    else:
        cycle = st.session_state.month_cycle

        # Sélection d'un jour
        jours = [d["jour"] for d in cycle]
        selected_day = st.selectbox("Choisir un jour du cycle", options=jours, index=0)
        day_data = next(d for d in cycle if d["jour"] == selected_day)
        idx_key = str(selected_day)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            arc = day_data["arcane"]
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">ARCANE DU JOUR</div>
                    <h3>{arc['emoji']} {arc['name']}</h3>
                    <p>Thème : {arc['theme']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">FEU</div>
                    <h3>{day_data['feu']}</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_c2:
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">SPHÈRE</div>
                    <h3>{day_data['sphere']}</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div class="card">
                    <div class="mini-label">DÉFAUT À OBSERVER</div>
                    <h3>🜁 {day_data['defaut']}</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Notes pour ce jour
        existing = st.session_state.month_cycle_notes.get(idx_key, {"synchro": "", "micro": ""})
        synchro_note = st.text_area(
            "Synchronicité (jour " + str(selected_day) + ")",
            value=existing.get("synchro", ""),
        )
        micro_note = st.text_area(
            "Micro-geste (jour " + str(selected_day) + ")",
            value=existing.get("micro", ""),
        )

        # Mise à jour des notes en mémoire
        st.session_state.month_cycle_notes[idx_key] = {
            "synchro": synchro_note,
            "micro": micro_note,
        }

        st.markdown("### 📤 Export du cycle complet")
        md_cycle = build_markdown_for_cycle(
            cycle,
            st.session_state.month_cycle_notes,
            title="Cycle mensuel — Cyber-Opéra",
        )

        st.download_button(
            label="📥 Exporter le cycle en Markdown",
            data=md_cycle,
            file_name="cycle-mensuel-cyber-opera.md",
            mime="text/markdown",
        )

# --- Onglet 5 : Stats & Grimoire ---
with tab5:
    st.subheader("📊 Stats — Feu, Sphères, Défauts")

    feux_counts = Counter()
    spheres_counts = Counter()
    defauts_counts = Counter()

    # Scenes de l'historique
    for entry in st.session_state.space_history:
        s = entry["scene"]
        feux_counts[s["feu"]] += 1
        spheres_counts[s["sphere"]] += 1
        defauts_counts[s["defaut"]] += 1

    # Cycle mensuel
    if st.session_state.month_cycle is not None:
        for day in st.session_state.month_cycle:
            feux_counts[day["feu"]] += 1
            spheres_counts[day["sphere"]] += 1
            defauts_counts[day["defaut"]] += 1

    if not feux_counts and not spheres_counts and not defauts_counts:
        st.info("Aucune donnée pour l’instant. Joue quelques scènes ou génère un cycle pour voir les stats.")
    else:
        col_s1, col_s2 = st.columns(2)

        # ---------- FEUX ----------
        with col_s1:
            st.markdown("#### 🔥 Feux les plus fréquents")
            if feux_counts:
                total_feux = sum(feux_counts.values())
                df_feux = pd.DataFrame(
                    {"Feu": list(feux_counts.keys()), "Occurrences": list(feux_counts.values())}
                )
                df_feux["%"] = (df_feux["Occurrences"] / total_feux * 100).round(1)
                df_feux = df_feux.sort_values("Occurrences", ascending=False)
                st.bar_chart(df_feux.set_index("Feu")["Occurrences"])
                st.table(df_feux)

                top_feu = df_feux.iloc[0]
                st.markdown(
                    f"**Feu dominant :** {top_feu['Feu']} "
                    f"({top_feu['%']}% des tirages Feu)."
                )
            else:
                st.caption("Pas encore de données sur le Feu.")

            st.markdown("#### 🜁 Défauts les plus fréquents")
            if defauts_counts:
                total_def = sum(defauts_counts.values())
                df_def = pd.DataFrame(
                    {"Défaut": list(defauts_counts.keys()), "Occurrences": list(defauts_counts.values())}
                )
                df_def["%"] = (df_def["Occurrences"] / total_def * 100).round(1)
                df_def = df_def.sort_values("Occurrences", ascending=False)
                st.bar_chart(df_def.set_index("Défaut")["Occurrences"])
                st.table(df_def)

                top_def = df_def.iloc[0]
                st.markdown(
                    f"**Défaut récurrent :** {top_def['Défaut']} "
                    f"({top_def['%']}% des défauts tirés)."
                )
            else:
                st.caption("Pas encore de données sur les défauts.")

        # ---------- SPHÈRES + PORTRAIT ----------
        with col_s2:
            st.markdown("#### 🌐 Sphères les plus activées")
            if spheres_counts:
                total_sph = sum(spheres_counts.values())
                df_sph = pd.DataFrame(
                    {"Sphère": list(spheres_counts.keys()), "Occurrences": list(spheres_counts.values())}
                )
                df_sph["%"] = (df_sph["Occurrences"] / total_sph * 100).round(1)
                df_sph = df_sph.sort_values("Occurrences", ascending=False)
                st.bar_chart(df_sph.set_index("Sphère")["Occurrences"])
                st.table(df_sph)

                top_sph = df_sph.iloc[0]
                sph_phrase = f"**Sphère dominante :** {top_sph['Sphère']} ({top_sph['%']}% des tirages de sphères)."
                st.markdown(sph_phrase)
            else:
                top_sph = None
                sph_phrase = ""
                st.caption("Pas encore de données sur les sphères.")

            # ---------- PORTRAIT DE SAISON ----------
            st.markdown("### 🧾 Portrait de saison")

            portrait_lines = []

            if feux_counts:
                portrait_lines.append(
                    f"- Ton feu dominant sur cette période est **{top_feu['Feu']}**, qui colore la majorité des scènes."
                )
            if spheres_counts:
                portrait_lines.append(
                    f"- La sphère la plus traversée est **{top_sph['Sphère']}**, théâtre fréquent de ton opéra intérieur."
                )
            if defauts_counts:
                portrait_lines.append(
                    f"- Le défaut qui revient comme matériau d'alchimie est **{top_def['Défaut']}**."
                )

            if portrait_lines:
                portrait_text = (
                    "Sur l’ensemble des tirages joués, on peut esquisser ce **portrait de saison** :\n\n"
                    + "\n".join(portrait_lines)
                    + "\n\nCela décrit la tonalité actuelle de ton Space Opera : les zones qui demandent "
                      "le plus d'attention, et les motifs qui insistent pour être transformés."
                )
                st.markdown(portrait_text)
            else:
                st.caption("Pas encore assez de matière pour un portrait de saison.")

        st.markdown("---")
        # ---------- IMPORT DE GRIMOIRE .MD ----------
        st.markdown("### 📥 Importer un grimoire (.md)")

        uploaded_md = st.file_uploader("Importer un fichier Markdown (.md)", type=["md"])
        if uploaded_md is not None:
            content = uploaded_md.read().decode("utf-8", errors="ignore")
            st.markdown("#### Contenu importé")
            st.markdown(content)

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🕯️ Chaque tirage est une scène. Chaque cycle est une saison de ton Space Opera.")
