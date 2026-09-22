# 💬 Unofficial WhatsApp message sender

A sleek, feature-rich desktop application that automates sending bulk messages on WhatsApp. Built with Python and Tkinter, it provides a modern dark-themed GUI with support for WhatsApp Desktop and WhatsApp Web, emoji insertion, message scheduling, and real-time progress tracking.

---

## 🔍 About the Project

**WhatsApp Bulk Message Sender** is a Python-based GUI automation tool that allows users to send a specified number of messages to any WhatsApp contact — either through the **WhatsApp Desktop app** or **WhatsApp Web**. The tool leverages GUI automation (`pyautogui`) and clipboard management (`pyperclip`) to type and send messages programmatically.

The application auto-detects whether WhatsApp Desktop is installed on your Windows machine. If found, it uses the native desktop app for faster performance; otherwise, it falls back to WhatsApp Web in your default browser.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Dual Mode Support** | Automatically detects WhatsApp Desktop; falls back to WhatsApp Web |
| **Bulk Messaging** | Send any number of messages (1 to N) to a single contact |
| **Built-in Emoji Picker** | Categorized emoji panel (Smileys, Gestures, Hearts, Objects, Food, Travel, Symbols, Pets) with click-to-insert |
| **Message Scheduling** | Schedule messages for a specific date and time with a live countdown timer |
| **Configurable Delay** | Set custom delay (in seconds) between consecutive messages |
| **Real-time Progress Tracking** | Visual progress bar + live status updates in the activity log |
| **Input Validation** | Validates phone number format, message content, message count, and delay values |
| **Stop Anytime** | Gracefully stop sending mid-way with the Stop button |
| **Auto Dependency Install** | Automatically installs missing `pyautogui` and `pyperclip` on first run |
| **Modern Dark UI** | GitHub-inspired dark theme with styled cards, smooth layout, and emoji support |
| **Scrollable Interface** | Full mousewheel-scrollable UI that adapts to window resizing |
| **Activity Log** | Timestamped log of every action with a clear-log option |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core programming language |
| **Tkinter / ttk** | GUI framework (built into Python) |
| **pyautogui** | GUI automation — simulates keyboard input |
| **pyperclip** | Clipboard management — handles emoji and special characters |
| **threading** | Non-blocking message sending in background threads |
| **subprocess** | WhatsApp Desktop detection and dependency installation |
| **webbrowser** | Opens WhatsApp Web URLs |

---

## 📋 Prerequisites

- **Operating System:** Windows (the app uses Windows-specific paths and commands like `tasklist`, `os.startfile`, and PowerShell for WhatsApp detection)
- **Python:** Version 3.7 or higher
- **WhatsApp:** Either WhatsApp Desktop installed **or** WhatsApp Web logged in on your default browser
- **Internet Connection:** Required for WhatsApp Web mode

---

## 📥 Installation & Setup

### 1. Clone or Download the Repository

```bash
git clone https://github.com/Abhinavaa-S-Kumar/unofficial_automated_whatsapp_message_sender.git
cd unofficial_automated_whatsapp_message_sender
```

Or simply download the `whats.py` file directly.

### 2. Install Python

Make sure Python 3.7+ is installed. You can download it from [python.org](https://www.python.org/downloads/).

Verify your installation:

```bash
python --version
```

### 3. Install Dependencies

The application **automatically installs** missing dependencies on first run. However, if you prefer to install them manually:

```bash
pip install pyautogui pyperclip
```

---

## 🚀 How to Run

### Option 1: Run from Terminal

```bash
python whats.py
```

### Option 2: Double-click

Simply double-click `whats.py` in your file explorer (if Python is associated with `.py` files).

### What Happens on Launch

1. The app checks for `pyautogui` and `pyperclip` — installs them if missing.
2. It scans common install locations and Windows Store for WhatsApp Desktop.
3. The GUI window launches with the detected mode pre-selected.

---

## 📘 Usage Guide

### Step-by-Step

1. **Select Connection Mode**
   - **Desktop App** — uses `whatsapp://` URL scheme (faster, requires WhatsApp Desktop)
   - **WhatsApp Web** — opens `web.whatsapp.com` in your browser (requires being logged in)

2. **Enter Phone Number**
   - Include the country code (e.g., `+91 9876543210`).
   - If you enter a 10-digit number without a country code, it defaults to India (`+91`).

3. **Type Your Message**
   - Type freely in the message box — emojis and special characters are fully supported.
   - Use the **emoji picker** to browse and insert emojis by category.

4. **Configure Settings**
   - **Number of Messages:** How many copies of the message to send (default: 1).
   - **Delay Between Messages:** Seconds to wait between each send (default: 2s).

5. **Schedule (Optional)**
   - Check "Schedule messages for later".
   - Set a future date (`YYYY-MM-DD`) and time (`HH:MM` in 24-hour format).
   - A live countdown is displayed until the scheduled time arrives.

6. **Send**
   - Click **▶ SEND MESSAGES**.
   - Confirm in the dialog that appears.
   - **Do not touch your mouse or keyboard** while messages are being sent — the app controls your input.

7. **Stop**
   - Click **⏹ STOP** anytime to gracefully halt after the current message.

---

## 🏗️ Project Architecture

```
whats.py (single-file application)
│
├── Dependency Management
│   ├── install_package()        — Installs a pip package silently
│   └── ensure_dependencies()    — Checks and installs pyautogui & pyperclip
│
├── WhatsApp Detection
│   └── detect_whatsapp_desktop() — Scans filesystem, Windows Store, and running processes
│
├── MessageSender (Engine)
│   ├── open_chat()              — Opens a WhatsApp chat via URL scheme or web
│   ├── send_messages()          — Main send loop with progress callbacks
│   ├── _type_and_send()         — Clipboard paste + Enter to send
│   └── _sanitize_phone()        — Cleans and normalizes phone numbers
│
├── Emoji Data
│   └── EMOJI_CATEGORIES         — Dict of categorized emoji lists (8 categories)
│
├── Theme / Colors
│   └── COLORS                   — GitHub-inspired dark theme color palette
│
├── WhatsAppAutomatorApp (GUI)
│   ├── UI Construction
│   │   ├── _build_header()          — App title and subtitle
│   │   ├── _build_mode_selector()   — Desktop/Web radio buttons
│   │   ├── _build_phone_input()     — Phone number entry with prefix
│   │   ├── _build_message_input()   — Message textarea with char count
│   │   ├── _build_emoji_picker()    — Collapsible categorized emoji panel
│   │   ├── _build_settings()        — Message count and delay inputs
│   │   ├── _build_schedule()        — Date/time picker with countdown
│   │   ├── _build_action_buttons()  — Send and Stop buttons
│   │   ├── _build_progress()        — Progress bar and status label
│   │   └── _build_log()             — Scrollable activity log
│   │
│   ├── Helpers
│   │   ├── _card()                  — Reusable styled card component
│   │   ├── _log()                   — Timestamped log appender
│   │   └── _update_progress()       — Thread-safe progress updater
│   │
│   └── Actions
│       ├── _validate_inputs()       — Full input validation
│       ├── _on_send()               — Send button handler
│       ├── _schedule_send()         — Scheduling with countdown
│       ├── _start_send()            — Immediate send trigger
│       ├── _execute_send()          — Worker thread send logic
│       └── _on_stop()               — Graceful stop handler
│
└── Entry Point
    └── main()                   — Initializes Tk root, applies theme, runs app
```

---

## ⚙️ Configuration

The following defaults can be modified directly in the source code:

| Setting | Default | Location |
|---|---|---|
| Default country code | `91` (India) | `_sanitize_phone()` method |
| PyAutoGUI fail-safe | `True` (move mouse to corner to abort) | Line 65 |
| PyAutoGUI pause | `0.3s` between actions | Line 66 |
| Chat load wait (Desktop) | `5s` | `open_chat()` method |
| Chat load wait (Web) | `10s` | `open_chat()` method |
| Window size | `680×920` | `__init__()` of `WhatsAppAutomatorApp` |
| Color theme | GitHub dark theme | `COLORS` dictionary |

---

## ⚠️ Known Limitations

- **Windows Only** — WhatsApp detection uses Windows-specific paths, `tasklist`, `os.startfile()`, and PowerShell commands.
- **Single Contact per Session** — Currently sends to one phone number at a time. No contact list or group support.
- **No Contact Name Lookup** — Despite the docstring mentioning "name or phone number", the app only supports phone numbers.
- **GUI Automation Fragility** — Since it relies on `pyautogui` (keyboard simulation), any mouse/keyboard interaction during sending will disrupt the process.
- **No WhatsApp API** — This tool does not use the official WhatsApp Business API; it automates the UI instead.
- **No Message Templates** — Each session requires manually typing the message.
- **No Attachment Support** — Only text messages (with emojis) can be sent. No images, videos, or documents.

---

## 🔮 Future Improvements

### High Priority

- [ ] **Cross-Platform Support** — Extend detection and automation logic to work on macOS and Linux.
- [ ] **Contact List / CSV Import** — Allow sending the same message to multiple contacts from a CSV or text file.
- [ ] **Group Messaging** — Support sending messages to WhatsApp groups by group name.
- [ ] **Message Templates** — Save and load reusable message templates for quick access.
- [ ] **Attachment Support** — Enable sending images, documents, and media files alongside text.

### Medium Priority

- [ ] **WhatsApp Business API Integration** — Use the official API for more reliable, scalable, and ToS-compliant messaging.
- [ ] **Contact Name Search** — Allow searching contacts by name instead of requiring phone numbers.
- [ ] **Message Personalization** — Support variables/placeholders (e.g., `Hello {name}!`) for personalized bulk messages.
- [ ] **Delivery Confirmation** — Implement image recognition or pixel detection to verify message delivery status (sent/delivered/read).
- [ ] **Retry on Failure** — Automatically retry failed messages with configurable retry count.

### Low Priority / Nice to Have

- [ ] **Multi-language UI** — Support for multiple interface languages.
- [ ] **Dark/Light Theme Toggle** — Let users switch between dark and light themes.
- [ ] **System Tray Support** — Minimize to system tray during scheduled sends.
- [ ] **Send History & Logging** — Persist a log of all sent messages to a file (CSV/JSON) for record-keeping.
- [ ] **Custom Emoji Upload** — Allow users to add custom emojis or stickers.
- [ ] **Rate Limiting / Anti-Ban Measures** — Add randomized delays and human-like typing patterns to reduce the risk of being flagged.
- [ ] **Notification on Completion** — Desktop notification or sound alert when all messages are sent.
- [ ] **Config File** — Externalize settings (default country code, delays, theme) into a JSON/YAML config file.
- [ ] **Packaging** — Bundle as a standalone `.exe` using PyInstaller for easy distribution without requiring a Python installation.

---

## 🎯 Purpose of This Project

> **This project was built purely for fun, learning, and experimentation.**

The sole purpose of this project is to serve as a **personal learning exercise and a fun automation experiment**. It was created to explore:

- **GUI Development with Tkinter** — Building a polished, modern-looking desktop application using Python's built-in GUI toolkit.
- **Desktop Automation** — Understanding how tools like `pyautogui` and `pyperclip` can be used to simulate human interaction with desktop applications.
- **Threading in Python** — Managing background tasks, progress updates, and responsive UIs using `threading` and Tkinter's `after()` method.
- **System Integration on Windows** — Detecting installed applications, interacting with the Windows Store, and launching system-level URL schemes.

**⚠️ Disclaimer:** This tool is **not intended** for spamming, harassment, or any form of unsolicited bulk messaging. Sending large volumes of automated messages may violate [WhatsApp's Terms of Service](https://www.whatsapp.com/legal/terms-of-service) and could result in your account being banned. Use responsibly and only with the recipient's consent. The creator holds no responsibility for any misuse of this tool.

---

<p align="center">
  Made with ❤️ for fun and learning
</p>
