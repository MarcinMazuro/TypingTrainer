"""
Game screen component for the typing trainer application.
"""

import tkinter as tk
from config.settings import FONT, STATS_FONT_SIZE, TIME_FONT_SIZE, TEXT_FONT_SIZE, TOP_PADDING, LINE_SIZE

class GameScreen:
    def __init__(self, root, callbacks, theme_manager=None):
        self.root = root
        self.callbacks = callbacks  # Dictionary of callback functions
        self.theme_manager = theme_manager
        
        # Font and UI configuration
        self.font = FONT
        self.stats_font_size = STATS_FONT_SIZE
        self.time_font_size = TIME_FONT_SIZE
        self.text_font_size = TEXT_FONT_SIZE
        self.top_padding = TOP_PADDING
        
        # Initialize frame
        self.game_frame = tk.Frame(root)
        
        # Track padding frames for theme updates
        self.padding_frames = []
        
        # Get the initial background color from the theme manager if available
        bg_color = "#1e1e1e"  # Default dark mode color
        if self.theme_manager:
            bg_color = self.theme_manager.get_initial_bg_color()
        
        self.create_game_screen(bg_color)
    
    def create_game_screen(self, bg_color):
        # Add top padding with correct background color
        top_padding_frame = tk.Frame(self.game_frame, height=self.top_padding, bg=bg_color)
        top_padding_frame.pack(side=tk.TOP, fill=tk.X)
        self.padding_frames.append(top_padding_frame)
        
        self.stats_frame = tk.Frame(self.game_frame)
        self.stats_frame.pack(pady=5)
        
        self.menu_button = tk.Button(self.stats_frame, text="Menu", font=(self.font, int(self.stats_font_size*0.75)),
                                    command=self.callbacks['show_menu'])
        self.menu_button.grid(row=0, column=3, padx=10)
        
        self.theme_game_button = tk.Button(self.stats_frame, text="Dark Mode", font=(self.font, int(self.stats_font_size*0.75)),
                                    command=self.callbacks['toggle_theme'])
        self.theme_game_button.grid(row=0, column=4, padx=10)
        
        self.time_label = tk.Label(self.stats_frame, text="Time: 00:00", font=(self.font, self.time_font_size))
        self.time_label.grid(row=0, column=0, padx=10)
        
        self.wpm_label = tk.Label(self.stats_frame, text="WPM: 0", font=(self.font, self.stats_font_size))
        self.wpm_label.grid(row=0, column=1, padx=10)
        
        self.accuracy_label = tk.Label(self.stats_frame, text="Accuracy: 100%", font=(self.font, self.stats_font_size))
        self.accuracy_label.grid(row=0, column=2, padx=10)
        
        self.letter_frames = tk.Frame(self.game_frame)
        self.letter_frames.pack(pady=20)
    
    def display_text(self, text):
        """Display the text for typing exercise."""
        for widget in self.letter_frames.winfo_children():
            widget.destroy()
        
        column = 0
        row = 0
        displayed_indices = []
        
        # Get the current theme colors
        fg_color = "#000000"  # Default foreground color
        bg_color = "#ffffff"  # Default background color
        
        if self.theme_manager:
            current_theme = self.theme_manager.get_current_theme()
            fg_color = current_theme["fg"]
            bg_color = current_theme["bg"]
        
        for i, char in enumerate(text):
            display_char = char

            if column > LINE_SIZE and display_char == ' ':
                column = 0
                row += 1
                continue
                
            # Apply theme colors to the letter labels
            letter_label = tk.Label(self.letter_frames, text=display_char, font=("Courier", self.text_font_size), 
                                width=1, borderwidth=0, relief="flat", fg=fg_color, bg=bg_color)
            letter_label.grid(row=row, column=column, padx=1)
            
            displayed_indices.append(i)
            column += 1
        
        return displayed_indices
    
    def update_letter_color(self, index, color):
        """Update the color of a letter at the given index."""
        if index < len(self.letter_frames.winfo_children()):
            self.letter_frames.winfo_children()[index].config(foreground=color)
    
    def show(self):
        self.game_frame.pack(expand=True, fill="both")
    
    def hide(self):
        self.game_frame.pack_forget()
    
    def get_frames(self):
        return {
            'game_frame': self.game_frame,
            'stats_frame': self.stats_frame,
            'letter_frames': self.letter_frames,
            'padding_frames': self.padding_frames,
            'time_label': self.time_label,
            'wpm_label': self.wpm_label,
            'accuracy_label': self.accuracy_label,
            'theme_game_button': self.theme_game_button
        }