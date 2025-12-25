"""
Script to upload the model to Hugging Face Hub.
Run this script to upload your trained model to Hugging Face for Streamlit Cloud deployment.
"""

import os
from huggingface_hub import HfApi
from pathlib import Path

# Configuration - UPDATE THESE VALUES
HF_USERNAME = "Sanjeev2004"  # Your Hugging Face username
MODEL_NAME = "mh_3class_distil_final"  # Name for your model on Hugging Face
LOCAL_MODEL_PATH = "models/base_model/mh_3class_distil_final"  # Local path to your model

def upload_model():
    """Upload the model to Hugging Face Hub."""
    # Check if model directory exists
    model_path = Path(LOCAL_MODEL_PATH)
    if not model_path.exists():
        print(f"❌ Error: Model directory not found at {LOCAL_MODEL_PATH}")
        print("Please check the path and try again.")
        return False
    
    # Check for required files
    required_files = ["model.safetensors", "config.json", "tokenizer.json"]
    missing_files = [f for f in required_files if not (model_path / f).exists()]
    if missing_files:
        print(f"❌ Error: Missing required files: {', '.join(missing_files)}")
        return False
    
    # Construct repo ID
    repo_id = f"{HF_USERNAME}/{MODEL_NAME}"
    
    print(f"📤 Uploading model to Hugging Face Hub...")
    print(f"   Repository: {repo_id}")
    print(f"   Source: {model_path.absolute()}")
    print()
    
    api = HfApi()
    
    # Create repository if it doesn't exist
    print(f"🔄 Ensuring repository exists: {repo_id}")
    api.create_repo(repo_id=repo_id, exist_ok=True, repo_type="model")
    
    # Upload files
    print("🔄 Uploading files (this may take a few minutes)...")
    api.upload_folder(
        folder_path=str(model_path.absolute()),
        repo_id=repo_id,
        repo_type="model",
        commit_message="Upload mental health detection model"
    )
    
    print()
    print(f"✅ Success! Model uploaded to: https://huggingface.co/{repo_id}")
    print()
    print("📝 Next steps:")
    print(f"   1. Update HUGGING_FACE_MODEL_ID in app/app.py to: '{repo_id}'")
    print("   2. Commit and push your changes to GitHub")
    print("   3. Your Streamlit Cloud app should now work!")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Upload Model to Hugging Face Hub")
    print("=" * 60)
    print()
    
    # Check if huggingface_hub is installed
    try:
        import huggingface_hub
    except ImportError:
        print("❌ Error: huggingface_hub not installed")
        print("   Install it with: pip install huggingface_hub")
        exit(1)
    
    # Check if logged in
    try:
        from huggingface_hub import whoami
        user_info = whoami()
        print(f"✅ Logged in as: {user_info.get('name', 'Unknown')}")
        print()
    except Exception:
        print("⚠️  Warning: Not logged in to Hugging Face")
        print("   Run: huggingface-cli login")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            exit(0)
    
    print()
    upload_model()

