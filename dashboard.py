import streamlit as st
import pandas as pd
import psycopg2

st.title("📊 Analyse Live - oTree")

# Connexion à la base de données
# Remplace par ton "External Database URL"
DB_URL = "postgresql://ma_base_otree_user:8mtdBRyT55FAlLDNWIgJGZl7Qn8aYFWQ@dpg-d5l7bmsoud1c7383cojg-a.frankfurt-postgres.render.com/ma_base_otree"


# 2. LA FONCTION (C'est ici qu'on la définit)
@st.cache_data(ttl=5)
def get_data():
    conn = psycopg2.connect(DB_URL)
    # Si 'granjo2_player' ne marche pas, essaie 'otree_player' 
    # ou vérifie le nom exact comme vu précédemment
    query = 'SELECT * FROM granjo2_player' 
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
