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
        self.results_frame = tk.Frame(self.root)  # New frame for results
        
        # Track padding frames for theme updates
        self.padding_frames = []
        
        self.current_text = [""]
        self.current_index = [0]
        self.displayed_indices = []
        
        # Time mode variables
        self.time_mode = "freeplay"  # Default mode
        self.custom_time = 0
        
        self.create_menu_screen()
        self.create_game_screen()
        self.create_results_screen()
        
        # Create GUI elements dictionary for theme manager
        self.gui_elements = {
            'tk': tk,
            'root': self.root,
            'menu_frame': self.menu_frame,
            'game_frame': self.game_frame,
            'results_frame': self.results_frame,  # Add results frame
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
            'accuracy_label': self.accuracy_label,
            'gui': self  # Pass self reference to allow callbacks
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
        
        # Main menu frame
        self.main_menu_frame = tk.Frame(self.menu_frame)
        self.main_menu_frame.pack(pady=20)
        
        # Custom time input frame (initially hidden)
        self.custom_time_frame = tk.Frame(self.menu_frame)
        
        # Add elements to main menu frame
        self.create_main_menu_content(self.main_menu_frame)
        
        # Add elements to custom time frame
        self.create_custom_time_content(self.custom_time_frame)

    def create_main_menu_content(self, parent_frame):
        # Mode selection buttons
        mode_label = tk.Label(parent_frame, text="Select Mode:", font=(self.font, self.stats_font_size))
        mode_label.pack(pady=5)
        
        modes_frame = tk.Frame(parent_frame)
        modes_frame.pack(pady=5)
        
        one_min_button = tk.Button(modes_frame, text="1 Minute", font=(self.font, self.stats_font_size),
                                command=lambda: self.set_time_mode("1min"), width=10)
        one_min_button.grid(row=0, column=0, padx=5, pady=5)
        
        five_min_button = tk.Button(modes_frame, text="5 Minutes", font=(self.font, self.stats_font_size),
                                 command=lambda: self.set_time_mode("5min"), width=10)
        five_min_button.grid(row=0, column=1, padx=5, pady=5)
        
        custom_time_button = tk.Button(modes_frame, text="Custom Time", font=(self.font, self.stats_font_size),
                                    command=self.custom_time_dialog, width=10)
        custom_time_button.grid(row=1, column=0, padx=5, pady=5)
        
        freeplay_button = tk.Button(modes_frame, text="Freeplay", font=(self.font, self.stats_font_size),
                                  command=lambda: self.set_time_mode("freeplay"), width=10)
        freeplay_button.grid(row=1, column=1, padx=5, pady=5)
        
        # Settings buttons
        settings_frame = tk.Frame(parent_frame)
        settings_frame.pack(pady=10)
        
        theme_button = tk.Button(settings_frame, text="Dark Mode", font=(self.font, self.stats_font_size),
                               command=self.toggle_theme, width=10)
        theme_button.pack(pady=10)
        self.theme_button = theme_button
        
        exit_button = tk.Button(settings_frame, text="Exit", font=(self.font, self.stats_font_size),
                                command=self.exit_application, width=10)
        exit_button.pack(pady=10)
        
    def create_custom_time_content(self, parent_frame):
        time_label = tk.Label(parent_frame, text="Enter time in seconds:", 
                             font=(self.font, self.stats_font_size))
        time_label.pack(pady=10)
        
        self.time_entry = tk.Entry(parent_frame, font=(self.font, self.stats_font_size),
                                  width=10)
        self.time_entry.pack(pady=10)
        
        buttons_frame = tk.Frame(parent_frame)
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

    def custom_time_dialog(self):
        # Hide main menu and show custom time input
        self.main_menu_frame.pack_forget()
        self.custom_time_frame.pack(pady=20)
        self.time_entry.focus_set()
        self.time_entry.delete(0, tk.END)  # Clear any previous input
        
        # Apply current theme
        current_theme = self.theme_manager.get_current_theme()
        self.custom_time_frame.config(bg=current_theme["bg"])
        for widget in self.custom_time_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
            elif isinstance(widget, tk.Frame):
                widget.config(bg=current_theme["bg"])
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    
    def show_main_menu(self):
        # Hide custom time input and show main menu
        self.custom_time_frame.pack_forget()
        self.main_menu_frame.pack(pady=20)
    
    def set_custom_time(self, time_str):
        try:
            time_sec = int(time_str)
            if time_sec > 0:
                self.custom_time = time_sec
                self.set_time_mode("custom")
            else:
                # Show error if time is zero or negative
                tk.messagebox.showerror("Invalid Input", "Please enter a positive number of seconds.")
        except ValueError:
            # Show error if input is not a valid number
            tk.messagebox.showerror("Invalid Input", "Please enter a valid number of seconds.")
    
    def create_results_screen(self):
        # Add top padding
        top_padding_frame = tk.Frame(self.results_frame, height=self.top_padding)
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
                             command=self.show_menu, width=10)
        menu_button.pack(side=tk.LEFT, padx=10)
        
        exit_button = tk.Button(button_frame, text="Exit", font=(self.font, self.stats_font_size),
                             command=self.exit_application, width=10)
        exit_button.pack(side=tk.RIGHT, padx=10)
    
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
    
    def set_time_mode(self, mode):
        self.time_mode = mode
        self.start_game()
    
    def toggle_theme(self):
        self.theme_manager.toggle_theme()
        self.theme_manager.apply_theme(self.gui_elements)
    
    def show_menu(self):
        # Make sure to cancel all timers before switching screens
        self.cancel_all_timers()
        
        # Ensure these are done in the right order
        self.root.unbind("<KeyPress>")
        self.game_frame.pack_forget()
        self.results_frame.pack_forget()
        
        # Show the main menu (not the custom time input)
        self.custom_time_frame.pack_forget()
        self.main_menu_frame.pack(pady=20)
        self.menu_frame.pack(expand=True, fill="both")
    
    def show_results(self):
        # Cancel timers before showing results
        self.cancel_all_timers()
        
        # Unbind key events
        self.root.unbind("<KeyPress>")
        
        # Update results labels with final stats
        wpm = self.stats_manager.calculate_wpm()
        accuracy = self.stats_manager.calculate_accuracy()
        elapsed_time = time.time() - self.stats_manager.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        self.result_wpm_label.config(text=f"WPM: {wpm}")
        self.result_accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        self.result_time_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
        # Switch to results screen
        self.game_frame.pack_forget()
        self.menu_frame.pack_forget()
        self.results_frame.pack(expand=True, fill="both")
        
        # Apply theme
        self.theme_manager.apply_theme(self.gui_elements)
    
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
        self.results_frame.pack_forget()
        self.game_frame.pack(expand=True, fill="both")
        
        # Set the game time limit based on the selected mode
        if self.time_mode == "1min":
            time_limit = 60  # 1 minute in seconds
        elif self.time_mode == "5min":
            time_limit = 300  # 5 minutes in seconds
        elif self.time_mode == "custom":
            time_limit = self.custom_time
        else:  # freeplay
            time_limit = 0  # No time limit
        
        self.stats_manager.reset_stats(time_limit)
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
        special = False
        if len(self.letter_frames.winfo_children()) == 0:
            self.create_new_sentence()
            return

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

        current_theme = self.theme_manager.get_current_theme()
        
        if self.current_index[0] > 0 and pressed_char == "backspace":
            letter_labels = self.letter_frames.winfo_children()
            displayed_idx = self.displayed_indices.index(self.current_index[0] - 1) if self.current_index[0] - 1 in self.displayed_indices else -1
            if displayed_idx >= 0:
                deleted_letter_color = letter_labels[displayed_idx].cget("foreground")
                print(f"Deleted letter color: {deleted_letter_color}")
                letter_labels[displayed_idx].config(foreground=current_theme["fg"], font=("Courier", self.text_font_size))
                self.stats_manager.update_stats_based_on_color(deleted_letter_color)
            self.current_index[0] -= 1
            return

        if self.current_index[0] < len(self.current_text[0]) and pressed_char == self.current_text[0][self.current_index[0]] and not special:
            displayed_idx = self.displayed_indices.index(self.current_index[0]) if self.current_index[0] in self.displayed_indices else -1
            
            letter_labels = self.letter_frames.winfo_children()
            if displayed_idx >= 0 and displayed_idx < len(letter_labels):
                letter_labels[displayed_idx].config(foreground=current_theme["correct"], font=("Courier", self.text_font_size))
            
            self.stats_manager.register_keystroke(True)
            self.current_index[0] += 1
        elif not special:
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
