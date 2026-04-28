# 🚀 AI Project Generator

An end-to-end full-stack web application that generates complete project codebases using AI. Users can input a prompt and instantly receive a structured project with files, preview, and download functionality.

---

## 🌐 Live Demo

* 🔗 Frontend: https://ai-project-generator.vercel.app
* 🔗 Backend API: https://ai-project-generator-ppa5.onrender.com

---

## 🧠 Features

* ✨ Generate full project code using AI (LLM-powered)
* 📁 Automatic file structure creation
* 👀 Preview generated files
* ⬇️ Download project as ZIP
* 🗂️ Persistent metadata storage using PostgreSQL
* 🌍 Fully deployed full-stack system

---

## 🛠️ Tech Stack

### Frontend

* React (Vite)
* JavaScript
* CSS

### Backend

* FastAPI (Python)
* LangGraph (AI workflow orchestration)
* Groq API (LLM inference)

### Database

* PostgreSQL (Render)

### Deployment

* Frontend → Vercel
* Backend → Render

---

## ⚙️ Architecture Overview

```text
User → React Frontend → FastAPI Backend → Groq LLM
                                   ↓
                             PostgreSQL DB
```

---

## 📂 Project Structure

```text
ai-project-generator/
│
├── frontend/           # React frontend (Vite)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── app.py              # FastAPI app entry point
├── graph.py            # AI workflow (LangGraph)
├── tools.py            # File generation utilities
├── prompts.py          # LLM prompts
├── states.py           # Workflow states
├── validator.py        # Validation logic
│
├── requirements.txt    # Python dependencies
├── runtime.txt         # Python version for deployment
└── README.md
```

---

## 🚀 How It Works

1. User enters a prompt in the frontend
2. Request is sent to FastAPI backend
3. Backend uses LangGraph + Groq LLM
4. AI generates structured project files
5. Files are saved and metadata stored in PostgreSQL
6. User can preview or download the generated project

---

## ⚡ Getting Started (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/luvkumarsiingh/ai-project-generator.git
cd ai-project-generator
```

---

### 2. Backend Setup

```bash
cd Agent
pip install -r requirements.txt
uvicorn app:app --reload
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

Create a `.env` file in backend:

```env
GROQ_API_KEY=your_api_key
DATABASE_URL=your_postgres_url
```

---

## ⚠️ Known Limitations

* Generated files are not persistently stored (reset on server restart)
* Free-tier backend may have cold start delays
* No user authentication (yet)

---

## 🚀 Future Improvements

* ☁️ Store files using AWS S3
* 🔐 Add authentication (JWT)
* 📊 User-specific project history
* 🎨 Improved UI/UX
* ⚡ Faster response streaming

---

## 📸 Screenshots

*(Add screenshots here for better presentation)*

---

## 🙌 Acknowledgements

* Groq for ultra-fast LLM inference
* LangGraph for workflow orchestration
* FastAPI for backend framework
* Vercel & Render for deployment

---

## 👨‍💻 Author

**Luv Kumar Singh**

* GitHub: https://github.com/luvkumarsiingh

---

## ⭐ If you like this project

Give it a star ⭐ and share it!

---
