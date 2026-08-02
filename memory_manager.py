# At the top of memory_manager.py
from profile_analyzer import ProfileAnalyzer

# Inside MemoryManager class, add:
def __init__(self, username: str):
    self.username = username
    self.profile_analyzer = ProfileAnalyzer(os.getenv('OPENROUTER_API_KEY'))

# Update _get_system_prompt method:
def _get_system_prompt(self) -> str:
    """Get enhanced system prompt with memory context"""
    base_prompt = (
        "You are Nelavista, an advanced AI tutor for Nigerian university students.\n\n"
        "GLOBAL RULES:\n"
        "- Always respond in clean HTML using <p>, <ul>, <li>, <strong>, <h2>, <h3>.\n"
        "- No greetings unless user greets first.\n"
        "- Use neutral, precise language. Avoid hype or emotion.\n"
        "- Focus on academic content only.\n\n"
    )
    
    # Add history context
    history_context = self.get_user_history_context()
    if history_context:
        base_prompt += f"{history_context}\n\n"
    
    # Add profile context (subtle, academic)
    profile_context = self.profile_analyzer.get_profile_context(self.username)
    if profile_context:
        base_prompt += f"{profile_context}\n"
    
    return base_prompt

# Update save_to_memory method to trigger profile analysis:
def save_to_memory(self, question: str, answer: str):
    """Save Q&A to long-term memory and trigger profile analysis"""
    try:
        # Save Q&A
        new_q = UserQuestions(
            username=self.username,
            question=question[:500],
            answer=answer[:1000]
        )
        db.session.add(new_q)
        db.session.commit()
        
        # Trigger profile analysis (async)
        self.trigger_profile_analysis()
        
        # Clean old entries
        self.clean_old_entries()
        
    except Exception as e:
        debug_print(f"⚠️ Error saving to memory: {e}")
        db.session.rollback()
    
def trigger_profile_analysis(self):
    """Trigger profile analysis (non-blocking)"""
    import threading
    
    def analyze_async():
        try:
            self.profile_analyzer.update_profile(self.username)
        except Exception as e:
            debug_print(f"⚠️ Async profile analysis failed: {e}")
    
    # Run in background thread
    thread = threading.Thread(target=analyze_async)
    thread.daemon = True
    thread.start()