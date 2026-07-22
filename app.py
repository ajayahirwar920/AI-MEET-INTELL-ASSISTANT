import sys
print("=" * 60)
print(sys.executable)
print("="*60)

from services.ai_service import ask_gemini
from services.file_service import validate_file, save_uploaded_file
from services.parser_service import extract_text
from services.speech_service import transcribe_audio


import streamlit as st

st.set_page_config(
    page_title="MeetMind AI",
    page_icon = "🧠",
    layout = "wide",
)


#Creating Sidebar
with st.sidebar:
    st.header("📁 Upload Meeting")
    uploaded_file = st.file_uploader(
        "Choose a meeting file",
        type=["mp3","wav","mp4","pdf","txt"]
    )
    
    #Meeting Type
    meeting_type = st.selectbox(
        "Meeting Type",
        [
            "Team Meeting",
            "Client Meeting",
            "Interview",
            "Conference",
            "Other"
        ]
    )

    st.divider()
    
    analyze = st.button(
        "📊 Analyze Meeting",
        use_container_width=True
    )

st.title("🧠 MeetMind AI")
st.subheader("Transform meetings into Actionable Insights")

st.divider()


# #Generate Button
# generate = st.button("🚀 Generate Summary")

#Welcome Section
if uploaded_file is None:
    st.info(
        """
        ### 👋 Welcome to MeetMind AI

        Upload a meeting recording or transcript to automatically generate:

        - 📄 Executive Summary
        - ✅ Action Items
        - 🎯 Key Decisions
        - ⚠️ Risks & Blockers
        - 📌 Follow-up Tasks

        Supported Formats:
        - MP3
        - WAV
        - PDF
        - TXT
        """
    )
    
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

#Testing Geminiv  
if st.button("🚀 Analyze"):

    if not document_text:
        st.warning("No text found to analyze.")
        st.stop()

    with st.spinner("🤖 AI is analyzing your meeting..."):

        try:

            prompt = f"""
Summarize the following meeting in simple professional language.

Meeting Transcript:

{document_text}
"""

            summary = ask_gemini(prompt)
            
            st.session_state["summary"] = summary
            
            if "summary" in st.session_state:
                st.divider()

            st.subheader("📝 AI Meeting Summary")
            st.markdown(st.session_state["summary"])
            # st.write(summary)
            
            st.download_button(
                label = "📥 Download Summary",
                data = st.session_state["summary"],
                file_name = "meeting_summary.txt",
                mime = "text/plain"
            )

        except Exception as e:

            st.exception(e)
                
if "summary" in st.session_state:
    st.subheader("📊 Meeting Insights")

    transcript_words = len(document_text.split())
    summary_words = len(st.session_state["summary"].split())

    compression = (
        (1 - summary_words /transcript_words) * 100
        if transcript_words else 0
    )
    st.divider()
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Transcript Words", transcript_words)
    metric2.metric("Summary Words", summary_words)
    metric3.metric("Compression",f"{compression:.1f}%")



#Progress Placeholder
st.divider()

st.subheader("⚙️ Processing Status")
st.progress(0)
st.caption("Waiting for Analysis...")

#Footer
st.divider()
st.markdown(
    "<center>MeetMind AI © 2026 | Powered by Gemini</center>",
    unsafe_allow_html=True
)