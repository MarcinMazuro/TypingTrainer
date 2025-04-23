"""
Menu screen component for the typing trainer application.
"""

import tkinter as tk
from config.settings import FONT, MENU_FONT_SIZE, STATS_FONT_SIZE, TOP_PADDING

class MenuScreen:
    def __init__(self, root, callbacks, theme_manager=None):
        self.root = root
        self.callbacks = callbacks  # Dictionary of callback functions
        self.theme_manager = theme_manager
        
        # Font and UI configuration
        self.font = FONT
        self.menu_font_size = MENU_FONT_SIZE
        self.stats_font_size = STATS_FONT_SIZE
        self.top_padding = TOP_PADDING
        
        # Initialize frames
        self.menu_frame = tk.Frame(root)
        self.custom_time_frame = tk.Frame(self.menu_frame)
        self.custom_keys_frame = tk.Frame(self.menu_frame)
        self.main_menu_frame = tk.Frame(self.menu_frame)
        
        # Track padding frames for theme updates
        self.padding_frames = []
        
        # Get the initial background color from the theme manager if available
        bg_color = "#1e1e1e"  # Default dark mode color
        if self.theme_manager:
            bg_color = self.theme_manager.get_initial_bg_color()
        
        self.create_menu_screen(bg_color)
        self.create_custom_time_content()
        self.create_custom_keys_content()
        
        # Initialize with main menu showing
        self.show_main_menu()
    
    def create_menu_screen(self, bg_color):
        # Add top padding with correct background color
        top_padding_frame = tk.Frame(self.menu_frame, height=self.top_padding, bg=bg_color)
        top_padding_frame.pack(side=tk.TOP, fill=tk.X)
        self.padding_frames.append(top_padding_frame)
        
        title_label = tk.Label(self.menu_frame, text="Typing Trainer", font=(self.font, self.menu_font_size, "bold"))
        title_label.pack(pady=40)
        
        # Create main menu content
        self.create_main_menu_content(self.main_menu_frame)
    
    def create_main_menu_content(self, parent_frame):
        # Mode selection buttons
        mode_label = tk.Label(parent_frame, text="Select Mode:", font=(self.font, self.stats_font_size))
        mode_label.pack(pady=5)
        
        modes_frame = tk.Frame(parent_frame)
        modes_frame.pack(pady=5)
        
        one_min_button = tk.Button(modes_frame, text="1 Minute", font=(self.font, self.stats_font_size),
                                command=lambda: self.callbacks['set_time_mode']("1min"), width=10)
        one_min_button.grid(row=0, column=0, padx=5, pady=5)
        
        five_min_button = tk.Button(modes_frame, text="5 Minutes", font=(self.font, self.stats_font_size),
                                 command=lambda: self.callbacks['set_time_mode']("5min"), width=10)
        five_min_button.grid(row=0, column=1, padx=5, pady=5)
        
        custom_time_button = tk.Button(modes_frame, text="Custom Time", font=(self.font, self.stats_font_size),
                                    command=self.show_custom_time, width=10)
        custom_time_button.grid(row=1, column=0, padx=5, pady=5)
        
        freeplay_button = tk.Button(modes_frame, text="Freeplay", font=(self.font, self.stats_font_size),
                                  command=lambda: self.callbacks['set_time_mode']("freeplay"), width=10)
        freeplay_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Settings buttons
        settings_frame = tk.Frame(parent_frame)
        settings_frame.pack(pady=10)
        
        # Add custom keys button
        custom_keys_button = tk.Button(settings_frame, text="Custom Keys", font=(self.font, self.stats_font_size),
                                     command=self.show_custom_keys, width=10)
        custom_keys_button.pack(pady=10)
        
        theme_button = tk.Button(settings_frame, text="Dark Mode", font=(self.font, self.stats_font_size),
                               command=self.callbacks['toggle_theme'], width=10)
        theme_button.pack(pady=10)
        self.theme_button = theme_button
        
        exit_button = tk.Button(settings_frame, text="Exit", font=(self.font, self.stats_font_size),
                                command=self.callbacks['exit_application'], width=10)
        exit_button.pack(pady=10)
    
    def create_custom_time_content(self):
        time_label = tk.Label(self.custom_time_frame, text="Enter time in seconds:", 
                             font=(self.font, self.stats_font_size))
        time_label.pack(pady=10)
        
        self.time_entry = tk.Entry(self.custom_time_frame, font=(self.font, self.stats_font_size),
                                  width=10)
        self.time_entry.pack(pady=10)
        
        buttons_frame = tk.Frame(self.custom_time_frame)
        buttons_frame.pack(pady=20)
        
        ok_button = tk.Button(buttons_frame, text="OK", 
                            font=(self.font, self.stats_font_size),
                            command=lambda: self.set_custom_time(self.time_entry.get()),
                            width=10)
        ok_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(buttons_frame, text="Cancel", 
                                font=(self.font, self.stats_font_size),
                                command=self.show_main_menu,
                                width=10)
        cancel_button.pack(side=tk.RIGHT, padx=10)
    
    def create_custom_keys_content(self):
        keys_label = tk.Label(self.custom_keys_frame, text="Enter keys to practice with:", 
                             font=(self.font, self.stats_font_size))
        keys_label.pack(pady=10)
        
        self.keys_entry = tk.Entry(self.custom_keys_frame, font=(self.font, self.stats_font_size),
                                 width=20)
        self.keys_entry.pack(pady=10)
        
        # Add a note about the keys
        note_label = tk.Label(self.custom_keys_frame, text="Use letters, numbers, and special characters", 
                             font=(self.font, int(self.stats_font_size*0.7)))
        note_label.pack(pady=5)
        
        reset_button = tk.Button(self.custom_keys_frame, text="Reset to Default", 
                               font=(self.font, int(self.stats_font_size*0.8)),
                               command=self.callbacks['reset_to_default_keys'],
                               width=15)
        reset_button.pack(pady=10)
        
        buttons_frame = tk.Frame(self.custom_keys_frame)
        buttons_frame.pack(pady=20)
        
        ok_button = tk.Button(buttons_frame, text="OK", 
                            font=(self.font, self.stats_font_size),
                            command=self.set_custom_keys,
                            width=10)
        ok_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(buttons_frame, text="Cancel", 
                                font=(self.font, self.stats_font_size),
                                command=self.show_main_menu,
                                width=10)
        cancel_button.pack(side=tk.RIGHT, padx=10)
    
    def show_main_menu(self):
        # Hide custom time input and show main menu
        self.custom_time_frame.pack_forget()
        self.custom_keys_frame.pack_forget()
        self.main_menu_frame.pack(pady=20)
    
    def show_custom_time(self):
        # Hide main menu and show custom time input
        self.main_menu_frame.pack_forget()
        self.custom_keys_frame.pack_forget()
        self.custom_time_frame.pack(pady=20)
        self.time_entry.focus_set()
        self.time_entry.delete(0, tk.END)  # Clear any previous input
    
    def show_custom_keys(self):
        # Hide main menu and show custom keys input
        self.main_menu_frame.pack_forget()
        self.custom_time_frame.pack_forget()
        self.custom_keys_frame.pack(pady=20)
        self.keys_entry.focus_set()
        self.keys_entry.delete(0, tk.END)
        self.keys_entry.insert(0, self.callbacks['get_keys_to_use']())
    
    def set_custom_time(self, time_str):
        try:
            time_sec = int(time_str)
            if time_sec > 0:
                self.callbacks['set_custom_time'](time_sec)
                self.show_main_menu()  # First return to main menu
                self.callbacks['set_time_mode']("custom")  # Then set the time mode
            else:
                # Show error if time is zero or negative
                tk.messagebox.showerror("Invalid Input", "Please enter a positive number of seconds.")
        except ValueError:
            # Show error if input is not a valid number
            tk.messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")
    
    def set_custom_keys(self):
        new_keys = self.keys_entry.get().strip()
        if new_keys:
            self.callbacks['set_custom_keys'](new_keys)
        self.show_main_menu()
    
    def show(self):
        self.menu_frame.pack(expand=True, fill="both")
    
    def hide(self):
        self.menu_frame.pack_forget()
    
    def get_frames(self):
        return {
            'menu_frame': self.menu_frame,
            'main_menu_frame': self.main_menu_frame,
            'custom_time_frame': self.custom_time_frame,
            'custom_keys_frame': self.custom_keys_frame,
            'padding_frames': self.padding_frames,
            'theme_button': self.theme_button
        }