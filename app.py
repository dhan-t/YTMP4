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
import time

# ASCII art (monochrome)
ASCII_ART = """
converter-app@nitro⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣤⣤⣄⣀⣀⠀⠀⠀⠀⠀⣠⠎⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣖⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⣄⣀⣠⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀
⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀
⠠⣾⣿⢿⣿⣿⣿⣿⡿⠁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⠉⠀⠀
⠀⠀⠀⢸⣿⣿⣿⡿⠑⠊⣿⣿⡿⠿⠛⠛⠙⠛⣻⣿⣿⣄⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀
⠀⠀⠀⢸⣿⣿⣿⡗⠾⠛⠉⠉⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀
⠀⠀⠀⢸⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠟⠛⠻⣿⣿⣿⣿⣿⣿⡄⠀
⠀⠀⠀⠀⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⢶⡋⠳⢸⣿⣿⣿⣿⣿⣇⠀
⠀⠂⠀⠀⠘⣿⣿⣿⡀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡗⠚⢁⣠⣾⣿⣿⣿⣿⣿⣿⠀
⠀⠉⠀⠀⠀⠈⣻⣿⣿⣦⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
   ⢺⣿⠤⠿⢿⣿⣿⣿⣿⣿⣿⣷⣶⡄⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣀⡠⠜⠋⠁⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡿⠛⣠⣟⣁⠤⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
⠀⠀⠀⠀⠀⠀⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢸⠿⠃⠀
⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣆⠀⠀⠀⠀⠀⠀"""

DEFAULT_OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "YTMP4")
YELLOW = "#FFD300"

class TerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x340")
        self.root.resizable(False, False)
        self.root.configure(bg="#242424")
        
        # Create main frame with two columns: ASCII art (50%) + text (50%)
        main_frame = tk.Frame(root, bg="#000000")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side: ASCII art
        left_frame = tk.Frame(main_frame, bg="#000000", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        left_frame.pack_propagate(False)
        
        art_label = tk.Label(
            left_frame,
            text=ASCII_ART,
            fg="#ffffff",
            bg="#000000",
            font=("Courier New", 8),
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
        
        # Configure text tags for styling
        self.terminal.tag_config("title", foreground=YELLOW, font=("Courier New", 9, "bold"))
        self.terminal.tag_config("yellow_bold", foreground=YELLOW, font=("Courier New", 9, "bold"))
        self.terminal.tag_config("current_cursor", foreground=YELLOW, background="#333333")
        self.terminal.tag_config("choice", foreground=YELLOW, font=("Courier New", 9, "bold"))
        
        self.selected_option = None
        self.fmt = None
        self.awaiting_url = False
        self.cursor_visible = True
        self.blink_task = None
        self.last_key_time = 0
        self.key_delay = 0.15
        
        self.show_header()
        self.show_menu()
    
    def write(self, text, newline=True, tag=None):
        """Write to terminal output with optional tag"""
        self.terminal.config(state=tk.NORMAL)
        start_idx = self.terminal.index(tk.END)
        self.terminal.insert(tk.END, text + ("\n" if newline else ""))
        if tag:
            end_idx = self.terminal.index(tk.END)
            self.terminal.tag_add(tag, start_idx, f"{start_idx}+{len(text)}c")
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)
        self.root.update()
    
    def show_header(self):
        pass
    
    def show_menu(self):
        self.terminal.config(state=tk.NORMAL)
        
        # Write menu items with arrow cursor visible at start
        self.terminal.insert(tk.END, "Use arrow keys ")
        self.terminal.insert(tk.END, "↑↓", "yellow_bold")
        self.terminal.insert(tk.END, " to select, then press ")
        self.terminal.insert(tk.END, "Enter", "yellow_bold")
        self.terminal.insert(tk.END, "\n\n")
        self.terminal.insert(tk.END, " [1] to mp4\n", "choice")    
        self.terminal.insert(tk.END, " [2] to mp3\n", "choice")
        self.terminal.insert(tk.END, "\n")

        self.terminal.config(state=tk.DISABLED)
        
        # Add color tag for choices
        self.terminal.tag_config("choice", foreground=YELLOW, font=("Courier New", 9, "bold"))
        
        self.selected_option = 0
        self.menu_line1_idx = self.terminal.search("[1]", "1.0")
        self.menu_line2_idx = self.terminal.search("[2]", self.menu_line1_idx)
        self.cursor_idx = None
        
        self.update_menu_cursor()
        self.start_cursor_blink()
        self.root.bind("<Up>", self.on_up)
        self.root.bind("<Down>", self.on_down)
        self.root.bind("<Return>", self.on_return_menu)
    
    def update_menu_cursor(self):
        """Update cursor position by toggling arrow visibility"""
        self.terminal.config(state=tk.NORMAL)
        
        # Identify the two menu lines
        line1_start = self.menu_line1_idx
        line1_end = self.terminal.index(f"{self.menu_line1_idx} lineend")
        line2_start = self.menu_line2_idx
        line2_end = self.terminal.index(f"{self.menu_line2_idx} lineend")
        
        if self.selected_option == 0:
            # First option selected: show arrow on line 1, hide on line 2
            self.terminal.delete(line1_start, f"{line1_start}+1c")
            self.terminal.insert(line1_start, "►")
            self.terminal.delete(line2_start, f"{line2_start}+1c")
            self.terminal.insert(line2_start, " ")
        else:
            # Second option selected: hide arrow on line 1, show on line 2
            self.terminal.delete(line1_start, f"{line1_start}+1c")
            self.terminal.insert(line1_start, " ")
            self.terminal.delete(line2_start, f"{line2_start}+1c")
            self.terminal.insert(line2_start, "►")
        
        self.terminal.config(state=tk.DISABLED)
    
    def start_cursor_blink(self):
        """Start blinking cursor animation - arrow blinks between visible and invisible"""
        def blink():
            self.terminal.config(state=tk.NORMAL)
            if self.cursor_visible:
                # Show arrow with yellow color
                if self.selected_option == 0:
                    line_start = self.menu_line1_idx
                else:
                    line_start = self.menu_line2_idx
                self.terminal.delete(line_start, f"{line_start}+1c")
                self.terminal.insert(line_start, "►", "yellow_bold")
            else:
                # Hide arrow with space
                if self.selected_option == 0:
                    line_start = self.menu_line1_idx
                else:
                    line_start = self.menu_line2_idx
                self.terminal.delete(line_start, f"{line_start}+1c")
                self.terminal.insert(line_start, " ")
            self.terminal.config(state=tk.DISABLED)
            self.cursor_visible = not self.cursor_visible
            self.blink_task = self.root.after(500, blink)
        
        if self.blink_task:
            self.root.after_cancel(self.blink_task)
        self.cursor_visible = True
        self.blink_task = self.root.after(500, blink)
    
    def stop_cursor_blink(self):
        """Stop cursor blinking"""
        if self.blink_task:
            self.root.after_cancel(self.blink_task)
            self.blink_task = None
    
    def on_up(self, event):
        """Handle up arrow"""
        if self.awaiting_url:
            return "break"
        current_time = time.time()
        if current_time < self.last_key_time + self.key_delay:
            return "break"
        self.last_key_time = current_time
        if self.selected_option > 0:
            self.selected_option -= 1
            self.update_menu_cursor()
        return "break"
    
    def on_down(self, event):
        """Handle down arrow"""
        if self.awaiting_url:
            return "break"
        current_time = time.time()
        if current_time < self.last_key_time + self.key_delay:
            return "break"
        self.last_key_time = current_time
        if self.selected_option < 1:
            self.selected_option += 1
            self.update_menu_cursor()
        return "break"
    
    def on_return_menu(self, event):
        """Handle return key on menu"""
        if self.awaiting_url:
            self.handle_url_input(event)
            return "break"
        
        self.stop_cursor_blink()
        self.fmt = "mp4" if self.selected_option == 0 else "mp3"
        self.write("")
        self.write(f"Selected: {self.fmt.upper()}", tag="yellow_bold")
        self.write("")
        self.get_url()
        return "break"
    
    def get_url(self):
        """Prompt for URL"""
        label = "Paste the link to convert to MP4:" if self.fmt == "mp4" else "Paste the link to convert to MP3:"
        self.write(label)
        self.write("> ", newline=False, tag="yellow_bold")
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
        if not self.awaiting_url:
            return "break"
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
        self.terminal.unbind("<KeyPress>")
        self.terminal.unbind("<Control-v>")
        self.terminal.config(state=tk.DISABLED)
        
        # Start download in separate thread
        thread = threading.Thread(target=self.download_url, args=(url, self.fmt, DEFAULT_OUTPUT_DIR))
        thread.daemon = True
        thread.start()
    
    def update_progress_bar(self, pct):
        """Update progress bar in place without creating new lines"""
        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "█" * filled + "░" * (bar_len - filled)
        progress_text = f"[{bar}] {pct:5.1f}%"
        
        self.terminal.config(state=tk.NORMAL)
        # Get the last line and replace it entirely
        end = self.terminal.index(tk.END)
        last_newline = self.terminal.index(f"{end} linestart")
        self.terminal.delete(last_newline, tk.END)
        self.terminal.insert(tk.END, progress_text)
        self.terminal.config(state=tk.DISABLED)
        self.root.update()
    
    def download_url(self, url, output_format, output_dir):
        """Download the video"""
        self.terminal.config(state=tk.NORMAL)
        self.terminal.insert(tk.END, "Downloading...\n")
        self.terminal.config(state=tk.DISABLED)
        self.progress_line_index = None
        
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
        self.progress_line_index = None
        
        def hook(d):
            status = d.get('status')
            if status == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate')
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    pct = downloaded / total * 100
                    bar_len = 30
                    filled = int(bar_len * pct / 100)
                    bar = "█" * filled + "░" * (bar_len - filled)
                    progress_text = f"[{bar}] {pct:5.1f}%"
                    
                    self.terminal.config(state=tk.NORMAL)
                    if self.progress_line_index is None:
                        # First time: insert progress line
                        self.terminal.insert(tk.END, progress_text + "\n")
                        self.progress_line_index = self.terminal.index("end-2l linestart")
                    else:
                        # Update existing progress line - delete old and insert new
                        line_end = self.terminal.index(f"{self.progress_line_index} lineend")
                        self.terminal.delete(self.progress_line_index, line_end)
                        self.terminal.insert(self.progress_line_index, progress_text)
                    self.terminal.config(state=tk.DISABLED)
                    self.root.update()
            elif status == 'finished':
                self.terminal.config(state=tk.NORMAL)
                self.terminal.insert(tk.END, "\nProcessing...")
                self.terminal.config(state=tk.DISABLED)
                self.root.update()
            elif status == 'error':
                self.terminal.config(state=tk.NORMAL)
                self.terminal.insert(tk.END, "\nError")
                self.terminal.config(state=tk.DISABLED)
        
        ydl_opts['progress_hooks'] = [hook]
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.write("")
            self.write("✓ Download completed!", tag="yellow_bold")
            self.write(f"✓ Saved to: {output_dir}")
        except Exception as e:
            self.write("")
            self.write("✗ Download failed:", tag="yellow_bold")
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
