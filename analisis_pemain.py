import streamlit as st
import pandas as pd
import numpy as np
import joblib

def show():
    # =========================
    # LOAD MODEL DAN SCALER
    # =========================
    model = joblib.load("random_forest_model.pkl")
    scaler = joblib.load("scaler_rf.pkl")  # tetap ada (tidak dihapus)

    df = pd.read_csv("sell_players.csv")  # dataset SUDAH scaling

    st.title("Analisis Performa Pemain Sepak Bola")
    st.write("Sistem Machine Learning untuk merekomendasikan pemain yang sebaiknya dijual/dipertahankan berdasarkan performa.")

    st.divider()

    # =========================
    # DEFAULT STATE
    # =========================
    default_values = {
        "player_name": "",
        "total_attempts": 0.0,
        "blocked": 0.0,
        "attempts_match_played": 0.0,
        "balls_recoverd": 0.0,
        "tackles": 0.0,
        "clearance_attempted": 0.0,
        "fouls_committed": 0.0,
        "fouls_suffered": 0.0,
        "red": 0.0,
        "pass_accuracy": 0.0,
        "pass_attempted": 0.0,
        "cross_accuracy": 0.0,
        "cross_attempted": 0.0,
        "freekicks_taken": 0.0,
        "distance_covered": 0.0,
        "performance_score": 0.0
    }

    def init_state():
        for k, v in default_values.items():
            if k not in st.session_state:
                st.session_state[k] = v

    init_state()

    # =========================
    # RESET BUTTON
    # =========================
    col_btn1, col_btn2 = st.columns([12,1])
    with col_btn2:
        if st.button("🔄 Reset"):
            for k, v in default_values.items():
                st.session_state[k] = v
            st.rerun()

    # =========================
    # INPUT
    # =========================
    st.subheader("Input Statistik Performa Pemain")

    # 🔥 AUTO FILL
    player_input = st.text_input("Nama Pemain", key="player_name")

    if player_input:
        match = df[df["player_name"].astype(str).str.lower().str.contains(player_input.lower())]

        if not match.empty:
            player_data = match.iloc[0]
            st.success(f"Pemain ditemukan: {player_data['player_name']}")

            for key in default_values.keys():
                if key != "player_name":
                    st.session_state[key] = float(player_data.get(key, 0))
        else:
            st.warning("Pemain tidak ditemukan")

    def input_row(label, key):
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write(label)
        with col2:
            return st.number_input(label, key=key, label_visibility="collapsed")

    colA, colB = st.columns(2)

    with colA:
        total_attempts = input_row("Total Attempts", "total_attempts")
        blocked = input_row("Blocked", "blocked")
        attempts_match_played = input_row("Attempts Match Played", "attempts_match_played")
        balls_recoverd = input_row("Balls Recovered", "balls_recoverd")
        tackles = input_row("Tackles", "tackles")
        clearance_attempted = input_row("Clearance Attempted", "clearance_attempted")
        fouls_committed = input_row("Fouls Committed", "fouls_committed")
        fouls_suffered = input_row("Fouls Suffered", "fouls_suffered")

    with colB:
        red = input_row("Red Card", "red")
        pass_accuracy = input_row("Pass Accuracy", "pass_accuracy")
        pass_attempted = input_row("Pass Attempted", "pass_attempted")
        cross_accuracy = input_row("Cross Accuracy", "cross_accuracy")
        cross_attempted = input_row("Cross Attempted", "cross_attempted")
        freekicks_taken = input_row("Freekicks Taken", "freekicks_taken")
        distance_covered = input_row("Distance Covered", "distance_covered")
        performance_score = input_row("Performance Score (Similarity)", "performance_score")

    st.divider()

    # =========================
    # ANALISIS
    # =========================
    if st.button("Analisis Pemain"):

        input_data = np.array([[ 
            total_attempts,
            blocked,
            attempts_match_played,
            balls_recoverd,
            tackles,
            clearance_attempted,
            fouls_committed,
            fouls_suffered,
            red,
            pass_accuracy,
            pass_attempted,
            cross_accuracy,
            cross_attempted,
            freekicks_taken,
            distance_covered
        ]])

        # 🔥 FIX: NO DOUBLE SCALING
        input_scaled = input_data

        prediction = model.predict(input_scaled)[0]
        prob = model.predict_proba(input_scaled)
        sell_prob = prob[0][1] * 100

        st.subheader(f"Hasil Analisis: {st.session_state.player_name if st.session_state.player_name else 'Tanpa Nama'}")

        reasons = []

        if pass_accuracy < 0.7:
            reasons.append("Akurasi passing rendah")
        if tackles < 0.3:
            reasons.append("Kontribusi defensif rendah")
        if balls_recoverd < 0.3:
            reasons.append("Kemampuan merebut bola rendah")
        if fouls_committed > 0.5:
            reasons.append("Terlalu sering melakukan pelanggaran")
        if red > 0:
            reasons.append("Memiliki riwayat kartu merah")
        if distance_covered < 0.5:
            reasons.append("Mobilitas rendah")
        if total_attempts < 0.3:
            reasons.append("Minim kontribusi serangan")

        if prediction == 1:
            st.error(f"⚠️ Rekomendasi: Pemain Sebaiknya Dijual (Confidence {sell_prob:.2f}%)")

            st.markdown("**Keterangan:**")
            st.write("Sistem menggunakan threshold sebesar 0.2 sebagai batas performa.")
            st.write("Pemain dengan nilai di bawah atau sama dengan threshold dianggap memiliki performa rendah dan direkomendasikan untuk dijual.")

            st.markdown("**Alasan:**")
            for r in reasons:
                st.write(f"- {r}")

        else:
            st.success(f"✅ Rekomendasi: Pemain Layak Dipertahankan (Confidence {100 - sell_prob:.2f}%)")

            st.markdown("**Keterangan:**")
            st.write("Sistem menggunakan threshold sebesar 0.2 sebagai batas performa.")
            st.write("Pemain dengan nilai di atas threshold dianggap memiliki performa baik dan layak dipertahankan.")

            # 🔥 ALASAN KEEP (DITAMBAHKAN)
            st.markdown("**Alasan:**")

            keep_reasons = []

            if pass_accuracy >= 0.7:
                keep_reasons.append("Akurasi passing baik")
            if tackles >= 0.3:
                keep_reasons.append("Kontribusi defensif baik")
            if balls_recoverd >= 0.3:
                keep_reasons.append("Kemampuan merebut bola baik")
            if fouls_committed <= 0.5:
                keep_reasons.append("Disiplin dalam bermain (minim pelanggaran)")
            if red == 0:
                keep_reasons.append("Tidak memiliki riwayat kartu merah")
            if distance_covered >= 0.5:
                keep_reasons.append("Mobilitas tinggi di lapangan")
            if total_attempts >= 0.3:
                keep_reasons.append("Aktif dalam kontribusi serangan")

            if keep_reasons:
                for r in keep_reasons:
                    st.write(f"- {r}")
            else:
                st.write("- Performa pemain stabil di berbagai aspek")

    st.divider()

    # =========================
    # DATASET
    # =========================
    st.subheader("Dataset All Players")

    st.markdown("""
    <style>
    [data-testid="stDataFrame"] { background-color: white !important; border-radius: 10px; }
    [data-testid="stDataFrame"] thead th { color: black !important; background-color: #f0f0f0 !important; }
    [data-testid="stDataFrame"] tbody td { color: black !important; background-color: white !important; }
    [data-testid="stDataFrame"] tbody th { color: black !important; background-color: white !important; }
    [data-testid="stDataFrame"] tbody tr:hover td { background-color: #f5c518 !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

    df_display = df[["player_name", "club", "position"]]
    st.dataframe(df_display, use_container_width=True, height=400)
    # =========================
# MODEL ML
# =========================
    st.divider()
    st.caption("Model: Random Forest Classifier")