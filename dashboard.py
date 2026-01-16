import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Live oTree Dashboard", layout="wide")
st.title("📊 Résultats de l'étude en Direct")

# --- ÉTAPE CRUCIALE : COLLEZ VOTRE LIEN ICI ---
# Exemple de format attendu : "postgres://user:password@host:port/database"
DB_URL = "postgresql://ma_base_otree_user:8mtdBRyT55FAlLDNWIgJGZl7Qn8aYFWQ@dpg-d5l7bmsoud1c7383cojg-a.frankfurt-postgres.render.com/ma_base_otree"

@st.cache_data(ttl=5)
def load_data():
    conn = psycopg2.connect(DB_URL)
    # Cette requête magique liste TOUTES les tables de votre étude
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- EXÉCUTION ---
try:
    # On appelle bien 'load_data' qui est défini juste au-dessus
    data = load_data()
    
    st.success("✅ Connecté à la base de données Render")
    
    # Affichage des statistiques
    st.metric("Nombre de participants", len(data))
    
    # Affichage du tableau
    st.subheader("Détail des réponses")
    st.dataframe(data)

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.info("Vérifiez que vous avez bien remplacé 'TON_EXTERNAL_DATABASE_URL_ICI' par votre vrai lien postgres:// dans le code.")
