import os
from openai import OpenAI
from utils.memory import Memory

class InterviewerAgent:
    def __init__(self, client: OpenAI, role: str, background: str, focus_area: str):
        self.client = client
        self.role = role
        self.background = background
        self.focus_area = focus_area
        with open(os.path.join(os.path.dirname(__file__), '..', 'prompts', 'interviewer_prompt.txt'), 'r') as f:
            self.system_prompt_template = f.read()
            
    def generate_question(self, memory: Memory, last_evaluation: dict = None) -> str:
        system_prompt = self.system_prompt_template.format(
            role=self.role,
            background=self.background,
            focus_area=self.focus_area
        )
        
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in memory.get_messages_for_llm():
            role = "assistant" if msg["role"] == "interviewer" else "user"
            messages.append({"role": role, "content": msg["content"]})
            
        if last_evaluation:
            eval_msg = (
                f"SYSTEM NOTE: The evaluator analyzed the candidate's last answer. "
                f"Reasoning: {last_evaluation.get('reasoning')}. "
                f"Flags: {last_evaluation.get('flags')}. "
                f"Adapt your next question/follow-up accordingly. Do not mention this note directly to the user."
            )
            messages.append({"role": "system", "content": eval_msg})
            
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
