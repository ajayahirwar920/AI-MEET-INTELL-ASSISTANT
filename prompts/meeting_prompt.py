def meeting_analysis_prompt(transcript: str) -> str:
    return f"""
You are an AI meeting Intelligence Assistant.
Analyze the following meeting transcript and generate a professional report.
Return your response in the following format:

#Executive Summary
Write a concise summary of the meeting.

#Action Items
List Every action item discussed.

#Key Decisions
Mention all important decisions taken.

# Risks & Blockers
List the next steps discussed.
If not exists, write "NONE".

# Follow-up tasks
List the next steps discussed.
Meeting Transcript:
{transcript}
"""