import { useState } from "react"
import axios from "axios"
import ReactMarkdown from "react-markdown"

export default function App() {
  const [question, setQuestion] = useState("")
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const ask = async () => {
    if (!question.trim()) return
    const userMsg = { role: "user", text: question }
    setMessages(prev => [...prev, userMsg])
    setQuestion("")
    setLoading(true)

    try {
      const res = await axios.post("http://localhost:8000/ask", { question })
      setMessages(prev => [...prev, { role: "bot", text: res.data.answer }])
    } catch {
      setMessages(prev => [...prev, { role: "bot", text: "Error reaching the server." }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === "Enter") ask()
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif", padding: "0 16px" }}>
      <h2>📄 College Doc Q&A</h2>
      <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 16, minHeight: 400, marginBottom: 16, overflowY: "auto" }}>
        {messages.length === 0 && <p style={{ color: "#aaa" }}>Ask anything from your uploaded documents.</p>}
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 12, textAlign: m.role === "user" ? "right" : "left" }}>
            <span style={{
              display: "inline-block",
              padding: "8px 12px",
              borderRadius: 8,
              background: m.role === "user" ? "#0070f3" : "#f1f1f1",
              color: m.role === "user" ? "#fff" : "#000",
              maxWidth: "80%"
            }}>
              <ReactMarkdown>{m.text}</ReactMarkdown>
            </span>
          </div>
        ))}
        {loading && <p style={{ color: "#aaa" }}>Thinking...</p>}
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Ask a question..."
          style={{ flex: 1, padding: "10px 14px", borderRadius: 8, border: "1px solid #ddd", fontSize: 15 }}
        />
        <button
          onClick={ask}
          style={{ padding: "10px 20px", borderRadius: 8, background: "#0070f3", color: "#fff", border: "none", cursor: "pointer", fontSize: 15 }}
        >
          Ask
        </button>
      </div>
    </div>
  )
}