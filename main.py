from gui import GUI

def main():
    # Default keys that will be used in typing exercises
    keys_to_use = "asdfghjkl;qwertyuiop"
    
    app = GUI(keys_to_use)
    app.run()

if __name__ == "__main__":
    main()
