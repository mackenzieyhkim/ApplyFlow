import streamlit as st
import os
from dotenv import load_dotenv
from src.classifier import classify_job_description, score_job_match

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

        # Match score
        score = match["match_score"]
        color = "green" if score >= 70 else "orange" if score >= 40 else "red"
        st.markdown(f"### Match Score: :{color}[{score}%]")
        st.caption(match["reason"])

        st.divider()

        # Job details
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

        # Save button
        if st.button("Save Posting"):
            os.makedirs("outputs", exist_ok=True)
            filename = f"outputs/{posting.company}_{posting.title}.txt".replace(" ", "_")
            with open(filename, "w") as f:
                f.write(f"Title:    {posting.title}\n")
                f.write(f"Company:  {posting.company}\n")
                f.write(f"Location: {posting.location}\n")
                f.write(f"Type:     {posting.job_type}\n")
                f.write(f"Salary:   {posting.salary}\n")
                f.write(f"URL:      {posting.source_url}\n")
                f.write(f"\nMatch Score: {score}%\n")
                f.write(f"Match Reason: {match['reason']}\n")
            st.success(f"Saved to {filename}")