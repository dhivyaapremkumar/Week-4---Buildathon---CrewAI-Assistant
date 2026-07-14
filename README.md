# 🤖 CrewAI Agentic Web Search Assistant

A multi-agent AI application built using **CrewAI**, **OpenAI GPT-4.1 Mini**, **SerpAPI**, and **Streamlit**.

This project demonstrates how multiple AI agents can collaborate to process a user query, perform real-time web search, generate a structured execution report, and provide a modern interactive dashboard.

---

## 🚀 Features

- 👋 Greeting Agent
  - Welcomes the user
  - Acknowledges the query
  - Hands over to the Search Agent

- 🌐 Search Agent
  - Uses Google Search via SerpAPI
  - Retrieves the latest information
  - Generates a concise summary

- 📝 Logger Agent
  - Collects outputs from previous agents
  - Generates a structured execution report

- 🎨 Premium Streamlit Dashboard
  - Modern dark theme
  - Live agent status
  - Workflow visualization
  - Execution metrics
  - Search history
  - Download execution log

---

## 🏗️ Architecture

```
                User
                  │
                  ▼
        👋 Greeting Agent
                  │
                  ▼
        🌐 Search Agent
                  │
                  ▼
         📝 Logger Agent
                  │
                  ▼
        📄 Execution Report
                  │
                  ▼
          Streamlit Dashboard
```

---

## 📁 Project Structure

```
CrewAI_Buildathon/
│
├── app.py
├── agents.py
├── crew.py
├── .env
├── requirements.txt
├── README.md
├── .gitignore
│
├── logs/
│   └── execution_log.txt
│
└── assets/
    └── logo.png
```

---

## ⚙️ Technologies Used

- CrewAI
- OpenAI GPT-4.1 Mini
- SerpAPI
- Streamlit
- Python 3.12
- python-dotenv

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

---

## 📦 Installation

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the project

```bash
cd CrewAI_Buildathon
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📸 Application Workflow

1. User enters a query.
2. Greeting Agent welcomes the user.
3. Search Agent performs real-time Google Search.
4. Logger Agent generates the execution report.
5. Dashboard displays results.
6. User downloads the execution log.

---

## 📊 Example Query

```
Latest AI News
```

---

## 🎯 Future Enhancements

- RAG Integration
- PDF Report Export
- Multi-language Support
- Voice Input
- Crew Memory
- Supervisor Agent
- Real-time Streaming

---
Screenshots :
![alt text](<Screenshot 2026-07-14 132528.png>)

## 👨‍💻 Developed By

**Dhivyaa Meenakshisundaram**

Fourth Axis Designers Pvt. Ltd.

Powered by

- CrewAI
- OpenAI
- SerpAPI
- Streamlit