# PERSONAL-VIRTUAL-ASSISTANT---NEPTUNE-

# 🧠 Neptune – The Personal Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![Last Commit](https://img.shields.io/github/last-commit/yourusername/neptune)  
![Repo Size](https://img.shields.io/github/repo-size/yourusername/neptune)  

> An AI-powered personal assistant that combines intelligent conversation, real-time data retrieval, and a clean local chat interface — all built with Python and modern web technologies.

---

## 📌 Overview
**Neptune** is a modular AI assistant designed to provide real-time information and handle multiple tasks in a single interface.  
It integrates **OpenAI’s GPT-4o mini** for natural language interaction, stores summarised conversation memory in JSON,  
and connects with APIs like **SerpAPI** for flight, job, and weather searches.

Built with a **modular architecture** and loosely following the **MVC pattern**, Neptune is maintainable, scalable, and easy to extend with new features.

---

## 🚀 Key Features
- **💬 AI Chat** – Natural conversation powered by GPT-4o mini with custom prompt engineering.  
- **🌦 Weather Updates** – Get weather information for any location you specify.  
- **✈ Flight Search** – Search for flights with prices, carriers, and details.  
- **💼 Job Search** – Find jobs by industry or field.  
- **🧠 Memory Handling** – Summarised conversations stored in structured JSON format.  
- **🔒 Login System** – Simple login screen with hardcoded credentials (single user).  
- **📂 Modular Design** – Easy to maintain and expand.

---

## 🛠 Tech Stack
**Languages & Frameworks**
- Python 3  
- HTML, CSS, JavaScript  
- FastAPI (Backend)  

**APIs**
- OpenAI API (GPT-4o mini)  
- SerpAPI  

**Libraries**
- Pydantic  
- JSON handling  

---

## 📂 Folder Structure
neptune/
│── app/
│   ├── templates/          # HTML templates (UI)
│   ├── utils/              # Utility scripts/helpers
│   └── main.py             # Main FastAPI backend & routing
│── .gitignore
│── README.md
│── chat_memory.json        # Summarised memory storage
│── requirements.txt        # Project dependencies
│── run.sh                  # Local server launch script


---

## ⚙ Installation & Startup Process

### 1️⃣ Clone Repository
Pull the project from GitHub:
```bash
git clone https://github.com/yourusername/neptune.git
cd neptune

### 2️⃣ Activate Environment
source venv/bin/activate
(
    if virtual environment is already created, if not, use following to create virtual env:
          python -m venv venv
)

### 3️⃣ Install Dependencies
pip install -r requirements.txt

###4️⃣ Initialize Server
bash run.sh

### 5️⃣ Start Backend
python app/main.py

💡 Access the application in your browser at shown URLs.

💡 Example Usage
Login using the predefined credentials.

Ask Neptune for:

“What’s the weather in London today?”

“Find flights from Delhi to Mumbai on 'date'.”

“Search jobs in Data Analytics in 'location'.”

“Explain quantum computing in simple terms.”


📚 What I Learned
Prompt engineering for LLMs

API handling and integration

Structuring JSON for conversation memory

Modular app architecture with FastAPI

Building a simple, responsive chat interface


