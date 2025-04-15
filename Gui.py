import tkinter as tk
import time
from utils import create_sentence, LINE_SIZE


class GUI:
    def __init__(self, keys_to_use):
        self.keys_to_use = keys_to_use
        
        self.root = tk.Tk()
        self.root.title("Typing Trainer")
        self.root.geometry("800x400")
        
        self.menu_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        
        self.current_text = [""]
        self.current_index = [0]
        self.timer_ids = []  # Track timer IDs for proper cleanup
        
        self.create_menu_screen()
        self.create_game_screen()
        self.show_menu()
    
    def create_menu_screen(self):
        title_label = tk.Label(self.menu_frame, text="Typing Trainer", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=40)
        
        buttons_frame = tk.Frame(self.menu_frame)
        buttons_frame.pack(pady=20)
        
        start_button = tk.Button(buttons_frame, text="Start", font=("Helvetica", 16),
                                 command=self.start_game, width=10)
        start_button.pack(pady=10)
        
        exit_button = tk.Button(buttons_frame, text="Exit", font=("Helvetica", 16),
                                command=self.exit_application, width=10)
        exit_button.pack(pady=10)
    
    def create_game_screen(self):
        self.stats_frame = tk.Frame(self.game_frame)
        self.stats_frame.pack(pady=5)
        
        self.menu_button = tk.Button(self.stats_frame, text="Menu", font=("Helvetica", 12),
                                    command=self.show_menu)
        self.menu_button.grid(row=0, column=3, padx=10)
        
        self.time_label = tk.Label(self.stats_frame, text="Time: 00:00", font=("Helvetica", 16))
        self.time_label.grid(row=0, column=0, padx=10)
        
        self.wpm_label = tk.Label(self.stats_frame, text="WPM: 0", font=("Helvetica", 16))
        self.wpm_label.grid(row=0, column=1, padx=10)
        
        self.accuracy_label = tk.Label(self.stats_frame, text="Accuracy: 100%", font=("Helvetica", 16))
        self.accuracy_label.grid(row=0, column=2, padx=10)
        
        self.letter_frames = tk.Frame(self.game_frame)
        self.letter_frames.pack(pady=20)
    
    def show_menu(self):
        self.cancel_all_timers()
        
        self.game_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill="both")
        self.root.unbind("<KeyPress>")
    
    def exit_application(self):
        self.cancel_all_timers()
        self.root.quit()
        self.root.destroy()
    
    def cancel_all_timers(self):
        for after_id in self.root.tk.call('after', 'info'):
            self.root.after_cancel(after_id)
    
    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")
        
        self.total_keystrokes = 0
        self.correct_keystrokes = 0
        self.chars_typed = 0
        self.current_index[0] = 0
        
        self.start_time = [time.time()]
        
        self.update_timer()
        self.update_stats()
        
        self.create_new_sentence()
        self.root.bind("<KeyPress>", self.on_key_press)
    
    def display_text(self, text):
        for widget in self.letter_frames.winfo_children():
            widget.destroy()
        
        column = 0
        row = 0
        self.displayed_indices = []
        
        for i, char in enumerate(text):
            display_char = char

            if column > LINE_SIZE and display_char == ' ':
                column = 0
                row += 1
                continue
                
            # Changed to Courier (monospace) font and fixed width
            letter_label = tk.Label(self.letter_frames, text=display_char, font=("Courier", 24), 
                                width=1, borderwidth=0, relief="flat")
            letter_label.grid(row=row, column=column, padx=1)  # Added small padding
            
            self.displayed_indices.append(i)
            column += 1
    
    def update_timer(self):
        elapsed_time = time.time() - self.start_time[0]
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_str = f"Time: {minutes:02d}:{seconds:02d}"
        
        self.time_label.config(text=time_str)
        timer_id = self.time_label.after(1000, self.update_timer)
        self.timer_ids.append(timer_id)
    
    def update_stats(self):
        elapsed_minutes = (time.time() - self.start_time[0]) / 60
        if elapsed_minutes > 0:
            wpm = int((self.chars_typed / 5) / elapsed_minutes)
        else:
            wpm = 0
            
        if self.total_keystrokes > 0:
            accuracy = (self.correct_keystrokes / self.total_keystrokes) * 100
        else:
            accuracy = 100
            
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        
        timer_id = self.root.after(1000, self.update_stats)
        self.timer_ids.append(timer_id)
    
    def create_new_sentence(self):
        new_text = create_sentence(self.keys_to_use)
        self.current_text[0] = new_text
        self.display_text(new_text)
        self.current_index[0] = 0
    
    def on_key_press(self, event):
        if len(self.letter_frames.winfo_children()) == 0:
            self.create_new_sentence()
            return

        if event.keysym == "space":
            pressed_char = ' '
        elif event.keysym == "period":
            pressed_char = '.'
        elif event.keysym == "comma":
            pressed_char = ','
        else:
            pressed_char = event.char

        self.total_keystrokes += 1
        
        if self.current_index[0] < len(self.current_text[0]) and pressed_char == self.current_text[0][self.current_index[0]]:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                # Only change color, not font weight
                letter_labels[displayed_idx].config(foreground="green", font=("Courier", 24))
            
            self.current_index[0] += 1
            self.correct_keystrokes += 1
            self.chars_typed += 1
        else:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                # Only change color, not font weight
                letter_labels[displayed_idx].config(foreground="red", font=("Courier", 24))
            
            self.current_index[0] += 1

        if self.current_index[0] == len(self.current_text[0]):
            self.create_new_sentence()
    
    def run(self):
        self.root.mainloop()