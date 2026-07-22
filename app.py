# import sys
# print("=" * 60)
# print(sys.executable)
# print("="*60)

from services.ai_service import ask_gemini
from services.file_service import (
    validate_file,
    save_uploaded_file,
    delete_uploaded_file,
)
from services.parser_service import extract_text
from services.speech_service import transcribe_audio
from prompts.meeting_prompt import meeting_analysis_prompt
from services.export_service import (
    generate_pdf,
    generate_docx
)

import streamlit as st

st.set_page_config(
    page_title="MeetMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.divider()

#Creating Sidebar
with st.sidebar:

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.image("assets/logo.png", width=120)

    st.markdown(
        "<h1 style='text-align:center;'>MeetMind AI</h1>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Transform Meetings into Actionable Insights"
    )

    st.divider()

    st.subheader("📂 Upload Meeting")

    uploaded_file = st.file_uploader(
        "Choose a meeting file",
        type=["mp3", "wav", "mp4", "pdf", "txt"],
    )

    meeting_type = st.selectbox(
        "Meeting Type",
        [
            "Team Meeting",
            "Client Meeting",
            "Interview",
            "Conference",
            "Other",
        ],
    )

    analyze = st.button(
        "🚀 Analyze Meeting",
        use_container_width=True,
    )

    st.divider()

    st.caption("Version 1.0")
    st.caption("Powered by Gemini")

#Home Page
# =========================
# Hero Section
# =========================

hero = st.container(border=True)

with hero:

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("assets/logo.png", width=250)

    with col2:
        st.title("MeetMind AI")

        st.caption("AI-Powered Meeting Intelligence Platform")

        st.write(
            "Convert meeting recordings, transcripts, and documents into professional summaries, action items, and insights in seconds."
        )

st.divider()

# #Generate Button
# generate = st.button("🚀 Generate Summary")

#Welcome Section
if uploaded_file is None:

    welcome = st.container(border=True)

    with welcome:

        st.subheader("👋 Welcome")

        st.write(
            """
                MeetMind AI helps you automatically generate:

                - 📄 Executive Summary
                - ✅ Action Items
                - 🎯 Key Decisions
                - ⚠️ Risks & Blockers
                - 📌 Follow-up Tasks
            """
        )

        st.divider()

        st.markdown("### Supported Files")

        c1, c2 = st.columns(2)

        c1.success("📄 PDF\n\nTXT")

        c2.success("🎤 MP3\n\nWAV")
        
        
if uploaded_file:
    valid, message = validate_file(uploaded_file)
    if not valid:
        st.error(message)
        st.stop()
    
    saved_path = save_uploaded_file(uploaded_file)
    
    # document_text = ""
    # if saved_path.suffix.lower() in [".txt", ".pdf"]:
    #     try:
    #         document_text = extract_text(saved_path)
    #     except Exception as e:
    #         st.error(f"Unable to read file:{e}")
    #         st.stop()
              
    document_text = ""

    try:

        extension = saved_path.suffix.lower()

        if extension in [".txt", ".pdf"]:
            document_text = extract_text(saved_path)

        elif extension in [".mp3", ".wav"]:

            with st.spinner("🎤 Transcribing audio..."):
                document_text = transcribe_audio(str(saved_path))
                from pathlib import Path
                transcript_dir = Path("outputs/transcripts")
                transcript_dir.mkdir(parents=True, exist_ok = True)
                
                from datetime import datetime

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                transcript_path = transcript_dir / f"Transcript_{timestamp}.txt"
                with open(transcript_path, "w", encoding = "utf-8") as f:
                    f.write(document_text)

    except Exception as e:
        st.error(f"Processing failed: {e}")
        st.stop()
        
    st.success("✅ File Uploaded Successfully!")
    st.caption(f"📂  Saved to: {saved_path.name}")
    

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 Uploaded File")
        
        st.write(f"**Filename:**{uploaded_file.name}")
        st.write(f"**Type:**{uploaded_file.type}")
        st.write(f"**Size:**{uploaded_file.size / 1024:.2f}KB")
    
    with col2:
        st.subheader("📌 Status")
        
        st.write("✅ Ready for Analysis")
        st.write(f"Meeting Type: **{meeting_type}**")
    
    if document_text:
        st.divider()
        with st.expander("📄 Transcript Preview", expanded = True):
        
         st.text_area(
            label="Transcript",
            value=document_text,
            height=350
        )
#Dashboard

st.divider()

#Testing Gemini 
if st.button("🚀 Analyze"):

    if not document_text:
        st.warning("No text found to analyze.")
        st.stop()

    with st.spinner("🤖 AI is analyzing your meeting..."):

        try:

            prompt = meeting_analysis_prompt(document_text)

            summary = ask_gemini(prompt)
            
            st.session_state["summary"] = summary
            from pathlib import Path
            
            report_dir = Path("outputs/reports")
            report_dir.mkdir(parents = True, exist_ok = True)
            
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            txt_path = report_dir / f"Meeting_Summary_{timestamp}.txt"
            with open(txt_path,"w", encoding = "utf-8") as f:
                f.write(summary)
            st.toast("✅ Meeting analyzed successfully!")
            
            if "summary" in st.session_state:
                st.divider()
            
            st.subheader("📌 Analysis Overview")
            col1, col2 = st.columns(2)

            with col1:
                st.info(f"🤖 **AI Model:** Gemini 3.5 Flash")
                st.info(f"📅 **Meeting Type:** {meeting_type}")

            with col2:
                st.info(f"📄 **Input File:** {uploaded_file.name}")
                st.success("✅ Status: Analysis Complete")
            
            st.subheader("🧠 AI Analysis Statistics")

            file_extension = uploaded_file.name.split(".")[-1].upper()

            source = (
                "Audio Transcription"
                if file_extension in ["MP3", "WAV"]
                else "Uploaded Document"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Model Used:** Gemini 3.5 Flash")
                st.write(f"**Input Format:** {file_extension}")

            with col2:
                st.write(f"**Transcript Source:** {source}")
                st.write("**Export Formats:** TXT • PDF • DOCX")            
            
            st.subheader("📝 AI Meeting Summary")
            
            with st.container(border=True):
                st.markdown(st.session_state["summary"])
                # st.write(summary)
                
            st.divider()
            st.subheader("📥 Export Report")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="📄 TXT",
                    data=st.session_state["summary"],
                    file_name="meeting_summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
                
            pdf_buffer = generate_pdf(
                report=st.session_state["summary"],
                meeting_type=meeting_type,
                model_name="Gemini 3.5 Flash"
            )
            
            with col2:
                st.download_button(
                    label="📕 PDF",
                    data=pdf_buffer,
                    file_name="Meeting_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

           
            
            docx_buffer = generate_docx(
                report=st.session_state["summary"],
                meeting_type=meeting_type,
                model_name="Gemini 3.5 Flash"
            )
            
            with col3:
                st.download_button(
                    label="📝 DOCX",
                    data=docx_buffer,
                    file_name="Meeting_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            delete_uploaded_file(saved_path)
                
            
        except Exception as e:
            error_message = str(e)
            
            if "503" in error_message or "Unavailable" in error_message:
                st.error(
                    "🚦 Gemini is currently experiencing high demand. "
                    "Please wait a minute and try again."
                )
                
            elif "404" in error_message:
                st.error("⚠ AI model unavailable")
                
            else:
                st.error(f"Unexpected Error:{error_message}")
            st.exception(e)

            
#Meeting Insights
                
if "summary" in st.session_state:
    st.subheader("📊 Meeting Insights")

if "summary" in st.session_state:

    transcript_words = len(document_text.split())
    summary_words = len(st.session_state["summary"].split())

    compression = (
        (1 - summary_words / transcript_words) * 100
        if transcript_words else 0
    )

    reading_time = max(1, round(summary_words / 200))

    estimated_pages = max(1, round(transcript_words / 500))

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📄 Transcript Words",
        transcript_words
    )

    col2.metric(
        "📝 Summary Words",
        summary_words
    )

    col3.metric(
        "📉 Compression",
        f"{compression:.1f}%"
    )

    st.divider()

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "⏱ Reading Time",
        f"{reading_time} min"
    )

    col5.metric(
        "📃 Estimated Pages",
        estimated_pages
    )

    col6.metric(
        "📅 Meeting Type",
        meeting_type
    )


#Progress Placeholder
st.divider()

st.subheader("⚙️ Processing Status")

if uploaded_file is None:

    st.info("Waiting for a meeting file...")

elif uploaded_file and "summary" not in st.session_state:

    st.warning("File uploaded. Ready for AI analysis.")

elif "summary" in st.session_state:

    st.success("Meeting analyzed successfully!")

    st.progress(100)

    st.caption("Analysis completed successfully.")


#Footer
st.markdown(
    """
---
<center>

### 🧠 MeetMind AI

AI-Powered Meeting Intelligence Platform

Version **1.0**

Powered by **Gemini 3.5 Flash**

Developed by **Ajay Ahirwar**

© 2026 MeetMind AI

</center>
""",
    unsafe_allow_html=True,
)