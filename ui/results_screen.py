"""
Results screen component for the typing trainer application.
"""

import tkinter as tk
from config.settings import FONT, MENU_FONT_SIZE, STATS_FONT_SIZE, TOP_PADDING

class ResultsScreen:
    def __init__(self, root, callbacks, theme_manager=None):
        self.root = root
        self.callbacks = callbacks  # Dictionary of callback functions
        self.theme_manager = theme_manager
        
        # Font and UI configuration
        self.font = FONT
        self.menu_font_size = MENU_FONT_SIZE
        self.stats_font_size = STATS_FONT_SIZE
        self.top_padding = TOP_PADDING
        
        # Initialize frame
        self.results_frame = tk.Frame(root)
        
        # Track padding frames for theme updates
        self.padding_frames = []
        
        # Get the initial background color from the theme manager if available
        bg_color = "#1e1e1e"  # Default dark mode color
        if self.theme_manager:
            bg_color = self.theme_manager.get_initial_bg_color()
        
        self.create_results_screen(bg_color)
    
    def create_results_screen(self, bg_color):
        # Add top padding with correct background color
        top_padding_frame = tk.Frame(self.results_frame, height=self.top_padding, bg=bg_color)
        top_padding_frame.pack(side=tk.TOP, fill=tk.X)
        self.padding_frames.append(top_padding_frame)
        
        # Results title
        results_title = tk.Label(self.results_frame, text="Your Results", font=(self.font, self.menu_font_size, "bold"))
        results_title.pack(pady=20)
        
        # Statistics display
        stats_display = tk.Frame(self.results_frame)
        stats_display.pack(pady=20)
        
        self.result_wpm_label = tk.Label(stats_display, text="WPM: 0", font=(self.font, self.menu_font_size))
        self.result_wpm_label.pack(pady=5)
        
        self.result_accuracy_label = tk.Label(stats_display, text="Accuracy: 100%", font=(self.font, self.menu_font_size))
        self.result_accuracy_label.pack(pady=5)
        
        self.result_time_label = tk.Label(stats_display, text="Time: 00:00", font=(self.font, self.menu_font_size))
        self.result_time_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.results_frame)
        button_frame.pack(pady=20)
        
        menu_button = tk.Button(button_frame, text="Menu", font=(self.font, self.stats_font_size),
                             command=self.callbacks['show_menu'], width=10)
        menu_button.pack(side=tk.LEFT, padx=10)
        
        exit_button = tk.Button(button_frame, text="Exit", font=(self.font, self.stats_font_size),
                             command=self.callbacks['exit_application'], width=10)
        exit_button.pack(side=tk.RIGHT, padx=10)
    
    def update_results(self, wpm, accuracy, elapsed_time):
        """Update the result labels with final stats."""
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        self.result_wpm_label.config(text=f"WPM: {wpm}")
        self.result_accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        self.result_time_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
    
    def show(self):
        self.results_frame.pack(expand=True, fill="both")
    
    def hide(self):
        self.results_frame.pack_forget()
    
    def get_frames(self):
        return {
            'results_frame': self.results_frame,
            'padding_frames': self.padding_frames
        }