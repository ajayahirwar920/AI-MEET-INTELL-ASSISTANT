import streamlit as st

st.set_page_config(
    page_title="MeetMind AI",
    page_icon = "🧠",
    layout = "wide",
)

st.title("🧠 MeetMind AI")
st.subheader("Transform meetings into Actionable Insights")

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

#Generate Button
generate = st.button("🚀 Generate Summary")

#File Info
if uploaded_file:
    st.success("File Uploaded Successfully!")
    
    st.write("** File Information **")
    
    st.write(f"**Filename:**{uploaded_file.name}")
    st.write(f"**Type:**{uploaded_file.type}")
    st.write(f"**Size:**{uploaded_file.size / 1024:.2f}KB")
    