import streamlit as st
import pandas as pd

# =========================
# FIX CSS KHUSUS SELECTBOX (PAKSA DI HALAMAN INI)
# =========================
st.markdown("""
<style>


/* SELECTBOX INPUT */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.95) !important;
    color: black !important;
}

div[data-baseweb="select"] * {
    color: black !important;
}

/* DROPDOWN POPUP */
body div[data-baseweb="popover"] {
    background-color: white !important;
}

body div[data-baseweb="menu"] {
    background-color: white !important;
}

/* ITEM */
body div[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* HOVER */
body div[role="option"]:hover {
    background-color: #f5c518 !important;
    color: black !important;
}

/* SELECTED */
body div[aria-selected="true"] {
    background-color: #f5c518 !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)


# load data
df = pd.read_csv("team_weakness_analysis.csv")

# mapping biar lebih readable
mapping = {
    'pass_accuracy': 'Akurasi Passing',
    'balls_recoverd': 'Recovery Bola',
    'goals': 'Produktivitas Gol'
}

# function ambil data
def get_team_analysis(team_name):
    team_data = df[df['club'] == team_name]

    if team_data.empty:
        return None

    team_data = team_data.iloc[0]

    factor_raw = team_data['weak_factor']
    factor = mapping.get(factor_raw, factor_raw)

    return {
        "team": team_data['club'],
        "category": team_data['category'],
        "factor": factor,
        "importance": float(team_data['feature_importance']),
        "score": float(team_data['performance_score'])
    }


# function tampilan
def show():
    st.title("Analisis Kelemahan Team")
    st.write("Sistem Machine Learning untuk menganalisis kelemahan pada setiap team berdasarkan performance score dan feature importance.")
    
    st.divider()

    team = st.selectbox("Pilih Tim", df['club'].unique())

    result = get_team_analysis(team)

    if result:
        st.subheader(result['team'])

        # =========================
        # STATUS TIM
        # =========================
        if result['category'] == "Weak Team":
            st.error("⚠️ Tim ini tergolong LEMAH")
            st.write("Kelemahan Utama:")
            st.write(f"**{result['factor']}**")
            st.info(f"Tim perlu meningkatkan **{result['factor']}** untuk performa lebih baik.")
        else:
            st.success("✅ Tim ini tergolong KUAT")
            st.write("Kekuatan Utama:")
            st.write(f"**{result['factor']}**")
            st.info(f"Kekuatan utama tim ada pada **{result['factor']}**.")

        # =========================
        # METRICS
        # =========================
        st.write("---")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("PERFORMA SCORE", f"{result['score']:.2f}")

        with col2:
            st.metric("FEATURE IMPORTANCE", f"{result['importance']*100:.1f}%")

        # =========================
        # PENJELASAN MODEL
        # =========================
        st.write("---")
        st.markdown("**Penjelasan Perhitungan**")

        st.info(f"""
**PERFORMA SCORE**  
Dihitung sebagai rata-rata dari fitur yang mempengaruhi performa tim.
Nilai ini merepresentasikan performa keseluruhan tim berdasarkan statistik.

**FEATURE IMPORTANCE ({result['factor']})**  
Diperoleh dari model Random Forest melalui feature importance.
Nilai ini menunjukkan seberapa besar pengaruh faktor terhadap performa tim.

Semakin tinggi nilainya, semakin besar pengaruhnya.
""")

    st.divider()
    st.caption("Model: Random Forest Classifier + (Feature Importance)")