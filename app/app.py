# app/streamlit_app.py
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import os
from pathlib import Path

# Hugging Face model ID - update this with your Hugging Face username/model name
# This will be used as fallback when local model files are not available (e.g., on Streamlit Cloud)
HUGGING_FACE_MODEL_ID = os.getenv("HUGGING_FACE_MODEL_ID", "Sanjeev2004/mh_3class_distil_final")

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
    """
    Get the model path, handling different execution contexts. 
    Returns absolute path string if local files exist, or None to use Hugging Face Hub.
    """
    # Try absolute path from current file location first (most reliable)
    try:
        current_file = Path(__file__).resolve()  # app/app.py
        project_root = current_file.parent.parent  # Go up from app/ to project root
        model_path = project_root / "models" / "base_model" / "mh_3class_distil_final"
        if model_path.exists() and (model_path / "model.safetensors").exists():
            return str(model_path.resolve())  # Return absolute path
    except Exception as e:
        print(f"Error resolving path from __file__: {e}")
    
    # Fallback to relative path (convert to absolute)
    model_path_str = "models/base_model/mh_3class_distil_final"
    model_path = Path(model_path_str)
    if model_path.exists() and (model_path / "model.safetensors").exists():
        return str(model_path.resolve())  # Return absolute path
    
    # Last resort: try current working directory
    try:
        cwd_model_path = Path.cwd() / "models" / "base_model" / "mh_3class_distil_final"
        if cwd_model_path.exists() and (cwd_model_path / "model.safetensors").exists():
            return str(cwd_model_path.resolve())  # Return absolute path
    except Exception as e:
        print(f"Error checking cwd path: {e}")
    
    return None  # Return None to indicate we should use Hugging Face Hub

@st.cache_resource
def load_model():
    """Load and cache the model and tokenizer. Falls back to Hugging Face Hub if local files not found."""
    try:
        model_path = get_model_path()
        
        # If local path not found, use Hugging Face Hub
        if model_path is None:
            st.info(f"📥 Local model files not found. Loading from Hugging Face Hub: `{HUGGING_FACE_MODEL_ID}`")
            with st.spinner("🔄 Downloading model from Hugging Face Hub... This may take a moment on first run."):
                try:
                    model = AutoModelForSequenceClassification.from_pretrained(HUGGING_FACE_MODEL_ID)
                    tokenizer = AutoTokenizer.from_pretrained(HUGGING_FACE_MODEL_ID)
                except Exception as hf_error:
                    error_msg = f"""
**Error loading model from Hugging Face Hub:**

Model ID: `{HUGGING_FACE_MODEL_ID}`

Error: {str(hf_error)}

**Solutions:**
1. **Upload your model to Hugging Face Hub:**
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   python -c "
   from huggingface_hub import HfApi
   api = HfApi()
   api.upload_folder(
       folder_path='models/base_model/mh_3class_distil_final',
       repo_id='YOUR_USERNAME/mh_3class_distil_final',
       repo_type='model'
   )
   "
   ```

2. **Update the model ID** in `app/app.py`:
   ```python
   HUGGING_FACE_MODEL_ID = "YOUR_USERNAME/mh_3class_distil_final"
   ```

3. **Or set it via environment variable** in Streamlit Cloud secrets:
   ```
   HUGGING_FACE_MODEL_ID=YOUR_USERNAME/mh_3class_distil_final
   ```
                    """
                    st.error(error_msg)
                    st.stop()
        else:
            # Verify model files exist before loading
            model_path_obj = Path(model_path)
            required_files = ["model.safetensors", "config.json", "tokenizer.json"]
            missing_files = [f for f in required_files if not (model_path_obj / f).exists()]
            if missing_files:
                st.warning(f"⚠️ Some model files missing locally. Falling back to Hugging Face Hub: `{HUGGING_FACE_MODEL_ID}`")
                with st.spinner("🔄 Loading model from Hugging Face Hub..."):
                    model = AutoModelForSequenceClassification.from_pretrained(HUGGING_FACE_MODEL_ID)
                    tokenizer = AutoTokenizer.from_pretrained(HUGGING_FACE_MODEL_ID)
            else:
                # Load from local path
                with st.spinner("🔄 Loading model from local files... This may take a moment on first run."):
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
        st.error(f"❌ File not found: {str(e)}")
        st.error("💡 Trying to load from Hugging Face Hub instead...")
        # Try Hugging Face as last resort
        try:
            with st.spinner("🔄 Attempting to load from Hugging Face Hub..."):
                model = AutoModelForSequenceClassification.from_pretrained(HUGGING_FACE_MODEL_ID)
                tokenizer = AutoTokenizer.from_pretrained(HUGGING_FACE_MODEL_ID)
                model.eval()
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                model.to(device)
                return model, tokenizer, device
        except Exception as hf_error:
            st.error(f"❌ Also failed to load from Hugging Face Hub: {str(hf_error)}")
            st.stop()
    except Exception as e:
        error_detail = f"""
**Error:** {str(e)}

**Troubleshooting:**
1. **For local development:** Verify model files exist in `models/base_model/mh_3class_distil_final/`
2. **For Streamlit Cloud:** Ensure model is uploaded to Hugging Face Hub and `HUGGING_FACE_MODEL_ID` is set correctly
3. Check that the model ID `{HUGGING_FACE_MODEL_ID}` exists on Hugging Face Hub
        """
        st.error(f"❌ Error loading model")
        st.error(error_detail)
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

import re

def clean_text(text: str) -> str:
    """Clean text to match training preprocessing"""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

if analyze_button:
    if not text.strip():
        st.warning("⚠️ Please enter some text to analyze.")
    else:
        try:
            # Load model
            model, tokenizer, device = load_model()
            
            # Preprocess text
            cleaned_text = clean_text(text)
            
            # Tokenize input
            with st.spinner("🔄 Processing..."):
                inputs = tokenizer(
                    cleaned_text,
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
