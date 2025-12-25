import streamlit as st
import requests
import matplotlib.pyplot as plt
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Mental Health Detection System",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .disclaimer {
        padding: 1rem;
        border-radius: 5px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🧠 Mental Health Detection System</div>', unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Ethical Disclaimer
st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This system is for academic purposes only and is not a medical diagnosis tool. 
        If you are experiencing mental health concerns, please consult with a qualified healthcare professional.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Text input area
st.markdown("### 📝 Enter Text for Analysis")
text_input = st.text_area(
    "Type or paste your text here:",
    height=150,
    placeholder="Enter your text here...",
    help="The model will analyze the text and classify it into one of three categories: Normal, Stress/Anxiety, or Depressed."
)

# Analyze button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

# Prediction results
if analyze_button:
    if not text_input or not text_input.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        with st.spinner("🔄 Analyzing text... Please wait."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    json={"text": text_input.strip()},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Prediction box
                    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
                    st.markdown("### 🎯 Prediction Result")
                    
                    # Highlighted label
                    label_color = {
                        "Normal": "🟢",
                        "Stress/Anxiety": "🟡",
                        "Depressed": "🔴"
                    }
                    emoji = label_color.get(result["label"], "⚪")
                    
                    st.markdown(f"**{emoji} Classification:** {result['label']}")
                    st.markdown(f"**📊 Confidence:** {result['confidence']*100:.2f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Probability visualization
                    st.markdown("### 📈 Probability Distribution")
                    
                    labels = list(result["probabilities"].keys())
                    probs = list(result["probabilities"].values())
                    colors = ["#2ecc71", "#f39c12", "#e74c3c"]
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    bars = ax.barh(labels, [p * 100 for p in probs], color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
                    
                    # Add value labels on bars
                    for i, (label, prob) in enumerate(zip(labels, probs)):
                        ax.text(prob * 100 + 1, i, f'{prob*100:.2f}%', 
                               va='center', fontsize=11, fontweight='bold')
                    
                    ax.set_xlabel('Probability (%)', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Category', fontsize=12, fontweight='bold')
                    ax.set_title('Classification Probabilities', fontsize=14, fontweight='bold', pad=20)
                    ax.set_xlim(0, 100)
                    ax.grid(axis='x', alpha=0.3, linestyle='--')
                    
                    # Highlight the predicted label
                    predicted_idx = labels.index(result["label"])
                    bars[predicted_idx].set_alpha(1.0)
                    bars[predicted_idx].set_edgecolor('black')
                    bars[predicted_idx].set_linewidth(2.5)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Detailed probabilities table
                    st.markdown("### 📋 Detailed Probabilities")
                    prob_data = {
                        "Category": labels,
                        "Probability (%)": [f"{p*100:.2f}" for p in probs]
                    }
                    st.dataframe(prob_data, use_container_width=True, hide_index=True)
                    
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Could not connect to the backend API. Please ensure the FastAPI server is running on http://localhost:8000")
                st.info("💡 Start the backend with: `uvicorn app.app:app --reload`")
            except requests.exceptions.Timeout:
                st.error("❌ Request Timeout: The server took too long to respond.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# Footer
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>Mental Health Detection System | Academic Project</p>
    </div>
""", unsafe_allow_html=True)




