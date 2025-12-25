# Removing Large Files from Git History

The model file (model.safetensors - 255MB) is too large for GitHub. Here's how to fix it:

## Solution: Remove Model Files from Git

Since you're deploying to Streamlit Cloud, you have two options:

### Option 1: Use Hugging Face Hub (Recommended)

1. Upload your model to Hugging Face Hub
2. Update `app/app.py` to download from Hugging Face
3. Remove model files from git

### Option 2: Use Git LFS

Install Git LFS and track large files:

```bash
git lfs install
git lfs track "models/**/*.safetensors"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push origin main
```

### Option 3: Remove from History Completely

If you want to remove the file completely:

```bash
# Install git-filter-repo (recommended) or use BFG Repo-Cleaner
# Or use this command:
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch models/**/*.safetensors models/**/*.bin" --prune-empty --tag-name-filter cat -- --all

# Force garbage collection
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (WARNING: This rewrites history)
git push origin main --force
```

## Quick Fix: Start Fresh Branch

The easiest solution is to create a new branch without the large files:

```bash
# Create new branch from a clean state
git checkout --orphan clean-main
git add .
git commit -m "Clean repository without large model files"
git branch -D main
git branch -m main
git push -f origin main
```




