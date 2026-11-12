"""
feature.py - YOUR AI FEATURE. This is the file you change most for the project.

The starter is a working example, a "Flashcard Maker": paste notes, get flashcards back.
Replace it with your own idea (see PROJECT_BRIEF.md). Both apps use these two functions:
  run_feature(text)        -> a dict (JSON-friendly) with the result. Calls Claude.
  format_result(result)    -> the result as Markdown text to show on the page.
The web apps only call these two, so you can change everything inside them.

Try it:  python project/feature.py      (1 Claude call, on data/sample_notes.md)
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent                                 # the week12_web folder
sys.path.insert(1, str(KIT))
from llm import ask_claude_json                   # noqa: E402  (Claude through your Claude Code login)

MAX_CHARS = 4000            # longer inputs are refused with 400: they cost more and can be abuse
EXAMPLE_INPUT = "HTTP status codes: 200 means OK, 400 means the client sent a bad request, 404 means not found."

SYSTEM = ("You turn a student's study notes into flashcards. Use only facts that are in the notes. "
          "Each question tests one idea; each answer is one short sentence. Write in the notes' language.")

SCHEMA = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"question": {"type": "string"}, "answer": {"type": "string"}},
                "required": ["question", "answer"],
            },
        }
    },
    "required": ["cards"],
}


def run_feature(text):
    """Ask Claude for up to 5 flashcards about `text`. Returns {"cards": [{"question", "answer"}, ...]}."""
    result = ask_claude_json(f"Make 3 to 5 flashcards from these notes:\n\n{text}", SCHEMA, system=SYSTEM)
    result["cards"] = result["cards"][:5]
    return result


def format_result(result):
    """Markdown for the page: one numbered card per line."""
    lines = [f"**{i}. {card['question']}**  \n{card['answer']}" for i, card in enumerate(result["cards"], 1)]
    return "\n\n".join(lines) or "No flashcards this time. Try longer notes."


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    notes = (KIT / "data" / "sample_notes.md").read_text(encoding="utf-8")
    result = run_feature(notes)
    print("run_feature() returned:", result, "\n")
    print("format_result() shows:\n" + format_result(result))
