"""
Main GUI class for the Typing Trainer application.
"""

import tkinter as tk
from tkinter import messagebox

from config.settings import DEFAULT_KEYS, DEFAULT_WINDOW_SIZE
from core.text_generator import TextGenerator
from core.theme_manager import ThemeManager
from core.stats_manager import StatsManager
from ui.menu_screen import MenuScreen
from ui.game_screen import GameScreen
from ui.results_screen import ResultsScreen

class GUI:
    def __init__(self, keys_to_use):
        self.keys_to_use = keys_to_use
        self.default_keys = keys_to_use  # Store the default keys
        
        # Initialize window
        self.root = tk.Tk()
        self.root.title("Typing Trainer")
        self.root.geometry(DEFAULT_WINDOW_SIZE)
        
        # Initialize modules
        self.theme_manager = ThemeManager(self.root)
        self.text_generator = TextGenerator()
        
        # Game state variables
        self.current_text = [""]
        self.current_index = [0]
        self.displayed_indices = []
        self.time_mode = "freeplay"  # Default mode
        self.custom_time = 0
        
        # Create callbacks for UI components
        self.callbacks = self.create_callbacks()
        
        # Create UI components - pass theme_manager to each one
        self.menu_screen = MenuScreen(self.root, self.callbacks, self.theme_manager)
        self.game_screen = GameScreen(self.root, self.callbacks, self.theme_manager)
        self.results_screen = ResultsScreen(self.root, self.callbacks, self.theme_manager)
        
        # Create GUI elements dictionary for theme manager
        self.gui_elements = {
            'tk': tk,
            'root': self.root,
            'padding_frames': [],  # Initialize an empty list for all padding frames
            **self.menu_screen.get_frames(),
            **self.game_screen.get_frames(),
            **self.results_screen.get_frames()
        }
        
        # Combine all padding frames from different screens into one list
        if 'padding_frames' in self.menu_screen.get_frames():
            self.gui_elements['padding_frames'].extend(self.menu_screen.get_frames()['padding_frames'])
        if 'padding_frames' in self.game_screen.get_frames():
            self.gui_elements['padding_frames'].extend(self.game_screen.get_frames()['padding_frames'])
        if 'padding_frames' in self.results_screen.get_frames():
            self.gui_elements['padding_frames'].extend(self.results_screen.get_frames()['padding_frames'])
        
        # Initialize stats manager
        self.stats_manager = StatsManager({
            'root': self.root,
            'time_label': self.game_screen.time_label,
            'wpm_label': self.game_screen.wpm_label,
            'accuracy_label': self.game_screen.accuracy_label,
            'gui': self  # Pass self reference to allow callbacks
        })
        
        # Apply theme and show menu screen
        self.theme_manager.apply_theme(self.gui_elements)
        self.show_menu()
    
    def create_callbacks(self):
        """Create a dictionary of callback functions for UI components."""
        return {
            'toggle_theme': self.toggle_theme,
            'show_menu': self.show_menu,
            'set_time_mode': self.set_time_mode,
            'set_custom_time': self.set_custom_time,
            'set_custom_keys': self.set_custom_keys,
            'reset_to_default_keys': self.reset_to_default_keys,
            'exit_application': self.exit_application,
            'get_keys_to_use': lambda: self.keys_to_use  # Function to return current keys
        }
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme_manager.toggle_theme()
        self.theme_manager.apply_theme(self.gui_elements)
    
    def show_menu(self):
        """Show the menu screen."""
        # Cancel all timers before switching screens
        self.cancel_all_timers()
        
        # Unbind key events
        self.root.unbind("<KeyPress>")
        
        # Hide other screens and show menu
        self.game_screen.hide()
        self.results_screen.hide()
        self.menu_screen.show()
    
    def show_results(self):
        """Show the results screen with stats from the game."""
        # Cancel timers before showing results
        self.cancel_all_timers()
        
        # Unbind key events
        self.root.unbind("<KeyPress>")
        
        # Get final stats
        wpm = self.stats_manager.calculate_wpm()
        accuracy = self.stats_manager.calculate_accuracy()
        elapsed_time = self.stats_manager.get_elapsed_time()
        
        # Update results screen with stats
        self.results_screen.update_results(wpm, accuracy, elapsed_time)
        
        # Hide other screens and show results
        self.game_screen.hide()
        self.menu_screen.hide()
        self.results_screen.show()
        
        # Apply theme
        self.theme_manager.apply_theme(self.gui_elements)
    
    def set_time_mode(self, mode):
        """Set the time mode and start the game."""
        self.time_mode = mode
        self.start_game()
    
    def set_custom_time(self, time_sec):
        """Set custom time limit in seconds."""
        self.custom_time = time_sec
    
    def set_custom_keys(self, keys):
        """Set custom keys to use for typing practice."""
        self.keys_to_use = keys
    
    def reset_to_default_keys(self):
        """Reset keys to default."""
        self.keys_to_use = self.default_keys
    
    def start_game(self):
        """Start a new typing game."""
        # Hide other screens and show game screen
        self.menu_screen.hide()
        self.results_screen.hide()
        self.game_screen.show()
        
        # Set the game time limit based on the selected mode
        if self.time_mode == "1min":
            time_limit = 60  # 1 minute in seconds
        elif self.time_mode == "5min":
            time_limit = 300  # 5 minutes in seconds
        elif self.time_mode == "custom":
            time_limit = self.custom_time
        else:  # freeplay
            time_limit = 0  # No time limit
        
        # Reset stats and start tracking
        self.stats_manager.reset_stats(time_limit)
        self.current_index[0] = 0
        
        self.stats_manager.update_timer()
        self.stats_manager.update_stats()
        
        # Generate and display new text
        self.create_new_sentence()
        self.theme_manager.apply_theme(self.gui_elements)
        
        # Bind key press events
        self.root.bind("<KeyPress>", self.on_key_press)
    
    def create_new_sentence(self):
        """Create and display a new sentence for typing."""
        new_text = self.text_generator.create_english_sentence(self.keys_to_use)
        self.current_text[0] = new_text
        self.displayed_indices = self.game_screen.display_text(new_text)
        self.current_index[0] = 0
    
    def on_key_press(self, event):
        """Handle key press events during the typing game."""
        if len(self.game_screen.letter_frames.winfo_children()) == 0:
            self.create_new_sentence()
            return

        # Determine which key was pressed
        special = False
        if event.keysym == "space":
            pressed_char = ' '
        elif event.keysym == "period":
            pressed_char = '.'
        elif event.keysym == "comma":
            pressed_char = ','
        elif event.keysym == "BackSpace":
            pressed_char = 'backspace'
            special = True
        else:
            pressed_char = event.char

        # Get current theme colors
        current_theme = self.theme_manager.get_current_theme()
        
        # Handle backspace - delete the previous character
        if self.current_index[0] > 0 and pressed_char == "backspace":
            displayed_idx = self.displayed_indices.index(self.current_index[0] - 1) if self.current_index[0] - 1 in self.displayed_indices else -1
            letter_labels = self.game_screen.letter_frames.winfo_children()
            
            if displayed_idx >= 0:
                deleted_letter_color = letter_labels[displayed_idx].cget("foreground")
                letter_labels[displayed_idx].config(foreground=current_theme["fg"], font=("Courier", self.game_screen.text_font_size))
                self.stats_manager.update_stats_based_on_color(deleted_letter_color)
            
            self.current_index[0] -= 1
            return

        # Handle regular key press
        if self.current_index[0] < len(self.current_text[0]) and pressed_char == self.current_text[0][self.current_index[0]] and not special:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.game_screen.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                letter_labels[displayed_idx].config(foreground=current_theme["correct"], font=("Courier", self.game_screen.text_font_size))
            
            self.stats_manager.register_keystroke(True)
            self.current_index[0] += 1
        elif not special:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.game_screen.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                letter_labels[displayed_idx].config(foreground=current_theme["incorrect"], font=("Courier", self.game_screen.text_font_size))
            
            self.stats_manager.register_keystroke(False)
            self.current_index[0] += 1

        # If we've reached the end of the text, generate a new sentence
        if self.current_index[0] == len(self.current_text[0]):
            self.create_new_sentence()
    
    def cancel_all_timers(self):
        """Cancel all active timers to prevent memory leaks."""
        # Cancel stats manager timers
        if hasattr(self, 'stats_manager'):
            self.stats_manager.cancel_timers()
            
        # Cancel any other after callbacks
        try:
            for after_id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(after_id)
        except Exception:
            pass
    
    def exit_application(self):
        """Safely exit the application."""
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
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()