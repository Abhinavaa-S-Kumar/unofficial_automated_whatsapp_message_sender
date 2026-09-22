import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import datetime
import os
import sys
import subprocess
import webbrowser
import urllib.parse


def install_package(package_name):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def ensure_dependencies():
    deps = {"pyautogui": "pyautogui", "pyperclip": "pyperclip"}
    missing = []
    for module, pip_name in deps.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f"[Setup] Installing missing packages: {', '.join(missing)} ...")
        for pkg in missing:
            try:
                install_package(pkg)
                print(f"  ✓ Installed {pkg}")
            except Exception as e:
                print(f"  ✗ Failed to install {pkg}: {e}")
                sys.exit(1)

ensure_dependencies()

import pyautogui
import pyperclip
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3



def detect_whatsapp_desktop():
    candidate_paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\whatsapp-desktop\WhatsApp.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\WhatsApp\WhatsApp.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\WhatsApp\WhatsApp.exe"),
    ]

    for path in candidate_paths:
        if os.path.isfile(path):
            return path

    try:
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                'Get-AppxPackage -Name "*WhatsApp*" | '
                'Select-Object -ExpandProperty InstallLocation',
            ],
            capture_output=True, text=True, timeout=8,
        )
        location = result.stdout.strip()
        if location:
            return location
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq WhatsApp.exe"],
            capture_output=True, text=True, timeout=5,
        )
        if "WhatsApp.exe" in result.stdout:
            return "running"
    except Exception:
        pass

    return None



class MessageSender:

    def __init__(self, mode="web", log_callback=None):
        self.mode = mode
        self.log = log_callback or print
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True

    def reset(self):
        self._stop_flag = False

    def open_chat(self, phone_number, initial_text=""):
        phone = self._sanitize_phone(phone_number)

        if self.mode == "desktop":
            url = f"whatsapp://send?phone={phone}"
            self.log(f"Opening WhatsApp Desktop for +{phone} ...")
            os.startfile(url)
            time.sleep(5) 
        else:
           
            url = f"https://web.whatsapp.com/send?phone={phone}"
            self.log(f"Opening WhatsApp Web for +{phone} ...")
            webbrowser.open(url)
            time.sleep(10)

    def send_messages(self, phone_number, message, count, delay_seconds,
                      progress_callback=None):
        
        self.reset()

       
        self.open_chat(phone_number)

        self.log("Chat opened. Waiting for it to fully load ...")

       
        if self.mode == "web":
            self.log("⏳ Please make sure WhatsApp Web is logged in and the chat is visible.")
            time.sleep(8)
        else:
            time.sleep(3)

        sent = 0
        for i in range(count):
            if self._stop_flag:
                self.log(f"⛔ Stopped after sending {sent}/{count} messages.")
                break

            try:
                self._type_and_send(message)
                sent += 1
                self.log(f"✅ Message {sent}/{count} sent!")

                if progress_callback:
                    progress_callback(sent, count)

                if i < count - 1 and delay_seconds > 0:
                    self.log(f"⏳ Waiting {delay_seconds}s before next message ...")
                    for _ in range(int(delay_seconds * 10)):
                        if self._stop_flag:
                            break
                        time.sleep(0.1)

            except Exception as e:
                self.log(f"❌ Error sending message {i + 1}: {e}")

        self.log(f"🏁 Done! Sent {sent}/{count} messages.")
        return sent

    def _type_and_send(self, message):
        pyperclip.copy(message)
        time.sleep(0.2)

        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.3)

        pyautogui.press("enter")
        time.sleep(0.5)

    @staticmethod
    def _sanitize_phone(phone):
        phone = phone.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if phone.startswith("+"):
            phone = phone[1:]
        if len(phone) == 10:
            phone = "91" + phone
        return phone



EMOJI_CATEGORIES = {
    "😀 Smileys": [
        "😀", "😃", "😄", "😁", "😆", "😅", "🤣", "😂", "🙂", "😊",
        "😇", "🥰", "😍", "🤩", "😘", "😗", "😚", "😙", "🥲", "😋",
        "😛", "😜", "🤪", "😝", "🤑", "🤗", "🤭", "🤫", "🤔", "🫡",
        "🤐", "🤨", "😐", "😑", "😶", "🫥", "😏", "😒", "🙄", "😬",
        "😮‍💨", "🤥", "😌", "😔", "😪", "🤤", "😴", "😷", "🤒", "🤕",
        "🤢", "🤮", "🥵", "🥶", "🥴", "😵", "🤯", "🤠", "🥳", "🥸",
        "😎", "🤓", "🧐", "😕", "🫤", "😟", "🙁", "😮", "😯", "😲",
        "😳", "🥺", "🥹", "😦", "😧", "😨", "😰", "😥", "😢", "😭",
    ],
    "👋 Gestures": [
        "👋", "🤚", "🖐️", "✋", "🖖", "🫱", "🫲", "🫳", "🫴", "👌",
        "🤌", "🤏", "✌️", "🤞", "🫰", "🤟", "🤘", "🤙", "👈", "👉",
        "👆", "🖕", "👇", "☝️", "🫵", "👍", "👎", "✊", "👊", "🤛",
        "🤜", "👏", "🙌", "🫶", "👐", "🤲", "🤝", "🙏", "💪", "🦾",
    ],
    "❤️ Hearts": [
        "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔",
        "❤️‍🔥", "❤️‍🩹", "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝",
        "💟", "♥️", "🫀", "💋", "💌", "💐", "🌹", "🥀", "🌺", "🌸",
    ],
    "🎉 Objects": [
        "🎉", "🎊", "🎈", "🎁", "🎀", "🏆", "🥇", "🥈", "🥉", "⚽",
        "🏀", "🏈", "⚾", "🎾", "🏐", "🎮", "🕹️", "🎲", "🎯", "🎳",
        "🔔", "🎵", "🎶", "🎤", "🎧", "📱", "💻", "⌨️", "🖥️", "📷",
        "📚", "📖", "📝", "✏️", "📌", "📎", "🔑", "🔒", "💡", "🔥",
    ],
    "🍕 Food": [
        "🍕", "🍔", "🍟", "🌭", "🍿", "🧂", "🥚", "🍳", "🥞", "🧇",
        "🥓", "🥩", "🍗", "🍖", "🌮", "🌯", "🥙", "🧆", "🥗", "🍝",
        "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🍤", "🍙", "🍚", "🍘",
        "🍰", "🎂", "🧁", "🍩", "🍪", "🍫", "🍬", "🍭", "☕", "🍵",
    ],
    "🚀 Travel": [
        "🚀", "✈️", "🛫", "🛬", "🚁", "🛸", "🚗", "🚕", "🚙", "🏎️",
        "🚌", "🚎", "🚐", "🚑", "🚒", "🚓", "🚔", "🚲", "🛵", "🏍️",
        "🚂", "🚆", "🚇", "🚊", "🚉", "⛵", "🚤", "🛥️", "🛳️", "⛴️",
        "🌍", "🌎", "🌏", "🗺️", "🏔️", "⛰️", "🌋", "🗻", "🏕️", "🏖️",
    ],
    "⭐ Symbols": [
        "⭐", "🌟", "✨", "💫", "⚡", "🔥", "💥", "☀️", "🌤️", "⛅",
        "🌈", "☁️", "🌧️", "⛈️", "❄️", "💧", "🌊", "🎃", "🎄", "🎆",
        "✅", "❌", "⭕", "❗", "❓", "💯", "🔴", "🟢", "🔵", "🟡",
        "⬛", "⬜", "🟥", "🟩", "🟦", "🟨", "▶️", "⏸️", "⏹️", "⏺️",
    ],
    "🐱 pets":[
        "🐱", "🐈",
    ],
}



COLORS = {
    "bg_dark":       "#0d1117",
    "bg_card":       "#161b22",
    "bg_input":      "#21262d",
    "bg_hover":      "#30363d",
    "border":        "#30363d",
    "border_focus":  "#58a6ff",
    "text":          "#e6edf3",
    "text_dim":      "#8b949e",
    "text_muted":    "#484f58",
    "accent":        "#58a6ff",
    "accent_hover":  "#79c0ff",
    "green":         "#3fb950",
    "green_dark":    "#238636",
    "red":           "#f85149",
    "orange":        "#d29922",
    "purple":        "#bc8cff",
    "gradient_start":"#58a6ff",
    "gradient_end":  "#bc8cff",
    "btn_primary":   "#238636",
    "btn_primary_h": "#2ea043",
    "btn_danger":    "#da3633",
    "btn_danger_h":  "#f85149",
    "emoji_bg":      "#1c2128",
}



class WhatsAppAutomatorApp:


    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Message Automator")
        self.root.geometry("680x920")
        self.root.minsize(600, 800)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.resizable(True, True)

        self.whatsapp_path = detect_whatsapp_desktop()
        self.desktop_available = self.whatsapp_path is not None
        self.sender = None
        self.sending_thread = None
        self.is_sending = False
        self.emoji_visible = False

        self.mode_var = tk.StringVar(value="desktop" if self.desktop_available else "web")
        self.phone_var = tk.StringVar()
        self.count_var = tk.StringVar(value="1")
        self.delay_var = tk.StringVar(value="2")
        self.schedule_var = tk.BooleanVar(value=False)
        self.hour_var = tk.StringVar(value=datetime.datetime.now().strftime("%H"))
        self.minute_var = tk.StringVar(value=datetime.datetime.now().strftime("%M"))
        self.date_var = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d"))

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        
        self._build_ui()


    def _build_ui(self):
        
        self.canvas = tk.Canvas(self.root, bg=COLORS["bg_dark"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=COLORS["bg_dark"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        container = tk.Frame(self.scroll_frame, bg=COLORS["bg_dark"])
        container.pack(fill="x", padx=20, pady=10)

        self._build_header(container)

        self._build_mode_selector(container)

        self._build_phone_input(container)

        self._build_message_input(container)

        self._build_emoji_picker(container)

        self._build_settings(container)

        self._build_schedule(container)

        self._build_action_buttons(container)

        self._build_progress(container)

        self._build_log(container)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _build_header(self, parent):

        header = tk.Frame(parent, bg=COLORS["bg_dark"])
        header.pack(fill="x", pady=(10, 5))

        title_frame = tk.Frame(header, bg=COLORS["bg_dark"])
        title_frame.pack(fill="x")

        icon_label = tk.Label(
            title_frame, text="💬", font=("Segoe UI Emoji", 28),
            bg=COLORS["bg_dark"], fg=COLORS["text"]
        )
        icon_label.pack(side="left", padx=(0, 10))

        text_frame = tk.Frame(title_frame, bg=COLORS["bg_dark"])
        text_frame.pack(side="left", fill="x")

        tk.Label(
            text_frame, text="WhatsApp Automator",
            font=("Segoe UI", 22, "bold"), bg=COLORS["bg_dark"], fg=COLORS["text"]
        ).pack(anchor="w")

        tk.Label(
            text_frame, text="Send bulk messages with scheduling & emoji support",
            font=("Segoe UI", 10), bg=COLORS["bg_dark"], fg=COLORS["text_dim"]
        ).pack(anchor="w")

        tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", pady=(15, 5))

    def _build_mode_selector(self, parent):
        card = self._card(parent, "Connection Mode")

        mode_frame = tk.Frame(card, bg=COLORS["bg_card"])
        mode_frame.pack(fill="x", pady=5)

        desktop_frame = tk.Frame(mode_frame, bg=COLORS["bg_card"])
        desktop_frame.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.desktop_radio = tk.Radiobutton(
            desktop_frame, text="  🖥️  Desktop App",
            variable=self.mode_var, value="desktop",
            font=("Segoe UI", 11), bg=COLORS["bg_card"], fg=COLORS["text"],
            selectcolor=COLORS["bg_input"], activebackground=COLORS["bg_card"],
            activeforeground=COLORS["text"], highlightthickness=0,
            borderwidth=0, indicatoron=True,
            state="normal" if self.desktop_available else "disabled",
        )
        self.desktop_radio.pack(anchor="w", padx=10, pady=5)

        web_frame = tk.Frame(mode_frame, bg=COLORS["bg_card"])
        web_frame.pack(side="left", expand=True, fill="x", padx=(5, 0))

        self.web_radio = tk.Radiobutton(
            web_frame, text="  🌐  WhatsApp Web",
            variable=self.mode_var, value="web",
            font=("Segoe UI", 11), bg=COLORS["bg_card"], fg=COLORS["text"],
            selectcolor=COLORS["bg_input"], activebackground=COLORS["bg_card"],
            activeforeground=COLORS["text"], highlightthickness=0,
            borderwidth=0, indicatoron=True,
        )
        self.web_radio.pack(anchor="w", padx=10, pady=5)

        if self.desktop_available:
            status_text = "✅ WhatsApp Desktop detected"
            status_color = COLORS["green"]
        else:
            status_text = "⚠️ WhatsApp Desktop not found — using Web"
            status_color = COLORS["orange"]

        tk.Label(
            card, text=status_text,
            font=("Segoe UI", 9), bg=COLORS["bg_card"], fg=status_color
        ).pack(anchor="w", padx=10, pady=(5, 0))

    def _build_phone_input(self, parent):
        card = self._card(parent, "📱 Phone Number")

        hint = tk.Label(
            card, text="Enter with country code (e.g., +91 9876543210)",
            font=("Segoe UI", 9), bg=COLORS["bg_card"], fg=COLORS["text_dim"]
        )
        hint.pack(anchor="w", padx=10, pady=(0, 5))

        input_frame = tk.Frame(card, bg=COLORS["bg_input"], highlightbackground=COLORS["border"],
                               highlightthickness=1, highlightcolor=COLORS["border_focus"])
        input_frame.pack(fill="x", padx=10, pady=(0, 5))

        prefix = tk.Label(
            input_frame, text=" + ", font=("Segoe UI", 13, "bold"),
            bg=COLORS["bg_input"], fg=COLORS["accent"]
        )
        prefix.pack(side="left", padx=(5, 0))

        self.phone_entry = tk.Entry(
            input_frame, textvariable=self.phone_var,
            font=("Segoe UI", 13), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", borderwidth=0,
        )
        self.phone_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=8)

    def _build_message_input(self, parent):
        card = self._card(parent, "✍️ Message")

        hint = tk.Label(
            card, text="Type your message below (emojis supported!)",
            font=("Segoe UI", 9), bg=COLORS["bg_card"], fg=COLORS["text_dim"]
        )
        hint.pack(anchor="w", padx=10, pady=(0, 5))

        text_frame = tk.Frame(card, bg=COLORS["bg_input"], highlightbackground=COLORS["border"],
                              highlightthickness=1, highlightcolor=COLORS["border_focus"])
        text_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.message_text = tk.Text(
            text_frame, font=("Segoe UI Emoji", 12), bg=COLORS["bg_input"],
            fg=COLORS["text"], insertbackground=COLORS["text"], relief="flat",
            borderwidth=0, height=5, wrap="word", padx=10, pady=8,
        )
        self.message_text.pack(fill="x", expand=True)

        self.char_count_label = tk.Label(
            card, text="0 characters",
            font=("Segoe UI", 9), bg=COLORS["bg_card"], fg=COLORS["text_muted"]
        )
        self.char_count_label.pack(anchor="e", padx=10)
        self.message_text.bind("<KeyRelease>", self._update_char_count)

    def _build_emoji_picker(self, parent):
        self.emoji_toggle_btn = tk.Button(
            parent, text="😀 Insert Emoji ▼", font=("Segoe UI Emoji", 11),
            bg=COLORS["bg_card"], fg=COLORS["accent"], relief="flat",
            borderwidth=0, cursor="hand2", activebackground=COLORS["bg_hover"],
            activeforeground=COLORS["accent_hover"],
            command=self._toggle_emoji_picker,
        )
        self.emoji_toggle_btn.pack(fill="x", pady=(5, 0))

        self.emoji_panel = tk.Frame(parent, bg=COLORS["emoji_bg"],
                                     highlightbackground=COLORS["border"],
                                     highlightthickness=1)

        self.category_frame = tk.Frame(self.emoji_panel, bg=COLORS["bg_dark"])
        self.category_frame.pack(fill="x", padx=5, pady=5)

        self.emoji_grid_frame = tk.Frame(self.emoji_panel, bg=COLORS["emoji_bg"])
        self.emoji_grid_frame.pack(fill="x", padx=5, pady=(0, 5))

        self._populate_emoji_categories()

    def _populate_emoji_categories(self):
        categories = list(EMOJI_CATEGORIES.keys())

        for i, cat in enumerate(categories):
            btn = tk.Button(
                self.category_frame, text=cat.split(" ")[0],
                font=("Segoe UI Emoji", 13), bg=COLORS["bg_card"],
                fg=COLORS["text"], relief="flat", borderwidth=0,
                cursor="hand2", padx=6, pady=2,
                activebackground=COLORS["bg_hover"],
                command=lambda c=cat: self._show_emoji_category(c),
            )
            btn.pack(side="left", padx=2)

        self._show_emoji_category(categories[0])

    def _show_emoji_category(self, category):
        for widget in self.emoji_grid_frame.winfo_children():
            widget.destroy()

        emojis = EMOJI_CATEGORIES[category]
        cols = 10

        for i, emoji in enumerate(emojis):
            row, col = divmod(i, cols)
            btn = tk.Button(
                self.emoji_grid_frame, text=emoji,
                font=("Segoe UI Emoji", 16), bg=COLORS["emoji_bg"],
                fg=COLORS["text"], relief="flat", borderwidth=0,
                cursor="hand2", width=2, height=1,
                activebackground=COLORS["bg_hover"],
                command=lambda e=emoji: self._insert_emoji(e),
            )
            btn.grid(row=row, column=col, padx=1, pady=1)

    def _insert_emoji(self, emoji):
        self.message_text.insert(tk.INSERT, emoji)
        self.message_text.focus_set()
        self._update_char_count()

    def _toggle_emoji_picker(self):
        if self.emoji_visible:
            self.emoji_panel.pack_forget()
            self.emoji_toggle_btn.configure(text="😀 Insert Emoji ▼")
        else:
            self.emoji_panel.pack(fill="x", pady=(0, 5), after=self.emoji_toggle_btn)
            self.emoji_toggle_btn.configure(text="😀 Insert Emoji ▲")
        self.emoji_visible = not self.emoji_visible

    def _build_settings(self, parent):
        card = self._card(parent, "⚙️ Settings")

        settings_grid = tk.Frame(card, bg=COLORS["bg_card"])
        settings_grid.pack(fill="x", padx=10, pady=5)

        tk.Label(
            settings_grid, text="Number of Messages",
            font=("Segoe UI", 11), bg=COLORS["bg_card"], fg=COLORS["text"]
        ).grid(row=0, column=0, sticky="w", padx=(0, 20), pady=5)

        count_input = tk.Frame(settings_grid, bg=COLORS["bg_input"],
                               highlightbackground=COLORS["border"], highlightthickness=1)
        count_input.grid(row=0, column=1, sticky="e", pady=5)

        self.count_entry = tk.Entry(
            count_input, textvariable=self.count_var,
            font=("Segoe UI", 12), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", width=8,
            borderwidth=0, justify="center",
        )
        self.count_entry.pack(padx=8, ipady=5)

        tk.Label(
            settings_grid, text="Delay Between Messages (sec)",
            font=("Segoe UI", 11), bg=COLORS["bg_card"], fg=COLORS["text"]
        ).grid(row=1, column=0, sticky="w", padx=(0, 20), pady=5)

        delay_input = tk.Frame(settings_grid, bg=COLORS["bg_input"],
                               highlightbackground=COLORS["border"], highlightthickness=1)
        delay_input.grid(row=1, column=1, sticky="e", pady=5)

        self.delay_entry = tk.Entry(
            delay_input, textvariable=self.delay_var,
            font=("Segoe UI", 12), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", width=8,
            borderwidth=0, justify="center",
        )
        self.delay_entry.pack(padx=8, ipady=5)

        settings_grid.columnconfigure(0, weight=1)

    def _build_schedule(self, parent):
        card = self._card(parent, "🕐 Schedule (Optional)")

        self.schedule_check = tk.Checkbutton(
            card, text="  Schedule messages for later",
            variable=self.schedule_var, font=("Segoe UI", 11),
            bg=COLORS["bg_card"], fg=COLORS["text"],
            selectcolor=COLORS["bg_input"], activebackground=COLORS["bg_card"],
            activeforeground=COLORS["text"], highlightthickness=0,
            command=self._toggle_schedule,
        )
        self.schedule_check.pack(anchor="w", padx=10, pady=5)

        self.schedule_inputs = tk.Frame(card, bg=COLORS["bg_card"])

        date_row = tk.Frame(self.schedule_inputs, bg=COLORS["bg_card"])
        date_row.pack(fill="x", padx=10, pady=5)

        tk.Label(
            date_row, text="📅 Date (YYYY-MM-DD):",
            font=("Segoe UI", 10), bg=COLORS["bg_card"], fg=COLORS["text"]
        ).pack(side="left", padx=(0, 10))

        date_input = tk.Frame(date_row, bg=COLORS["bg_input"],
                              highlightbackground=COLORS["border"], highlightthickness=1)
        date_input.pack(side="left")

        self.date_entry = tk.Entry(
            date_input, textvariable=self.date_var,
            font=("Segoe UI", 12), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", width=14,
            borderwidth=0, justify="center",
        )
        self.date_entry.pack(padx=8, ipady=5)

        time_row = tk.Frame(self.schedule_inputs, bg=COLORS["bg_card"])
        time_row.pack(fill="x", padx=10, pady=5)

        tk.Label(
            time_row, text="⏰ Time (HH:MM 24hr):",
            font=("Segoe UI", 10), bg=COLORS["bg_card"], fg=COLORS["text"]
        ).pack(side="left", padx=(0, 10))

        time_container = tk.Frame(time_row, bg=COLORS["bg_card"])
        time_container.pack(side="left")

        hour_input = tk.Frame(time_container, bg=COLORS["bg_input"],
                              highlightbackground=COLORS["border"], highlightthickness=1)
        hour_input.pack(side="left")
        self.hour_entry = tk.Entry(
            hour_input, textvariable=self.hour_var,
            font=("Segoe UI", 12), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", width=4,
            borderwidth=0, justify="center",
        )
        self.hour_entry.pack(padx=5, ipady=5)

        tk.Label(
            time_container, text=" : ", font=("Segoe UI", 14, "bold"),
            bg=COLORS["bg_card"], fg=COLORS["text"]
        ).pack(side="left")

        min_input = tk.Frame(time_container, bg=COLORS["bg_input"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
        min_input.pack(side="left")
        self.minute_entry = tk.Entry(
            min_input, textvariable=self.minute_var,
            font=("Segoe UI", 12), bg=COLORS["bg_input"], fg=COLORS["text"],
            insertbackground=COLORS["text"], relief="flat", width=4,
            borderwidth=0, justify="center",
        )
        self.minute_entry.pack(padx=5, ipady=5)

        self.countdown_label = tk.Label(
            self.schedule_inputs, text="",
            font=("Segoe UI", 10, "italic"), bg=COLORS["bg_card"], fg=COLORS["accent"]
        )
        self.countdown_label.pack(anchor="w", padx=10, pady=(5, 0))

    def _build_action_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", pady=15)

        self.send_btn = tk.Button(
            btn_frame, text="  ▶  SEND MESSAGES  ",
            font=("Segoe UI", 13, "bold"), bg=COLORS["btn_primary"],
            fg="white", relief="flat", cursor="hand2", padx=20, pady=10,
            activebackground=COLORS["btn_primary_h"], activeforeground="white",
            command=self._on_send,
        )
        self.send_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.stop_btn = tk.Button(
            btn_frame, text="  ⏹  STOP  ",
            font=("Segoe UI", 13, "bold"), bg=COLORS["btn_danger"],
            fg="white", relief="flat", cursor="hand2", padx=20, pady=10,
            activebackground=COLORS["btn_danger_h"], activeforeground="white",
            command=self._on_stop, state="disabled",
        )
        self.stop_btn.pack(side="left", expand=True, fill="x", padx=(5, 0))

    def _build_progress(self, parent):
        card = self._card(parent, "")

        self.status_label = tk.Label(
            card, text="⏸️ Ready",
            font=("Segoe UI", 11, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_dim"]
        )
        self.status_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.progress_frame = tk.Frame(card, bg=COLORS["bg_input"], height=24)
        self.progress_frame.pack(fill="x", padx=10, pady=(0, 5))
        self.progress_frame.pack_propagate(False)

        self.progress_bar = tk.Frame(self.progress_frame, bg=COLORS["green"], width=0, height=24)
        self.progress_bar.pack(side="left", fill="y")

        self.progress_text = tk.Label(
            card, text="0 / 0 messages sent",
            font=("Segoe UI", 10), bg=COLORS["bg_card"], fg=COLORS["text_dim"]
        )
        self.progress_text.pack(anchor="e", padx=10)

    def _build_log(self, parent):
        card = self._card(parent, "📋 Activity Log")

        log_frame = tk.Frame(card, bg=COLORS["bg_input"],
                             highlightbackground=COLORS["border"], highlightthickness=1)
        log_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.log_text = tk.Text(
            log_frame, font=("Cascadia Mono", 10), bg=COLORS["bg_input"],
            fg=COLORS["text_dim"], relief="flat", borderwidth=0,
            height=8, wrap="word", padx=10, pady=8, state="disabled",
        )
        self.log_text.pack(fill="x", expand=True)

        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)

        tk.Button(
            card, text="🗑️ Clear Log", font=("Segoe UI", 9),
            bg=COLORS["bg_card"], fg=COLORS["text_muted"], relief="flat",
            cursor="hand2", borderwidth=0,
            activebackground=COLORS["bg_hover"],
            command=self._clear_log,
        ).pack(anchor="e", padx=10, pady=(0, 5))

        self._log("WhatsApp Automator initialized.")
        if self.desktop_available:
            self._log(f"WhatsApp Desktop detected: {self.whatsapp_path}")
        else:
            self._log("WhatsApp Desktop not found. Using WhatsApp Web.")


    def _card(self, parent, title):
        outer = tk.Frame(parent, bg=COLORS["bg_dark"])
        outer.pack(fill="x", pady=5)

        if title:
            tk.Label(
                outer, text=title, font=("Segoe UI", 12, "bold"),
                bg=COLORS["bg_dark"], fg=COLORS["text"]
            ).pack(anchor="w", padx=5, pady=(5, 3))

        card = tk.Frame(outer, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border"], highlightthickness=1,
                        padx=5, pady=8)
        card.pack(fill="x")

        return card

    def _log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, f"[{timestamp}]  {message}\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.configure(state="disabled")

    def _update_char_count(self, event=None):
        content = self.message_text.get("1.0", tk.END).strip()
        count = len(content)
        self.char_count_label.configure(text=f"{count} characters")

    def _toggle_schedule(self):
        if self.schedule_var.get():
            self.schedule_inputs.pack(fill="x", pady=5)
        else:
            self.schedule_inputs.pack_forget()

    def _update_progress(self, sent, total):
        def _update():
            pct = sent / total if total > 0 else 0
            bar_width = int(pct * (self.progress_frame.winfo_width() or 400))
            self.progress_bar.configure(width=max(bar_width, 0))
            self.progress_text.configure(text=f"{sent} / {total} messages sent")

            if sent >= total:
                self.status_label.configure(text="✅ Completed!", fg=COLORS["green"])
            else:
                self.status_label.configure(text=f"📤 Sending... ({sent}/{total})", fg=COLORS["accent"])

        self.root.after(0, _update)

    def _set_sending_state(self, is_sending):
        self.is_sending = is_sending
        state = "disabled" if is_sending else "normal"

        self.send_btn.configure(state=state)
        self.stop_btn.configure(state="normal" if is_sending else "disabled")
        self.phone_entry.configure(state=state)
        self.count_entry.configure(state=state)
        self.delay_entry.configure(state=state)


    def _validate_inputs(self):
        phone = self.phone_var.get().strip()
        if not phone:
            messagebox.showwarning("Missing Phone", "Please enter a phone number.")
            return None

        clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
        if not clean_phone.isdigit() or len(clean_phone) < 7:
            messagebox.showwarning("Invalid Phone",
                                   "Phone number appears invalid.\n"
                                   "Use format: +91 9876543210")
            return None

        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Missing Message", "Please type a message to send.")
            return None

        try:
            count = int(self.count_var.get())
            if count < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Count", "Number of messages must be a positive integer.")
            return None

        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Delay", "Delay must be a non-negative number.")
            return None

        return phone, message, count, delay

    def _on_send(self):
        result = self._validate_inputs()
        if not result:
            return

        phone, message, count, delay = result
        mode = self.mode_var.get()

        mode_label = "WhatsApp Desktop" if mode == "desktop" else "WhatsApp Web"
        confirm = messagebox.askyesno(
            "Confirm Send",
            f"Send {count} message(s) via {mode_label}?\n\n"
            f"📱 To: +{MessageSender._sanitize_phone(phone)}\n"
            f"💬 Message: {message[:80]}{'...' if len(message) > 80 else ''}\n"
            f"⏱️ Delay: {delay}s between messages"
        )
        if not confirm:
            return

        if self.schedule_var.get():
            self._schedule_send(phone, message, count, delay, mode)
        else:
            self._start_send(phone, message, count, delay, mode)

    def _schedule_send(self, phone, message, count, delay, mode):
        try:
            date_str = self.date_var.get().strip()
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())

            target_dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            target_dt = target_dt.replace(hour=hour, minute=minute, second=0)

            now = datetime.datetime.now()
            if target_dt <= now:
                messagebox.showwarning(
                    "Invalid Schedule",
                    "Scheduled time must be in the future."
                )
                return

            wait_seconds = (target_dt - now).total_seconds()

            self._log(f"📅 Scheduled for {target_dt.strftime('%Y-%m-%d %H:%M')} "
                      f"(in {int(wait_seconds)}s)")
            self.status_label.configure(
                text=f"🕐 Scheduled: {target_dt.strftime('%H:%M on %b %d')}",
                fg=COLORS["orange"]
            )
            self._set_sending_state(True)

            def _wait_and_send():
                remaining = wait_seconds
                while remaining > 0 and not (self.sender and self.sender._stop_flag):
                    mins = int(remaining // 60)
                    secs = int(remaining % 60)
                    self.root.after(0, lambda m=mins, s=secs: self.countdown_label.configure(
                        text=f"⏳ Starting in {m}m {s}s ..."
                    ))
                    time.sleep(1)
                    remaining -= 1

                if not (self.sender and self.sender._stop_flag):
                    self.root.after(0, lambda: self.countdown_label.configure(text=""))
                    self._execute_send(phone, message, count, delay, mode)
                else:
                    self.root.after(0, lambda: self._set_sending_state(False))
                    self.root.after(0, lambda: self.status_label.configure(
                        text="⛔ Schedule cancelled", fg=COLORS["red"]
                    ))

            self.sender = MessageSender(mode=mode, log_callback=lambda m: self.root.after(0, lambda msg=m: self._log(msg)))

            self.sending_thread = threading.Thread(target=_wait_and_send, daemon=True)
            self.sending_thread.start()

        except ValueError as e:
            messagebox.showwarning(
                "Invalid Schedule",
                f"Please check your date/time format.\n"
                f"Date: YYYY-MM-DD, Time: HH (0-23), MM (0-59)\n\n{e}"
            )

    def _start_send(self, phone, message, count, delay, mode):
        self._set_sending_state(True)
        self.status_label.configure(text="📤 Preparing...", fg=COLORS["accent"])
        self._update_progress(0, count)

        self.sending_thread = threading.Thread(
            target=self._execute_send,
            args=(phone, message, count, delay, mode),
            daemon=True,
        )
        self.sending_thread.start()

    def _execute_send(self, phone, message, count, delay, mode):
        self.sender = MessageSender(
            mode=mode,
            log_callback=lambda m: self.root.after(0, lambda msg=m: self._log(msg)),
        )

        self.root.after(0, lambda: self._set_sending_state(True))
        self.root.after(0, lambda: self.status_label.configure(
            text="📤 Sending...", fg=COLORS["accent"]
        ))

        sent = self.sender.send_messages(
            phone, message, count, delay,
            progress_callback=self._update_progress,
        )

        self.root.after(0, lambda: self._set_sending_state(False))

        if sent == count:
            self.root.after(0, lambda: self.status_label.configure(
                text=f"✅ All {count} messages sent!", fg=COLORS["green"]
            ))
        else:
            self.root.after(0, lambda: self.status_label.configure(
                text=f"⚠️ Sent {sent}/{count} messages", fg=COLORS["orange"]
            ))

    def _on_stop(self):
        if self.sender:
            self.sender.stop()
            self._log("⛔ Stop requested — finishing current message...")
            self.status_label.configure(text="⛔ Stopping...", fg=COLORS["red"])



def main():
    root = tk.Tk()

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("TScrollbar",
                    background=COLORS["bg_hover"],
                    troughcolor=COLORS["bg_dark"],
                    borderwidth=0,
                    arrowsize=0)

    app = WhatsAppAutomatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
