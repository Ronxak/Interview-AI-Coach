from typing import List, Dict, Any

class Memory:
    def __init__(self):
        self.transcript: List[Dict[str, str]] = []
        self.evaluations: List[Dict[str, Any]] = []
        
    def add_message(self, role: str, content: str):
        self.transcript.append({"role": role, "content": content})
        
    def add_evaluation(self, evaluation: Dict[str, Any]):
        self.evaluations.append(evaluation)
        
    def get_transcript_str(self) -> str:
        return "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.transcript])
        
    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        return self.transcript
