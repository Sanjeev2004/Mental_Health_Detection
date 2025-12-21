import pandas as pd
import re
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

# -------------------------------
# 1. DATA HANDLING
# -------------------------------

def load_data(path):
    """Load CSV data."""
    return pd.read_csv(path)

def split_data(df, test_size=0.2, random_state=42):
    """Split dataset into train and test."""
    return train_test_split(df, test_size=test_size, random_state=random_state)

# -------------------------------
# 2. TEXT CLEANING
# -------------------------------

def clean_text(text):
    """Remove links, symbols, and extra spaces."""
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    return text.lower().strip()

def preprocess_dataframe(df, text_col):
    """Apply text cleaning to entire dataframe."""
    df[text_col] = df[text_col].astype(str).apply(clean_text)
    return df

# -------------------------------
# 3. MODEL INPUT PREPARATION
# -------------------------------

def encode_texts(tokenizer, texts, max_length=128):
    """Tokenize and encode a batch of texts."""
    return tokenizer(
        list(texts),
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )

# -------------------------------
# 4. EVALUATION METRICS
# -------------------------------

def evaluate_predictions(preds, labels, label_names=None):
    """Compute and print classification metrics."""
    preds = torch.argmax(preds, dim=1).cpu().numpy()
    labels = labels.cpu().numpy()
    print("Accuracy:", accuracy_score(labels, preds))
    print(classification_report(labels, preds, target_names=label_names))

# -------------------------------
# 5. LOGGING
# -------------------------------

def log(message):
    print(f"[INFO] {message}")

# -------------------------------
# 6. MODEL LOADING AND INFERENCE
# -------------------------------

MODEL_PATH = "models/base_model/mh_3class_distil_final"
LABEL_MAPPING = {
    "normal": "Normal",
    "stress_anxiety": "Stress/Anxiety",
    "depressed": "Depressed"
}

_tokenizer = None
_model = None

def load_tokenizer():
    """Load and return the tokenizer."""
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    return _tokenizer

def load_model():
    """Load and return the model."""
    global _model
    if _model is None:
        _model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
        _model.eval()
    return _model

def predict(text):
    """
    Predict mental health classification for given text.
    
    Args:
        text: Input text string
        
    Returns:
        dict: {
            "label": str,
            "confidence": float,
            "probabilities": {
                "Normal": float,
                "Stress/Anxiety": float,
                "Depressed": float
            }
        }
    """
    tokenizer = load_tokenizer()
    model = load_model()
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=-1).detach().numpy()[0]
    
    label_ids = ["normal", "stress_anxiety", "depressed"]
    predicted_idx = probabilities.argmax()
    predicted_label_id = label_ids[predicted_idx]
    
    probabilities_dict = {
        LABEL_MAPPING["normal"]: float(probabilities[0]),
        LABEL_MAPPING["stress_anxiety"]: float(probabilities[1]),
        LABEL_MAPPING["depressed"]: float(probabilities[2])
    }
    
    return {
        "label": LABEL_MAPPING[predicted_label_id],
        "confidence": float(probabilities[predicted_idx]),
        "probabilities": probabilities_dict
    }
