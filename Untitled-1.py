#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
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
        
        tk.Label(frame, text="Discord Clone", font=("Arial", 24, "bold"), 
                bg="#36393F", fg="white").pack(pady=20)
        
        tk.Label(frame, text="Username:", font=("Arial", 12), 
                bg="#36393F", fg="white").pack(pady=5)
        username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        username_entry.pack(pady=5)
        username_entry.focus()
        
        tk.Label(frame, text="Server IP:", font=("Arial", 12), 
                bg="#36393F", fg="white").pack(pady=5)
        ip_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        ip_entry.insert(0, "127.0.0.1")
        ip_entry.pack(pady=5)
        
        tk.Label(frame, text="Port:", font=("Arial", 12), 
                bg="#36393F", fg="white").pack(pady=5)
        port_entry = tk.Entry(frame, font=("Arial", 12), width=30)
        port_entry.insert(0, "5555")
        port_entry.pack(pady=5)
        
        def connect():
            username = username_entry.get().strip()
            ip = ip_entry.get().strip()
            port = port_entry.get().strip()
            
            if not username:
                messagebox.showerror("Error", "Username required")
                return
            
            self.username = username
            try:
                port = int(port)
                self.connect_to_server(ip, port)
                frame.destroy()
                self.setup_chat_screen()
            except ValueError:
                messagebox.showerror("Error", "Invalid port number")
            except Exception as e:
                messagebox.showerror("Connection Error", f"Could not connect: {e}")
        
        tk.Button(frame, text="Connect", command=connect, 
                 font=("Arial", 12), bg="#7289DA", fg="white",
                 padx=20, pady=10).pack(pady=20)
        
    def connect_to_server(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        self.socket.send(self.username.encode())
        
    def setup_chat_screen(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg="#2C2F33", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH)
        sidebar.pack_propagate(False)
        
        tk.Label(sidebar, text="Channels", font=("Arial", 10, "bold"),
                bg="#2C2F33", fg="white").pack(pady=10)
        
        for channel in ["#general", "#random", "#news"]:
            tk.Label(sidebar, text=channel, font=("Arial", 10),
                    bg="#2C2F33", fg="#B0BEC5", cursor="hand2").pack(anchor="w", padx=10, pady=5)
        
        # Main chat area
        main_frame = tk.Frame(self.root, bg="#36393F")
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(main_frame, text=f"Welcome, {self.username}!", font=("Arial", 14, "bold"),
                bg="#36393F", fg="white").pack(anchor="w", pady=10)
        
        # Messages display
        self.message_display = scrolledtext.ScrolledText(main_frame, height=20, width=80,
                                                         font=("Arial", 10), bg="#2C2F33", 
                                                         fg="white", wrap=tk.WORD,
                                                         insertbackground="white")
        self.message_display.pack(fill=tk.BOTH, expand=True, pady=10)
        self.message_display.config(state=tk.DISABLED)
        
        # Message input
        input_frame = tk.Frame(main_frame, bg="#36393F")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.message_input = tk.Entry(input_frame, font=("Arial", 10),
                                     bg="#40444B", fg="white", insertbackground="white")
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.message_input.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message,
                            bg="#7289DA", fg="white", font=("Arial", 10))
        send_btn.pack(side=tk.LEFT, padx=5)
        
        self.add_message("System", "Connected to server!")
        
        # Start receiving messages
        threading.Thread(target=self.receive_messages, daemon=True).start()
        
    def send_message(self, event=None):
        message = self.message_input.get().strip()
        if message:
            try:
                data = json.dumps({"user": self.username, "message": message})
                self.socket.send(data.encode())
                self.message_input.delete(0, tk.END)
            except:
                self.add_message("System", "Failed to send message")
                
    def receive_messages(self):
        try:
            while self.running:
                data = self.socket.recv(1024).decode()
                if data:
                    msg_data = json.loads(data)
                    self.add_message(msg_data.get("user", "Unknown"), 
                                   msg_data.get("message", ""))
        except:
            self.add_message("System", "Connection closed")
            
    def add_message(self, user, message):
        self.message_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.message_display.insert(tk.END, f"[{timestamp}] {user}: {message}\n")
        self.message_display.see(tk.END)
        self.message_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
