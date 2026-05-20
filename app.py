import tkinter as tk

root = tk.Tk()
root.title("Mijn Eerste App")
root.geometry("400x200")

label = tk.Label(
    root,
    text="Hallo vanuit Linux Mint!",
    font=("Arial", 20)
)

label.pack(pady=40)

root.mainloop()
