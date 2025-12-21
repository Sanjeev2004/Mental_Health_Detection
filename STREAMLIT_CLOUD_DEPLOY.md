# 🌐 Streamlit Cloud Deployment Guide

Complete step-by-step guide for deploying on Streamlit Cloud (100% Free).

## 🎯 Why Streamlit Cloud?

- ✅ **100% Free** - No credit card required
- ✅ **Easy Setup** - Deploy in 2 minutes
- ✅ **Auto-Deploy** - Updates on every Git push
- ✅ **HTTPS Included** - Automatic SSL certificate
- ✅ **Custom Domain** - Free subdomain
- ✅ **GitHub Integration** - Seamless workflow

## ⚠️ Limitations (Free Tier)

- 1GB RAM limit
- Model files must be <100MB (or use Git LFS)
- Public GitHub repositories only
- No persistent storage

---

## 📋 Prerequisites

- GitHub account (free)
- Public GitHub repository
- Model files ready
- Python 3.9+ compatible code

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

#### 1.1 Initialize Git (if not already done)

```bash
# Navigate to your project directory
cd c:\Users\Sanjeev\Downloads\MentalHealthDetection

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Streamlit Cloud"
```

#### 1.2 Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click **"New repository"** (or the **+** icon)
3. Fill in:
   - **Repository name**: `mental-health-detector` (or your choice)
   - **Description**: "Mental Health Detection App using DistilBERT"
   - **Visibility**: **Public** ⚠️ (Required for free tier)
   - **Initialize**: Don't check any boxes (we already have files)
4. Click **"Create repository"**

#### 1.3 Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mental-health-detector.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You may need to authenticate. Use GitHub Personal Access Token if prompted.

---

### Step 2: Handle Large Model Files

#### Option A: Model Files <100MB (Recommended)

If your model files are small enough, just commit them normally:

```bash
# Check model size
du -sh models/base_model/mh_3class_distil_final

# If <100MB, commit normally
git add models/
git commit -m "Add model files"
git push
```

#### Option B: Model Files >100MB (Use Git LFS)

If your model is large, use Git LFS:

```bash
# Install Git LFS (if not installed)
# Windows: Download from https://git-lfs.github.com/
# Mac: brew install git-lfs
# Linux: sudo apt-get install git-lfs

# Initialize Git LFS
git lfs install

# Track large model files
git lfs track "models/**/*.safetensors"
git lfs track "models/**/*.bin"

# Add .gitattributes
git add .gitattributes

# Add and commit model files
git add models/
git commit -m "Add model files with LFS"
git push
```

#### Option C: Host Model on Hugging Face Hub (Best for Large Models)

1. **Upload model to Hugging Face**:

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

2. **Update `app/app.py`** to use Hugging Face model:

   ```python
   # Change this line in app/app.py
   MODEL_NAME = "YOUR_USERNAME/mh_3class_distil_final"  # Hugging Face model ID
   ```

3. **Remove local model from Git** (if already committed):

   ```bash
   git rm -r --cached models/
   echo "models/" >> .gitignore
   git add .gitignore
   git commit -m "Remove large model files, using Hugging Face Hub"
   git push
   ```

---

### Step 3: Verify Repository Structure

Your repository should have this structure:

```
mental-health-detector/
├── app/
│   ├── app.py          # Main Streamlit app
│   └── utils.py        # Utilities (if used)
├── models/             # Model files (or use Hugging Face)
│   └── base_model/
│       └── mh_3class_distil_final/
├── requirements.txt    # Dependencies
├── README.md          # Documentation
└── .gitignore         # Git ignore file
```

**Important**: Make sure `app/app.py` is the main file (not `app.py` in root).

---

### Step 4: Create requirements.txt (If Not Exists)

Ensure you have a `requirements.txt` file in the root directory:

```bash
# Check if requirements.txt exists
cat requirements.txt

# If it doesn't exist or needs updating, create it
```

Your `requirements.txt` should include:

```txt
streamlit==1.28.0
torch==2.1.0
transformers==4.35.0
sentencepiece==0.1.99
numpy==1.24.3
pandas==2.0.3
```

**Note**: Use CPU-only PyTorch to reduce size. Streamlit Cloud will install automatically.

---

### Step 5: Deploy on Streamlit Cloud

#### 5.1 Sign In to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit Cloud to access your GitHub account

#### 5.2 Create New App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select `YOUR_USERNAME/mental-health-detector`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app/app.py` ⚠️ (Important: include `app/` prefix)
   - **App URL**: `mental-health-detector` (or your choice)
   - **Python version**: `3.11` (or latest available)
3. Click **"Deploy"**

#### 5.3 Wait for Deployment

- First deployment takes **3-5 minutes**
- You'll see build logs in real-time
- Watch for any errors in the logs
- Once complete, you'll see "Your app is live!"

---

### Step 6: Access Your App

Your app will be available at:

```
https://mental-health-detector.streamlit.app
```

Or:

```
https://YOUR_APP_NAME.streamlit.app
```

---

## 🔧 Configuration

### Advanced Settings

1. Go to your app in Streamlit Cloud dashboard
2. Click **"Settings"** (⚙️ icon)
3. Configure:
   - **Python version**: 3.9, 3.10, or 3.11
   - **Secrets**: Add environment variables if needed
   - **App URL**: Change subdomain
   - **Sharing**: Public or private

### Using Secrets (For Private Models)

If using Hugging Face private models:

1. Go to **Settings** → **Secrets**
2. Add secret:

   ```
   MODEL_NAME = yourusername/mh_3class_distil_final
   ```

3. Update `app/app.py`:

   ```python
   import os
   MODEL_NAME = os.getenv("MODEL_NAME", "yourusername/mh_3class_distil_final")
   ```

---

## 🔄 Updating Your App

### Automatic Updates

Streamlit Cloud **auto-deploys** on every push to your main branch:

```bash
# Make changes to your code
# ...

# Commit and push
git add .
git commit -m "Update app"
git push

# Streamlit Cloud will automatically redeploy
```

### Manual Redeploy

1. Go to Streamlit Cloud dashboard
2. Click **"⋮"** (three dots) on your app
3. Click **"Redeploy"**

---

## 🆘 Troubleshooting

### Build Fails

**Error**: "Module not found"

- **Solution**: Add missing package to `requirements.txt`

**Error**: "Model not found"

- **Solution**:
  - Check model path in `app/app.py`
  - Verify model files are committed (or use Hugging Face Hub)
  - Check file paths are correct

**Error**: "Out of memory"

- **Solution**:
  - Use smaller model
  - Use model quantization
  - Host model on Hugging Face Hub instead

### App Crashes

**Check logs**:

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View **"Logs"** tab
4. Look for error messages

**Common fixes**:

- Check `requirements.txt` has all dependencies
- Verify model path is correct
- Ensure code syntax is correct
- Check memory usage (1GB limit)

### Model Loading Issues

**If using local model**:

- Ensure model files are committed
- Check path: `models/base_model/mh_3class_distil_final`
- Verify all model files are present

**If using Hugging Face Hub**:

- Verify model ID is correct
- Check model is public (or use secrets for private)
- Test model loading locally first

### Slow Performance

- First load is slow (model download)
- Subsequent loads are faster (cached)
- Consider using Hugging Face Hub for faster model loading
- Optimize model size with quantization

---

## 📊 Monitoring

### View Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View **"Logs"** tab for real-time logs

### Usage Stats

- Check **"Settings"** → **"Usage"** for:
  - App views
  - Compute time
  - Bandwidth usage

---

## ✅ Deployment Checklist

- [ ] GitHub repository created (public)
- [ ] Code pushed to GitHub
- [ ] Model files handled (<100MB or Git LFS or Hugging Face)
- [ ] `requirements.txt` exists and is correct
- [ ] `app/app.py` is the main file
- [ ] Streamlit Cloud account created
- [ ] App deployed successfully
- [ ] App accessible via URL
- [ ] Tested predictions work
- [ ] Auto-deploy working (test with a small change)

---

## 🎉 Success

Your app is now live on Streamlit Cloud!

**Next Steps**:

1. ✅ Test your app with different inputs
2. ✅ Share the URL with others
3. ✅ Monitor usage and logs
4. ✅ Make updates and push to GitHub (auto-deploys!)

---

## 💡 Pro Tips

1. **Use Hugging Face Hub** for large models (recommended)
2. **Optimize requirements.txt** - Only include what's needed
3. **Use Git LFS** if model files are large
4. **Monitor logs** regularly for issues
5. **Test locally first** before deploying
6. **Use secrets** for sensitive information
7. **Keep dependencies updated** in requirements.txt

---

## 📚 Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Git LFS Guide](https://git-lfs.github.com/)
- [Hugging Face Hub](https://huggingface.co/docs/hub)

---

## 🔗 Quick Links

- **Deploy**: [share.streamlit.io](https://share.streamlit.io)
- **Dashboard**: [share.streamlit.io](https://share.streamlit.io) (after login)
- **Documentation**: [docs.streamlit.io/streamlit-cloud](https://docs.streamlit.io/streamlit-cloud)

---

**Need help?** Check Streamlit Cloud documentation or community forums!
