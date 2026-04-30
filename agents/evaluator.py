import os
from openai import OpenAI
from utils.scoring import EvaluationResult

class EvaluatorAgent:
    def __init__(self, client: OpenAI, role: str, focus_area: str):
        self.client = client
        self.role = role
        self.focus_area = focus_area
        with open(os.path.join(os.path.dirname(__file__), '..', 'prompts', 'evaluator_prompt.txt'), 'r') as f:
            self.system_prompt_template = f.read()
            
    def evaluate(self, question: str, answer: str) -> dict:
        system_prompt = self.system_prompt_template.format(
            role=self.role,
            focus_area=self.focus_area,
            question=question,
            answer=answer
        )
        
        import json
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Return the evaluation JSON."}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            # Fallback for parsing issues
            return {
                "scores": {"clarity": 5, "depth": 5, "accuracy": 5, "communication": 5, "completeness": 5},
                "flags": {"is_weak": False, "is_strong": False, "needs_followup": False, "is_off_topic": False},
                "reasoning": f"Evaluation failed: {str(e)}"
            }
