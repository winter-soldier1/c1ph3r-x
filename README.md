# C1PH3R-X 🚀

> **THE AUTONOMOUS CYBER-TERMINAL IDE ENGINE v2.0**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)
![Model](https://img.shields.io/badge/model-Gemini%202.5%20Flash-orange)

C1PH3R-X is an agentic, cyber-styled terminal IDE engine written in Python. It uses [Rich](https://github.com/Textualize/rich) for high-performance terminal rendering and the official [Google GenAI SDK](https://github.com/googleapis/python-genai) to stream AI responses directly inside your native shell. It is built for command-line power users, system administrators, and developers who want an intelligent assistant without ever leaving the terminal.

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [How It Works](#-how-it-works)
4. [Prerequisites](#-prerequisites)
5. [Installation & Setup](#-installation--setup)
6. [Configuration](#-configuration)
7. [Usage & Commands](#-usage--commands)
8. [Example Session](#-example-session)
9. [Troubleshooting](#-troubleshooting)
10. [Security Best Practices](#-security-best-practices)
11. [Project Structure](#-project-structure)
12. [FAQ](#-faq)
13. [Roadmap](#-roadmap)
14. [Contributing](#-contributing)
15. [License](#-license)

---

## 🔭 Overview

Most AI tooling lives in browser tabs or heavyweight editors. C1PH3R-X takes a different approach: it turns the terminal you already have open into an interactive AI workspace. You type a question, paste a code snippet, or describe a problem, and the response streams back token by token, rendered in a styled cyberpunk interface.

**Design goals**

- **Stay in the shell.** No context switching between browser, editor, and terminal.
- **Fast feedback.** Streaming output means you start reading the answer immediately.
- **Minimal setup.** One dependency install, one environment variable, one command to launch.
- **Portable.** The same experience on Linux, macOS, and Windows.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Cyberpunk Terminal UI** | Styled ASCII banner, a dynamic working-directory status bar, and color-coded environment status indicators powered by `rich`. |
| **Gemini 2.5 Flash Streaming** | Low-latency, real-time AI response streaming directly to standard output. |
| **Environment Autodetect** | On launch, C1PH3R-X checks whether `GEMINI_API_KEY` is set and reports its status in the interface. |
| **Interactive System Commands** | Built-in `/help` menu and `/exit` session control. |
| **Cross-Platform** | Supports Linux, macOS, and Windows (Command Prompt, PowerShell, and WSL). |
| **Lightweight Footprint** | Only two runtime dependencies: `google-genai` and `rich`. |

---

## ⚙️ How It Works

At a high level, each session follows this lifecycle:

```
 ┌──────────────┐     ┌────────────────────┐     ┌──────────────────┐
 │  Launch app  │ ──► │ Render banner +    │ ──► │ Check for        │
 │              │     │ status bar (Rich)  │     │ GEMINI_API_KEY   │
 └──────────────┘     └────────────────────┘     └────────┬─────────┘
                                                          │
                                                          ▼
 ┌──────────────┐     ┌────────────────────┐     ┌──────────────────┐
 │ Stream reply │ ◄── │ Send prompt to     │ ◄── │ Read user input  │
 │ to terminal  │     │ Gemini 2.5 Flash   │     │ (prompt/command) │
 └──────┬───────┘     └────────────────────┘     └──────────────────┘
        │
        └──────────────► loop until /exit or Ctrl+C
```

1. **Startup**: the ASCII banner and status bar are rendered with Rich. The status bar shows the current working directory and whether an API key was detected.
2. **Input loop**: the shell waits for input. Anything beginning with `/` is treated as a system command; everything else is treated as a prompt.
3. **Streaming**: prompts are sent to Gemini 2.5 Flash through the Google GenAI SDK, and response chunks are printed as they arrive.
4. **Shutdown**: `/exit`, `exit`, or `Ctrl + C` ends the session cleanly.

---

## 📋 Prerequisites

Before installing C1PH3R-X, make sure your environment meets the requirements below.

### 1. Python

C1PH3R-X is a Python application. Python **3.10 or newer** is recommended, since recent releases of the `google-genai` SDK may no longer support older interpreters. The project's minimum supported version is **3.8**, but if installation fails on an older interpreter, upgrade Python first.

Check your version:

```bash
python3 --version
# On Windows:
python --version
```

Install or upgrade Python:

- **Linux (Ubuntu/Debian)**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip -y
  ```
- **macOS (Homebrew)**
  ```bash
  brew install python
  ```
- **Windows**: download the latest 64-bit installer from [python.org](https://www.python.org/downloads/). Tick **"Add Python to PATH"** during installation.

### 2. Git

Git is needed to clone the repository and pull updates.

```bash
git --version
```

- **Linux (Ubuntu/Debian)**: `sudo apt install git -y`
- **macOS**: `brew install git` or `xcode-select --install`
- **Windows**: download from [git-scm.com](https://git-scm.com/downloads).

### 3. Google Gemini API Key

C1PH3R-X talks to Google's models through the Gemini API, so you need a key.

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Sign in with your Google account.
3. Click **Get API key** and create a key for your project.
4. Copy the key and store it somewhere safe. **Never commit it to source control.**

### 4. Terminal Recommendations

For the best visual experience:

- Use a terminal with **truecolor (24-bit) and Unicode support**: Windows Terminal, iTerm2, GNOME Terminal, Alacritty, Kitty, WezTerm, etc.
- Use a **monospaced font** with good box-drawing glyph coverage (e.g., JetBrains Mono, Fira Code, Cascadia Code).
- Legacy consoles (older `cmd.exe` windows) may render colors and symbols imperfectly. Prefer Windows Terminal or WSL.

---

## 🛠️ Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/c1ph3r-x.git
cd c1ph3r-x
```

### Step 2: Create and Activate a Virtual Environment

A virtual environment keeps C1PH3R-X's dependencies isolated from your system Python and avoids version conflicts.

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt)**

```bat
python -m venv venv
.\venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If PowerShell blocks the activation script, run this once and try again:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

**Verify:** your prompt should now start with `(venv)`.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Core dependencies**

| Package | Purpose |
|---|---|
| `google-genai` | Official Google GenAI Python client used for model streaming and API connectivity. |
| `rich` | Terminal formatting engine for the banner, status bar, colors, and styled output. |

Verify the install:

```bash
pip list | grep -i -E "google-genai|rich"
# Windows PowerShell:
pip list | Select-String "google-genai|rich"
```

### Step 4: Set Your API Key

C1PH3R-X reads the key from the `GEMINI_API_KEY` environment variable at startup.

#### 🐧 Linux / 🍎 macOS

Current session only:

```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

Persistent (Bash):

```bash
echo 'export GEMINI_API_KEY="your_actual_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

Persistent (Zsh, the macOS default):

```bash
echo 'export GEMINI_API_KEY="your_actual_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

#### 🪟 Windows

Command Prompt (current session; **no quotes**, or they become part of the value):

```bat
set GEMINI_API_KEY=your_actual_api_key_here
```

PowerShell (current session):

```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

Persistent (user-level; open a **new** terminal afterward):

```bat
setx GEMINI_API_KEY "your_actual_api_key_here"
```

Confirm the variable is visible (without printing the whole key):

```bash
# Linux / macOS
[ -n "$GEMINI_API_KEY" ] && echo "Key is set" || echo "Key is NOT set"
```

```powershell
# PowerShell
if ($env:GEMINI_API_KEY) { "Key is set" } else { "Key is NOT set" }
```

### Step 5: Launch

```bash
python c1ph3r-x.py
```

On startup you should see the ASCII banner, the working-directory status bar, and an indicator showing whether your API key was detected.

---

## 🔧 Configuration

C1PH3R-X is intentionally configuration-light.

| Setting | Where | Default | Notes |
|---|---|---|---|
| `GEMINI_API_KEY` | Environment variable | *(none)* | **Required.** Authenticates requests to the Gemini API. |
| Model | Source (`c1ph3r-x.py`) | `gemini-2.5-flash` | Change the model name in the script to try other Gemini models. |
| Working directory | Shell | Current directory | The status bar reflects wherever you launched the app. |

**Tip:** launch C1PH3R-X from inside the project folder you are working on, so the status bar shows the correct context.

---

## 🚀 Usage & Commands

Once inside the C1PH3R-X shell, type a prompt and press **Enter**.

| Input | Description |
|---|---|
| *any text* | Sends your prompt to Gemini 2.5 Flash and streams the response to the terminal. |
| `/help` | Shows system status, active settings, and available commands. |
| `/exit` or `exit` | Gracefully ends the session. |
| `Ctrl + C` | Interrupts a streaming response, or closes the shell. |

### Things you can ask

- **Explain code:** *"Explain what this regex does: `^(?=.*[A-Z])(?=.*\d).{8,}$`"*
- **Debug errors:** paste a stack trace and ask for likely causes.
- **Generate snippets:** *"Write a Bash one-liner to find the 10 largest files under the current directory."*
- **Review & refactor:** paste a function and ask for improvements.
- **Learn tooling:** *"How do I rebase my branch onto main interactively?"*
- **Write docs:** ask for docstrings, commit messages, or README sections.

### Writing effective prompts

- **Be specific.** Include language, framework, and version.
- **Provide context.** Paste the relevant snippet and the exact error message.
- **State the goal.** "I want X to do Y" beats "this doesn't work".
- **Ask for format.** "Answer in a numbered list" or "show only the diff".

---

## 💻 Example Session

```text
╔═══════════════════════════════╗
║          C1PH3R-X  v2.0       ║
╚═══════════════════════════════╝
 📂 /home/user/projects/demo        🔑 GEMINI_API_KEY: DETECTED

c1ph3r-x ❯ how do I undo my last git commit but keep my changes?

You can use a soft reset:

    git reset --soft HEAD~1

This moves HEAD back one commit while leaving your changes staged...

c1ph3r-x ❯ /exit
Session closed. Goodbye.
```

*(Illustrative only; exact styling depends on your terminal and the current build.)*

---

## ⚡ Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `GEMINI_API_KEY NOT SET` | The variable is not visible to the shell that launched the app. | Re-export the key in the **same terminal** (or open a new one after `setx`), then relaunch. |
| `ModuleNotFoundError: No module named 'google'` | Dependencies were not installed in the active environment. | Activate the venv (look for `(venv)`), then run `pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'rich'` | Same as above. | Same fix. |
| `API_KEY_INVALID` / `403 Forbidden` | Key is wrong, revoked, restricted, or has stray quotes/whitespace. | Generate a new key in Google AI Studio and re-export it. On Windows CMD, don't wrap the value in quotes. |
| `429 Too Many Requests` / quota errors | You hit the free-tier rate or daily limit. | Wait and retry, reduce request frequency, or check your quota and billing in Google AI Studio. |
| `externally-managed-environment` | Your OS blocks global `pip` installs. | Use a virtual environment as shown in Step 2. |
| `python: command not found` | Python is missing or not on `PATH`. | Install Python; on Linux/macOS use `python3`; on Windows reinstall with **Add to PATH** ticked. |
| Garbled boxes or missing colors | Terminal lacks Unicode/truecolor support. | Switch to a modern terminal and a font with box-drawing glyphs. |
| Streaming hangs or times out | Network, proxy, or firewall interference. | Check your connection, VPN, and proxy settings; retry. |
| PowerShell won't activate venv | Execution policy blocks scripts. | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |

**Still stuck?** Open an issue and include your OS, Python version (`python --version`), the full error output, and the steps to reproduce. **Remove your API key from anything you paste.**

---

## 🔐 Security Best Practices

- **Never hard-code or commit your API key.** The provided `.gitignore` helps, but double-check before every push.
- **Rotate keys immediately** if one is ever exposed. Revoke it in Google AI Studio and create a new one.
- **Restrict your key** where the console allows it.
- **Mind what you paste.** Prompts are sent to Google's API. Do not paste passwords, private keys, customer data, or proprietary code you are not permitted to share.
- **Review generated commands before running them.** AI output can be wrong or destructive (e.g., `rm -rf`). Treat suggestions as drafts, not instructions.
- **Keep dependencies updated:** `pip install --upgrade google-genai rich`

---

## 📦 Project Structure

```text
c1ph3r-x/
│
├── c1ph3r-x.py         # Main entry point: ASCII UI renderer & API streaming integration
├── requirements.txt    # Dependencies (google-genai, rich)
├── LICENSE             # MIT License
├── .gitignore          # Exclusions for venvs, caches, and secrets
└── README.md           # Documentation and deployment guide
```

---

## ❓ FAQ

**Is C1PH3R-X free?**
The software is MIT-licensed and free. Usage of the Gemini API is governed by Google's pricing and quota terms for your key.

**Which model does it use?**
Gemini 2.5 Flash by default, chosen for speed and low latency.

**Does it remember previous messages?**
Check the current build of `c1ph3r-x.py`. If you need multi-turn memory, the GenAI SDK supports chat sessions, which can be wired into the input loop (see the roadmap).

**Does it execute commands on my machine?**
Out of the box it streams text responses only. Run any suggested commands yourself, after reviewing them.

**Can I use it offline?**
No. It requires an internet connection to reach the Gemini API.

**Can I use a different model?**
Yes. Edit the model name in the script to any Gemini model your key can access.

**Does it work over SSH or inside tmux/screen?**
Yes, as long as the terminal supports the colors and Unicode you want to display.

---

## 🗺️ Roadmap

Ideas under consideration (not yet implemented):

- [ ] Multi-turn conversation memory using SDK chat sessions
- [ ] Persistent configuration file (model, theme, defaults)
- [ ] `.env` file support for API key loading
- [ ] Markdown and syntax-highlighted rendering of streamed code blocks
- [ ] Session transcript export (`/save`)
- [ ] Context injection from local files (`/file <path>`)
- [ ] Selectable themes and color palettes
- [ ] Optional confirmed command execution mode

Have an idea? Open an issue and tell us about it.

---

## 🤝 Contributing

Contributions are welcome, whether they are bug fixes, features, documentation, or UI polish.

1. **Fork** the repository on GitHub.
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/NewAwesomeFeature
   ```
3. **Make your changes**, keeping code readable and consistent with the existing style.
4. **Test locally** on at least one platform, and note which one in your PR.
5. **Commit:**
   ```bash
   git commit -m "Add NewAwesomeFeature"
   ```
6. **Push:**
   ```bash
   git push origin feature/NewAwesomeFeature
   ```
7. **Open a Pull Request** describing what changed and why, with screenshots for UI changes.

**Guidelines**

- Keep pull requests focused: one change per PR.
- Never include API keys or personal data in commits, issues, or screenshots.
- Update this README if your change affects setup or usage.

---

## 📄 License

Distributed under the **MIT License**. Copyright © 2026 C1PH3R-X. See [`LICENSE`](LICENSE) for full terms.

---

<p align="center"><b>C1PH3R-X</b> — jack in, stay in the shell. ⚡</p>
