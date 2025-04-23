"""
Theme manager for handling application appearance.
"""

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.is_dark_mode = True
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "button_bg": "#f0f0f0",
                "button_fg": "#000000",
                "correct": "#008800",
                "incorrect": "#ff0000"
            },
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "button_bg": "#2a2a2a",
                "button_fg": "#ffffff",
                "correct": "#00cc00",
                "incorrect": "#ff4444"
            }
        }
        
        # Set the initial theme on the root window
        current_theme = self.get_current_theme()
        self.root.config(bg=current_theme["bg"])
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        return self.is_dark_mode
    
    def get_current_theme(self):
        return self.themes["dark"] if self.is_dark_mode else self.themes["light"]
    
    def get_initial_bg_color(self):
        """Get the initial background color to use for new frames."""
        return self.get_current_theme()["bg"]
    
    def apply_theme(self, gui_elements):
        current_theme = self.get_current_theme()
        button_text = "Light Mode" if self.is_dark_mode else "Dark Mode"
        
        # Update button text
        if 'theme_button' in gui_elements:
            gui_elements['theme_button'].config(text=button_text)
        if 'theme_game_button' in gui_elements:
            gui_elements['theme_game_button'].config(text=button_text)
        
        # Apply theme to root and frames
        self.root.config(bg=current_theme["bg"])
        
        # Apply theme to main frames
        for frame_name in ['menu_frame', 'game_frame', 'results_frame', 'custom_keys_frame']:
            if frame_name in gui_elements:
                gui_elements[frame_name].config(bg=current_theme["bg"])
        
        # Apply theme to padding frames - make sure these match the background
        if 'padding_frames' in gui_elements:
            for frame in gui_elements['padding_frames']:
                frame.config(bg=current_theme["bg"])
        
        # Apply to menu screen
        if 'menu_frame' in gui_elements:
            for widget in gui_elements['menu_frame'].winfo_children():
                if isinstance(widget, gui_elements['tk'].Label):
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
                elif isinstance(widget, gui_elements['tk'].Frame):
                    widget.config(bg=current_theme["bg"])
                    for child in widget.winfo_children():
                        if isinstance(child, gui_elements['tk'].Button):
                            child.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
                        elif isinstance(child, gui_elements['tk'].Label):
                            child.config(bg=current_theme["bg"], fg=current_theme["fg"])
                        elif isinstance(child, gui_elements['tk'].Frame):
                            child.config(bg=current_theme["bg"])
                            for subchild in child.winfo_children():
                                if isinstance(subchild, gui_elements['tk'].Button):
                                    subchild.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        
        # Apply to game screen
        if 'stats_frame' in gui_elements:
            gui_elements['stats_frame'].config(bg=current_theme["bg"])
            for widget in gui_elements['stats_frame'].winfo_children():
                if isinstance(widget, gui_elements['tk'].Label):
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
                elif isinstance(widget, gui_elements['tk'].Button):
                    widget.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        
        # Apply to results screen
        if 'results_frame' in gui_elements:
            for widget in gui_elements['results_frame'].winfo_children():
                if isinstance(widget, gui_elements['tk'].Label):
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])
                elif isinstance(widget, gui_elements['tk'].Frame):
                    widget.config(bg=current_theme["bg"])
                    for child in widget.winfo_children():
                        if isinstance(child, gui_elements['tk'].Label):
                            child.config(bg=current_theme["bg"], fg=current_theme["fg"])
                        elif isinstance(child, gui_elements['tk'].Button):
                            child.config(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
        
        if 'letter_frames' in gui_elements:
            gui_elements['letter_frames'].config(bg=current_theme["bg"])
            # Update letter display colors
            for widget in gui_elements['letter_frames'].winfo_children():
                if widget.cget("foreground") == "green":
                    widget.config(bg=current_theme["bg"], fg=current_theme["correct"])
                elif widget.cget("foreground") == "red":
                    widget.config(bg=current_theme["bg"], fg=current_theme["incorrect"])
                else:
                    widget.config(bg=current_theme["bg"], fg=current_theme["fg"])