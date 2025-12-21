# Mental Health Detection App

A Streamlit web application for detecting mental health states from text using a fine-tuned DistilBERT model.

## Features

- **3-Class Classification**: Detects Normal, Stress/Anxiety, and Depressed states
- **Interactive Web UI**: User-friendly Streamlit interface
- **Confidence Scores**: Returns probability distributions for all classes
- **Visualizations**: Bar charts and progress indicators
- **Helpful Suggestions**: Context-aware recommendations based on predictions
- **Model**: Fine-tuned DistilBERT model (`mh_3class_distil_final`)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Model Location

The trained model should be located at:

```
models/base_model/mh_3class_distil_final/
```

## Running the App

### Streamlit App (Recommended)

**Windows:**

```bash
run_streamlit.bat
```

**Linux/Mac:**

```bash
chmod +x run_streamlit.sh
./run_streamlit.sh
```

**Manual:**

```bash
streamlit run app/app.py
```

The app will be available at: `http://localhost:8501`

### FastAPI (Alternative)

**Windows:**

```bash
run_api.bat
```

**Linux/Mac:**

```bash
chmod +x run_api.sh
./run_api.sh
```

**Manual:**

```bash
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## Usage

### Streamlit App

1. Start the app using one of the methods above
2. Enter text in the text area
3. Click "Analyze" button
4. View predictions, probabilities, and suggestions

### API Endpoints (FastAPI)

#### GET `/`

Health check endpoint.

**Response:**

```json
{
  "message": "Mental Health Detection API",
  "endpoint": "/predict"
}
```

#### POST `/predict`

Predict mental health classification for input text.

**Request Body:**

```json
{
  "text": "I've been feeling really stressed lately with all the work deadlines."
}
```

**Response:**

```json
{
  "label": "Stress/Anxiety",
  "confidence": 0.85,
  "probabilities": {
    "Normal": 0.10,
    "Stress/Anxiety": 0.85,
    "Depressed": 0.05
  }
}
```

### Example API Usage

**Using cURL:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel great today!"}'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "I've been feeling really stressed lately."}
)
print(response.json())
```

**API Documentation:**

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 🚀 Deployment

See [STREAMLIT_CLOUD_DEPLOY.md](STREAMLIT_CLOUD_DEPLOY.md) for detailed Streamlit Cloud deployment instructions.

**Quick Deploy to Streamlit Cloud:**

1. Push code to GitHub (public repository)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" → Select repository → Main file: `app/app.py`
5. Click "Deploy"

Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

## Project Structure

```
MentalHealthDetection/
├── app/
│   ├── app.py          # Streamlit application
│   └── utils.py        # Model loading and prediction utilities
├── models/
│   └── base_model/
│       └── mh_3class_distil_final/  # Trained model
├── data/
│   ├── raw/            # Raw datasets
│   └── processed/      # Processed datasets
├── notebook/           # Jupyter notebooks for training/analysis
├── .streamlit/         # Streamlit configuration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration (optional)
├── docker-compose.yml  # Docker Compose configuration (optional)
└── README.md          # This file
```

## Model Details

- **Architecture**: DistilBERT (DistilBertForSequenceClassification)
- **Classes**: 3 (Normal, Stress/Anxiety, Depressed)
- **Max Sequence Length**: 128 tokens
- **Base Model**: distilbert-base-uncased

## License

[Add your license here]
