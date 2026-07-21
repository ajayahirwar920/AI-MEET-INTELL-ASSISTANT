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
    st.caption(f"Saved to: {saved_path.name}")
    

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

st.subheader("📊 Meeting Insights")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric("📄 Pages", "--")
metric2.metric("✅ Action Items", "--")
metric3.metric("⚠️ Risks", "--")
metric4.metric("⏱️ Watch Duration", "--")


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