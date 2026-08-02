# context_manager.py
class ContextManager:
    def __init__(self):
        # In-memory for now, later Redis
        self.sessions = {}
    
    def get_session(self, session_id):
        """Get or create session context"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "last_file_hash": None,
                "last_subject": None,
                "last_topic": None,
                "conversation": []
            }
        return self.sessions[session_id]
    
    def update_file_context(self, session_id, file_hash, subject, topic):
        """Store what file we just analyzed"""
        session = self.get_session(session_id)
        session["last_file_hash"] = file_hash
        session["last_subject"] = subject
        session["last_topic"] = topic
        return True
    
    def should_reanalyze(self, session_id, file_hash):
        """Check if same file was just analyzed"""
        session = self.get_session(session_id)
        return session["last_file_hash"] != file_hash
    
    def get_last_context(self, session_id):
        """What was the last thing we talked about?"""
        session = self.get_session(session_id)
        return {
            "subject": session["last_subject"],
            "topic": session["last_topic"]
        }