# Quick Guide: Upload Model to Hugging Face Hub

## Step 1: Login to Hugging Face

You need to be logged in to upload your model. Choose one method:

### Method A: Using HF CLI (Recommended)
```bash
hf auth login
```
When prompted, paste your Hugging Face token. Get one from: https://huggingface.co/settings/tokens

### Method B: Set Token as Environment Variable
1. Get your token from: https://huggingface.co/settings/tokens
2. Set it as environment variable:

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="your_token_here"
```

**Windows (Command Prompt):**
```cmd
set HF_TOKEN=your_token_here
```

**Linux/Mac:**
```bash
export HF_TOKEN=your_token_here
```

## Step 2: Run the Upload Script

```bash
python upload_model.py
```

This will:
- Check if you're logged in
- Verify model files exist
- Upload your model to: `Sanjeev2004/mh_3class_distil_final`

## Step 3: Commit and Push Code

After successful upload:

```bash
git add app/app.py upload_model.py DEPLOYMENT_FIX.md
git commit -m "Add Hugging Face Hub support for Streamlit Cloud"
git push
```

## That's it!

Your Streamlit Cloud app will now automatically load the model from Hugging Face Hub!

