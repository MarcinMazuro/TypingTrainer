"""
Entry point for the Typing Trainer application.
"""

from ui.gui import GUI
from config.settings import DEFAULT_KEYS

def main():
    # Initialize the GUI with the default keys from settings
    app = GUI(DEFAULT_KEYS)
    app.run()

if __name__ == "__main__":
    main()
