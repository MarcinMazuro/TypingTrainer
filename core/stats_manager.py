"""
Stats manager for tracking typing performance.
"""

import time

class StatsManager:
    def __init__(self, gui_elements):
        self.gui_elements = gui_elements
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        self.start_time = time.time()
        self.timer_ids = []
        self.time_limit = 0  # 0 means no time limit (freeplay)
        self.gui = gui_elements.get('gui')  # Reference to GUI object
    
    def reset_stats(self, time_limit=0):
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        self.start_time = time.time()
        self.time_limit = time_limit
    
    def register_keystroke(self, is_correct):
        self.total_keystrokes += 1
        if is_correct:
            self.correct_keystrokes += 1
        self.chars_typed += 1
    
    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        
        # Check if time limit is set and has been reached
        if self.time_limit > 0 and elapsed_time >= self.time_limit:
            # Time's up - show results screen
            if self.gui:
                self.gui.show_results()
            return
            
        # If time limit is set, show countdown
        if self.time_limit > 0:
            remaining = max(0, self.time_limit - elapsed_time)
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            time_str = f"Time: {minutes:02d}:{seconds:02d}"
        else:  # Show elapsed time for freeplay
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        self.gui_elements['time_label'].config(text=time_str)
        timer_id = self.gui_elements['root'].after(1000, self.update_timer)
        self.timer_ids.append(timer_id)
    
    def calculate_wpm(self):
        """Calculate words per minute"""
        elapsed_minutes = (time.time() - self.start_time) / 60
        
        if elapsed_minutes > 0:
            wpm = int((self.correct_keystrokes / 5) / elapsed_minutes)
        else:
            wpm = 0
            
        return wpm
        
    def calculate_accuracy(self):
        """Calculate accuracy percentage"""
        if self.total_keystrokes > 0:
            accuracy = (self.correct_keystrokes / self.total_keystrokes) * 100
        else:
            accuracy = 100
            
        return accuracy
    
    def update_stats(self):
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()
            
        self.gui_elements['wpm_label'].config(text=f"WPM: {wpm}")
        self.gui_elements['accuracy_label'].config(text=f"Accuracy: {accuracy:.1f}%")
        
        timer_id = self.gui_elements['root'].after(1000, self.update_stats)
        self.timer_ids.append(timer_id)
    
    def get_timer_ids(self):
        return self.timer_ids
        
    def cancel_timers(self):
        """Cancel all active timers in the stats manager"""
        for timer_id in self.timer_ids:
            try:
                self.gui_elements['root'].after_cancel(timer_id)
            except Exception:
                pass
        self.timer_ids = []

    def update_stats_based_on_color(self, color):
        """Update statistics based on the color of the deleted letter."""
        if color.lower() in ("red", "#ff4444"):
            self.total_keystrokes -= 1
        elif color.lower() in ("green", "#00cc00"):
            self.total_keystrokes -= 1
            self.correct_keystrokes -= 1
        # Add more color-based logic if needed

        self.update_stats()
        
    def get_elapsed_time(self):
        """Get the elapsed time since starting."""
        return time.time() - self.start_time