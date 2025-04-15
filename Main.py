import tkinter as tk
from Gui import GUI

def main():
    keys_to_use = 'asdfghjkl;qwertyuiop'  # You can extend with more characters

    app = GUI(keys_to_use)
    app.run()


if __name__ == "__main__":
    main()