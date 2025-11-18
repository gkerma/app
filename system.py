import streamlit as st
import random

st.set_page_config(page_title="Cyber-Opéra — Générative", layout="centered")

# --- Données du système ---
triades = [
    {"name": "Gémeaux", "clair": "Clair", "ombre": "Dispersion", "pouvoir": "Compréhension"},
    {"name": "Verseau", "clair": "Vision", "ombre": "Froideur", "pouvoir": "Vision du futur"},
    {"name": "Poissons", "clair": "Intuition", "ombre": "Confusion", "pouvoir": "Synchronicités"}
]

spheres = [
    "Amour", "Boulot", "Corps", "Développement", "Expression", "Flow Créatif",
    "Générosité", "Habitat", "Intelligence", "Joie", "Karma", "Lien social"
]

feux = ["Étincelle", "Flamme", "Brasier", "Cendre", "Phoenix"]

familles = [
    {"name": "Action", "motto": "produire", "hint": "Fais avancer quelque chose, même en version brouillon."},
    {"name": "Pause", "motto": "ressentir", "hint": "Fais silence 3 minutes et écoute ce qui se passe en toi."},
    {"name": "Combat", "motto": "trancher", "hint": "Choisis une chose à arrêter ou une limite à poser aujourd'hui."},
    {"name": "Initiation", "motto": "transformer", "hint": "Fais une petite chose nouvelle qui te met légèrement mal à l'aise."},
    {"name": "Chaos", "motto": "brouiller pour révéler", "hint": "Bouscule un automatisme : change l'ordre, le chemin, la forme habituelle."}
]

# --- Fonctions ---
def pick_random(lst):
    return random.choice(lst)

# --- UI ---
st.title("🎭 Cyber-Opéra — Générateur Interactif")
st.markdown("Tirage des éléments opératiques pour naviguer ta journée.")

if st.button("✨ Tirer Tout"):
    st.session_state.triade = pick_random(triades)
    st.session_state.sphere = pick_random(spheres)
    st.session_state.feu = pick_random(feux)
    st.session_state.famille = pick_random(familles)

# Initialisation
for key in ["triade", "sphere", "feu", "famille"]:
    st.session_state.setdefault(key, None)

# --- Affichage du tirage ---
st.subheader("Résultats du tirage :")

if st.session_state.triade:
    tri = st.session_state.triade
    st.write(f"**Triade : {tri['name']}** — Pouvoir : *{tri['pouvoir']}*")

if st.session_state.sphere:
    st.write(f"**Sphère :** {st.session_state.sphere}")

if st.session_state.feu:
    st.write(f"**Feu :** {st.session_state.feu}")

if st.session_state.famille:
    fam = st.session_state.famille
    st.markdown(f"**Famille du Grimoire : {fam['name']}** — {fam['motto']}")
    st.caption(f"Suggestion : {fam['hint']}")

# --- Footer ---
st.markdown("---")
st.caption("Cyber-Opéra — Système personnel de navigation symbolique.")
