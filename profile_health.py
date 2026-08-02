# profile_health.py
import psutil
from datetime import datetime, timedelta
import json

class ProfileHealthMonitor:
    """Monitor profile analysis system health"""
    
    def __init__(self):
        self.analysis_log = []
        self.max_log_size = 100
    
    def log_analysis(self, username: str, success: bool, duration: float, fields_updated: int):
        """Log analysis attempt"""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'username': username,
            'success': success,
            'duration': duration,
            'fields_updated': fields_updated,
            'memory_used': psutil.Process().memory_info().rss / 1024 / 1024  # MB
        }
        
        self.analysis_log.append(entry)
        
        # Keep log manageable
        if len(self.analysis_log) > self.max_log_size:
            self.analysis_log = self.analysis_log[-self.max_log_size:]
    
    def get_health_status(self) -> dict:
        """Get system health status"""
        if not self.analysis_log:
            return {"status": "no_analyses_yet"}
        
        recent_logs = [log for log in self.analysis_log 
                      if datetime.fromisoformat(log['timestamp']) > datetime.utcnow() - timedelta(hours=1)]
        
        if not recent_logs:
            return {"status": "idle"}
        
        success_rate = sum(1 for log in recent_logs if log['success']) / len(recent_logs)
        avg_duration = sum(log['duration'] for log in recent_logs) / len(recent_logs)
        
        return {
            "status": "healthy" if success_rate > 0.8 else "degraded",
            "success_rate": success_rate,
            "avg_duration_seconds": avg_duration,
            "recent_analyses": len(recent_logs),
            "memory_usage_mb": psutil.Process().memory_info().rss / 1024 / 1024
        }
    
    def should_throttle(self) -> bool:
        """Check if we should throttle analysis due to health"""
        status = self.get_health_status()
        
        # Throttle if:
        # 1. Success rate below 50%
        # 2. Average duration > 30 seconds
        # 3. Memory usage > 500MB
        if (status.get('success_rate', 1.0) < 0.5 or
            status.get('avg_duration_seconds', 0) > 30 or
            status.get('memory_usage_mb', 0) > 500):
            return True
        
        return False

# Global instance
health_monitor = ProfileHealthMonitor()