import streamlit as st
import pandas as pd
import pickle
import numpy as np
import os
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI-ICU | Medical Monitor", page_icon="🏥", layout="wide")

# 2. قاموس الترجمة والدعم الطبي
texts = {
    "English": {
        "header": "🏥 ICU AI-Medical Monitor",
        "sub": "Real-time SpO2 Estimation & Clinical Decision Support System",
        "vitals": "📋 Patient Vitals Input",
        "btn": "🚀 Analyze Patient",
        "status_title": "Clinical Diagnosis",
        "loading": "Analyzing signals...",
        "sites": ["Fingertip", "Wrist"]
    },
    "العربية": {
        "header": "🏥 نظام مراقبة العناية المركزة الذكي",
        "sub": "تقدير نسبة الأكسجين ونظام دعم القرار السريري",
        "vitals": "📋 إدخال المؤشرات الحيوية",
        "btn": "🚀 تحليل حالة المريض",
        "status_title": "التشخيص السريري",
        "loading": "جاري معالجة الإشارات...",
        "sites": ["إصبع (Fingertip)", "معصم (Wrist)"]
    }
}

# إعداد اللغة
lang = st.sidebar.selectbox("Select Language / اختر اللغة:", ["English", "العربية"])
t = texts[lang]

# 3. وظيفة التشخيص الطبي (Medical CDSS Logic)
def get_medical_status(spo2):
    if spo2 >= 95:
        return "✅ Normal (طبيعي)", "#10b981"
    elif 90 <= spo2 < 95:
        return "⚠️ Mild Hypoxia (منخفض - يحتاج ملاحظة)", "#f59e0b"
    else:
        return "🚨 Severe Hypoxia (خطر - تدخل فوري)", "#ef4444"

# 4. تحميل الموديل
model_path = 'reduced_spo2_model.pkl'
@st.cache_resource
def load_model():
    with open(model_path, 'rb') as f: return pickle.load(f)

model = load_model()

# 5. الواجهة الرسومية (UI)
st.markdown(f"## {t['header']}")
st.markdown(f"*{t['sub']}*")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.write(f"### {t['vitals']}")
    # 11 Features Input
    pwv = st.number_input("Pulse Wave Velocity (m/s)", value=8.64)
    p2p = st.number_input("Peak-to-Peak (ms)", value=855.90)
    ai = st.number_input("Augmentation Index (%)", value=10.30)
    pi = st.number_input("Perfusion Index (%)", value=4.26)
    pr = st.number_input("Pulse Rate (BPM)", value=70.0)
    sa = st.number_input("Systolic Amplitude", value=0.71)
    noise = st.number_input("Noise Level (dB)", value=-37.60)
    si = st.number_input("Stiffness Index (m/s)", value=8.67)
    age = st.number_input("Age", value=50)
    dt = st.number_input("Diastolic Time (ms)", value=521.90)
    site = st.selectbox(f"Sensor Site", t['sites'])
    msite = 0 if "Fingertip" in site else 1

with col2:
    st.write("### 📈 Patient Signal Simulation")
    # محاكاة موجة نبض حقيقية للـ Dashboard
    chart_data = pd.DataFrame(np.random.randn(20, 1) + 70, columns=['Pulse'])
    st.line_chart(chart_data)
    
    if st.button(t['btn']):
        with st.spinner(t['loading']):
            features = np.array([[pwv, p2p, ai, pi, pr, sa, noise, si, age, dt, msite]])
            prediction = model.predict(features)[0]
            status, color = get_medical_status(prediction)
            
            st.markdown(f"""
                <div style="background-color: {color}20; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
                    <h2 style="color: {color};">SpO2: {prediction:.2f}%</h2>
                    <h3>{t['status_title']}: <span style="color: {color};">{status}</span></h3>
                </div>
            """, unsafe_allow_html=True)

st.sidebar.info("💡 **Clinical Note:** This AI model provides high-precision estimation by analyzing vascular stiffness and signal noise, beyond standard linear equations.")
