#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import json
from datetime import datetime

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord-like Chat")
        self.root.geometry("900x600")
        self.root.configure(bg="#36393F")

        self.username = None
        self.socket = None
        self.running = True

        self.setup_login_screen()

    def setup_login_screen(self):
        frame = tk.Frame(self.root, bg="#36393F")
        frame.pack(expand=True)

        tk.Label(
            frame,
            text="Discord Clone",
            font=("Arial", 24, "bold"),
            bg="#36393F",
            fg="white"
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Username:",
            bg="#36393F",
            fg="white"
        ).pack()

        username_entry = tk.Entry(frame, width=30)
        username_entry.pack(pady=5)

        tk.Label(
            frame,
            text="Server IP:",
            bg="#36393F",
            fg="white"
        ).pack()

        ip_entry = tk.Entry(frame, width=30)
        ip_entry.insert(0, "127.0.0.1")
        ip_entry.pack(pady=5)

        tk.Label(
            frame,
            text="Port:",
            bg="#36393F",
            fg="white"
        ).pack()

        port_entry = tk.Entry(frame, width=30)
        port_entry.insert(0, "5555")
        port_entry.pack(pady=5)

        def connect():
            username = username_entry.get().strip()
            ip = ip_entry.get().strip()

            try:
                port = int(port_entry.get().strip())

                self.username = username

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((ip, port))

                self.socket.send(username.encode())

                frame.destroy()

                self.setup_chat_screen()

            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            frame,
            text="Connect",
            command=connect,
            bg="#7289DA",
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)

    def setup_chat_screen(self):
        sidebar = tk.Frame(self.root, bg="#2C2F33", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            sidebar,
            text="Channels",
            bg="#2C2F33",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        for channel in ["#general", "#random", "#news"]:
            tk.Label(
                sidebar,
                text=channel,
                bg="#2C2F33",
                fg="#B0BEC5"
            ).pack(anchor="w", padx=10, pady=5)

        main_frame = tk.Frame(self.root, bg="#36393F")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.message_display = scrolledtext.ScrolledText(
            main_frame,
            bg="#2C2F33",
            fg="white",
            insertbackground="white",
            wrap=tk.WORD
        )

        self.message_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.message_display.config(state=tk.DISABLED)

        input_frame = tk.Frame(main_frame, bg="#36393F")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_input = tk.Entry(
            input_frame,
            bg="#40444B",
            fg="white",
            insertbackground="white"
        )

        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_input.bind("<Return>", self.send_message)

        tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg="#7289DA",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        message = self.message_input.get().strip()

        if message:
            data = json.dumps({
                "user": self.username,
                "message": message
            })

            self.socket.send(data.encode())

            self.message_input.delete(0, tk.END)

    def receive_messages(self):
        while self.running:
            try:
                data = self.socket.recv(1024).decode()

                if data:
                    msg = json.loads(data)

                    self.add_message(
                        msg.get("user", "Unknown"),
                        msg.get("message", "")
                    )

            except:
                break

    def add_message(self, user, message):
        self.message_display.config(state=tk.NORMAL)

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.message_display.insert(
            tk.END,
            f"[{timestamp}] {user}: {message}\n"
        )

        self.message_display.see(tk.END)

        self.message_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()

    app = ChatApp(root)

    root.mainloop()
