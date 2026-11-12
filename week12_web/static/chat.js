// chat.js - the browser side of your web app. It runs in the browser, not in Python.
// It sends each message to your Flask API with fetch() and shows the reply.
// Like the Messages API, your server is stateless: the page keeps the chat history and sends it each time.

const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("message");
const button = document.getElementById("send");
const facts = document.getElementById("facts");
const history = [];   // [{role: "user" | "assistant", content: "..."}]

function show(role, text) {
  const div = document.createElement("div");
  div.className = "msg " + role;
  div.textContent = text;          // textContent, never innerHTML: the reply is shown as text, not run as HTML
  chat.appendChild(div);
  div.scrollIntoView({ behavior: "smooth" });
}

async function loadMemory() {
  const response = await fetch("/api/memory");
  const data = await response.json();
  const items = Object.entries(data.memory).map(([key, value]) => key + ": " + value);
  facts.textContent = items.length ? items.join(" · ") : "nothing yet";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();                 // don't reload the page
  const message = input.value.trim();
  if (!message) return;
  show("user", message);
  input.value = "";
  button.disabled = true;
  button.textContent = "Thinking...";
  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message, history: history }),
    });
    const data = await response.json();
    if (!response.ok) {                   // 400, 503...: fetch doesn't throw for these, so check
      show("error", data.error || "Something went wrong");
      return;
    }
    show("assistant", data.reply);
    history.push({ role: "user", content: message }, { role: "assistant", content: data.reply });
    loadMemory();
  } catch (err) {
    show("error", "Can't reach the server. Is it still running?");
  } finally {
    button.disabled = false;
    button.textContent = "Send";
    input.focus();
  }
});

loadMemory();
