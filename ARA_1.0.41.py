#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Android Root Assistant (ARA) - Enhanced Darknet Edition
Piracka wersja z terminalowym stylem i zaawansowanymi funkcjami
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import time
from datetime import datetime
from pathlib import Path
import os
import sys
import signal
import shutil

# -----------------------
# Helper / config
# -----------------------
APP_VERSION = "ARA v2.0-PIRATE"
WORK_DIR = Path.home() / ".android_root_assistant"
DOWNLOADS_DIR = WORK_DIR / "downloads"
LOGS_DIR = WORK_DIR / "logs"
WORK_DIR.mkdir(exist_ok=True)
DOWNLOADS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

MONO_FONT = ("Consolas", 9)
TERMINAL_FONT = ("Courier New", 9)
H1_FONT = ("Courier New", 20, "bold")
H2_FONT = ("Courier New", 11, "bold")

# -----------------------
# Main class
# -----------------------
class AndroidRootAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title(f"ARA - Android Root Assistant {APP_VERSION}")
        self.root.geometry("1500x950")
        self.root.minsize(1200, 800)

        # state
        self.device_info = {}
        self.root_methods = []
        self.is_scanning = False
        self.is_rooting = False
        self.device_connected = False
        self.current_method_index = 0
        self.logcat_process = None
        self.logcat_thread = None
        self.logcat_running = False
        self.all_logs = []  # przechowywanie wszystkich logów

        # Darknet color theme - bardziej mroczny
        self.colors = {
            'bg': '#0a0e14',           # very dark background
            'panel': '#0d1117',        # dark panel
            'terminal_bg': '#000000',  # black terminal
            'terminal_fg': '#a2e0a2',  # soft green text
            'muted': '#6e7681',        # grey
            'accent': '#00aaff',       # bright blue
            'accent2': '#00d0d0',      # cyan
            'warn': '#ffcc00',         # amber
            'danger': '#ff4444',       # soft red
            'success': '#44dd44',      # soft green
            'text': '#c9d1d9',         # light grey
            'border': '#1f2937',       # dark border
            'hover': '#161b22'         # hover effect
        }
        self.root.configure(bg=self.colors['bg'])

        # build UI
        self._build_ui()

        # initial checks
        self.root.after(800, self.auto_check_device)

    # -----------------------
    # UI BUILD
    # -----------------------
    def _build_ui(self):
        # HEADER z pirackimi ASCII art
        header = tk.Frame(self.root, bg=self.colors['panel'], height=90)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Ultra-Elegant Elite Pro Header (new, non-destructive addition)
        elite_header_text = """
A R A
Android Root Assistant
• D A R K   E D I T I O N •
"""
        elite_label = tk.Label(
            header,
            text=elite_header_text,
            bg=self.colors['panel'],
            fg=self.colors['accent2'],
            font=("Courier New", 12, "bold"),
            justify="center"
        )
        elite_label.pack(pady=6)
        
        # # Piracka papuga ASCII + ARA logo
        # parrot_frame = tk.Frame(header, bg=self.colors['panel'])
        # parrot_frame.pack(side=tk.LEFT, padx=10)
        
        # parrot_art = r"""
    # _
   # / \
  # | (o) (o) | Arrr!
   # \  ^  //
    # |||
   # /   \
        # """
        # parrot_label = tk.Label(parrot_frame, text=parrot_art, bg=self.colors['panel'],
        #                        fg=self.colors['accent'], font=("Courier New", 8), justify=tk.LEFT)
        # parrot_label.pack()
        
        # # ARA logo z pierwszych liter
        # title_frame = tk.Frame(header, bg=self.colors['panel'])
        # title_frame.pack(side=tk.LEFT, padx=20)
        
        # ara_logo = """
 # █████╗ ██████╗  █████╗ 
# ██╔══██╗██╔══██╗██╔══██╗
# ███████║██████╔╝███████║
# ██╔══██║██╔══██╗██╔══██║
# ██║  ██║██║  ██║██║  ██║
# ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝"""
        
        # ara_label = tk.Label(title_frame, text=ara_logo, bg=self.colors['panel'],
        #                     fg=self.colors['accent'], font=("Courier New", 9, "bold"), justify=tk.LEFT)
        # ara_label.pack()
        
        # subtitle = tk.Label(title_frame, text="Android Root Assistant - Darknet Edition", 
        #                    bg=self.colors['panel'], fg=self.colors['accent2'], 
        #                    font=("Courier New", 10))
        # subtitle.pack()
        
        ver = tk.Label(header, text=f"v2.0 | {datetime.now().strftime('%Y-%m-%d')}", 
                      bg=self.colors['panel'], fg=self.colors['muted'],
                      font=("Courier New", 9))
        ver.pack(side=tk.RIGHT, padx=16)

        # STATUS BAR
        status = tk.Frame(self.root, bg=self.colors['panel'], height=32)
        status.pack(fill=tk.X)
        status.pack_propagate(False)
        self.device_status_label = tk.Label(status, text="[DEVICE: OFFLINE]", bg=self.colors['panel'],
                                            fg=self.colors['danger'], font=("Courier New", 9, "bold"))
        self.device_status_label.pack(side=tk.LEFT, padx=12)
        self.adb_status_label = tk.Label(status, text="[ADB: CHECKING...]", bg=self.colors['panel'],
                                         fg=self.colors['muted'], font=("Courier New", 9, "bold"))
        self.adb_status_label.pack(side=tk.RIGHT, padx=12)

        # MAIN
        main = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED,
                              bg=self.colors['bg'], sashwidth=4)
        main.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # LEFT: Info / Methods / Security / Logcat
        left = tk.Frame(main, bg=self.colors['bg'])
        main.add(left, minsize=600)

        # Device Info panel
        self.info_frame = self._card(left, "[ DEVICE INFORMATION ]")
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=9, bg=self.colors['terminal_bg'],
                                                   fg=self.colors['terminal_fg'], font=TERMINAL_FONT, 
                                                   wrap=tk.WORD, insertbackground=self.colors['accent'])
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Root Methods panel
        self.methods_frame = self._card(left, "[ ROOT METHODS AVAILABLE ]")
        self.methods_text = scrolledtext.ScrolledText(self.methods_frame, height=7, bg=self.colors['terminal_bg'],
                                                      fg=self.colors['accent2'], font=TERMINAL_FONT, 
                                                      wrap=tk.WORD, insertbackground=self.colors['accent'])
        self.methods_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Security panel
        self.security_frame = self._card(left, "[ SECURITY ANALYSIS ]")
        self.security_text = scrolledtext.ScrolledText(self.security_frame, height=6, bg=self.colors['terminal_bg'],
                                                       fg=self.colors['warn'], font=TERMINAL_FONT, 
                                                       wrap=tk.WORD, insertbackground=self.colors['accent'])
        self.security_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Logcat panel - terminalowy styl
        logcat_card = self._card(left, "[ LIVE LOGCAT STREAM ]")
        logcat_controls = tk.Frame(logcat_card, bg=self.colors['panel'])
        logcat_controls.pack(fill=tk.X, padx=4, pady=(2,0))
        
        btn_cfg_logcat = {
            'padx': 14, 'pady': 7, 'bd': 1, 'relief': tk.SOLID, 
            'font': ("Courier New", 9, "bold"), 'cursor': 'hand2',
            'activebackground': self.colors['hover']
        }
        
        self.logcat_start_btn = tk.Button(
            logcat_controls, text="► START", command=self.start_logcat,
            bg=self.colors['success'], fg=self.colors['terminal_bg'], **btn_cfg_logcat
        )
        self.logcat_start_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.logcat_start_btn, self.colors['success'], self.colors['terminal_bg'], self.colors['hover'], self.colors['success'])
        
        self.logcat_stop_btn = tk.Button(
            logcat_controls, text="■ STOP", command=self.stop_logcat,
            bg=self.colors['danger'], fg='#ffffff', state=tk.DISABLED, **btn_cfg_logcat
        )
        self.logcat_stop_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.logcat_stop_btn, self.colors['danger'], '#ffffff', self.colors['hover'], self.colors['danger'])
        
        self.logcat_save_btn = tk.Button(
            logcat_controls, text="💾 SAVE", command=self.save_logcat,
            bg=self.colors['accent2'], fg=self.colors['terminal_bg'], **btn_cfg_logcat
        )
        self.logcat_save_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.logcat_save_btn, self.colors['accent2'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent2'])
        
        self.logcat_clear_btn = tk.Button(
            logcat_controls, text="✖ CLEAR", command=self.clear_logcat,
            bg=self.colors['muted'], fg='#ffffff', **btn_cfg_logcat
        )
        self.logcat_clear_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.logcat_clear_btn, self.colors['muted'], '#ffffff', self.colors['hover'], self.colors['muted'])

        self.logcat_text = scrolledtext.ScrolledText(
            logcat_card, height=11, bg=self.colors['terminal_bg'], 
            fg=self.colors['terminal_fg'], font=TERMINAL_FONT,
            insertbackground=self.colors['accent']
        )
        self.logcat_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # RIGHT: Logs & Controls & Tech Terminal
        right = tk.Frame(main, bg=self.colors['bg'])
        main.add(right, minsize=700)

        # Logs
        self.log_frame = self._card(right, "[ SYSTEM LOGS - REAL TIME ]")
        
        # Log controls
        log_controls = tk.Frame(self.log_frame, bg=self.colors['panel'])
        log_controls.pack(fill=tk.X, padx=4, pady=(2,0))
        
        tk.Button(
            log_controls, text="💾 SAVE LOGS", command=self.save_system_logs,
            bg=self.colors['accent'], fg=self.colors['terminal_bg'], **btn_cfg_logcat
        ).pack(side=tk.LEFT, padx=3)
        self._bind_hover(log_controls.winfo_children()[0], self.colors['accent'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent'])
        
        tk.Button(
            log_controls, text="✖ CLEAR", command=self.clear_system_logs,
            bg=self.colors['muted'], fg='#ffffff', **btn_cfg_logcat
        ).pack(side=tk.LEFT, padx=3)
        self._bind_hover(log_controls.winfo_children()[1], self.colors['muted'], '#ffffff', self.colors['hover'], self.colors['muted'])
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, bg=self.colors['terminal_bg'],
            fg=self.colors['text'], font=TERMINAL_FONT, wrap=tk.WORD,
            insertbackground=self.colors['accent']
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Control buttons
        controls = tk.Frame(right, bg=self.colors['bg'])
        controls.pack(fill=tk.X, pady=(6,0), padx=4)

        btn_cfg = {
            'padx': 18, 'pady': 10, 'bd': 2, 'relief': tk.RAISED, 
            'font': ("Courier New", 10, "bold"), 'cursor': 'hand2'
        }

        self.scan_btn = tk.Button(
            controls, text="🔍 SCAN", command=self.start_scan, 
            bg=self.colors['accent2'], fg=self.colors['terminal_bg'], **btn_cfg
        )
        self.scan_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.scan_btn, self.colors['accent2'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent2'])
        
        self.auto_root_btn = tk.Button(
            controls, text="🤖 AUTO ROOT", command=self.auto_root,
            bg=self.colors['accent'], fg=self.colors['terminal_bg'], state=tk.DISABLED, **btn_cfg
        )
        self.auto_root_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.auto_root_btn, self.colors['accent'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent'])
        
        self.choose_btn = tk.Button(
            controls, text="📋 CHOOSE", command=self.choose_method,
            bg=self.colors['accent2'], fg=self.colors['terminal_bg'], state=tk.DISABLED, **btn_cfg
        )
        self.choose_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.choose_btn, self.colors['accent2'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent2'])
        
        self.unlock_btn = tk.Button(
            controls, text="🔓 UNLOCK", command=self.unlock_bootloader,
            bg=self.colors['warn'], fg=self.colors['terminal_bg'], state=tk.DISABLED, **btn_cfg
        )
        self.unlock_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.unlock_btn, self.colors['warn'], self.colors['terminal_bg'], self.colors['hover'], self.colors['warn'])

        # Extra controls (second row)
        controls2 = tk.Frame(right, bg=self.colors['bg'])
        controls2.pack(fill=tk.X, pady=(4,0), padx=4)

        self.kingroot_btn = tk.Button(
            controls2, text="👑 KINGROOT", command=self.auto_install_kingroot,
            bg=self.colors['panel'], fg=self.colors['accent'], **btn_cfg
        )
        self.kingroot_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.kingroot_btn, self.colors['panel'], self.colors['accent'], self.colors['hover'], self.colors['accent'])

        self.magisk_wiz_btn = tk.Button(
            controls2, text="⚡ MAGISK", command=self.show_magisk_wizard,
            bg=self.colors['panel'], fg=self.colors['accent'], **btn_cfg
        )
        self.magisk_wiz_btn.pack(side=tk.LEFT, padx=3)
        self._bind_hover(self.magisk_wiz_btn, self.colors['panel'], self.colors['accent'], self.colors['hover'], self.colors['accent'])
        
        # Technical Terminal (Integrated)
        terminal_card = self._card(right, "[ TECHNICAL SHELL ACCESS ]")
        terminal_card.pack(fill=tk.BOTH, expand=True, padx=4, pady=(6,0))

        self.tech_terminal_output = scrolledtext.ScrolledText(
            terminal_card, bg=self.colors['terminal_bg'],
            fg=self.colors['terminal_fg'], font=TERMINAL_FONT, wrap=tk.WORD,
            insertbackground=self.colors['accent']
        )
        self.tech_terminal_output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.tech_terminal_output.insert(tk.END, "ARA Technical Terminal - Ready\n")
        self.tech_terminal_output.insert(tk.END, "Type commands and press Enter to execute.\n\n")
        self.tech_terminal_output.tag_config('command', foreground=self.colors['accent'])
        self.tech_terminal_output.tag_config('output', foreground=self.colors['text'])
        self.tech_terminal_output.tag_config('exit_code', foreground=self.colors['muted'])

        # Input frame
        input_frame = tk.Frame(terminal_card, bg=self.colors['panel'])
        input_frame.pack(fill=tk.X, padx=4, pady=2)

        self.tech_terminal_prompt = tk.Label(input_frame, text="> ", fg=self.colors['accent'], bg=self.colors['panel'], font=TERMINAL_FONT)
        self.tech_terminal_prompt.pack(side=tk.LEFT, padx=(0,2))

        self.tech_terminal_input = tk.Entry(
            input_frame, bg=self.colors['terminal_bg'], fg=self.colors['terminal_fg'],
            font=TERMINAL_FONT, insertbackground=self.colors['accent'], bd=0
        )
        self.tech_terminal_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.tech_terminal_input.bind("<Return>", self.execute_tech_command_event)
        
        execute_btn = tk.Button(
            input_frame, text="EXECUTE", command=self.execute_tech_command,
            bg=self.colors['accent'], fg=self.colors['terminal_bg'], 
            font=("Courier New", 9, "bold"), cursor='hand2', padx=8, pady=4, bd=1, relief=tk.SOLID
        )
        execute_btn.pack(side=tk.RIGHT, padx=(4,0))
        self._bind_hover(execute_btn, self.colors['accent'], self.colors['terminal_bg'], self.colors['hover'], self.colors['accent'])


        # Bottom status bar
        self.status_bar = tk.Label(
            self.root, text=f"[ READY ] | {APP_VERSION}",
            bg=self.colors['panel'], fg=self.colors['accent'], 
            anchor=tk.W, font=("Courier New", 9, "bold")
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Technical Terminal Frame (Initially hidden) - NO LONGER USED
        self.tech_terminal_window = None

    def _card(self, parent, title):
        """Tworzy ramkę w stylu terminala"""
        card = tk.LabelFrame(
            parent, text=title, bg=self.colors['panel'], 
            fg=self.colors['accent'], font=H2_FONT, 
            padx=4, pady=4, labelanchor='n', bd=1, 
            relief=tk.FLAT, highlightbackground=self.colors['border'], highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        return card

    def _bind_hover(self, button, normal_bg, normal_fg, hover_bg, hover_fg):
        """Dodaje efekt hover do przycisku"""
        button.bind('<Enter>', lambda e: button.config(bg=hover_bg, fg=hover_fg))
        button.bind('<Leave>', lambda e: button.config(bg=normal_bg, fg=normal_fg))

    # -----------------------
    # Logging & Command Exec
    # -----------------------
    def log(self, message, level='INFO'):
        ts = datetime.now().strftime("%H:%M:%S")
        prefix_map = {
            'INFO': '[i]',
            'SUCCESS': '[✓]',
            'WARNING': '[!]',
            'ERROR': '[X]',
            'CRITICAL': '[!!]',
            'PROGRESS': '[~]'
        }
        prefix = prefix_map.get(level, '[?]')
        line = f"[{ts}] {prefix} {message}\n"
        
        # Zapisz do listy wszystkich logów
        self.all_logs.append(line)
        
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

    def run_command(self, cmd, timeout=30):
        """Run shell command and return stdout, code"""
        try:
            self.log(f"Executing: {cmd}", 'PROGRESS')
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            out = result.stdout.strip()
            return out, result.returncode
        except subprocess.TimeoutExpired:
            self.log(f"Command timeout: {cmd}", 'ERROR')
            return "", 1
        except Exception as e:
            self.log(f"Command exception: {e}", 'CRITICAL')
            return str(e), 1

    def save_system_logs(self):
        """Zapisuje logi systemowe do pliku"""
        if not self.all_logs:
            messagebox.showinfo("No logs", "No logs to save yet.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOGS_DIR / f"system_log_{timestamp}.txt"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.writelines(self.all_logs)
            self.log(f"Logs saved to: {log_file}", 'SUCCESS')
            messagebox.showinfo("Saved", f"System logs saved to:\n{log_file}")
        except Exception as e:
            self.log(f"Failed to save logs: {e}", 'ERROR')
            messagebox.showerror("Error", f"Failed to save logs:\n{e}")

    def clear_system_logs(self):
        """Czyści okno logów"""
        self.log_text.delete(1.0, tk.END)
        self.log("Logs cleared", 'INFO')

    def save_logcat(self):
        """Zapisuje logcat do pliku"""
        content = self.logcat_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("No data", "Logcat is empty.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logcat_file = LOGS_DIR / f"logcat_{timestamp}.txt"
        
        try:
            with open(logcat_file, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"Logcat saved to: {logcat_file}", 'SUCCESS')
            messagebox.showinfo("Saved", f"Logcat saved to:\n{logcat_file}")
        except Exception as e:
            self.log(f"Failed to save logcat: {e}", 'ERROR')
            messagebox.showerror("Error", f"Failed to save logcat:\n{e}")

    def clear_logcat(self):
        """Czyści okno logcat"""
        self.logcat_text.delete(1.0, tk.END)
        self.log("Logcat cleared", 'INFO')

    def execute_tech_command_event(self, event):
        self.execute_tech_command()

    def execute_tech_command(self):
        command = self.tech_terminal_input.get().strip()
        if not command:
            return
        self.tech_terminal_input.delete(0, tk.END)
        self.tech_terminal_output.insert(tk.END, f"> {command}\n", 'command')
        self.tech_terminal_output.see(tk.END)

        def run_in_thread():
            output, code = self.run_command(command, timeout=60)
            self.root.after(0, lambda: self.tech_terminal_output.insert(tk.END, f"{output}\n", 'output'))
            self.root.after(0, lambda: self.tech_terminal_output.insert(tk.END, f"[Exit Code: {code}]\n\n", 'exit_code'))
            self.root.after(0, lambda: self.tech_terminal_output.see(tk.END))
            self.log(f"Tech command '{command}' finished with exit code {code}", 'INFO')

        threading.Thread(target=run_in_thread, daemon=True).start()

    # -----------------------
    # Logcat stream methods
    # -----------------------
    def start_logcat(self):
        if self.logcat_running:
            self.log("Logcat is already running.", 'WARNING')
            return
        if not self.device_connected:
            messagebox.showwarning("Connection Error", "No Android device detected.")
            return

        self.log("Starting logcat stream...", 'INFO')
        self.logcat_running = True
        self.logcat_start_btn.config(state=tk.DISABLED)
        self.logcat_stop_btn.config(state=tk.NORMAL)
        self.logcat_text.delete(1.0, tk.END)

        def stream_logcat():
            try:
                # Use Popen to have control over the process
                self.logcat_process = subprocess.Popen(
                    ['adb', 'logcat'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                for line in iter(self.logcat_process.stdout.readline, ''):
                    if not self.logcat_running:
                        break
                    # Schedule the GUI update on the main thread
                    self.root.after(0, self.logcat_text.insert, tk.END, line)
                    self.root.after(0, self.logcat_text.see, tk.END)
                self.logcat_process.stdout.close()
            except Exception as e:
                if self.logcat_running: # Only log error if it wasn't stopped manually
                    self.root.after(0, self.log, f"Logcat stream error: {e}", 'ERROR')
            finally:
                self.root.after(0, self.stop_logcat)

        self.logcat_thread = threading.Thread(target=stream_logcat, daemon=True)
        self.logcat_thread.start()

    def stop_logcat(self):
        if not self.logcat_running:
            return
        
        self.log("Stopping logcat stream...", 'INFO')
        self.logcat_running = False
        
        if self.logcat_process:
            try:
                # Terminate the process cleanly
                self.logcat_process.terminate()
                self.logcat_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.logcat_process.kill() # Force kill if terminate fails
                self.log("Forcibly killed logcat process.", 'WARNING')
            except Exception as e:
                self.log(f"Error while stopping logcat: {e}", 'ERROR')
            self.logcat_process = None

        if self.logcat_thread and self.logcat_thread.is_alive():
            self.logcat_thread.join(timeout=2)

        self.logcat_start_btn.config(state=tk.NORMAL)
        self.logcat_stop_btn.config(state=tk.DISABLED)
        self.log("Logcat stream stopped.", 'SUCCESS')

    # -----------------------
    # Rooting & Actions
    # -----------------------
    def auto_root(self):
        self.log("Auto Root function is not implemented yet.", "WARNING")
        messagebox.showinfo("Not Implemented", "Auto Root is a placeholder for future versions.")

    def choose_method(self):
        self.log("Choose Method function is not implemented yet.", "WARNING")
        messagebox.showinfo("Not Implemented", "This would allow selecting a specific root method.")

    def unlock_bootloader(self):
        if not self.device_connected:
            messagebox.showerror("Error", "No device connected.")
            return

        confirmed = messagebox.askyesno(
            "⚠️ UNLOCK BOOTLOADER ⚠️",
            "This is a dangerous operation that will WIPE ALL DATA on your device.\n"
            "Your warranty may be voided.\n\n"
            "Steps:\n1. The device will reboot into bootloader (fastboot) mode.\n"
            "2. You may need to run a 'fastboot oem unlock' command manually.\n\n"
            "Do you want to proceed with rebooting to bootloader?",
            icon='warning'
        )

        if confirmed:
            self.log("Rebooting device to bootloader...", "WARNING")
            self.run_command("adb reboot bootloader")
            messagebox.showinfo(
                "Rebooting", 
                "Device is rebooting into bootloader.\n"
                "Once in fastboot mode, you might need to execute:\n"
                "fastboot flashing unlock\nOR\nfastboot oem unlock"
            )
        else:
            self.log("Bootloader unlock cancelled by user.", "INFO")

    def auto_install_kingroot(self):
        self.log("KingRoot installer is a placeholder.", "WARNING")
        messagebox.showinfo("Not Implemented", "This feature is for demonstration purposes and not implemented.")

    def show_magisk_wizard(self):
        self.log("Magisk Wizard is a placeholder.", "WARNING")
        messagebox.showinfo("Not Implemented", "This would open a step-by-step guide for Magisk.")

    def show_scan_report(self):
        self.log("Displaying scan report.", "INFO")
        if not self.device_info:
            messagebox.showinfo("Scan Report", "Scan has not been run yet.")
            return
        report = f"""
    *** SCAN COMPLETE ***
    - Device: {self.device_info.get('Manufacturer')} {self.device_info.get('Model')}
    - Android: {self.device_info.get('Android')} (SDK {self.device_info.get('SDK')})
    - Arch: {self.device_info.get('Arch')}
    - Detected Methods: {len(self.root_methods)}
    
    Review the panels for detailed information.
    """
        messagebox.showinfo("Scan Report", report)
    
    # -----------------------
    # Device checks & scan
    # -----------------------
    def auto_check_device(self):
        self.log("Initializing system checks...", 'INFO')
        self.check_adb()
        self.check_device_connection()

    def check_adb(self):
        adb_path = shutil.which("adb")
        if adb_path:
            ver, _ = self.run_command("adb version")
            self.adb_status_label.config(
                text=f"[ADB: ONLINE - {ver.splitlines()[0] if ver else 'READY'}]", 
                fg=self.colors['success']
            )
            self.log("ADB daemon ready", 'SUCCESS')
            return True
        else:
            self.adb_status_label.config(text="[ADB: NOT FOUND]", fg=self.colors['danger'])
            self.log("ADB not detected in PATH", 'ERROR')
            return False

    def check_device_connection(self):
        self.run_command("adb start-server")
        time.sleep(0.5)
        out, code = self.run_command("adb devices -l")
        if code != 0:
            self.update_device_status(False)
            return False
        lines = out.splitlines()
        devices = [l for l in lines[1:] if l.strip() and ('device' in l or 'unauthorized' in l)]
        if devices:
            self.device_connected = True
            self.update_device_status(True, devices[0])
            self.log(f"Device connected: {devices[0]}", 'SUCCESS')
            self.auto_root_btn.config(state=tk.NORMAL)
            self.choose_btn.config(state=tk.NORMAL)
            self.unlock_btn.config(state=tk.NORMAL)
            return True
        else:
            self.device_connected = False
            self.update_device_status(False)
            self.log("No Android device detected", 'WARNING')
            return False

    def update_device_status(self, connected, info=""):
        if connected:
            self.device_status_label.config(
                text=f"[DEVICE: ONLINE] {info[:50]}", 
                fg=self.colors['success']
            )
            self.status_bar.config(text=f"[ DEVICE READY ] | {info[:80]}")
        else:
            self.device_status_label.config(
                text="[DEVICE: OFFLINE]", 
                fg=self.colors['danger']
            )
            self.status_bar.config(text="[ NO DEVICE CONNECTED ]")

    def start_scan(self):
        if self.is_scanning:
            self.log("Scan operation already in progress", 'WARNING')
            return
        if not self.device_connected:
            messagebox.showwarning("Connection Error", "No Android device detected.\nConnect device via USB and enable USB debugging.")
            return
        self.is_scanning = True
        self.scan_btn.config(text="⏳ SCANNING...", state=tk.DISABLED)
        thread = threading.Thread(target=self.scan_device, daemon=True)
        thread.start()

    def scan_device(self):
        try:
            self.log("="*60, 'INFO')
            self.log("INITIATING FULL DEVICE SCAN", 'INFO')
            self.log("="*60, 'INFO')
            self.collect_device_info()
            self.check_root_status()
            self.analyze_security()
            self.detect_root_methods_advanced()
            self.log("="*60, 'SUCCESS')
            self.log("SCAN COMPLETE - ALL SYSTEMS ANALYZED", 'SUCCESS')
            self.log("="*60, 'SUCCESS')
            self.show_scan_report()
        except Exception as e:
            self.log(f"Critical scan error: {e}", 'CRITICAL')
        finally:
            self.is_scanning = False
            self.root.after(0, lambda: self.scan_btn.config(text="🔍 SCAN", state=tk.NORMAL))

    def collect_device_info(self):
        self.info_text.delete(1.0, tk.END)
        props = {
            'Model': 'ro.product.model',
            'Manufacturer': 'ro.product.manufacturer',
            'Android': 'ro.build.version.release',
            'SDK': 'ro.build.version.sdk',
            'Arch': 'ro.product.cpu.abi',
            'Bootloader': 'ro.bootloader',
            'Build ID': 'ro.build.id'
        }
        info_data = {}
        self.info_text.insert(tk.END, "╔═══════════════════════════════════╗\n")
        self.info_text.insert(tk.END, "║    DEVICE SPECIFICATIONS          ║\n")
        self.info_text.insert(tk.END, "╠═══════════════════════════════════╣\n")
        for k, prop in props.items():
            out, _ = self.run_command(f"adb shell getprop {prop}")
            if out:
                info_data[k] = out
                self.info_text.insert(tk.END, f"║ {k:13}: {out:18} ║\n")
        self.info_text.insert(tk.END, "╚═══════════════════════════════════╝\n")
        self.device_info = info_data

    def check_root_status(self):
        out, code = self.run_command("adb shell which su")
        has_root = (code == 0 and '/su' in out)
        magisk_out, _ = self.run_command("adb shell pm list packages | grep -i magisk")
        has_magisk = 'magisk' in magisk_out.lower()
        
        self.info_text.insert(tk.END, "\n╔═══════════════════════════════════╗\n")
        self.info_text.insert(tk.END, "║       ROOT STATUS                 ║\n")
        self.info_text.insert(tk.END, "╠═══════════════════════════════════╣\n")
        self.info_text.insert(tk.END, f"║ ROOT ACCESS : {'[YES]' if has_root else '[NO]':18} ║\n")
        self.info_text.insert(tk.END, f"║ MAGISK      : {'[YES]' if has_magisk else '[NO]':18} ║\n")
        self.info_text.insert(tk.END, "╚═══════════════════════════════════╝\n")
        
        self.log(f"Root analysis: {'ROOTED' if has_root else 'NOT ROOTED'}", 'INFO')

    def analyze_security(self):
        self.security_text.delete(1.0, tk.END)
        self.security_text.insert(tk.END, ">>> Analyzing installed packages...\n")
        self.security_text.insert(tk.END, ">>> Searching for suspicious patterns...\n\n")
        
        suspect = ['facebook', 'tencent', 'baidu', 'analytics', 'tracker', 'cleanmaster', 'adware']
        out, _ = self.run_command("adb shell pm list packages")
        found = 0
        
        for s in suspect:
            if s in out.lower():
                self.security_text.insert(tk.END, f"[!] WARNING: Package containing '{s}' detected\n")
                found += 1
        
        if found == 0:
            self.security_text.insert(tk.END, "[✓] No obvious suspicious packages found\n")
            self.security_text.insert(tk.END, "[✓] Security scan passed\n")
        else:
            self.security_text.insert(tk.END, f"\n[!] Total suspicious entries: {found}\n")
            self.security_text.insert(tk.END, "[!] Recommend manual review\n")

    def detect_root_methods_advanced(self):
        self.methods_text.delete(1.0, tk.END)
        sdk = int(self.device_info.get('SDK', '0') or 0)
        manu = self.device_info.get('Manufacturer', '').lower()
        model = self.device_info.get('Model', '').lower()
        methods = []

        methods.append({
            'name': 'MAGISK (Universal - Recommended)',
            'compatibility': '98%',
            'risk': 'LOW',
            'steps': [
                '> Unlock bootloader',
                '> Extract boot.img from firmware',
                '> Patch with Magisk Manager',
                '> Flash patched boot via fastboot'
            ]
        })

        if 'samsung' in manu:
            methods.append({
                'name': 'ODIN + MAGISK (Samsung Specific)',
                'compatibility': '95%',
                'risk': 'LOW',
                'steps': [
                    '> Download firmware (AP_*.tar.md5)',
                    '> Extract boot.img',
                    '> Patch with Magisk',
                    '> Flash via Odin in AP slot'
                ]
            })

        if 'xiaomi' in manu or 'redmi' in model:
            methods.append({
                'name': 'MI UNLOCK + MAGISK (Xiaomi)',
                'compatibility': '90%',
                'risk': 'MEDIUM',
                'steps': [
                    '> Apply for unlock permission from Xiaomi',
                    '> Use Mi Unlock Tool',
                    '> Flash Magisk via Fastboot'
                ]
            })

        if sdk <= 22: # Android 5.1 and below
             methods.append({
                'name': 'KINGROOT (Old Devices)',
                'compatibility': '60%',
                'risk': 'HIGH',
                'steps': [
                    '> Install KingRoot APK',
                    '> Run one-click root',
                    '> Recommended: Replace with SuperSU afterwards'
                ]
            })
        
        self.root_methods = methods
        self.methods_text.insert(tk.END, f"Found {len(methods)} potential methods:\n\n")
        for i, m in enumerate(methods):
            self.methods_text.insert(tk.END, f"[{i+1}] {m['name']}\n")
            self.methods_text.insert(tk.END, f"    Compat: {m['compatibility']} | Risk: {m['risk']}\n")
            for step in m['steps']:
                self.methods_text.insert(tk.END, f"    {step}\n")
            self.methods_text.insert(tk.END, "\n")
        
        self.log(f"Detected {len(methods)} potential rooting methods.", 'INFO')

# -----------------------
# Main execution
# -----------------------
def main():
    """Main function to start the app"""
    root = tk.Tk()
    app = AndroidRootAssistant(root)
    
    def on_closing():
        if app.logcat_running:
            app.stop_logcat()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    # Add a handler for Ctrl+C
    def signal_handler(sig, frame):
        print("\nCtrl+C detected. Shutting down ARA...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    main()