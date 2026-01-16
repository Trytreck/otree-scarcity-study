import streamlit as st
import pandas as pd
import psycopg2

st.title("📊 Analyse Live - oTree")

# Connexion à la base de données
# Remplace par ton "External Database URL"
DB_URL = "TON_EXTERNAL_DATABASE_URL_ICI"


@st.cache_data(ttl=10)  # Rafraîchit les données toutes les 10 secondes
def load_data():
    conn = psycopg2.connect(DB_URL)
    # On récupère la table des joueurs de ton app Granjo2
    query = "SELECT * FROM granjo2_player"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


try:
    data = load_data()

    # Affichage de quelques stats
    st.metric("Nombre de participants", len(data))

    # Exemple : Moyenne des enchères
    if 'mon_enchere' in data.columns:
        moyenne = data['mon_enchere'].mean()
        st.subheader(f"Moyenne des enchères : {moyenne:.2f} €")
        st.bar_chart(data['mon_enchere'])

except Exception as e:
    st.error(f"Erreur de connexion : {e}")
