#!/usr/bin/env python3
"""
Converter App — Terminal-style popup with ASCII art using Tkinter
"""
import os
import sys
import yt_dlp
import tkinter as tk
from tkinter import scrolledtext
import threading

# ASCII art (monochrome)
ASCII_ART = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⢉⣉⠉⠉⠋⠐⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠰⠒⠒⠂⠀⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠿⠿⣶⣶⣥⣴⠢⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢊⡀⢤⣤⣤⣶⣶⣶⣖⠃⠀⠀⠀⠀⠀
⠀⠀⠠⢴⣾⣿⡿⠋⠀⠀⠀⣴⣾⣿⣿⣿⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣥⣾⣿⣟⠉⠉⠙⠻⣿⣿⣦⣀⠀⠀⠀
⠀⠀⣠⣾⣿⠋⠀⠀⠀⠀⠠⣿⣜⢶⡗⣹⡯⠣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣟⢭⣛⢹⣧⠀⠀⠀⠀⠻⣿⣧⡀⠀⠀
⠲⠿⠿⠿⣿⡀⠀⠀⠀⠀⠀⠻⠿⣷⡼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣯⣫⣼⡏⠀⠀⠀⠀⠀⣹⣿⠿⠷⠦
⠀⠀⠀⠀⠈⠉⠒⠀⠀⡀⢀⣠⠶⠖⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠭⢭⢥⣄⠀⠀⠀⠀⠊⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "YTMP4")

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("converter app")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#000000")
        
        # Create main frame with two columns: ASCII art (50%) + text (50%)
        main_frame = tk.Frame(root, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side: ASCII art
        left_frame = tk.Frame(main_frame, bg="#000000", width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        art_label = tk.Label(
            left_frame,
            text=ASCII_ART,
            fg="#ffffff",
            bg="#000000",
            font=("Courier New", 7),
            justify=tk.LEFT,
            anchor="nw"
        )
        art_label.pack(side=tk.TOP, anchor="nw")
        
        # Right side: Terminal output and input
        right_frame = tk.Frame(main_frame, bg="#000000")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Output text widget
        self.terminal = scrolledtext.ScrolledText(
            right_frame,
            bg="#000000",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=("Courier New", 9),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED
        )
        self.terminal.pack(fill=tk.BOTH, expand=True)
        
        self.selected_option = None
        self.fmt = None
        self.awaiting_url = False
        
        self.show_header()
        self.show_menu()
    
    def write(self, text, newline=True):
        """Write to terminal output"""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, text + ("\n" if newline else ""))
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)
        self.root.update()
    
    def show_header(self):
        self.write("converter app", newline=True)
        self.write("")
    
    def show_menu(self):
        self.write("[1] to mp4")
        self.write("[2] to mp3")
        self.write("")
        self.write("Use arrow keys ↑/↓ to select, then press Enter")
        self.write("")
        self.selected_option = 0
        self.update_menu_display()
        self.root.bind("<Up>", self.on_up)
        self.root.bind("<Down>", self.on_down)
        self.root.bind("<Return>", self.on_return_menu)
    
    def update_menu_display(self):
        """Update menu display with selection"""
        self.terminal.config(state=tk.NORMAL)
        # Find and replace the menu lines
        content = self.terminal.get("1.0", tk.END)
        lines = content.split("\n")
        
        # Find menu start
        menu_start = None
        for i, line in enumerate(lines):
            if "[1] to mp4" in line:
                menu_start = i
                break
        
        if menu_start is not None:
            option1 = "  [1] to mp4" if self.selected_option == 0 else "> [1] to mp4"
            option2 = "  [2] to mp3" if self.selected_option == 1 else "> [2] to mp3"
            
            start_idx = self.terminal.search("[1]", "1.0")
            if start_idx:
                end_idx_1 = self.terminal.search("\n", start_idx)
                self.terminal.delete(start_idx, tk.END)
            
            self.terminal.insert(tk.END, option1 + "\n" + option2 + "\n\nUse arrow keys ↑/↓ to select, then press Enter\n")
        
        self.terminal.config(state=tk.DISABLED)
        self.root.update()
    
    def on_up(self, event):
        """Handle up arrow"""
        if self.awaiting_url:
            return
        if self.selected_option > 0:
            self.selected_option -= 1
            self.update_menu_display()
    
    def on_down(self, event):
        """Handle down arrow"""
        if self.awaiting_url:
            return
        if self.selected_option < 1:
            self.selected_option += 1
            self.update_menu_display()
    
    def on_return_menu(self, event):
        """Handle return key on menu"""
        if self.awaiting_url:
            self.handle_url_input(event)
            return
        
        self.fmt = "mp4" if self.selected_option == 0 else "mp3"
        self.write("")
        self.write(f"Selected: {self.fmt.upper()}")
        self.write("")
        self.get_url()
    
    def get_url(self):
        """Prompt for URL"""
        label = "Paste the link to convert to MP4:" if self.fmt == "mp4" else "Paste the link to convert to MP3:"
        self.write(label)
        self.write("> ", newline=False)
        self.awaiting_url = True
        self.url_input = ""
        self.root.unbind("<Up>")
        self.root.unbind("<Down>")
        self.terminal.config(state=tk.NORMAL)
        self.terminal.focus_set()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<Control-v>", self.on_paste)
    
    def on_key_press(self, event):
        """Handle key press while waiting for URL"""
        if event.keysym == "Return":
            self.handle_url_input(event)
        elif event.keysym == "BackSpace":
            self.url_input = self.url_input[:-1]
            content = self.terminal.get("1.0", tk.END)
            lines = content.split("\n")
            lines[-1] = "> " + self.url_input
            self.terminal.delete("1.0", tk.END)
            self.terminal.insert("1.0", "\n".join(lines))
        elif event.keysym == "Control_L" or event.keysym == "Control_R":
            pass
        elif len(event.char) >= 1:
            self.url_input += event.char
            self.terminal.insert(tk.END, event.char)
        self.terminal.see(tk.END)
        return "break"
    
    def on_paste(self, event):
        """Handle paste (Ctrl+V)"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_input += clipboard_text
            self.terminal.insert(tk.END, clipboard_text)
            self.terminal.see(tk.END)
        except tk.TclError:
            pass
        return "break"
    
    def handle_url_input(self, event):
        """Handle URL input"""
        url = self.url_input.strip()
        
        if not url:
            self.write("")
            self.write("No URL provided. Please try again.")
            self.get_url()
            return
        
        self.write("")
        self.awaiting_url = False
        self.terminal.unbind("<Key>")
        self.terminal.config(state=tk.DISABLED)
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_url, args=(url, self.fmt, DEFAULT_OUTPUT_DIR))
        thread.daemon = True
        thread.start()
    
    def download_url(self, url, output_format, output_dir):
        """Download the video"""
        self.write("Downloading...")
        output_path = os.path.join(output_dir, '%(title)s.%(ext)s')
        
        if output_format == 'mp4':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
        else:  # mp3
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0',
                }],
            }
        
        os.makedirs(output_dir, exist_ok=True)
        
        def hook(d):
            status = d.get('status')
            if status == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    pct = downloaded / total * 100
                    bar_len = 30
                    filled = int(bar_len * downloaded / total)
                    bar = "█" * filled + "░" * (bar_len - filled)
                    self.write(f"[{bar}] {pct:5.1f}%", newline=False)
            elif status == 'finished':
                self.write("")
                self.write("Processing...")
            elif status == 'error':
                self.write("Error")
        
        ydl_opts['progress_hooks'] = [hook]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.write("")
            self.write("✓ Download completed!")
            self.write(f"✓ Saved to: {output_dir}")
        except Exception as e:
            self.write("")
            self.write("✗ Download failed:")
            self.write(f"✗ {str(e)}")

def main():
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(1)
