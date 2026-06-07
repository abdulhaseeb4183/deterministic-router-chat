# ⚡ Deterministic Engine: O(1) Dispatch Router Control Layer

A high-performance, zero-variance **Deterministic Router Control Layer** chatbot built to route user intents in $O(1)$ constant time complexity. This project demonstrates how to bypass slow conditional branching ($O(N)$ matching cascades) and costly model inference loops for deterministic agent flows.

🌐 **[Live Demo: Run Directly in Your Browser!](https://abdulhaseeb4183.github.io/deterministic-router-chat/)**

---

## 🚀 Key Features

* **$O(1)$ Dispatch Table Routing**: Backend intent matching resolves atomically via a direct hash table query, ensuring absolute constant-time processing.
* **Isolated Multi-Session State**: Supports parallel, independent chat sessions. Turn counts, unique hits, and command history are fully isolated per session.
* **Premium Cybertech Interface**: A fully responsive conversational UI styled with dark mode gradients, glassmorphic panels, glowing backdrops, and interactive animations.
* **Persistent History**: Integrated with browser `localStorage` so conversations and dynamic settings persist across page reloads.
* **Dual-Mode Execution (Local + Static hosting)**: Automatically detects environment—routes to the Python server when running locally, or falls back to clean, silent client-side simulation when hosted statically (e.g. GitHub Pages).

---

## 🛠️ Architecture & Routing Design

### The Dispatch Table Pattern
Instead of cascading `if-elif-else` branches to resolve intent, the engine maps string queries directly to execution handlers (callables or lambda functions):

```python
# Atomic intent mapping in chatbot_web.py
responses: Dict[str, HandlerType] = {
    "hello": lambda ctx: f"Hello! [Turn {ctx['turn_count']}] How can I assist you today?",
    "status": lambda ctx: f"Operational. System uptime: {int(time.time() - ctx['start_time'])}s.",
    "ping": lambda ctx: f"Pong! [Turn {ctx['turn_count']}] Latency: <1ms.",
    "clear": handle_clear,
    # Additional deterministic routes...
}
```

This guarantees that response latency remains identical regardless of the number of commands supported.

---

## ⚡ Supported Commands

Type these commands directly in the input field or click their chips in the sidebar:

| Command | Action | Output Description |
| :--- | :--- | :--- |
| `hello` / `hi` | Greeting | Context-aware greeting printing session turn number. |
| `status` | Telemetry | Operational uptime, complexity verification, and latency details. |
| `capabilities`| Capability Log | Summary of core control layer features. |
| `stats` | Metrics | Turn count and total unique commands executed in active session. |
| `ping` | Health Check | Connectivity validation with loopback latency telemetry. |
| `time` | Clock | Accurate system/browser timestamp. |
| `about` | Spec Sheet | Project design principles and execution specifications. |
| `joke` | Dev Quote | Short programmer/deterministic engine humor. |
| `clear` | Reset State | Wipes transaction telemetry and command history logs. |
| `exit` / `quit` | End Session | Safely exits/terminates active session context. |

---

## 💻 Local Setup & Execution

You can run the full stateful Python HTTP backend server locally in seconds:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/abdulhaseeb4183/deterministic-router-chat.git
   cd deterministic-router-chat
   ```

2. **Run the server**:
   ```bash
   python chatbot_web.py
   ```

3. **Interact**:
   The script will automatically launch a web browser window pointing to `http://localhost:8000`.

---

## 📁 Repository Structure

* `chatbot_web.py` — Stateful Python HTTP base server, session state management dictionary, and intent routing tables.
* `index.html` — Premium front-end dashboard, local storage persistence, responsive styling, and offline simulation fallback.
* `README.md` — Project description and system configuration specs.
## Snapshot
<img width="959" height="422" alt="image" src="https://github.com/user-attachments/assets/e94424a9-cb54-4e82-aaa8-4e4bc8c4d5b0" />
