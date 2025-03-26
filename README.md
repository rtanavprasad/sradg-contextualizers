# 🚀 SMARTER RECONCILIATION

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
A brief overview of your project and its purpose. Mention which problem statement are your attempting to solve. Keep it concise and engaging.

## 🎥 Demo
📹 [Video Demo](./artifacts/demo/Video.mp4) (if applicable)  

🖼️ Screenshots:

![Screenshot 1](./artifacts/arch/UI.png)

## 💡 Inspiration
What inspired you to create this project? Describe the problem you're solving.

## ⚙️ What It Does
Explain the key features and functionalities of your project.

## 🛠️ How We Built It
Briefly outline the technologies, frameworks, and tools used in development.

## 🚧 Challenges We Faced
Describe the major technical or non-technical challenges your team encountered.

## 🏃 How to Run
0. Create Google API Studio API Key:
   - 🔹 URL: [Create API Key](https://aistudio.google.com/apikey?pli=1)
---
1. Clone the repository  
   ```sh
   git clone https://github.com/ewfx/sradg-contextualizers --branch FinalRelease .
   ```
---
2. Download Python Version Between >= 3.10,<3.11 
   - 🔹 Download URL: [Download Python](https://www.python.org/downloads/)
---
3. Validate the python Version
   ```sh
   python --version
   ```
---
4. Create the Virtual Environment   
   ```sh
   python -m venv .venv 
   ```
---
5. Activate Virtual Environment
- 🔹 Windows:
   ```sh
   .venv\Scripts\activate
   ```

- 🔹 Mac:
   ```sh
   source .venv/bin/activate
   ```
---
6. Install Poetry
   ```sh
   python -m pip install poetry
   ```
---
7. Install Dependencies (Same Directory/Folder as Git ROOT)
   ```sh
   poetry install 
   ```
---
8. Create Vector Database (Same Directory/Folder as Git ROOT)   
   ```sh
   python code/src/backend/create_vector_db.py
   ```
---
9. Run Application (Same Directory/Folder as Git ROOT)   
   ```sh
   poetry run uvicorn code.src.app:app --port 8000 --workers 4
   ```
---
10. Open URL in Browser:
   ```sh
   http://127.0.0.1:8000
   ```



## 🏗️ Tech Stack
- 🔹 Frontend & Backend: FastAPI / Vanilla (HTML, CSS, JS)
- 🔹 Backend: FastAPI
- 🔹 Vector Database: Chroma DB
- 🔹 AI Model: GoogleGenerativeAI / gemini-2.0-flash
- 🔹 Embeddings Model: HuggingFaceEmbeddings / snowflake-arctic-embed-m-long

## 👥 Team
- **Sugaanth Mohan** - [GitHub](https://github.com/SugaanthMohan) |[LinkedIn](#) 
- **Karthik S** - [GitHub](https://github.com/karthiksenthil2803) | [LinkedIn](#)
- **Gowsiman AR** - [GitHub](https://github.com/gowsiman) | [LinkedIn](#)
- **Krishna** - [GitHub](https://github.com/rtanavprasad) | [LinkedIn](#)