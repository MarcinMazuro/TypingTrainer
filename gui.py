import tkinter as tk
import time
from utils import LINE_SIZE
from theme_manager import ThemeManager
from text_generator import TextGenerator
from stats_manager import StatsManager

class GUI:
    def __init__(self, keys_to_use):
        self.keys_to_use = keys_to_use
        
        self.root = tk.Tk()
        # Font and UI configuration variables
        self.font = "Helvetica"  # The main font to use throughout the app
        self.top_padding = 30    # Padding from the top of the window
        self.font_size = 32
        self.menu_font_size = 24
        self.text_font_size = 32
        self.stats_font_size = 16
        self.time_font_size = 16
        self.root.title("Typing Trainer")
        self.root.geometry("800x400")
        
        # Initialize modules
        self.theme_manager = ThemeManager(self.root)
        self.text_generator = TextGenerator()
        
        self.menu_frame = tk.Frame(self.root)
        self.game_frame = tk.Frame(self.root)
        
        # Track padding frames for theme updates
        self.padding_frames = []
        
        self.current_text = [""]
        self.current_index = [0]
        self.displayed_indices = []
        
        self.create_menu_screen()
        self.create_game_screen()
        
        # Create GUI elements dictionary for theme manager
        self.gui_elements = {
            'tk': tk,
            'root': self.root,
            'menu_frame': self.menu_frame,
            'game_frame': self.game_frame,
            'padding_frames': self.padding_frames,
            'theme_button': self.theme_button,
            'theme_game_button': self.theme_game_button,
            'stats_frame': self.stats_frame,
            'letter_frames': self.letter_frames
        }
        
        # Initialize stats manager
        self.stats_manager = StatsManager({
            'root': self.root,
            'time_label': self.time_label,
            'wpm_label': self.wpm_label,
            'accuracy_label': self.accuracy_label
        })
        
        self.theme_manager.apply_theme(self.gui_elements)
        self.show_menu()
    
    def create_menu_screen(self):
        # Add top padding
        top_padding_frame = tk.Frame(self.menu_frame, height=self.top_padding)
        top_padding_frame.pack(side=tk.TOP, fill=tk.X)
        self.padding_frames.append(top_padding_frame)
        
        title_label = tk.Label(self.menu_frame, text="Typing Trainer", font=(self.font, self.menu_font_size, "bold"))
        title_label.pack(pady=40)
        
        buttons_frame = tk.Frame(self.menu_frame)
        buttons_frame.pack(pady=20)
        
        start_button = tk.Button(buttons_frame, text="Start", font=(self.font, self.stats_font_size),
                                 command=self.start_game, width=10)
        start_button.pack(pady=10)
        
        theme_button = tk.Button(buttons_frame, text="Dark Mode", font=(self.font, self.stats_font_size),
                               command=self.toggle_theme, width=10)
        theme_button.pack(pady=10)
        self.theme_button = theme_button
        
        exit_button = tk.Button(buttons_frame, text="Exit", font=(self.font, self.stats_font_size),
                                command=self.exit_application, width=10)
        exit_button.pack(pady=10)
    
    def create_game_screen(self):
        # Add top padding
        top_padding_frame = tk.Frame(self.game_frame, height=self.top_padding)
        top_padding_frame.pack(side=tk.TOP, fill=tk.X)
        self.padding_frames.append(top_padding_frame)
        
        self.stats_frame = tk.Frame(self.game_frame)
        self.stats_frame.pack(pady=5)
        
        self.menu_button = tk.Button(self.stats_frame, text="Menu", font=(self.font, int(self.stats_font_size*0.75)),
                                    command=self.show_menu)
        self.menu_button.grid(row=0, column=3, padx=10)
        
        self.theme_game_button = tk.Button(self.stats_frame, text="Dark Mode", font=(self.font, int(self.stats_font_size*0.75)),
                                    command=self.toggle_theme)
        self.theme_game_button.grid(row=0, column=4, padx=10)
        
        self.time_label = tk.Label(self.stats_frame, text="Time: 00:00", font=(self.font, self.time_font_size))
        self.time_label.grid(row=0, column=0, padx=10)
        
        self.wpm_label = tk.Label(self.stats_frame, text="WPM: 0", font=(self.font, self.stats_font_size))
        self.wpm_label.grid(row=0, column=1, padx=10)
        
        self.accuracy_label = tk.Label(self.stats_frame, text="Accuracy: 100%", font=(self.font, self.stats_font_size))
        self.accuracy_label.grid(row=0, column=2, padx=10)
        
        self.letter_frames = tk.Frame(self.game_frame)
        self.letter_frames.pack(pady=20)
    
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.theme_manager.apply_theme(self.gui_elements)
    
    def show_menu(self):
        # Make sure to cancel all timers before switching screens
        self.cancel_all_timers()
        
        # Ensure these are done in the right order
        self.root.unbind("<KeyPress>")
        self.game_frame.pack_forget()
        self.menu_frame.pack(expand=True, fill="both")
    
    def exit_application(self):
        # First cancel all timers to prevent callbacks during destruction
        self.cancel_all_timers()
        
        # Unbind key events
        self.root.unbind("<KeyPress>")
        
        try:
            # Quit the mainloop first
            self.root.quit()
        except Exception:
            pass
            
        try:
            # Then destroy the window
            self.root.destroy()
        except Exception:
            pass
    
    def cancel_all_timers(self):
        # Cancel stats manager timers
        if hasattr(self, 'stats_manager'):
            self.stats_manager.cancel_timers()
            
        # Cancel any other after callbacks
        try:
            for after_id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(after_id)
        except Exception:
            pass
    
    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")
        
        self.stats_manager.reset_stats()
        self.current_index[0] = 0
        
        self.stats_manager.update_timer()
        self.stats_manager.update_stats()
        
        self.create_new_sentence()
        self.theme_manager.apply_theme(self.gui_elements)
        self.root.bind("<KeyPress>", self.on_key_press)
    
    def display_text(self, text):
        for widget in self.letter_frames.winfo_children():
            widget.destroy()
        
        column = 0
        row = 0
        self.displayed_indices = []
        current_theme = self.theme_manager.get_current_theme()
        
        for i, char in enumerate(text):
            display_char = char

            if column > LINE_SIZE and display_char == ' ':
                column = 0
                row += 1
                continue
                
            # Add theme colors to the letter labels
            letter_label = tk.Label(self.letter_frames, text=display_char, font=("Courier", self.text_font_size), 
                                width=1, borderwidth=0, relief="flat",
                                bg=current_theme["bg"], fg=current_theme["fg"])
            letter_label.grid(row=row, column=column, padx=1)
            
            self.displayed_indices.append(i)
            column += 1
    
    def create_new_sentence(self):
        new_text = self.text_generator.create_english_sentence(self.keys_to_use)
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

        current_theme = self.theme_manager.get_current_theme()
        
        if self.current_index[0] < len(self.current_text[0]) and pressed_char == self.current_text[0][self.current_index[0]]:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                letter_labels[displayed_idx].config(foreground=current_theme["correct"], font=("Courier", self.text_font_size))
            
            self.stats_manager.register_keystroke(True)
            self.current_index[0] += 1
        else:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                letter_labels[displayed_idx].config(foreground=current_theme["incorrect"], font=("Courier", self.text_font_size))
            
            self.stats_manager.register_keystroke(False)
            self.current_index[0] += 1

        if self.current_index[0] == len(self.current_text[0]):
            self.create_new_sentence()
    
    def run(self):
        self.root.mainloop()
