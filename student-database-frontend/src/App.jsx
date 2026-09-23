import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "Hello! 👋 I'm your Student Database AI Assistant. Ask me anything about the students.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatAreaRef = useRef(null);
  const inputRef = useRef(null);

  // Auto scroll
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages, loading]);

  // Focus input
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const clearChat = () => {
    setMessages([
      {
        id: Date.now(),
        type: "bot",
        text: "Hello! 👋 I'm your Student Database AI Assistant. Ask me anything about the students.",
      },
    ]);

    setInput("");
    setTimeout(() => inputRef.current?.focus(), 100);
  };

  const sendMessage = async () => {
    const message = input.trim();

    if (!message || loading) return;

    const userMessage = {
      id: Date.now(),
      type: "user",
      text: message,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chatbot/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      if (!response.ok) {
        let errorMessage = "Something went wrong.";

        try {
          const errorData = await response.json();

          if (errorData?.detail) {
            errorMessage = errorData.detail;
          }
        } catch {
          // Ignore JSON parsing error
        }

        throw new Error(errorMessage);
      }

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "bot",
          text: data.response || "I couldn't find a response.",
        },
      ]);
    } catch (error) {
      console.error("Chat error:", error);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "error",
          text:
            error.message ||
            "Unable to connect to the backend. Please make sure the FastAPI server is running.",
        },
      ]);
    } finally {
      setLoading(false);

      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  const renderBotMessage = (text) => {
    // Student result formatting
    const studentMatch = text.match(
      /ID:\s*(\d+),\s*Name:\s*(.*?),\s*Email:\s*(.*?),\s*Age:\s*(\d+),\s*Course:\s*(.*)/i
    );

    if (studentMatch) {
      const [, id, name, email, age, course] = studentMatch;

      return (
        <div className="student-card">
          <div className="student-card-header">
            <div className="student-avatar">🎓</div>

            <div>
              <h3>Student Found</h3>
              <span>Student ID: #{id}</span>
            </div>

            <div className="success-icon">✓</div>
          </div>

          <div className="student-details">
            <div className="student-detail">
              <div className="detail-icon">👤</div>
              <div>
                <small>FULL NAME</small>
                <strong>{name}</strong>
              </div>
            </div>

            <div className="student-detail">
              <div className="detail-icon">📧</div>
              <div>
                <small>EMAIL</small>
                <strong>{email}</strong>
              </div>
            </div>

            <div className="student-detail">
              <div className="detail-icon">🎂</div>
              <div>
                <small>AGE</small>
                <strong>{age} years</strong>
              </div>
            </div>

            <div className="student-detail">
              <div className="detail-icon">🎓</div>
              <div>
                <small>COURSE</small>
                <strong>{course}</strong>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return <div className="normal-text">{text}</div>;
  };

  return (
    <div className="app">
      <div className="background-glow glow-one"></div>
      <div className="background-glow glow-two"></div>

      <main className="chat-container">
        {/* Header */}
        <header className="chat-header">
          <div className="brand-section">
            <div className="brand-icon">🎓</div>

            <div>
              <h1>Student Database AI</h1>

              <div className="status">
                <span className="status-dot"></span>
                <span>AI Assistant</span>
                <span className="status-separator">•</span>
                <span>Online</span>
              </div>
            </div>
          </div>

          <button
            className="clear-button"
            onClick={clearChat}
            title="Clear conversation"
            aria-label="Clear conversation"
          >
            🗑️
          </button>
        </header>

        {/* Chat */}
        <section className="chat-area" ref={chatAreaRef}>
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message-row ${message.type}`}
            >
              {message.type !== "user" && (
                <div className="message-avatar bot-avatar">🤖</div>
              )}

              <div
                className={`message-bubble ${
                  message.type === "user"
                    ? "user-bubble"
                    : message.type === "error"
                    ? "error-bubble"
                    : "bot-bubble"
                }`}
              >
                {message.type === "error" ? (
                  <>
                    <span className="error-symbol">×</span>
                    {message.text}
                  </>
                ) : message.type === "bot" ? (
                  renderBotMessage(message.text)
                ) : (
                  message.text
                )}
              </div>

              {message.type === "user" && (
                <div className="message-avatar user-avatar">👤</div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <div className="message-avatar bot-avatar">🤖</div>

              <div className="message-bubble bot-bubble typing-bubble">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            </div>
          )}
        </section>

        {/* Input */}
        <div className="input-section">
          <div className="input-wrapper">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about students..."
              rows="1"
              disabled={loading}
            />

            <button
              className={`send-button ${
                input.trim() && !loading ? "active" : ""
              }`}
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              aria-label="Send message"
            >
              {loading ? "⋯" : "➤"}
            </button>
          </div>

          <div className="input-hint">
            <span>Press Enter to send</span>
            <span>•</span>
            <span>Student Database AI</span>
          </div>
        </div>

        {/* Footer */}
        <footer className="footer">
          Powered by <strong>FastAPI</strong>
          <span>•</span>
          <strong>Gemini</strong>
          <span>•</span>
          <strong>LangGraph</strong>
        </footer>
      </main>
    </div>
  );
}

export default App;