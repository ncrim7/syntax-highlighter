import tkinter as tk
from gui import SyntaxHighlighter

def main():
    root = tk.Tk()
    app = SyntaxHighlighter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
