#!/usr/bin/env python3
"""
C1PH3R-X :: The Autonomous Cyber-Terminal IDE Engine (v2.1)

A cyberpunk-styled terminal chat client for Google Gemini.

Highlights
    * Live, markdown-rendered streaming (code blocks, lists, tables).
    * Multi-turn memory: the model remembers the conversation.
    * Real git branch detection in the status bar.
    * Slash commands: /help /status /model /clear /reset /save /exit
    * Ctrl+C stops a streaming reply without killing the session.

Setup
    pip install -r requirements.txt
    export GEMINI_API_KEY="your_key"      # GOOGLE_API_KEY also works
    python c1ph3r-x.py
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from google import genai
from google.genai import types
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

VERSION = "2.1"
DEFAULT_MODEL = "gemini-2.5-flash"
EXIT_WORDS = {"/exit", "/quit", "exit", "quit"}

SYSTEM_PROMPT = (
    "You are C1PH3R-X, a sharp, concise command-line coding assistant. "
    "Answers are rendered in a terminal: prefer short paragraphs, fenced code "
    "blocks with a language tag, and brief bullet lists. Skip filler."
)

# One colour per banner row gives a cool top-to-bottom gradient.
BANNER_LINES = [
    r"  ____  _  ____   _   _  _____  ____         __  __",
    r" / ___|/ ||  _ \ | | | ||___ / |  _ \        \ \/ /",
    r"| |    | || |_) || |_| |  |_ \ | |_) | _____  \  / ",
    r"| |___ | ||  __/ |  _  | ___) ||  _ < |_____| /  \ ",
    r" \____||_||_|    |_| |_||____/ |_| \_\       /_/\_\ ",
]
BANNER_COLORS = ["bright_cyan", "cyan", "bright_blue", "blue", "magenta"]

console = Console()


# ─────────────────────────────────────────────────────────────────────────────
# Environment helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_api_key() -> Optional[str]:
    """Return the API key from the environment, if any."""
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def mask_key(key: Optional[str]) -> str:
    """Show only the last 4 characters of a key, e.g. '••••••••x9Z4'."""
    if not key:
        return "NOT SET"
    return "•" * 8 + key[-4:]


def current_dir_name() -> str:
    """Name of the current working directory (or '/' at the filesystem root)."""
    return os.path.basename(os.getcwd()) or "/"


def git_branch() -> str:
    """Return the current git branch, or 'n/a' outside a repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=1.5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "n/a"
    branch = result.stdout.strip()
    return branch if result.returncode == 0 and branch else "n/a"


# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Session:
    """Everything that changes while the app is running."""

    client: Optional[genai.Client]
    model: str = DEFAULT_MODEL
    chat: object = None
    transcript: List[Tuple[str, str]] = field(default_factory=list)  # (role, text)
    started_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        self.new_chat()

    @property
    def turns(self) -> int:
        return sum(1 for role, _ in self.transcript if role == "user")

    def new_chat(self) -> None:
        """Start a fresh conversation (wipes the model's memory)."""
        if self.client is None:
            self.chat = None
            return
        self.chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )


# ─────────────────────────────────────────────────────────────────────────────
# UI: header, status bar, help
# ─────────────────────────────────────────────────────────────────────────────

def build_status_panel(session: Session) -> Panel:
    """One-line status bar: model, directory, git branch, key, turn count."""
    key_ok = session.client is not None
    fields = [
        ("Model", session.model, "cyan"),
        ("Dir", current_dir_name(), "cyan"),
        ("Git", git_branch(), "magenta"),
        ("Key", mask_key(get_api_key()), "green" if key_ok else "bold red"),
        ("Turns", str(session.turns), "cyan"),
    ]
    line = Text()
    for index, (label, value, style) in enumerate(fields):
        if index:
            line.append("  │  ", style="dim")
        line.append(f"{label} ", style="bold yellow")
        line.append(value, style=style)
    return Panel(line, border_style="cyan", title="[dim]SYSTEM[/dim]", title_align="left")


def print_header(session: Session) -> None:
    """Clear the screen and draw the banner + status bar."""
    console.clear()
    for line, color in zip(BANNER_LINES, BANNER_COLORS):
        console.print(Text(line, style=f"bold {color}"))

    subtitle = Text(f":: THE AUTONOMOUS CYBER-TERMINAL IDE ENGINE v{VERSION} ::", style="bold yellow")
    console.print(subtitle)
    console.print(Text("Streaming AI • Live Markdown • Multi-turn Memory", style="dim green"))
    console.print()
    console.print(build_status_panel(session))

    if session.client is None:
        console.print(
            "[bold red]✖ No API key found.[/bold red] "
            "Set one with [green]export GEMINI_API_KEY=your_key[/green] and relaunch.\n"
        )
    else:
        console.print("[green]✔ Link established.[/green] Type a prompt, or [green]/help[/green].\n")


def show_help(session: Session, _arg: str) -> bool:
    table = Table(title="C1PH3R-X Command Deck", border_style="cyan", title_style="bold green")
    table.add_column("Command", style="bold cyan", no_wrap=True)
    table.add_column("What it does")
    table.add_row("<any text>", "Send a prompt to Gemini and stream the reply")
    for name, (_, description) in COMMANDS.items():
        table.add_row(name, description)
    table.add_row("Ctrl+C", "Stop a streaming reply (twice at the prompt to quit)")
    console.print(table)
    console.print()
    return False


# ─────────────────────────────────────────────────────────────────────────────
# Slash commands  (each returns True only if the app should quit)
# ─────────────────────────────────────────────────────────────────────────────

def cmd_status(session: Session, _arg: str) -> bool:
    uptime = int(time.time() - session.started_at)
    console.print(build_status_panel(session))
    console.print(f"[dim]Session uptime: {uptime // 60}m {uptime % 60}s[/dim]\n")
    return False


def cmd_model(session: Session, arg: str) -> bool:
    if not arg:
        console.print(f"Current model: [bold cyan]{session.model}[/bold cyan]")
        console.print("[dim]Switch with: /model <model-name>  (this resets the conversation)[/dim]\n")
        return False
    session.model = arg
    session.new_chat()
    session.transcript.clear()
    console.print(f"[green]✔ Model switched to[/green] [bold cyan]{arg}[/bold cyan] [dim](memory reset)[/dim]\n")
    return False


def cmd_clear(session: Session, _arg: str) -> bool:
    print_header(session)
    return False


def cmd_reset(session: Session, _arg: str) -> bool:
    session.new_chat()
    session.transcript.clear()
    console.print("[green]✔ Memory wiped. Fresh conversation started.[/green]\n")
    return False


def cmd_save(session: Session, _arg: str) -> bool:
    if not session.transcript:
        console.print("[yellow]Nothing to save yet.[/yellow]\n")
        return False
    path = Path.cwd() / f"c1ph3r-x-session-{datetime.now():%Y%m%d-%H%M%S}.md"
    lines = [f"# C1PH3R-X session ({session.model})", ""]
    for role, text in session.transcript:
        heading = "## 🧑 You" if role == "user" else "## 🤖 Gemini"
        lines += [heading, "", text, ""]
    try:
        path.write_text("\n".join(lines), encoding="utf-8")
    except OSError as error:
        console.print(f"[bold red]Could not save transcript:[/bold red] {error}\n")
        return False
    console.print(f"[green]✔ Transcript saved to[/green] [cyan]{path.name}[/cyan]\n")
    return False


def cmd_exit(_session: Session, _arg: str) -> bool:
    console.print("[bold yellow]Disconnecting from the grid... Goodbye![/bold yellow]")
    return True


# name -> (handler, description)
COMMANDS: Dict[str, Tuple[Callable[[Session, str], bool], str]] = {
    "/help": (show_help, "Show this command deck"),
    "/status": (cmd_status, "Show model, directory, git branch, key and turns"),
    "/model": (cmd_model, "Show or switch the model (resets memory)"),
    "/clear": (cmd_clear, "Redraw the screen (keeps memory)"),
    "/reset": (cmd_reset, "Wipe conversation memory"),
    "/save": (cmd_save, "Save the transcript to a Markdown file"),
    "/exit": (cmd_exit, "Quit C1PH3R-X"),
}


def handle_command(session: Session, raw: str) -> bool:
    """Dispatch a slash command. Returns True if the app should quit."""
    name, _, arg = raw.partition(" ")
    entry = COMMANDS.get(name.lower())
    if entry is None:
        console.print(f"[bold red]Unknown command:[/bold red] {name}  [dim](try /help)[/dim]\n")
        return False
    handler, _ = entry
    return handler(session, arg.strip())


# ─────────────────────────────────────────────────────────────────────────────
# Talking to Gemini
# ─────────────────────────────────────────────────────────────────────────────

def stream_reply(session: Session, prompt: str) -> None:
    """Send a prompt and render the reply live as markdown."""
    buffer = ""
    interrupted = False
    started = time.perf_counter()
    first_token_at: Optional[float] = None

    def view(body):
        return Panel(body, title="[bold green]◆ GEMINI[/bold green]", title_align="left", border_style="green")

    try:
        with Live(
            view(Spinner("dots", text="Decrypting response...", style="cyan")),
            console=console,
            refresh_per_second=12,
            vertical_overflow="visible",
        ) as live:
            for chunk in session.chat.send_message_stream(prompt):
                piece = chunk.text or ""  # some chunks carry no text
                if not piece:
                    continue
                if first_token_at is None:
                    first_token_at = time.perf_counter() - started
                buffer += piece
                live.update(view(Markdown(buffer)))
    except KeyboardInterrupt:
        interrupted = True
    except Exception as error:  # network, quota, invalid key, ...
        console.print(Panel(str(error), title="[bold red]API ERROR[/bold red]", border_style="red"))
        console.print("[dim]Tip: check your key, quota and connection, then try again.[/dim]\n")
        return

    if buffer:
        session.transcript.append(("user", prompt))
        session.transcript.append(("model", buffer))

    elapsed = time.perf_counter() - started
    stats = f"⏱ {elapsed:.1f}s"
    if first_token_at is not None:
        stats += f" · first token {first_token_at:.1f}s"
    stats += f" · {len(buffer.split())} words"
    if interrupted:
        stats += " · [yellow]interrupted[/yellow]"
    console.print(f"[dim]{stats}[/dim]\n")


# ─────────────────────────────────────────────────────────────────────────────
# Main loop
# ─────────────────────────────────────────────────────────────────────────────

def create_client() -> Optional[genai.Client]:
    """Build the Gemini client, or return None if no key / init fails."""
    api_key = get_api_key()
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception as error:
        console.print(f"[bold red]Failed to initialise Gemini client:[/bold red] {error}")
        return None


def main() -> int:
    session = Session(client=create_client())
    print_header(session)

    prompt_label = "[bold cyan]c1ph3r-x[/bold cyan] [magenta]❯[/magenta] "
    pending_interrupt = False  # first Ctrl+C warns, second quits

    while True:
        try:
            user_input = console.input(prompt_label).strip()
            pending_interrupt = False
        except KeyboardInterrupt:
            if pending_interrupt:
                console.print("\n[bold yellow]Session terminated.[/bold yellow]")
                return 0
            pending_interrupt = True
            console.print("\n[dim]Press Ctrl+C again (or type /exit) to quit.[/dim]")
            continue
        except EOFError:
            console.print("\n[bold yellow]Session terminated.[/bold yellow]")
            return 0

        if not user_input:
            continue

        if user_input.lower() in EXIT_WORDS:
            cmd_exit(session, "")
            return 0

        if user_input.startswith("/"):
            if handle_command(session, user_input):
                return 0
            continue

        if session.client is None:
            console.print(
                "[bold red]Error:[/bold red] no API key set. "
                "Run [green]export GEMINI_API_KEY=your_key[/green] and relaunch.\n"
            )
            continue

        stream_reply(session, user_input)


if __name__ == "__main__":
    sys.exit(main())
