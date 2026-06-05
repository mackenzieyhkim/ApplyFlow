import streamlit as st
from dotenv import load_dotenv
from src.classifier import classify_job_description, score_job_match, generate_resume_points
from src.storage import save_posting, save_resume_points

load_dotenv()

st.title("AI Job Filtering System")

url = st.text_input("Paste a job posting link")

if st.button("Analyze"):
    if not url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner("Fetching and classifying..."):
            posting = classify_job_description(url)

        with st.spinner("Scoring against profile..."):
            match = score_job_match(posting)
        with st.spinner("Generating resume points..."):
            resume_points = generate_resume_points(posting)

        st.session_state["posting"] = posting
        st.session_state["match"] = match
        st.session_state["resume_points"] = resume_points

if "posting" in st.session_state and "match" in st.session_state:
    posting = st.session_state["posting"]
    match = st.session_state["match"]

    score = match["match_score"]
    color = "green" if score >= 70 else "orange" if score >= 40 else "red"
    st.markdown(f"### Match Score: :{color}[{score}%]")
    st.caption(match["reason"])

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Title:** {posting.title}")
        st.markdown(f"**Company:** {posting.company}")
        st.markdown(f"**Location:** {posting.location}")
    with col2:
        st.markdown(f"**Type:** {posting.job_type}")
        st.markdown(f"**Salary:** {posting.salary}")
        st.markdown(f"**URL:** {posting.source_url}")

    st.divider()

    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown("**Skills**")
        for s in posting.skills:
            st.markdown(f"- {s}")

    with col4:
        st.markdown("**Responsibilities**")
        for r in posting.responsibilities:
            st.markdown(f"- {r}")

    with col5:
        st.markdown("**Qualifications**")
        for q in posting.qualifications:
            st.markdown(f"- {q}")

    st.divider()

    if st.button("Save Posting"):
        output_path = save_posting(posting, match)
        st.success(f"Saved to {output_path}")

    if "resume_points" in st.session_state:
        resume_points = st.session_state["resume_points"]

    st.divider()
    st.subheader("AI Tailored Resume Points")

    st.text_area(
        "Resume Points",
        resume_points,
        height=350
    )

    if st.button("Save Resume Points"):
        resume_path = save_resume_points(posting, resume_points)
        st.success(f"Saved resume points to {resume_path}")