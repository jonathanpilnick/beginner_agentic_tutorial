// project.js - the browser side of the Flask starter. It sends your input to POST /api/run
// and shows the answer. Change it to fit your idea.

const form = document.getElementById("form");
const input = document.getElementById("text");
const button = document.getElementById("run");
const results = document.getElementById("results");

function show(text, className) {
  const div = document.createElement("div");
  div.className = className;
  div.textContent = text;            // textContent, never innerHTML: AI output is shown as text, not run as HTML
  results.prepend(div);              // newest first
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  button.disabled = true;
  button.textContent = "Thinking...";
  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });
    const data = await response.json();
    if (!response.ok) {               // 400 or 503: fetch doesn't throw for these, so check
      show(data.error || "Something went wrong", "error");
      return;
    }
    show(data.text.replaceAll("**", ""), "result");   // the Markdown bold marks are for Streamlit
  } catch (err) {
    show("Can't reach the server. Is it still running?", "error");
  } finally {
    button.disabled = false;
    button.textContent = "Run";
  }
});
