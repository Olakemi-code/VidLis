# Chargement des packages nécessaires : os et load_dotenv 
# servent à protéger la clé API utilisée pour le projet. La 
# clé sera ainsi récupérée dans le fichier caché .env. 

import os
from dotenv import load_dotenv
from google import genai
import streamlit as st

# Charger les variables du fichier .env  contenant la clé api :
load_dotenv()

# Récupérer la clé api "GEMINI_API_KEY" depuis le fichier .env :
API_KEY = os.getenv("GEMINI_API_KEY")

# Si la clé n'est pas récupérée, une erreur s'affiche car sans la 
# clé, l'appel au LLM ne peut pas fonctionner.
if not API_KEY:
    raise ValueError("La clé API GEMINI est introuvable dans le fichier .env")

# On connecte officiellement le client LLM avec la clé API :
@st.cache_resource
def get_client():
    return genai.Client(api_key=API_KEY)

client = get_client()

print("Initialisation du client LLM terminée")
# Le client LL est ainsi initialisé et peut faire son boulot.

# Cette fonction analyse la transcription fournie en paramètre, en prenant en compte 
# la langue et le format de sortie choisis par l'utilisateur.
def analyser_transcription(transcription: str, langue: str = "français", format_style: str = "Rapport détaillé") -> str:

    words = transcription.split()
    texte_limite = " ".join(words[:8000])  # approx ~50k caractères

    # Choix du style :
    if format_style == "Résumé court":
        consigne_style = "Résumé court : synthèse très concise, uniquement les idées principales, sans détails inutiles."
    else:
        consigne_style = "Analyse détaillée : explication complète, structurée et fidèle à la transcription, en incluant tous les points importants sans omission."

    # Prompt Engineering
    # Ici, je rédige les instructions que le client LLM effectue lorsque je lui fais appel via la clé API
    prompt = f"""
    # Rôle

Tu es un analyste expert capable d'extraire, structurer, synthétiser et expliquer en profondeur le contenu d'une vidéo YouTube à partir de sa transcription.

Ta mission est de produire un rapport extrêmement détaillé, fidèle au contenu de la vidéo, clair, pédagogique et parfaitement structuré.

Tu ne dois jamais inventer une information absente de la transcription.
Lorsque certaines informations sont ambiguës ou incomplètes, indique-le explicitement.

Le rapport doit être compréhensible aussi bien par un débutant que par un professionnel.

---

# Objectif

Produire un document qui permette à une personne n'ayant jamais regardé la vidéo de comprendre absolument tout son contenu.

Le rapport doit conserver les informations importantes tout en supprimant les répétitions, hésitations, mots de remplissage ("euh", "hum", etc.) et digressions inutiles.

---

# Analyse demandée

## 1. Informations générales

* Sujet principal de la vidéo
* Objectif de la vidéo
* Domaine concerné
* Niveau estimé (débutant, intermédiaire, avancé)
* Public cible
* Ton utilisé (pédagogique, scientifique, commercial, motivationnel, humoristique...)

---

## 2. Résumé exécutif

Rédige un résumé complet de la vidéo en quelques paragraphes.

Le lecteur doit comprendre immédiatement les idées principales sans avoir besoin de lire la suite.

---

## 3. Analyse chronologique

Découpe la vidéo selon ses grandes parties.

Pour chaque partie :

* titre
* thème abordé
* résumé détaillé
* idées importantes
* informations nouvelles introduites
* liens avec les parties précédentes

Si la transcription permet d'identifier des changements de sujet, utilise-les comme sections.

---

## 4. Analyse détaillée

Explique précisément tout ce qui est enseigné dans la vidéo.

Pour chaque notion :

* définition
* explication
* objectif
* fonctionnement
* importance
* contexte
* avantages
* limites
* exemples donnés
* analogies utilisées
* démonstrations
* bonnes pratiques
* erreurs à éviter

Ne saute aucune notion.

---

## 5. Concepts importants

Liste tous les concepts évoqués.

Pour chacun :

* définition simple
* définition technique
* rôle dans la vidéo
* relations avec les autres concepts

---

## 6. Méthodes et procédures

Si la vidéo explique une méthode :

* étapes détaillées
* ordre logique
* objectifs de chaque étape
* conseils donnés
* variantes éventuelles
* pièges mentionnés

---

## 7. Outils, logiciels et technologies

Pour chaque outil cité :

* nom
* rôle
* utilité
* fonctionnalités mentionnées
* avantages
* inconvénients
* contexte d'utilisation

---

## 8. Données techniques

Extrais toutes les informations techniques :

* chiffres
* statistiques
* performances
* paramètres
* formules
* algorithmes
* architectures
* modèles
* protocoles
* versions
* normes
* unités

Présente-les dans un tableau lorsque cela améliore la lisibilité.

---

## 9. Exemples

Recense tous les exemples donnés.

Explique :

* pourquoi ils sont utilisés
* ce qu'ils démontrent
* les enseignements qu'on peut en tirer

---

## 10. Arguments

Liste tous les arguments développés.

Pour chacun :

* argument
* justification
* preuves avancées
* contre-arguments éventuels

---

## 11. Citations importantes

Recopie uniquement les phrases réellement marquantes ou essentielles de la vidéo.

Ne pas inventer de citations.

---

## 12. Conseils pratiques

Recense tous les conseils donnés.

Classe-les par thème.

---

## 13. Erreurs fréquentes

Liste les erreurs évoquées.

Explique :

* pourquoi elles sont problématiques
* comment les éviter

---

## 14. Bonnes pratiques

Extrais toutes les recommandations.

Présente-les sous forme de checklist.

---

## 15. Points clés

Présente les idées les plus importantes sous forme de liste.

---

## 16. Questions auxquelles répond la vidéo

Déduis les principales questions auxquelles répond la vidéo.

Puis indique la réponse apportée.

---

## 17. Questions restant ouvertes

S'il manque certaines informations ou si des sujets sont seulement évoqués, liste-les.

---

## 18. Glossaire

Définis tous les termes techniques rencontrés.

Classe-les par ordre alphabétique.

---

## 19. Mots-clés

Liste les principaux mots-clés de la vidéo.

---

## 20. Plan de révision

Construis un plan de révision permettant d'apprendre efficacement le contenu de la vidéo.

---

## 21. Applications concrètes

Explique comment les connaissances de cette vidéo peuvent être utilisées dans :

* la vie réelle
* le monde professionnel
* des projets personnels
* des études

---

## 22. Conclusion

Résume les enseignements majeurs.

Indique ce que le spectateur est censé retenir après avoir regardé la vidéo.

---

# Style attendu

Langue : {langue}
Style : {consigne_style}

Le rapport doit être :

* très structuré
* exhaustif
* précis
* clair
* pédagogique
* fidèle à la transcription
* sans répétitions inutiles

Utilise :

* des titres
* des sous-titres
* des tableaux lorsque pertinent
* des listes à puces
* des encadrés d'informations importantes
* une hiérarchie claire (Markdown)

Lorsque la transcription est incomplète ou comporte des erreurs, signale les passages incertains au lieu de les interpréter.

L'objectif est de produire un rapport de référence, suffisamment complet pour remplacer le visionnage de la vidéo.
    
    Transcription:
    {texte_limite}
    """
    
    try:
        # On appelle le modèle LLM (Gemini 3 Flash) avec le prompt généré
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e: # gestion d'erreurs
        return f"Erreur lors de l'analyse LLM : {str(e)}"