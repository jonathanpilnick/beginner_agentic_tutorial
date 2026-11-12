"""
assistant.py - your assistant's "brain" from Week 11, ready to use. Nothing to do in this file.

This week you put a web interface around it. The brain stays the same:
  load_memory(path), save_memory(memory, path)   long-term facts in memory.json (Week 11 Lab 1)
  extract_facts(message)                         Claude picks the facts worth remembering
  chat(message, memory, history, persona)        one answer that uses the memory and the recent chat

Try it:  python assistant.py   (2 Claude calls)
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "solutions" else HERE   # works from either folder
sys.path.insert(1, str(ROOT))
from llm import ask_claude, ask_claude_json               # noqa: E402  (calls Claude through Claude Code)

MEMORY_FILE = ROOT / "memory.json"    # facts about the user: stays on your laptop (it is in .gitignore)

PERSONA = ("You are Remy, a friendly personal assistant who remembers the user. You know only what this "
           "conversation and your memory notes tell you about the user; ignore anything else. "
           "Use what you remember when it helps, without listing it. Answer in at most 3 sentences.")


# ---------- long-term memory: a JSON file (Week 11 Lab 1, Part 2) ----------------
def load_memory(path=MEMORY_FILE):
    """Return the saved facts as a dict, or {} if there is no memory file yet."""
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_memory(memory, path=MEMORY_FILE):
    """Write the facts to a JSON file that a person can read (UTF-8, indented)."""
    Path(path).write_text(json.dumps(memory, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------- Claude decides what to remember (Week 11 Lab 1, Part 3) ----------------
FACTS_SCHEMA = {
    "type": "object",
    "properties": {"facts": {"type": "object", "additionalProperties": {"type": "string"}}},
    "required": ["facts"],
}
EXTRACT_SYSTEM = (
    "You manage a user's long-term memory. From the user's message, pick out stable facts and preferences "
    "worth remembering in future conversations: name, diet, likes, dislikes, goals, budget, constraints. "
    "Use short snake_case keys and values of 1-5 words. If there is nothing worth remembering, return an empty object. "
    "Never store passwords, ID or card numbers, health details or other sensitive data."
)


def extract_facts(message):
    """Ask Claude which facts in `message` are worth remembering, as a dict like {"name": "Noa"}."""
    return ask_claude_json(message, schema=FACTS_SCHEMA, system=EXTRACT_SYSTEM)["facts"]


# ---------- answering with memory (Week 11 Lab 1, Part 1 and Part 3) ----------------
def build_prompt(history, user_message, max_messages=6):
    """The last `max_messages` messages as 'User: ...' / 'Assistant: ...' lines, then the new message."""
    lines = []
    for m in history[-max_messages:]:
        who = "User" if m["role"] == "user" else "Assistant"
        lines.append(f"{who}: {m['content']}")
    lines.append(f"User: {user_message}")
    return "\n".join(lines)


def build_system(memory, persona=PERSONA):
    """The persona plus the saved facts: external memory loaded into the prompt."""
    facts = "\n".join(f"- {k}: {v}" for k, v in (memory or {}).items()) or "- (nothing yet)"
    return persona + "\n\nWhat you remember about the user from earlier sessions:\n" + facts


def chat(message, memory=None, history=None, persona=PERSONA):
    """Answer `message` using the saved facts and the recent chat history. Returns the reply text."""
    return ask_claude(build_prompt(history or [], message), system=build_system(memory, persona))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    msg = "Hi, I'm Noa. I'm vegetarian and I love live jazz."
    print("Facts:", extract_facts(msg))
    print("Reply:", chat("Any idea for dinner tonight?", {"name": "Noa", "diet": "vegetarian"}))
