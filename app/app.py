import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sys
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Feature extractor
sys.path.append(os.path.join(BASE_DIR, "features"))
from feature_extractor import extract_features

# Load model and scaler
model = joblib.load(os.path.join(BASE_DIR, "model", "phishing_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "model", "scaler.pkl"))



LABEL_MAP = {
    0: "Legitimate",
    1: "Phishing"
}

st.set_page_config(page_title="Phishing Detection System", layout="centered")

st.title("🔐 Phishing Detection System")
st.write("Paste a URL to check whether it is **Phishing** or **Legitimate**.")

st.markdown("---")

url_input = st.text_input("Enter URL", placeholder="https://example.com")

if st.button("🔍 Analyze URL"):
    if url_input.strip() == "":
        st.warning("Please enter a URL")
    else:
        features = extract_features(url_input)
        feature_df = pd.DataFrame([features])

        # Ensure correct feature order
        feature_df = feature_df[scaler.feature_names_in_]

        scaled_features = scaler.transform(feature_df)

        # Prediction
        prediction = model.predict(scaled_features)[0]
        probabilities = model.predict_proba(scaled_features)[0]

        # Get index of predicted class
        class_index = list(model.classes_).index(prediction)
        confidence = probabilities[class_index]

        st.markdown("---")

        # 🚨 CORRECT LABEL MAPPING
        if prediction == 1:
            st.error(f"🚨 Phishing Website Detected!\n\nConfidence: {confidence:.2f}")
        else:
            st.success(f"✅ Legitimate Website\n\nConfidence: {confidence:.2f}")

        # Debug info (keep for now)
        st.caption(f"Model classes: {model.classes_}")

