# 🚀 Quick GitHub Commands - Cheat Sheet

## 📦 **Files You Need**

Download these from outputs and place in your project:

```
Your Project Root/
├── .gitignore                          ← Protects personal data
├── README.md                           ← Project documentation
├── requirements.txt                    ← Python dependencies
├── LICENSE                             ← MIT license (edit your name)
├── app.py                              ← Your main application
│
└── examples/                           ← Create this folder
    ├── template_profile_example.json  ← Anonymized template
    ├── snippets_example.jsonl         ← Example snippets
    └── skills_map.json                ← Copy from data/
```

---

## ⚡ **Quick Start (5 Commands)**

```bash
# 1. Navigate to your project
cd D:\AI\cvgen

# 2. Initialize git
git init

# 3. Add files (gitignore protects personal data)
git add .

# 4. First commit
git commit -m "Initial commit: AI-powered CV personalization system"

# 5. Create main branch
git branch -M main
```

**STOP HERE** - Now create GitHub repository online, then continue:

```bash
# 6. Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/cv-personalization-system.git

# 7. Push to GitHub
git push -u origin main
```

---

## 🔐 **Before You Push - Safety Check**

```bash
# Check what will be committed
git status

# ✅ Should see:
# - app.py
# - README.md
# - requirements.txt
# - LICENSE
# - .gitignore
# - examples/

# ❌ Should NOT see:
# - data/master_profile.json
# - data/template_profile.json
# - data/snippets.jsonl (your real one)
# - Any .docx files
```

If you see personal files: **STOP! Add them to .gitignore first!**

---

## 📝 **Common Git Commands**

### **Making Changes**
```bash
# See what changed
git status

# Add specific file
git add filename.py

# Add all changes
git add .

# Commit with message
git commit -m "Your descriptive message"

# Push to GitHub
git push
```

### **Viewing History**
```bash
# See commit history
git log

# See recent commits (short)
git log --oneline

# See what changed in a file
git diff filename.py
```

### **Undoing Changes**
```bash
# Undo changes to a file (before commit)
git checkout -- filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Remove file from staging
git reset filename.py
```

---

## 🏷️ **Creating Releases**

```bash
# Tag a version
git tag -a v1.0.0 -m "Initial release"

# Push tag to GitHub
git push origin v1.0.0
```

Then on GitHub: Releases → Draft new release → Select tag

---

## 🔧 **Troubleshooting**

### **"Permission denied"**
You need a Personal Access Token:
1. GitHub → Settings → Developer settings
2. Personal access tokens → Generate new
3. Use token instead of password

### **"Repository not found"**
Check remote URL:
```bash
git remote -v
git remote set-url origin https://github.com/USERNAME/REPO.git
```

### **Accidentally committed personal data**
```bash
# Before pushing:
git rm --cached data/master_profile.json
git commit --amend

# After pushing: Use git-filter-repo or contact GitHub support
```

### **Merge conflicts**
```bash
# Pull latest changes first
git pull origin main

# If conflicts, edit files, then:
git add .
git commit -m "Resolved merge conflicts"
git push
```

---

## 📋 **Pre-Push Checklist**

Every time before `git push`:

- [ ] Ran `git status` - no personal files
- [ ] Committed with good message
- [ ] Tested code locally
- [ ] Updated README if needed
- [ ] No passwords/API keys in code

---

## 🎯 **Repository Setup Checklist**

- [ ] Downloaded all files from outputs
- [ ] Created `examples/` folder
- [ ] Copied anonymized examples
- [ ] Edited LICENSE (your name)
- [ ] Edited README (your contact)
- [ ] Created `.gitignore`
- [ ] Created GitHub repository
- [ ] Initialized git locally
- [ ] Connected remote
- [ ] Pushed code
- [ ] Verified on GitHub
- [ ] Added repository topics
- [ ] Checked no personal data visible

---

## 📧 **Share Your Repo**

**URL Format:**
```
https://github.com/YOUR_USERNAME/cv-personalization-system
```

**Short Description for Recruiters:**
```
AI-powered CV personalization system using RAG, ChromaDB, 
and local LLMs. Features semantic search, NLP pipeline, 
and template-based document generation.
```

---

## 🆘 **Need Help?**

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Docs](https://docs.github.com/en)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Your GitHub URL:**
```
https://github.com/YOUR_USERNAME/cv-personalization-system
```

Update this in:
- Resume
- LinkedIn
- Email signature
- Cover letters
