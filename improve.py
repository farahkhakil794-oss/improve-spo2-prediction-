import streamlit as st
import pandas as pd
import pickle
import numpy as np

# إعداد الصفحة لتكون احترافية
st.set_page_config(page_title="AI-SpO2 Professional", page_icon="🏥", layout="wide")

# 1. قاموس الترجمة (Localization Dictionary)
texts = {
    "English": {
        "header": "🏥 Smart SpO2 Prediction System",
        "sub": "Advanced AI-Powered Clinical Decision Support",
        "inputs": "📋 Clinical Patient Inputs",
        "run_btn": "🚀 Run Prediction",
        "result_title": "Clinical Assessment",
        "normal": "✅ Normal Condition (Stable)",
        "mild": "⚠️ Mild Hypoxia (Monitor Required)",
        "severe": "🚨 Severe Hypoxia (Immediate Action Required)",
        "site": "Measurement Site",
        "sites": ["Fingertip", "Wrist"]
    },
    "العربية": {
        "header": "🏥 المنظومة الذكية لتقدير نسبة الأكسجين (SpO2)",
        "sub": "نظام دعم قرار سريري متطور يعتمد على الذكاء الاصطناعي",
        "inputs": "📋 المدخلات السريرية للمريض",
        "run_btn": "🚀 احسب نسبة الأكسجين الفورية",
        "result_title": "التقرير الطبي والتقدير الفوري",
        "normal": "✅ حالة مستقرة وطبيعية (Normal)",
        "mild": "⚠️ حالة نقص أكسجين خفيف (يحتاج ملاحظة)",
        "severe": "🚨 حالة تدهور حاد (تدخل فوري)",
        "site": "مكان القياس الفعلي",
        "sites": ["الصبع (Fingertip)", "المعصم (Wrist)"]
    }
}

# اختيار اللغة من الشريط الجانبي
lang = st.sidebar.selectbox("Select Language / اختر اللغة", ["English", "العربية"])
t = texts[lang]

# 2. واجهة التطبيق
st.title(t["header"])
st.markdown(f"### *{t['sub']}*")
st.divider()

# 3. إدخال البيانات (Inputs)
col1, col2 = st.columns(2)
with col1:
    st.subheader(t["inputs"])
    age = st.slider("Age / العمر", 18, 90, 50)
    pr = st.slider("Pulse Rate (BPM) / معدل النبض", 40, 150, 70)
    stiffness = st.slider("Stiffness Index / مؤشر تصلب الشرايين", 5.0, 12.0, 8.5)
    site = st.selectbox(t["site"], t["sites"])

with col2:
    # محاكاة الرسم البياني
    st.subheader("📊 Pulse Signal Simulation")
    chart_data = pd.DataFrame(np.random.randn(20, 1) + 70, columns=['Pulse'])
    st.line_chart(chart_data)

# 4. المعالجة والنتيجة
if st.button(t["run_btn"]):
    # هنا يتم استدعاء الموديل (تأكدي من وجود الملف)
    # prediction = model.predict(features)
    prediction = 98.8 # مثال للتجربة
    
    st.divider()
    st.subheader(t["result_title"])
    
    # تحديد الحالة الطبية
    if prediction >= 95:
        status_text = t["normal"]
        color = "#10b981"
    elif 90 <= prediction < 95:
        status_text = t["mild"]
        color = "#f59e0b"
    else:
        status_text = t["severe"]
        color = "#ef4444"
        
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; border: 2px solid {color}; border-radius: 15px;">
            <h1 style="color: {color};">{prediction}%</h1>
            <h3>{status_text}</h3>
        </div>
    """, unsafe_allow_html=True)
