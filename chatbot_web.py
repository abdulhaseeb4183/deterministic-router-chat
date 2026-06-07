import http.server
import socketserver
import urllib.parse
import json
import time
import webbrowser
from typing import Dict, Any, Callable

# Type definitions for the deterministic control layer
ContextType = Dict[str, Any]
HandlerType = Callable[[ContextType], str]

# Multi-session state management to support parallel chat threads
sessions: Dict[str, ContextType] = {}

def get_session_context(session_id: str) -> ContextType:
    if session_id not in sessions:
        sessions[session_id] = {
            "start_time": time.time(),
            "turn_count": 0,
            "history": set(),
            "last_query": ""
        }
    return sessions[session_id]

def handle_clear(ctx: ContextType) -> str:
    ctx["turn_count"] = 0
    ctx["history"].clear()
    ctx["start_time"] = time.time()
    ctx["last_query"] = ""
    return "Context cache cleared. Command history reset."

# Knowledge Base (Hash Map) using the Dispatch Table Pattern.
# Maps user intents (keys) to handler callables (values) for dynamic responses.
responses: Dict[str, HandlerType] = {
    "hello": lambda ctx: f"Hello! [Turn {ctx['turn_count']}] How can I assist you today?",
    "hi": lambda ctx: f"Hi there! [Turn {ctx['turn_count']}] What can I do for you?",
    "help": lambda ctx: "Available commands: 'services', 'status', 'contact', 'time', 'stats', 'ping', 'about', 'capabilities', 'joke', 'clear'.",
    "services": lambda ctx: "We provide deterministic AI agent control layers, routing tables, and microservices.",
    "status": lambda ctx: f"Operational. System uptime: {int(time.time() - ctx['start_time'])}s. Latency: <1ms.",
    "contact": lambda ctx: "Reach us at architecture-team@deterministic-control.io.",
    "time": lambda ctx: f"System time: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    "stats": lambda ctx: f"Session Stats -> Turn count: {ctx['turn_count']}, Unique commands used: {len(ctx['history'])}",
    "ping": lambda ctx: f"Pong! [Turn {ctx['turn_count']}] Latency: <1ms. Control layer connection is active.",
    "about": lambda ctx: "Deterministic Engine v1.5.0 - Built to achieve O(1) matching efficiency using a hash map dispatch table. Designed for deterministic, zero-variance AI response routing.",
    "capabilities": lambda ctx: "System capabilities: 1. O(1) Intent matching; 2. Session state tracking; 3. Parallel session isolation; 4. Dynamic feedback dispatch.",
    "joke": lambda ctx: "Why did the deterministic chatbot cross the road? Because it was hardcoded to.",
    "clear": handle_clear
}

class ChatbotHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress request logs in console to keep terminal clean
        return

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Serve Frontend Page
        if path == "/" or path == "/index.html":
            try:
                with open("index.html", "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "index.html file not found in directory.")

        # API endpoint for O(1) matching requests
        elif path == "/api/chat":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            message = query_params.get("message", [""])[0]
            session_id = query_params.get("sessionId", ["default"])[0]

            # Sanitization
            sanitized_input = message.lower().strip()

            # Exit Strategy
            if sanitized_input in ("exit", "quit"):
                response_data = {"exit": True}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                return

            # Get or create state context for this session
            ctx = get_session_context(session_id)

            # Update session context
            ctx["turn_count"] += 1
            ctx["last_query"] = sanitized_input
            if sanitized_input in responses:
                ctx["history"].add(sanitized_input)

            # Dynamic fallback handler
            fallback: HandlerType = lambda c: f"Error 404: Command '{c['last_query']}' not recognized. Type 'help' for options."

            # Atomic lookup
            handler = responses.get(sanitized_input, fallback)
            reply = handler(ctx)

            # JSON payload response
            response_data = {
                "reply": reply,
                "turns": ctx["turn_count"],
                "unique_commands": len(ctx["history"])
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        else:
            self.send_error(404, "Resource Not Found")

def run_server():
    PORT = 8000
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), ChatbotHandler) as httpd:
        print(f"\n=======================================================")
        print(f"Server running at: http://localhost:{PORT}")
        print(f"Opening browser... Press Ctrl+C in this terminal to stop.")
        print(f"=======================================================\n")
        
        # Open web browser automatically to the running local server
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
