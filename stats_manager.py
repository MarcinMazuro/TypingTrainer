import time

class StatsManager:
    def __init__(self, gui_elements):
        self.gui_elements = gui_elements
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        self.start_time = time.time()
        self.timer_ids = []
    
    def reset_stats(self):
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        self.start_time = time.time()
    
    def register_keystroke(self, is_correct):
        self.total_keystrokes += 1
        if is_correct:
            self.correct_keystrokes += 1
        self.chars_typed += 1
    
    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        self.gui_elements['time_label'].config(text=time_str)
        timer_id = self.gui_elements['time_label'].after(1000, self.update_timer)
        self.timer_ids.append(timer_id)
    
    def update_stats(self):
        elapsed_minutes = (time.time() - self.start_time) / 60
        
        if elapsed_minutes > 0:
            wpm = int((self.chars_typed / 5) / elapsed_minutes)
        else:
            wpm = 0
            
        if self.total_keystrokes > 0:
            accuracy = (self.correct_keystrokes / self.total_keystrokes) * 100
        else:
            accuracy = 100
            
        self.gui_elements['wpm_label'].config(text=f"WPM: {wpm}")
        self.gui_elements['accuracy_label'].config(text=f"Accuracy: {accuracy:.1f}%")
        
        timer_id = self.gui_elements['root'].after(1000, self.update_stats)
        self.timer_ids.append(timer_id)
    
    def get_timer_ids(self):
        return self.timer_ids
