import os
import json
from openai import OpenAI
from utils.memory import Memory

class CoachAgent:
    def __init__(self, client: OpenAI, role: str, background: str):
        self.client = client
        self.role = role
        self.background = background
        with open(os.path.join(os.path.dirname(__file__), '..', 'prompts', 'coach_prompt.txt'), 'r') as f:
            self.system_prompt_template = f.read()
            
    def generate_feedback(self, memory: Memory) -> str:
        system_prompt = self.system_prompt_template.format(
            role=self.role,
            background=self.background
        )
        
        transcript = memory.get_transcript_str()
        evaluations = json.dumps(memory.evaluations, indent=2)
        
        content = f"TRANSCRIPT:\n{transcript}\n\nEVALUATIONS:\n{evaluations}\n\nPlease generate the final coaching report in Markdown format."
        
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content.strip()
