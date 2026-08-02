# tutor_formatter.py
class TutorFormatter:
    @staticmethod
    def format_analysis(analysis_result: Dict) -> str:
        """Format ANY analysis into consistent tutor response"""
        subject = analysis_result.get("subject", "Mathematics")
        topic = analysis_result.get("topic", "Unknown Topic")
        summary = analysis_result.get("summary", "")
        
        # ALWAYS use this exact format
        return f"""
## Analysis Complete

**Subject:** {subject}
**Topic:** {topic}

**What I See:**
{summary}

**Next Steps:**
1. Explain step-by-step
2. Relate to course material
3. Generate practice questions

*How would you like to proceed?*
""".strip()
    
    @staticmethod
    def format_follow_up(context: Dict, question: str) -> str:
        """Format follow-up questions using context"""
        subject = context.get("subject", "the subject")
        topic = context.get("topic", "this topic")
        
        if "course" in question.lower():
            return f"This is from **{subject}**, specifically covering **{topic}**."
        
        if "explain" in question.lower():
            return f"Let me explain **{topic}** in {subject} step by step."
        
        return f"I see you're asking about {topic} in {subject}. How can I help?"