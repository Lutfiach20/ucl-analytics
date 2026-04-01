import streamlit as st

st.set_page_config(page_title="Football Analytics System", layout="wide")

# =========================
# CUSTOM CSS (FINAL FIX ALL)
# =========================

st.markdown("""
<style>
/* =========================
   FIX ICON DATAFRAME
   ========================= */

/* container toolbar */
[data-testid="stDataFrame"] button {
    color: black !important;
}

/* icon svg */
[data-testid="stDataFrame"] svg {
    fill: black !important;
    color: black !important;
    opacity: 1 !important;
}

/* hover icon */
[data-testid="stDataFrame"] button:hover svg {
    fill: #f5c518 !important;
    color: #f5c518 !important;
}

/* BACKGROUND UCL */
.stApp {
    background: linear-gradient(rgba(11,29,58,0.95), rgba(11,29,58,0.95)),
    url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* spacing */
.block-container {
    padding-top: 2.3rem;
    padding-bottom: 1rem;
}

/* text */
h1, h2, h3 {
    margin-bottom: 0.4rem;
    color: #f5c518;
}

p, label, div {
    color: #e6e6e6;
}

/* divider */
hr {
    margin: 0.8rem 0;
    border: 1px solid rgba(255,255,255,0.1);
}

/* button */
.stButton > button {
    background-color: #f5c518;
    color: black;
    border-radius: 8px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #ffd700;
}

/* =========================
   INPUT FIX
   ========================= */
.stNumberInput input, .stTextInput input {
    background-color: rgba(255,255,255,0.95) !important;
    color: black !important;
}

.stNumberInput input::placeholder,
.stTextInput input::placeholder {
    color: #555 !important;
}

/* =========================
   SELECTBOX FIX (FINAL)
   ========================= */

/* box */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.95) !important;
}

/* text select */
div[data-baseweb="select"] span {
    color: black !important;
    opacity: 1 !important;
}

/* popup dropdown */
body div[data-baseweb="popover"] {
    background-color: white !important;
}

/* FORCE semua text dropdown */
body div[data-baseweb="popover"] * {
    color: black !important;
    opacity: 1 !important;
}

/* item */
body div[role="option"] {
    background-color: white !important;
    color: black !important;
}

/* hover */
body div[role="option"]:hover {
    background-color: #f5c518 !important;
    color: black !important;
}

/* selected */
body div[aria-selected="true"] {
    background-color: #f5c518 !important;
    color: black !important;
}

/* dataframe */
[data-testid="stDataFrame"] {
    background-color: rgba(255,255,255,0.05);
}

</style>
""", unsafe_allow_html=True)



# =========================
# STATE NAVIGASI
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

menu = st.session_state.page


# =========================
# HOME
# =========================
if menu == "home":

    st.title("UCL | Matches & Players Data")
    st.markdown("### UEFA Champions League Analytics Dashboard")
    
    # 🔥 UPDATED CAPTION + SOURCE
    st.caption("Data: UCL Matches & Players | Season 2021–2022 | Source: Kaggle (Azmine Toushik Wasi)")

    st.markdown(
        "[Dataset Link](https://www.kaggle.com/datasets/azminetoushikwasi/ucl-202122-uefa-champions-league)"
    )
    st.markdown(
    "👨‍💻 Developed by **Achmad Lutfi** | [LinkedIn](https://www.linkedin.com/in/achmadlutfi20)"
    )

    st.write("---")

    st.subheader("About UEFA Champions League")

    st.markdown("""
    <div style="text-align: justify; line-height:1.6;">
    UEFA Champions League adalah kompetisi sepak bola tahunan antar klub terbaik di Eropa.
    Tim bersaing melalui fase grup hingga knockout untuk menentukan juara terbaik.<br><br>
    Dashboard ini digunakan untuk menganalisis performa tim dan pemain berdasarkan data statistik.
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("Challenge")

    st.markdown("""
    - Discover the weak points of any team  
    - Suggest players to be sold based on performance analysis  
    """)

    st.write("---")

    st.subheader("Start Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Analisis Pemain")
        st.write("Evaluasi performa pemain untuk keputusan transfer.")

        if st.button("Analisis Pemain"):
            st.session_state.page = "Analisis Pemain"
            st.rerun()

    with col2:
        st.markdown("### 📉 Weakness Tim")
        st.write("Identifikasi kelemahan utama dalam tim.")

        if st.button("Analisis Tim"):
            st.session_state.page = "Weakness Tim"
            st.rerun()


# =========================
# ANALISIS PEMAIN
# =========================
elif menu == "Analisis Pemain":

    st.write("")

    col1, col2 = st.columns([12,1])
    with col2:
        if st.button("⬅ Home"):
            st.session_state.page = "home"
            st.rerun()

    from analisis_pemain import show
    show()


# =========================
# WEAKNESS TIM
# =========================
elif menu == "Weakness Tim":

    st.write("")

    col1, col2 = st.columns([12,1])
    with col2:
        if st.button("⬅ Home"):
            st.session_state.page = "home"
            st.rerun()

    from weakness import show
    show()