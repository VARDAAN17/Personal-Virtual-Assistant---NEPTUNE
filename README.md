# PERSONAL-VIRTUAL-ASSISTANT---NEPTUNE-

# 🧠 Neptune – The Personal Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

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
```neptune/
│── app/
│   ├── templates/          # HTML templates (UI)
│   ├── utils/              # Utility scripts/helpers
│   └── main.py             # Main FastAPI backend & routing
│── .gitignore
│── README.md
│── chat_memory.json        # Summarised memory storage
│── requirements.txt        # Project dependencies
│── run.sh                  # Local server launch script
```

---

## ⚙ Installation & Startup Process

### 1️⃣ Clone Repository
Pull the project from GitHub:

```
git clone https://github.com/VARDAAN17/Personal-Virtual-Assistant---NEPTUNE.git
cd Personal-Virtual-Assistant---NEPTUNE
```

### 2️⃣ Create & Activate Virtual Environment
Create a virtual environment:

```
python3 -m venv venv
```
Activate the virtual environment:

```
source venv/bin/activate
```

### 3️⃣ Install Dependencies
Install all required Python libraries:

```
pip install -r requirements.txt
pip install uvicorn
```

### 4️⃣ Configure API Keys
Set your API keys before running the application:
```
 - If using .env file → Add your keys there.
 - If using hardcoded values → Add them in app/main.py.
```

### 5️⃣ Initialize Server Environment
Run the setup script:

```
bash run.sh
```

### 6️⃣ Start Backend with Uvicorn
Run Uvicorn from the project root:
``` 
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
```

### 7️⃣ Access the Application
Open your browser and go to:
```
http://127.0.0.1:7000
```


## 💡 **Example Usage Login using the predefined credentials.**

**Ask Neptune for:**

**·** “What’s the weather in London today?”

**·** “Find flights from Delhi to Mumbai on 'date'.”

**·** “Search jobs in Data Analytics in 'location'.”

**·** “Explain quantum computing in simple terms.”


## 📚 **What I Learned**

**·** Prompt engineering for LLMs.

**·** API handling and integration.

**·** Structuring JSON for conversation memory.

**·** Modular app architecture with FastAPI.

**·** Building a simple, responsive chat interface.


