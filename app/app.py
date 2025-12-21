# app/streamlit_app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Mental Health Detector",
    page_icon="😌",
    layout="centered"
)

st.title("Mental Health Detector 😌")
st.markdown("Enter text below to analyze mental health state using AI.")

# Sidebar for info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This tool uses a fine-tuned DistilBERT model to classify text into:
    - **Normal**: Healthy mental state
    - **Stress/Anxiety**: Signs of stress or anxiety
    - **Depressed**: Signs of depression
    
    **Note**: This is a tool for research/educational purposes and should not replace professional medical advice.
    """)

# Get model path - handle both relative and absolute paths
def get_model_path():
    """Get the model path, handling different execution contexts."""
    model_path = "models/base_model/mh_3class_distil_final"
    if not os.path.exists(model_path):
        # Try absolute path from current file location
        try:
            current_dir = Path(__file__).parent.parent
            model_path = current_dir / "models" / "base_model" / "mh_3class_distil_final"
            if not model_path.exists():
                return None
        except:
            return None
    return str(model_path)

@st.cache_resource
def load_model():
    """Load and cache the model and tokenizer."""
    try:
        model_path = get_model_path()
        if model_path is None:
            raise FileNotFoundError("Model directory not found. Please ensure the model is in 'models/base_model/mh_3class_distil_final/'")
        
        with st.spinner("🔄 Loading model... This may take a moment on first run."):
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model.eval()  # Set to evaluation mode
            
            # Move to GPU if available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
        
        # Show device info in sidebar (only once)
        if torch.cuda.is_available():
            st.sidebar.success(f"✅ Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            st.sidebar.info("ℹ️ Using CPU")
        
        return model, tokenizer, device
    except FileNotFoundError as e:
        st.error(f"❌ {str(e)}")
        st.error("Please ensure the model files are in the correct location.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        st.error("Please check if the model files are properly configured and try again.")
        st.stop()

# Text input
text = st.text_area(
    "Type message here:",
    height=150,
    placeholder="Example: I've been feeling really stressed lately with all the work deadlines..."
)

col1, col2 = st.columns([1, 4])
with col1:
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)

if analyze_button:
    if not text.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        try:
            # Load model
            model, tokenizer, device = load_model()
            
            # Tokenize input
            with st.spinner("🔄 Processing..."):
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=128
                )
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                # Get prediction
                with torch.no_grad():
                    outputs = model(**inputs)
                    logits = outputs.logits
                    probs = F.softmax(logits, dim=-1).cpu().numpy()[0]
            
            # Labels mapping
            labels = ["normal", "stress_anxiety", "depressed"]
            label_display = {
                "normal": "Normal",
                "stress_anxiety": "Stress/Anxiety",
                "depressed": "Depressed"
            }
            
            idx = probs.argmax()
            predicted_label = labels[idx]
            confidence = probs[idx]
            
            # Display results
            st.success("✅ Analysis Complete!")
            
            # Main prediction with color coding
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("### 📊 Prediction Result")
                # Color-coded result
                if predicted_label == "normal":
                    st.success(f"**{label_display[predicted_label]}**")
                elif predicted_label == "stress_anxiety":
                    st.warning(f"**{label_display[predicted_label]}**")
                else:
                    st.error(f"**{label_display[predicted_label]}**")
            
            with col2:
                st.metric("Confidence", f"{confidence*100:.1f}%")
            
            # Probability distribution
            st.markdown("### 📈 Probability Distribution")
            prob_data = {
                label_display[label]: float(prob) 
                for label, prob in zip(labels, probs)
            }
            
            # Bar chart
            st.bar_chart(prob_data)
            
            # Detailed probabilities
            with st.expander("📋 View Detailed Probabilities"):
                for label, prob in zip(labels, probs):
                    st.progress(float(prob), text=f"{label_display[label]}: {prob*100:.2f}%")
            
            # Suggestions
            st.markdown("### 💡 Suggestions")
            suggestions = {
                "normal": "Keep going! 😊 You're doing well. Continue maintaining healthy habits and self-care routines.",
                "stress_anxiety": """
                **Try these techniques:**
                - Take a short break and practice deep breathing
                - Try the 5-4-3-2-1 grounding exercise: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste
                - Consider talking to someone you trust
                - Practice mindfulness or meditation
                """,
                "depressed": """
                **Important steps:**
                - Consider talking to someone you trust (friend, family, or professional)
                - Remember: You're not alone, and there are people who care about you
                - If you're in crisis, please reach out to a mental health professional or crisis hotline
                - Small steps matter: try to maintain a routine, get some fresh air, or do something you used to enjoy
                """
            }
            
            if predicted_label == "normal":
                st.info(suggestions[predicted_label])
            elif predicted_label == "stress_anxiety":
                st.warning(suggestions[predicted_label])
            else:
                st.error(suggestions[predicted_label])
            
            # Disclaimer
            st.markdown("---")
            st.caption("⚠️ **Disclaimer**: This tool is for educational/research purposes only and should not replace professional medical advice or diagnosis.")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.error("Please try again or check if the model files are properly configured.")
