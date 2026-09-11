import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

from rag import ResumeVectorStore
from tracker import (
    create_table,
    add_application,
    get_applications,
    delete_application,
)


# =========================================
# Page Configuration
# =========================================

st.set_page_config(
    page_title="AI Resume & Interview Copilot",
    page_icon="🤖",
    layout="wide",
)

# Keep the application at a comfortable reading width.
st.markdown(
    """
    <style>
        .block-container {
            max-width: 950px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .stMarkdown {
            font-size: 1rem;
            line-height: 1.65;
        }

        h1 {
            font-size: 2.2rem !important;
        }

        h2 {
            font-size: 1.6rem !important;
        }

        h3 {
            font-size: 1.3rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================
# Setup
# =========================================

load_dotenv()
create_table()

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)


@st.cache_resource(show_spinner=False)
def build_vector_store(resume_text):
    """
    Build the FAISS index only once for a given resume.
    Streamlit reuses the cached vector store on later reruns.
    """
    vector_store = ResumeVectorStore()
    vector_store.create_index(resume_text)
    return vector_store


def get_response_text(response):
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text = ""
        for item in content:
            if isinstance(item, dict):
                text += item.get("text", "")
        return text

    return str(content)


def show_ai_error(error):
    error_message = str(error)

    if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
        st.error(
            "⚠️ AI request limit reached. "
            "Please wait a little and try again."
        )
    elif "503" in error_message or "UNAVAILABLE" in error_message:
        st.error(
            "⚠️ AI service is temporarily unavailable. "
            "Please try again in a moment."
        )
    else:
        st.error(
            "⚠️ Something went wrong while contacting the AI service. "
            "Please try again."
        )


# =========================================
# Session State
# =========================================

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = ""

if "interview_answer" not in st.session_state:
    st.session_state.interview_answer = ""

if "cover_answer" not in st.session_state:
    st.session_state.cover_answer = ""

if "previous_jd" not in st.session_state:
    st.session_state.previous_jd = None

if "previous_resume_name" not in st.session_state:
    st.session_state.previous_resume_name = None


# =========================================
# Header
# =========================================

st.title("🤖 AI Resume & Interview Copilot")

st.write(
    "Analyze your resume against a Job Description, "
    "prepare for interviews, generate tailored cover letters, "
    "and track your job applications."
)

st.divider()


# =========================================
# Resume Upload
# =========================================

st.header("📄 Resume")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    help="Upload your resume in PDF format.",
)

if uploaded_file:

    # Clear old AI results when a different resume is uploaded.
    if (
        st.session_state.previous_resume_name is not None
        and st.session_state.previous_resume_name != uploaded_file.name
    ):
        st.session_state.resume_analysis = ""
        st.session_state.interview_answer = ""
        st.session_state.cover_answer = ""
        st.session_state.previous_jd = None

    st.session_state.previous_resume_name = uploaded_file.name

    # =========================================
    # Extract Resume Text
    # =========================================

    try:
        reader = PdfReader(uploaded_file)
        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

    except Exception:
        st.error(
            "Unable to read this PDF. "
            "Please upload a valid resume PDF."
        )
        st.stop()

    # =========================================
    # Validate Resume
    # =========================================

    if not resume_text.strip():
        st.error(
            "No readable text was found in this PDF. "
            "Please upload a text-based resume PDF."
        )
        st.stop()

    # =========================================
    # Display Resume
    # =========================================

    with st.expander("👀 View Extracted Resume Text"):
        st.text_area(
            "Resume Content",
            resume_text,
            height=250,
        )

    # =========================================
    # Create FAISS Vector Store
    # =========================================

    with st.spinner("Preparing resume for semantic search..."):
        vector_store = build_vector_store(resume_text)

    st.success("Resume processed successfully! ✅")

    st.divider()

    # =========================================
    # Job Description
    # =========================================

    st.header("💼 Job Description")

    jd_text = st.text_area(
        "Paste the Job Description here",
        height=220,
        placeholder=(
            "Paste the job description you want to "
            "compare your resume against..."
        ),
    )

    # If the JD changes, previous generated results belong to the
    # previous JD, so clear them.
    if (
        st.session_state.previous_jd is not None
        and st.session_state.previous_jd != jd_text
    ):
        st.session_state.resume_analysis = ""
        st.session_state.interview_answer = ""
        st.session_state.cover_answer = ""

    st.session_state.previous_jd = jd_text

    if not jd_text.strip():

        st.info(
            "👆 Paste a Job Description to start the AI analysis."
        )

    else:

        # =========================================
        # Resume Analysis
        # =========================================

        st.divider()
        st.header("📊 Resume Analysis")

        if st.button(
            "🔍 Analyze Resume",
            use_container_width=True,
        ):
            with st.spinner(
                "Analyzing resume against Job Description..."
            ):

                # RAG retrieval
                results = vector_store.search(
                    jd_text,
                    top_k=3,
                )

                context = "\n\n".join(results)

                prompt_template = PromptTemplate(
                    input_variables=["context", "jd"],
                    template="""
You are an AI Resume Assistant.

Analyze the candidate's resume against the Job Description.

Use ONLY the provided resume context and Job Description.

Return the answer using EXACTLY this structure:

MATCH_SCORE:
Give an estimated compatibility score from 0-100.

MATCHING_SKILLS:
- skill 1
- skill 2
- skill 3

MISSING_SKILLS:
- skill 1
- skill 2
- skill 3

RELEVANT_EXPERIENCE:
Write a short explanation of the candidate's relevant experience.

STRENGTHS:
- strength 1
- strength 2
- strength 3

AREAS_FOR_IMPROVEMENT:
- improvement 1
- improvement 2
- improvement 3

Important rules:

- Do not invent information.
- Base the analysis only on the provided resume context and Job Description.
- Do not infer work authorization, visa status, citizenship,
  location, or sponsorship requirements unless explicitly stated.
- The match score is an estimate, not an official ATS score.

Resume Context:
{context}

Job Description:
{jd}
""",
                )

                prompt = prompt_template.format(
                    context=context,
                    jd=jd_text,
                )

                try:
                    response = llm.invoke(prompt)
                    st.session_state.resume_analysis = get_response_text(
                        response
                    )
                except Exception as error:
                    show_ai_error(error)

        if st.session_state.resume_analysis:
            st.markdown(st.session_state.resume_analysis)

        # =========================================
        # Interview Preparation
        # =========================================

        st.divider()
        st.header("🎯 Interview Preparation")

        st.write(
            "Generate technical, project-based, and behavioral "
            "questions based on your resume and the Job Description."
        )

        if st.button(
            "🎤 Generate Interview Questions",
            use_container_width=True,
        ):
            with st.spinner(
                "Generating interview questions..."
            ):

                interview_query = f"""
Find the candidate's skills, projects, experience,
and technical knowledge that are relevant to this
Job Description:

{jd_text}
"""

                interview_results = vector_store.search(
                    interview_query,
                    top_k=3,
                )

                interview_context = "\n\n".join(
                    interview_results
                )

                interview_prompt_template = PromptTemplate(
                    input_variables=["context", "jd"],
                    template="""
You are an AI Interview Preparation Assistant.

Generate interview questions for the candidate based ONLY on
the provided resume context and Job Description.

Organize the questions into exactly these sections:

TECHNICAL_QUESTIONS:
1. Question
2. Question
3. Question
4. Question
5. Question

PROJECT_BASED_QUESTIONS:
1. Question
2. Question
3. Question

BEHAVIORAL_QUESTIONS:
1. Question
2. Question

IMPORTANT:

- Questions should be relevant to the Job Description.
- Questions should be based on skills, projects, and experience
  actually present in the resume context.
- Do not invent projects or experience.
- Do not assume technologies that are not mentioned.
- Make the questions realistic for an entry-level candidate.

Resume Context:
{context}

Job Description:
{jd}
""",
                )

                interview_prompt = interview_prompt_template.format(
                    context=interview_context,
                    jd=jd_text,
                )

                try:
                    interview_response = llm.invoke(
                        interview_prompt
                    )

                    st.session_state.interview_answer = (
                        get_response_text(interview_response)
                    )
                except Exception as error:
                    show_ai_error(error)

        if st.session_state.interview_answer:
            st.markdown(st.session_state.interview_answer)

        # =========================================
        # Cover Letter
        # =========================================

        st.divider()
        st.header("✉️ Cover Letter")

        st.write(
            "Generate a professional, tailored cover letter "
            "for the selected Job Description."
        )

        if st.button(
            "📝 Generate Cover Letter",
            use_container_width=True,
        ):
            with st.spinner(
                "Generating tailored cover letter..."
            ):

                cover_letter_query = f"""
Find the candidate's most relevant skills, projects,
experience, and achievements for this Job Description:

{jd_text}
"""

                cover_results = vector_store.search(
                    cover_letter_query,
                    top_k=3,
                )

                cover_context = "\n\n".join(
                    cover_results
                )

                cover_letter_prompt = PromptTemplate(
                    input_variables=["context", "jd"],
                    template="""
You are an AI Career Assistant.

Write a professional, tailored cover letter for the candidate
based ONLY on the provided resume context and Job Description.

Requirements:

- Do not invent experience, skills, projects, or achievements.
- Highlight only experience relevant to the Job Description.
- Keep the tone professional and suitable for an entry-level candidate.
- Keep the cover letter concise: approximately 3-4 paragraphs.
- Do not include placeholders such as [Company Name] unless the
  company name is actually provided in the Job Description.
- Do not mention ATS scores or missing skills.
- Do not infer work authorization, visa status, citizenship,
  or sponsorship requirements.

Resume Context:
{context}

Job Description:
{jd}

Return only the cover letter.
""",
                )

                cover_prompt = cover_letter_prompt.format(
                    context=cover_context,
                    jd=jd_text,
                )

                try:
                    cover_response = llm.invoke(cover_prompt)

                    st.session_state.cover_answer = (
                        get_response_text(cover_response)
                    )
                except Exception as error:
                    show_ai_error(error)

        if st.session_state.cover_answer:
            st.markdown(st.session_state.cover_answer)

else:
    st.info("👆 Upload your resume to use the AI resume features.")


# =========================================
# Job Application Tracker
# This section is independent of resume upload.
# =========================================

st.divider()
st.header("📋 Job Application Tracker")

st.write(
    "Track your job applications and monitor their status."
)


# =========================================
# Add Application
# =========================================

with st.form("application_form"):

    company = st.text_input("Company")

    role = st.text_input("Job Role")

    status = st.selectbox(
        "Application Status",
        [
            "Saved",
            "Applied",
            "Interview",
            "Rejected",
            "Selected",
        ],
    )

    application_date = st.date_input(
        "Application Date"
    )

    notes = st.text_area("Notes")

    submitted = st.form_submit_button(
        "➕ Add Application",
        use_container_width=True,
    )

    if submitted:

        if company.strip() and role.strip():

            add_application(
                company,
                role,
                status,
                str(application_date),
                notes,
            )

            st.success(
                "Application added successfully! ✅"
            )

            st.rerun()

        else:
            st.warning(
                "Please enter the company and job role."
            )


# =========================================
# Display Applications
# =========================================

applications = get_applications()

if applications:

    st.write("### Your Applications")

    for application in applications:

        application_id = application[0]
        company = application[1]
        role = application[2]
        status = application[3]
        application_date = application[4]
        notes = application[5]

        with st.expander(
            f"{company} — {role}"
        ):

            st.write(f"**Status:** {status}")
            st.write(f"**Date:** {application_date}")
            st.write(f"**Notes:** {notes}")

            if st.button(
                "🗑️ Delete",
                key=f"delete_{application_id}",
            ):

                delete_application(application_id)

                st.success("Application deleted.")
                st.rerun()

else:

    st.info("No job applications added yet.")
