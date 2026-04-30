import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from orchestrator.controller import InterviewController

console = Console()

def main():
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    console.print(Panel.fit("[bold magenta]Mock Interview AI[/bold magenta]", border_style="magenta"))
    
    if not api_key:
        console.print("[bold red]Error: GROQ_API_KEY not found.[/bold red]")
        console.print("Please set it in your .env file.")
        sys.exit(1)
        
    console.print("\n[bold cyan]Interview Configuration:[/bold cyan]")
    role = console.input("Target Role (e.g., Senior SWE): ")
    background = console.input("Background (Optional): ")
    focus_area = console.input("Focus Area (e.g., System Design): ")
    
    turns_str = console.input("Number of questions/turns (default 5): ")
    try:
        turns = int(turns_str) if turns_str.strip() else 5
    except ValueError:
        turns = 5
        
    controller = InterviewController(
        api_key=api_key,
        role=role,
        background=background,
        focus_area=focus_area,
        max_turns=turns
    )
    
    try:
        controller.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Interview interrupted by user. Exiting...[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred: {str(e)}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
