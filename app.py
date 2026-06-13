# Ici, on écrit le code nécessaire pour obtenir l'interface utilisateur de l'application

# Chargement des bibliothèques
import streamlit as st
from youtube_utils import extraire_id_youtube, obtenir_transcription_ytdlp
from analyseur_llm import analyser_transcription


# Configuration de la page

# Définir le titre de l'onglet et l'icône, avec le mode wide afin d'utiliser toute la largeur de l'écran
st.set_page_config(page_title="RESUME VIDEO IA", page_icon=":movie_camera:", layout="wide")

# Afficher le titre principal en haut de la page
st.title(" VidLis ")

# Zone de saisie où l'utilisateur colle le lien de la vidéo Youtube dont il veut la transcription résumée
url_video = st.text_input("🔗 URL de la vidéo YouTube :", placeholder="https://www.youtube.com/watch?v=...")

# Si un lien est donné, la vidéo est extraite et affichée directement dans l'application dans l'application
if url_video:
    try:
        video_id = extraire_id_youtube(url_video)
        # --- AJOUT DU LECTEUR VIDÉO ---
        st.video(f"https://www.youtube.com/watch?v={video_id}")
        # ------------------------------
    except:
        st.error("URL non valide")

# Définir les paramètres de l'analyse où l'utilisateur peut faire ses choix
with st.sidebar:
    st.title("Configuration")

    # pour le choix de la langue
    langue_choisie = st.selectbox( 
        "Langue :",
        ["Français", "Anglais"]
    )
    
    # pour le choix du format
    format_choisi = st.radio(
        "Format de l'analyse :",
        ["Résumé court", "Rapport détaillé"],
        index=1
    )
    
    st.divider()

    # Afficher un petit encadré avec les paramètres choisis
    st.info(f"Analyse en **{langue_choisie}** au format **{format_choisi}**.")

# Configuration du bouton de lancement
if st.button("Lancer l'analyse", type="primary"):
    if not url_video:
        st.error("Veuillez entrer une URL valide.")
    else:
        try:
            # Afficher une barre de progression pour informer l'utilisateur de l'étape actuelle de l'analyse
            with st.status("Traitement en cours...", expanded=True) as status:

                # Récupérer la vidéo YouTube
                video_id = extraire_id_youtube(url_video)
                
                st.write("Récupération de la transcription...")
                # Appeler le script comprenant la fonction servant à obtenir la transcription de la vidéo récupérée
                texte = obtenir_transcription_ytdlp(video_id)
                
                # Une fois que la transcription est obtenue, on passe à l'analyse
                if texte:
                    st.write(f"Analyse par l'IA en cours ({langue_choisie}, {format_choisi})...")
                    
                    # On passe les variables récupérées dans la sidebar
                    compte_rendu = analyser_transcription(
                        texte, 
                        langue=langue_choisie, 
                        format_style=format_choisi
                    )
                    
                    # Une fois que l'analyse est achevée, un message s'affiche et l'utilisateur en est ainsi informé
                    status.update(label="Analyse terminée !", state="complete", expanded=False)

                    # Mise en page des résultats obtenus suite à l'analyse
                    # Division en deux colonnes pour une meilleure présentation
                    col1, col2 = st.columns([2, 1])
                    
                    # Avec la colonne 1, on affiche l'analyse avec une mise en forme Markdown
                    with col1:
                        st.subheader(f"📝 Rapport d'Analyse ({langue_choisie})")
                        st.markdown(compte_rendu)
                    
                    # Avec la colonne 2, on affiche les options télécharger et effacer le rapport généré
                    with col2:
                        st.subheader("⚙️ Options")

                        # Définir le bouton sur lequel l'utilisateur clique pour télécharger le rapport généré
                        st.download_button(
                            label="📥 Télécharger (.md)",
                            data=compte_rendu,
                            file_name=f"analyse_{video_id}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                        # Définir le bouton sur lequel l'utilisateur clique pour effacer les résultats et par 
                        # la suite, raffraîchir la page afin de recommencer une nouvelle analyse
                        if st.button("Effacer les résultats", use_container_width=True):
                            st.rerun()
                    
                else:
                    st.error("Transcription introuvable.")
        except Exception as e: # gestion des erreurs
            st.error(f"Erreur ( pas d'analyse effectuée): {e}")