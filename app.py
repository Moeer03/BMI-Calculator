import streamlit as st
from datetime import datetime

# Store past results
if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []

st.set_page_config(page_title="Advanced BMI Calculator", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
        .main {background-color: #f0f2f6;}
        .stTabs [data-baseweb="tab"] {font-size:18px; font-weight:600}
    </style>
""", unsafe_allow_html=True)

st.title("🏋️ Advanced BMI Calculator")

# --- Layout: Tabs ---
tab1, tab2 = st.tabs(["💡 Calculator", "📊 History"])

with tab1:
    col1, col2 = st.columns(2)

    # Gender input (optional)
    gender = col1.selectbox("Gender (optional)", ["Prefer not to say", "Male", "Female", "Other"])

    # Height input
    height_unit = col1.selectbox("Height unit", ["cm", "feet/inches"])
    if height_unit == "cm":
        height = col1.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
    else:
        feet = col1.number_input("Feet", min_value=1, max_value=8)
        inches = col1.number_input("Inches", min_value=0, max_value=11)
        height = (feet * 12 + inches) * 2.54

    # Weight input
    weight_unit = col2.selectbox("Weight unit", ["kg", "lbs"])
    if weight_unit == "kg":
        weight = col2.number_input("Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)
    else:
        weight_lbs = col2.number_input("Weight (lbs)", min_value=20.0, max_value=660.0, step=0.1)
        weight = weight_lbs * 0.453592

    # Calculate BMI
    if height > 0 and weight > 0:
        with st.spinner("Calculating BMI..."):
            bmi = round(weight / ((height / 100) ** 2), 1)

            # Categorization
            if bmi < 18.5:
                category = "Underweight"
                color = "🔵"
                advice = "Consider eating more balanced meals and consult a dietitian."
            elif 18.5 <= bmi < 25:
                category = "Normal"
                color = "🟢"
                advice = "Great job! Keep up the healthy lifestyle."
                st.balloons()
            elif 25 <= bmi < 30:
                category = "Overweight"
                color = "🟠"
                advice = "Consider regular exercise and watching your calorie intake."
            else:
                category = "Obese"
                color = "🔴"
                advice = "Seek medical advice and consider a structured weight loss plan."

            st.metric(label="Your BMI", value=f"{bmi} ({category})")

            st.progress(min(bmi / 40, 1.0))

            st.markdown(f"**{color} Health Advice:** {advice}")

            # Save result
            if st.button("💾 Save result"):
                st.session_state.bmi_history.insert(0, {
                    "bmi": bmi,
                    "category": category,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Result saved!")

            if st.button("🔄 Reset"):
                if hasattr(st, "rerun"):
                    st.rerun()
                else:
                    st.experimental_rerun()



with tab2:
    st.subheader("📅 Last 5 BMI Records")
    if st.session_state.bmi_history:
        for entry in st.session_state.bmi_history[:5]:
            st.write(f"{entry['timestamp']}: **{entry['bmi']} ({entry['category']})**")
    else:
        st.info("No history yet. Save your BMI to see it here.")

