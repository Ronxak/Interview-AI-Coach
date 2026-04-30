from openai import OpenAI
from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.coach import CoachAgent
from utils.memory import Memory
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

class InterviewController:
    def __init__(self, api_key: str, role: str, background: str, focus_area: str, max_turns: int = 5):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.role = role
        self.max_turns = max_turns
        
        self.memory = Memory()
        self.interviewer = InterviewerAgent(self.client, role, background, focus_area)
        self.evaluator = EvaluatorAgent(self.client, role, focus_area)
        self.coach = CoachAgent(self.client, role, background)
        
    def run(self):
        console.print(f"\n[bold green]Starting interview for {self.role}...[/bold green]\n")
        
        last_eval = None
        turn = 0
        
        while turn < self.max_turns:
            console.print(f"[dim]Turn {turn + 1}/{self.max_turns}[/dim]")
            
            # Get next question from interviewer
            question = self.interviewer.generate_question(self.memory, last_evaluation=last_eval)
            self.memory.add_message("interviewer", question)
            
            console.print(f"\n[bold blue]Interviewer:[/bold blue] {question}")
            
            answer = console.input("\n[bold yellow]You:[/bold yellow] ")
            
            if answer.strip().lower() in ['quit', 'exit', 'stop']:
                console.print("[bold red]Ending session.[/bold red]")
                break
                
            self.memory.add_message("user", answer)
            
            # Background evaluation
            console.print("[dim]Analyzing response...[/dim]")
            last_eval = self.evaluator.evaluate(question, answer)
            self.memory.add_evaluation(last_eval)
            
            # Check for follow-up flags safely
            flags = last_eval.get("flags", {})
            if flags.get("needs_followup"):
                console.print("[dim italic]System Note: Probing deeper on previous answer.[/dim italic]")
                if turn == self.max_turns - 1:
                    console.print("[dim italic]Extending session for follow-up.[/dim italic]")
                    self.max_turns += 1
            
            turn += 1
            console.print("-" * 50)
                
        # Final feedback synthesis
        console.print("\n[bold green]Generating coaching report...[/bold green]\n")
        with console.status("[bold green]Preparing report...[/bold green]"):
            report = self.coach.generate_feedback(self.memory)
            
        console.print(Panel(Markdown(report), title="[bold magenta]Final Report[/bold magenta]", border_style="magenta"))
