import streamlit as st
import pandas as pd
import psycopg2

# 1. Configuration de la page
st.set_page_config(page_title="Live oTree Dashboard", layout="wide")
st.title("📊 Analyse des données en temps réel")

# 2. Ta connexion (Vérifie bien que c'est l'URL EXTERNAL de Render)
DB_URL = "TON_EXTERNAL_DATABASE_URL_ICI"

# 3. Définition de la fonction (On l'appelle 'load_data' ici)
@st.cache_data(ttl=5)
def load_data():
    conn = psycopg2.connect(DB_URL)
    # On essaye de lire la table. Si tu as toujours l'erreur "relation does not exist", 
    # vérifie le nom 'granjo2_player'
    query = "SELECT * FROM granjo2_player"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# 4. Appel de la fonction et affichage
try:
    # C'est ici qu'on utilise le nom défini plus haut
    data = load_data()
    
    st.success("Connexion établie avec succès !")
    
    # Affichage rapide
    st.metric("Nombre de participants", len(data))
    
    # Affichage du tableau de données
    st.subheader("Données brutes")
    st.dataframe(data)

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Astuce : Si l'erreur dit 'name not defined', vérifiez que le nom après 'def' est identique à celui de l'appel.")
