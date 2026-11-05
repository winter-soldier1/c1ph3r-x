import os
import sys
import shutil
from google import genai
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

BANNER = r"""
  ____  __ ____  _   _________  ___     _  __
 / ___|/ /|  _ \| | | |___ /  \/  |   | |/ /
| |   / / | |_) | |_| | |_ \  \/| |___| ' / 
| |__/ /  |  __/|  _  |___) |   | |___| . \ 
 \____/   |_|   |_| |_|____/    |_|   |_|\_\
"""

def print_header():
    console.clear()
    
    # Render ASCII banner
    banner_text = Text(BANNER, style="bold cyan")
    console.print(banner_text)
    
    # Subtitle
    subtitle = Text(":: THE AUTONOMOUS CYBER-TERMINAL IDE ENGINE v2.0 ::\n", style="bold yellow")
    subtitle.append("Linux-Native Agentic Coding • Realtime Tool Orchestration", style="dim green")
    console.print(subtitle)
    console.print()

    # System status bar
    current_dir = os.path.basename(os.getcwd()) or "/"
    api_key = os.environ.get("GEMINI_API_KEY")
    key_status = "[bold green]GEMINI_API_KEY[/bold green]" if api_key else "[bold red]NOT SET[/bold red]"
    
    status_msg = f"[bold yellow]Model:[/bold yellow] gemini-2.5-flash • [bold yellow]Dir:[/bold yellow] [cyan]{current_dir}[/cyan] • [bold yellow]Git:[/bold yellow] n/a • [bold yellow]Type[/bold yellow] [green]/help[/green] or [magenta]/exit[/magenta]"
    console.print(Panel(status_msg, border_style="cyan", expand=True))
    
    console.print(f"✔ Active Keys: {key_status}\n")

def main():
    print_header()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = None
    if api_key:
        try:
            client = genai.Client()
        except Exception as e:
            console.print(f"[bold red]Failed to initialize Gemini Client: {e}[/bold red]")

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]c1ph3r-x[/bold cyan] ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["/exit", "exit", "quit"]:
                console.print("[bold yellow]Exiting C1PH3R-X... Goodbye![/bold yellow]")
                break

            if user_input.lower() == "/help":
                console.print("\n[bold green]C1PH3R-X v2.0 Help Menu[/bold green]")
                console.print(" • [cyan]Type any prompt[/cyan] to send a request to Gemini AI.")
                console.print(" • [cyan]/exit[/cyan] - Terminate the session.")
                console.print(" • [cyan]/help[/cyan] - Display this help message.\n")
                continue

            if not client:
                console.print("[bold red]Error:[/bold red] GEMINI_API_KEY is not set in environment. Set it using 'export GEMINI_API_KEY=your_key'\n")
                continue

            # Call Gemini stream
            console.print("[dim cyan]Streaming response...[/dim cyan]")
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-2.5-flash",
                    contents=user_input
                )
                
                console.print("\n[bold green]AI Response:[/bold green]")
                for chunk in response_stream:
                    console.print(chunk.text, end="")
                console.print("\n")
            except Exception as e:
                console.print(f"\n[bold red]API Error:[/bold red] {e}\n")

        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold yellow]Session terminated.[/bold yellow]")
            break

if __name__ == "__main__":
    main()
