\# 🤖 AI Resume \& Interview Copilot



An AI-powered Resume \& Interview Copilot that analyzes a resume against a Job Description, identifies matching and missing skills, and generates personalized interview questions and cover letters.



The application uses \*\*Gemini, LangChain, RAG, FAISS, Sentence Transformers, and Streamlit\*\* to provide resume analysis and interview preparation.



\## 🚀 Features



\* 📄 Upload and extract text from PDF resumes

\* 💼 Compare resume content with a Job Description

\* 📊 Generate an estimated resume-JD compatibility score

\* ✅ Identify matching skills

\* ❌ Identify missing skills

\* 💡 Highlight strengths and areas for improvement

\* 🎯 Generate personalized interview questions



&#x20; \* Technical questions

&#x20; \* Project-based questions

&#x20; \* Behavioral questions

\* ✉️ Generate a tailored cover letter

\* 🔎 Use semantic search with RAG and FAISS to retrieve relevant resume content

\* 📋 Track job applications using an integrated job tracker

\* 🖥️ Streamlit-based user interface



\## 🛠️ Tech Stack



\* \*\*Python\*\* – Core programming language

\* \*\*Streamlit\*\* – Web application interface

\* \*\*Google Gemini\*\* – LLM for analysis and content generation

\* \*\*LangChain\*\* – LLM integration and prompt management

\* \*\*Sentence Transformers\*\* – Text embeddings

\* \*\*FAISS\*\* – Vector similarity search

\* \*\*PyPDF\*\* – PDF text extraction

\* \*\*SQLite\*\* – Job application tracking

\* \*\*python-dotenv\*\* – Environment variable management



\## 🧠 How It Works



The application follows a Retrieval-Augmented Generation (RAG) workflow.



```text

Resume PDF

&#x20;   ↓

PDF Text Extraction

&#x20;   ↓

Text Chunking

&#x20;   ↓

Sentence Transformer Embeddings

&#x20;   ↓

FAISS Vector Index

&#x20;   ↓

Job Description → Query Embedding

&#x20;   ↓

Semantic Search

&#x20;   ↓

Relevant Resume Context

&#x20;   ↓

LangChain Prompt

&#x20;   ↓

Google Gemini

&#x20;   ↓

Resume Analysis / Interview Questions / Cover Letter

```



\### RAG Flow



1\. The resume PDF is uploaded through the Streamlit interface.

2\. \*\*PyPDF\*\* extracts the text from the resume.

3\. The extracted text is divided into smaller chunks.

4\. \*\*Sentence Transformers\*\* converts the chunks into numerical embeddings.

5\. The embeddings are stored in a \*\*FAISS\*\* vector index.

6\. The Job Description is converted into a query embedding.

7\. FAISS retrieves the most relevant resume chunks using semantic similarity.

8\. The retrieved resume context and Job Description are passed to \*\*Gemini through LangChain\*\*.

9\. Gemini generates the final analysis or personalized content.



\### Key Concept



\*\*FAISS = Retrieval\*\*



\*\*Gemini = Reasoning + Generation\*\*



\*\*RAG = Retrieve → Augment → Generate\*\*



\## 📊 Resume Analysis



The resume analysis provides:



\* Match score

\* Matching skills

\* Missing skills

\* Relevant experience

\* Strengths

\* Areas for improvement



The generated analysis is based on the provided resume context and Job Description.



\## 🎯 Interview Preparation



The application generates interview questions based on the candidate's resume and the target Job Description.



Questions are organized into:



\* Technical Questions

\* Project-Based Questions

\* Behavioral Questions



This helps candidates prepare specifically for the role they are applying for.



\## ✉️ Cover Letter Generation



The application uses the retrieved resume context and Job Description to generate a personalized cover letter relevant to the target role.



\## 📋 Job Application Tracker



The project includes a simple job application tracker backed by SQLite.



It can be used to keep track of job applications and their progress.



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Shruthi-hasini/ai-resume-interview-copilot.git

cd ai-resume-interview-copilot

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



Activate it on Windows:



```powershell

venv\\Scripts\\activate

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Configure Gemini API Key



Create a `.env` file in the project root:



```env

GEMINI\_API\_KEY=your\_api\_key\_here

```



Do not commit the `.env` file to GitHub.



\### 5. Run the application



```bash

streamlit run app.py

```



The application will open in your browser.



\## 📁 Project Structure



```text

ai-resume-interview-copilot/

│

├── app.py              # Main Streamlit application

├── rag.py              # Embeddings, chunking and FAISS retrieval

├── tracker.py          # Job application tracker

├── requirements.txt    # Project dependencies

├── .gitignore          # Files excluded from Git

└── README.md           # Project documentation

```



\## 🔐 Security



The Gemini API key is stored in a `.env` file and excluded from Git using `.gitignore`.



Sensitive files such as the local database and virtual environment are also excluded from the repository.



\## ⚠️ Limitations



\* The match score is an estimated compatibility score and is not an official ATS score.

\* The quality of generated results depends on the resume and Job Description provided.

\* The application currently focuses on text-based PDF resumes.

\* Gemini API availability and quota can affect generation requests.

\* FAISS retrieval quality depends on the embedding model and chunking strategy.



\## 🔮 Future Improvements



\* Improve resume parsing for complex PDF layouts

\* Add support for multiple resume formats

\* Improve semantic retrieval and chunking

\* Add more advanced ATS analysis

\* Add authentication and user accounts

\* Deploy the application to a cloud platform

\* Add persistent cloud-based job tracking

\* Add automated resume improvement suggestions



\## 👩‍💻 Author



\*\*Shruthi Hasini\*\*



Built as a practical GenAI project to explore \*\*LLM applications, RAG, semantic search, vector databases, and AI-powered career tools\*\*.



