"""
Timer State Manager - Manages saving and loading of timer state
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


class TimerStateManager:
    """Manages saving and loading timer state for session persistence"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.state_file = os.path.join(data_dir, "timer_state.json")
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_timer_state(self, timer_core) -> bool:
        """
        Save current timer state to file
        Returns True if successful, False otherwise
        """
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            state_data = {
                "date": current_date,
                "timestamp": datetime.now().isoformat(),
                "timer_state": {
                    "main_running": timer_core.main_running,
                    "break_running": timer_core.break_running,
                    "main_time": timer_core.main_time,
                    "break_time": timer_core.break_time,
                    "break_session_time": timer_core.break_session_time,
                    "current_session": timer_core.current_session,
                    "target_sessions": timer_core.target_sessions,
                    "session_duration": timer_core.session_duration,
                    "break_duration": timer_core.break_duration,
                    "auto_continue": timer_core.auto_continue,
                    "last_session_check": timer_core.last_session_check,
                    "session_completed": timer_core.session_completed,
                    "all_sessions_completed": timer_core.all_sessions_completed,
                    "waiting_for_user_choice": timer_core.waiting_for_user_choice
                }
            }
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving timer state: {e}")
            return False
    
    def load_timer_state(self) -> Optional[Dict]:
        """
        Load timer state from file if it exists and is from today
        Returns state dict if successful, None otherwise
        """
        try:
            if not os.path.exists(self.state_file):
                return None
            
            with open(self.state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
            
            # Check if the saved state is from today
            saved_date = state_data.get("date", "")
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            if saved_date != current_date:
                # State is from a different day, don't restore
                return None
            
            return state_data.get("timer_state", {})
            
        except Exception as e:
            print(f"Error loading timer state: {e}")
            return None
    
    def restore_timer_state(self, timer_core, state_data: Dict) -> bool:
        """
        Restore timer state from loaded data
        Returns True if successful, False otherwise
        """
        try:
            # Restore all timer core properties
            timer_core.main_running = state_data.get("main_running", False)
            timer_core.break_running = state_data.get("break_running", False)
            timer_core.main_time = state_data.get("main_time", 0)
            timer_core.break_time = state_data.get("break_time", 0)
            timer_core.break_session_time = state_data.get("break_session_time", 0)
            timer_core.current_session = state_data.get("current_session", 0)
            timer_core.target_sessions = state_data.get("target_sessions", 8)
            timer_core.session_duration = state_data.get("session_duration", 3600)
            timer_core.break_duration = state_data.get("break_duration", 300)
            timer_core.auto_continue = state_data.get("auto_continue", False)
            timer_core.last_session_check = state_data.get("last_session_check", 0)
            timer_core.session_completed = state_data.get("session_completed", False)
            timer_core.all_sessions_completed = state_data.get("all_sessions_completed", False)
            timer_core.waiting_for_user_choice = state_data.get("waiting_for_user_choice", False)
            
            return True
            
        except Exception as e:
            print(f"Error restoring timer state: {e}")
            return False
    
    def clear_timer_state(self) -> bool:
        """
        Clear saved timer state file
        Returns True if successful, False otherwise
        """
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
            return True
        except Exception as e:
            print(f"Error clearing timer state: {e}")
            return False
    
    def has_saved_state_today(self) -> bool:
        """
        Check if there's a saved state from today
        Returns True if there's a valid state from today, False otherwise
        """
        state_data = self.load_timer_state()
        return state_data is not None
