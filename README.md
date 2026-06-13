# VidLis

VidLis est une application qui transforme des vidéos YouTube en rapports structurés, détaillés et exploitables grâce à l’intelligence artificielle.

L’objectif est de permettre la compréhension rapide et complète d’une vidéo sans avoir besoin de la regarder intégralement.

---

# Fonctionnalités

* Extraction et analyse de transcription YouTube
* Génération de rapports structurés et détaillés
* Résumé exécutif automatique
* Analyse par sections logiques
* Extraction des concepts clés
* Identification des outils, méthodes et idées importantes
* Interface interactive via Streamlit

---

# Cas d’usage

VidLis peut être utilisé pour :

* Résumer des cours en ligne
* Comprendre des conférences et podcasts
* Extraire les points clés de vidéos éducatives
* Réviser plus efficacement
* Accélérer la prise de notes et la recherche d’informations

---

# Technologies utilisées

* Python
* Streamlit
* IA générative : modèle LLM (Gemini 3 Flash), clé API de Google Gemini
* yt-dlp
* Prompt Engineering
* Traitement de texte
* Git / GitHub

---

# Installation

```bash id="9a1kq2"
git clone https://github.com/ton-compte/VidLis.git
cd VidLis
pip install -r requirements.txt
```

---

# Lancement de l’application

```bash id="4m2nq8"
streamlit run app.py
```

---

# Structure du projet

```text id="8c0xvz"
VidLis/
│
├── app.py
├── requirements.txt
├── README.md
└── assets/
```

---

# Fonctionnement

1. L’utilisateur fournit un lien YouTube
2. La transcription est récupérée
3. Le contenu est analysé par un modèle IA
4. Un rapport structuré est généré

---

# Objectif du projet

Transformer les contenus vidéo en connaissances structurées et directement exploitables.

---

# Améliorations futures

* Génération de quiz automatiques
* Flashcards intelligentes
* Mode apprentissage interactif
* Amélioration du support multilingue
* Personnalisation du niveau de détail

---

# Auteure

Lucia Adjinda

---

# Licence

Projet à but éducatif
