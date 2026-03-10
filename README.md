# Tourism RAG Assistant
## Project Overview

This project is an **AI-powered Tourism Assistant** built using a **Retrieval-Augmented Generation (RAG)** system.
The assistant allows users to ask tourism-related questions and receive answers based on information stored in tourism documents such as **destinations, hotels, and accommodation information**.

The system works by:

1. Extracting information from tourism PDF documents
2. Converting the information into embeddings
3. Storing them in a vector database
4. Retrieving relevant information when a user asks a question
5. Generating a grounded response using an LLM

The project uses:

* **FastAPI** – Backend API
* **ChromaDB** – Vector database
* **Sentence Transformers** – Text embeddings
* **Groq + Llama Model** – Response generation
* **HTML, CSS, JavaScript** – Frontend interface

---

# 📁 Project Structure

```
Travel Tour Rag
│
├── data/                  # Tourism PDF documents
├── chromadb/              # Vector database storage
│
├── ingest.py              # Processes PDFs and stores embeddings
├── query.py               # Retrieves documents and generates answers
├── app.py                 # FastAPI backend API
│
├── index.html             # Frontend chat interface
├── script.js              # Frontend logic
├── style.css              # Frontend styling
│
├── requirements.txt       # Project dependencies
├── .env                   # API key configuration
└── README.md
```

---

# ⚙️ Environment Setup

## 1 Install Dependencies

Install all required libraries using:

```
pip install -r requirements.txt
```

Dependencies include:

<img width="590" height="396" alt="image" src="https://github.com/user-attachments/assets/d65df243-21c0-4e6c-8eb4-c50c682d0374" />

---

## 2 Configure API Key

Create a **.env file** in the root folder and add your Groq API key.

```
GROQ_API_KEY=your_api_key_here
```

<img width="274" height="120" alt="image" src="https://github.com/user-attachments/assets/a6797417-9cf9-448d-92ab-b6bb257a2ffb" />

This file keeps your API key secure and prevents it from being exposed in your code.

---

# 📄 Data Ingestion

Tourism information is stored as **PDF documents** in the `data` folder.

The script **ingest.py** performs the following steps:

1. Reads all PDF files
2. Extracts the text
3. Splits the text into smaller chunks
4. Converts the chunks into embeddings using `SentenceTransformer`
5. Stores embeddings and metadata in **ChromaDB**

Run ingestion using:

```
python ingest.py
```

<img width="1142" height="504" alt="image" src="https://github.com/user-attachments/assets/f24b8047-2f63-43ac-9e3c-71c92dd3ef92" />

---

# 🗂 Vector Database (ChromaDB)

The project uses **ChromaDB** to store and retrieve text embeddings.

Each stored chunk contains metadata such as:

* Location
* Category
* Source document
* Chunk index

This allows the system to perform **semantic search** when users ask questions.

Database location:

```
chromadb/
```

---

# 🔎 Query System

The **query.py** script handles question answering.

Process:

1. User question is converted into an embedding
2. ChromaDB retrieves the **top relevant chunks**
3. Retrieved context is sent to the **Llama model via Groq**
4. The model generates a grounded response

Example usage inside the backend:

```
answer, sources = ask("Which hotels are in Maasai Mara?")
```

The system also returns the **source documents** used to generate the answer.

---

# 🚀 Backend API

The backend is built using **FastAPI**.

Run the API server:

```
uvicorn app:app --reload
```

The server will run at:

```
http://127.0.0.1:8000
```

Available endpoints:

| Endpoint  | Description           |
| --------- | --------------------- |
| `/`       | API status            |
| `/health` | Health check          |
| `/query`  | Ask tourism questions |

Example request:

```
POST /query

{
 "question": "Which are the best hotels in Maasai Mara?"
}
```

Response body

```
{
  "answer": "Based on the provided information, here are some of the top-rated hotels in Maasai Mara:\n\n1. **Mahali Mzuri** - 5-star hotel\n2. **Mara Serena Safari Lodge** - 5-star hotel\n3. **Sand River Masai Mara by Elewana** - 5-star hotel\n4. **Fig Tree Camp** - 5-star hotel\n5. **PrideInn Mara Camp** - 5-star hotel\n6. **JW Marriott Masai Mara Lodge** - 5-star hotel\n7. **Olare Mara Kempinski Masai Mara** - 5-star hotel\n8. **Fairmont Mara Safari Club** - 5-star hotel\n9. **The Ritz-Carlton, Masai Mara Safari Camp** - Hotel \n\nThese are just a few of the many great hotels in Maasai Mara. I recommend checking the current ratings and reviews on Google Maps or other travel websites for the most up-to-date information.",
  "sources": [
    "Maasai Mara Hotels.pdf"
  ]
}
```

<img width="1864" height="911" alt="image" src="https://github.com/user-attachments/assets/cb620f45-4f2c-459d-b2ac-7d86b33e2c1c" />

---

# 💻 Frontend Interface

The frontend provides a **simple chat interface** where users can ask tourism questions.

Frontend files include:

* `index.html`
* `script.js`
* `style.css`

The frontend sends requests to the **FastAPI backend** and displays the response.

<img width="974" height="809" alt="image" src="https://github.com/user-attachments/assets/f8c45809-b475-4157-9898-650aa0de1d9d" />

---

## 🧠 Example Questions

Users can ask questions such as:

- Where can tourists stay in Mombasa?
- Which are the best hotels found at Mount Kenya?

The system retrieves relevant information from tourism documents and generates a helpful answer.

---

## 🛠 Technologies Used

- Python  
- FastAPI  
- ChromaDB  
- Sentence Transformers  
- Groq API  
- Llama Model  
- HTML  
- CSS  
- JavaScript  

---

## ✨ Key Features

- AI-powered tourism assistant  
- Retrieval-Augmented Generation (RAG)  
- Document-based question answering  
- Vector similarity search  
- Grounded responses from tourism documents  
- Simple chat-based interface  

---

## 🚀 Future Improvements

Possible improvements include:

- Adding more tourism documents  
- Improving the frontend interface  
- Adding location filters  
- Deploying the application online  
- Adding multilingual support  
## 👩‍💻 Author

**Teresa Kungu**
