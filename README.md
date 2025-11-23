# 🚀 AI-Powered CV Personalization System

An intelligent document tailoring platform that generates customized CVs and cover letters using Retrieval-Augmented Generation (RAG) and local LLMs.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)

## 📖 Overview

This system uses RAG (Retrieval-Augmented Generation) to automatically tailor your CV and cover letter to specific job descriptions. Unlike traditional CV builders, it:

- ✅ **No Hallucinations**: Uses template-based selection instead of content generation
- ✅ **Semantic Matching**: Leverages vector embeddings for intelligent content retrieval
- ✅ **100% Local**: Runs entirely on your machine - no data sent to external APIs
- ✅ **Skills-Aware**: Normalizes and matches technology synonyms (e.g., "Azure AD" = "Entra ID")
- ✅ **Production Ready**: Robust error handling and quality validation

## 🏗️ Architecture

```
┌─────────────────┐
│  Job Description│
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  NLP Parser     │──────▶│ Skills Map   │
│  • Extract JD   │      │ Normalization│
│  • Normalize    │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Vector Search   │◀─────│  ChromaDB    │
│ (Sentence-BERT) │      │ 50+ Snippets │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Local LLM      │◀─────│   Ollama     │
│  (Llama 3.2)    │      │ (llama3.2:3b)│
│  • Selection    │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Template Engine │◀─────│ Template CV  │
│ • Assemble      │      │   (JSON)     │
│ • Format        │      └──────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output DOCX    │
│  + Cover Letter │
└─────────────────┘
```

## 🔑 Key Features

### 1. **Intelligent Retrieval**
- Vector embeddings via Sentence Transformers
- Hybrid ranking: semantic similarity + skill overlap
- Metadata filtering by seniority and tags

### 2. **Template-Based Selection**
```python
# LLM doesn't generate - it selects!
{
  "experience": {
    "insead": {
      "include": true,
      "bullets_to_keep": [0, 2, 4, 6],  # Indices only
      "achievements_to_keep": [0, 1]
    }
  }
}
```

### 3. **Skills Normalization**
```python
"azure ad" → ["AAD", "Entra ID", "Azure Active Directory"]
"mfa" → ["Multi-Factor Authentication", "2FA", "Two-Factor"]
```

### 4. **Quality Assurance**
- Validates all must-have keywords are covered
- Checks for missing experience sections
- Provides debug mode for transparency

## 🛠️ Tech Stack

- **LLM Framework**: Ollama (local inference)
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **NLP**: Custom regex-based parsers
- **Document Gen**: python-docx
- **Frontend**: Streamlit
- **Language**: Python 3.11+

## 📦 Installation

### Prerequisites

1. **Python 3.11+**
   ```bash
   python --version
   ```

2. **Ollama** (for local LLM)
   - Download from: https://ollama.com/download
   - Install and start: `ollama serve`
   - Pull model: `ollama pull llama3.2:3b`

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cv-personalization-system.git
   cd cv-personalization-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   ```bash
   # Create data directory
   mkdir data
   
   # Copy example templates
   cp examples/template_profile_example.json data/template_profile.json
   cp examples/master_profile_example.json data/master_profile.json
   cp examples/skills_map.json data/
   cp examples/snippets.jsonl data/
   
   # Edit with your actual CV content
   # IMPORTANT: Never commit your personal data!
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## 📁 Project Structure

```
cv-personalization-system/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
├── .gitignore                      # Git ignore rules
│
├── data/                           # Your personal data (gitignored)
│   ├── master_profile.json         # Your complete profile
│   ├── template_profile.json       # Your CV template
│   ├── skills_map.json             # Skills normalization
│   ├── snippets.jsonl              # Experience snippets
│   └── chroma_store/               # Vector DB (auto-generated)
│
├── examples/                       # Example templates
│   ├── template_profile_example.json
│   ├── master_profile_example.json
│   ├── skills_map.json
│   └── snippets_example.jsonl
│
└── docs/                           # Documentation
    ├── ARCHITECTURE.md
    ├── TROUBLESHOOTING.md
    └── DATA_SETUP.md
```

## 🎯 Usage

### Basic Workflow

1. **Start the app**
   ```bash
   streamlit run app.py
   ```

2. **Paste a job description**
   - Copy the full JD from the job posting
   - Paste into the text area

3. **Generate documents**
   - Click "🎯 Generate CV & Cover Letter"
   - Wait 1-3 minutes for generation
   - Review the selection in debug mode

4. **Download & customize**
   - Download the DOCX file
   - Make minor tweaks if needed
   - Ready to apply!

### Example Job Description

```
Title: Senior Cloud Engineer
Company: TechCorp

Requirements:
- 5+ years experience with Azure/AWS
- Strong automation skills (Terraform, Ansible)
- Active Directory and identity management
- CI/CD pipeline experience
- Bachelor's degree in Computer Science
```

### Output

The system will:
1. ✅ Parse requirements and skills
2. ✅ Retrieve relevant experience snippets
3. ✅ Select matching bullets from your CV
4. ✅ Generate tailored CV highlighting cloud/automation
5. ✅ Create custom cover letter

## 🔧 Configuration

### Change LLM Model

Edit `app.py`:
```python
OLLAMA_MODEL = "llama3.2:3b"  # Fast, good quality
# or
OLLAMA_MODEL = "llama3.1:8b"  # Slower, better quality
```

### Adjust Snippet Count

In the UI, use the number input (5-30 snippets).
- **5-10**: Faster, focused selection
- **20-30**: More comprehensive, slower

### Skills Normalization

Edit `data/skills_map.json`:
```json
{
  "kubernetes": ["k8s", "K8s", "Kubernetes", "kube"],
  "python": ["Python", "python3", "py"]
}
```

## 📊 Data Setup

### Your CV Template (`template_profile.json`)

```json
{
  "header": {
    "name": "YOUR NAME",
    "email": "your.email@example.com",
    "phone": "+1234567890"
  },
  "summary": {
    "paragraph": "Your summary...",
    "bullets": ["Achievement 1", "Achievement 2"]
  },
  "experience": [
    {
      "id": "company1",
      "title": "Senior Engineer",
      "company": "Company Name",
      "dates": "Jan 2020 - Present",
      "bullets": ["Responsibility 1", "Responsibility 2"],
      "achievements": ["Achievement 1"]
    }
  ]
}
```

See `examples/` folder for complete templates.

## 🧪 Testing

Run a quick test:

```bash
# 1. Start Ollama
ollama serve

# 2. In another terminal, run the app
streamlit run app.py

# 3. Use test job description from examples/
```

## 🐛 Troubleshooting

### Common Issues

**"Cannot connect to Ollama"**
```bash
# Start Ollama service
ollama serve
```

**"Model not found"**
```bash
# Download the model
ollama pull llama3.2:3b
```

**"ChromaDB error"**
```bash
# Delete and rebuild index
rm -rf data/chroma_store
```

**Empty experience sections**
- Check Selection JSON in debug mode
- Verify template_profile.json has all experience entries
- Ensure snippets.jsonl is properly formatted

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

## 📈 Performance

- **Initial Index Build**: 10-30 seconds (first run only)
- **CV Generation**: 1-3 minutes
- **Snippet Retrieval**: <1 second
- **Memory Usage**: ~500MB (with model loaded)

## 🔒 Privacy & Security

- ✅ **100% Local**: All processing happens on your machine
- ✅ **No External APIs**: No data sent to third parties
- ✅ **Your Data**: Stays in your `data/` folder
- ✅ **Gitignored**: Personal files excluded from version control

**IMPORTANT**: Never commit personal data to GitHub!

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [Streamlit](https://streamlit.io/) for the web interface

## 📧 Contact

**Ashen Perera** - [@ashensha90](https://github.com/ashensha90)

Project Link: [cv-personalization-system](https://github.com/ashensha90/cv-personalization-system)

---

**⭐ Star this repo if you find it useful!**

## 🎓 Learn More

- [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)
- [LLM Prompt Engineering](https://www.promptingguide.ai/)

## 📚 Related Projects

- [Resume Parser](https://github.com/topics/resume-parser)
- [CV Builder](https://github.com/topics/cv-builder)
- [RAG Applications](https://github.com/topics/rag)
