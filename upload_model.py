"""
Simple script to upload model to Hugging Face Hub.
"""
import sys
from pathlib import Path

try:
    from huggingface_hub import HfApi, whoami
except ImportError:
    print("❌ Error: huggingface_hub not installed")
    print("   Install it with: pip install huggingface_hub")
    sys.exit(1)

# Configuration
HF_USERNAME = "Sanjeev2004"  # Your Hugging Face username
MODEL_NAME = "mh_3class_distil_final"
LOCAL_MODEL_PATH = Path("models/base_model/mh_3class_distil_final")
REPO_ID = f"{HF_USERNAME}/{MODEL_NAME}"

def main():
    print("=" * 60)
    print("Upload Model to Hugging Face Hub")
    print("=" * 60)
    print()
    
    # Check login status
    try:
        user_info = whoami()
        print(f"SUCCESS: Logged in as: {user_info.get('name', 'Unknown')}")
        print()
    except Exception as e:
        print("ERROR: Not logged in to Hugging Face")
        print()
        print("Please login first using one of these methods:")
        print()
        print("Method 1 (Recommended):")
        print("   hf auth login")
        print("   (Then paste your token when prompted)")
        print()
        print("Method 2: Get a token from https://huggingface.co/settings/tokens")
        print("Then set it as an environment variable:")
        print("   set HF_TOKEN=your_token_here  (Windows)")
        print("   export HF_TOKEN=your_token_here  (Linux/Mac)")
        print()
        sys.exit(1)
    
    # Check if model directory exists
    if not LOCAL_MODEL_PATH.exists():
        print(f"ERROR: Model directory not found at {LOCAL_MODEL_PATH}")
        sys.exit(1)
    
    # Check for required files
    required_files = ["model.safetensors", "config.json", "tokenizer.json"]
    missing_files = [f for f in required_files if not (LOCAL_MODEL_PATH / f).exists()]
    if missing_files:
        print(f"ERROR: Missing required files: {', '.join(missing_files)}")
        sys.exit(1)
    
    print(f"Uploading model to Hugging Face Hub...")
    print(f"   Repository: {REPO_ID}")
    print(f"   Source: {LOCAL_MODEL_PATH.absolute()}")
    print()
    
    try:
        api = HfApi()
        print("Uploading files (this may take a few minutes)...")
        api.upload_folder(
            folder_path=str(LOCAL_MODEL_PATH.absolute()),
            repo_id=REPO_ID,
            repo_type="model",
            commit_message="Upload mental health detection model"
        )
        
        print()
        print("SUCCESS! Model uploaded!")
        print(f"   View at: https://huggingface.co/{REPO_ID}")
        print()
        print("Next steps:")
        print(f"   1. Model ID in app/app.py is already set to: {REPO_ID}")
        print("   2. Commit and push your changes:")
        print("      git add app/app.py upload_model.py DEPLOYMENT_FIX.md")
        print("      git commit -m 'Add Hugging Face Hub support'")
        print("      git push")
        print("   3. Your Streamlit Cloud app should now work!")
        
    except Exception as e:
        print(f"ERROR uploading model: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

