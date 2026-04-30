# AI Mock Interview Coach

A production-ready, multi-agent system designed to conduct realistic, adaptive mock interviews. This project leverages an orchestration layer to coordinate specialized LLM agents, providing candidates with dynamic questioning and deep, multi-dimensional feedback.

## Key Features

- **Adaptive Questioning:** The system doesn't follow a script. It probes weak answers, acknowledges strong ones, and pivots based on real-time evaluation.
- **Multi-Agent Orchestration:** Isolation of concerns between an **Interviewer**, a **Background Evaluator**, and a **Synthesis Coach**.
- **Ultra-Low Latency:** Optimized using **Groq** for near-instant inference, making the conversation feel natural.
- **Structured Analytics:** Uses JSON-mode data extraction to score candidates across 5 dimensions: Clarity, Depth, Accuracy, Communication, and Completeness.
- **Actionable Coaching:** Generates a comprehensive Markdown report including a personalized practice roadmap.

## System Architecture

```mermaid
graph TD
    User([Candidate]) -->|Answer| Orchestrator{Orchestrator}
    Orchestrator -->|Analyze| Evaluator[Evaluator: Llama 3.1 8B]
    Evaluator -->|JSON Scores & Flags| Orchestrator
    Orchestrator -->|Hidden Context| Interviewer[Interviewer: Llama 3.3 70B]
    Interviewer -->|Next Question| User
    Orchestrator -->|Full Transcript| Coach[Coach: Llama 3.3 70B]
    Coach -->|Markdown Report| User
```

## Technical Stack

- **Language:** Python 3.10+
- **Inference Engine:** [Groq](https://groq.com/) (OpenAI-compatible SDK)
- **Models:** 
    - `llama-3.3-70b-versatile` (Reasoning & Synthesis)
    - `llama-3.1-8b-instant` (High-speed JSON Extraction)
- **Utilities:** Pydantic (Data Validation), Rich (CLI UI), Python-Dotenv.

## Design Decisions & Tradeoffs

### 1. The Multi-Agent Advantage
A common failure in AI interviewers is "persona bleed"—where the model starts giving feedback *during* the interview. By separating the **Evaluator** into a hidden background process, the **Interviewer** stays 100% in character, while the system still maintains perfect analytical awareness.

### 2. Strategic Model Selection
I chose a tiered model approach:
- **Llama 3.3 70B** is used for the Interviewer and Coach because these roles require high emotional intelligence and complex reasoning.
- **Llama 3.1 8B** is used for the Evaluator. Since the Evaluator's job is specific data extraction into JSON, the smaller model provides 10x faster response times without sacrificing accuracy for this specific task.

### 3. Adaptive Turn Logic
The Orchestrator monitors "needs_followup" flags from the Evaluator. If a candidate provides a vague answer, the system dynamically extends the interview length to ensure the topic is fully explored, mimicking a real-world senior-level interview.

## Setup & Execution

1. **Clone and Install:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configuration:** Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```
3. **Run the Coach:**
   ```bash
   python3 main.py
   ```

## Example Scenario: Probing for Depth

**Interviewer:** "How do you handle a memory leak in a Python application?"
**User:** "I'd just restart the server or check the logs."
**Evaluator (Internal):** Flags as `is_weak: true` and `needs_followup: true`.
**Interviewer (Follow-up):** *"Restarting is a temporary fix, but if the leak is in the code, it will return. How would you actually isolate the source of the leak? Are there specific tools or libraries you'd use to inspect the heap?"*

## Future Roadmap

- [ ] **Voice Integration:** Adding Whisper (STT) and ElevenLabs (TTS) for hands-free mock calls.
- [ ] **RAG-Enhanced Questioning:** Grounding the interviewer in specific company engineering blogs or open-source documentation.
- [ ] **PDF Export:** Option to save the final coaching report as a branded PDF.

---
*Developed as part of the AI Engineer Internship Assignment.*
