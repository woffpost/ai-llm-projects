"use client"

import { useState } from "react"

export default function Home() {
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState("")
  const [loading, setLoading] = useState(false)

  const ask = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer("")

    const res = await fetch("http://127.0.0.1:8000/ask-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    })

    const reader = res.body!.getReader()
    const decoder = new TextDecoder()
    setLoading(false)

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      setAnswer(prev => prev + decoder.decode(value))
    }
  }

  return (
    <main className="max-w-2xl mx-auto mt-20 p-6">
      <h1 className="text-2xl font-bold mb-6">🚗 Каталог советских моделей</h1>
      
      <input
        className="w-full border rounded p-3 mb-4 text-black"
        placeholder="Задай вопрос по каталогу..."
        value={question}
        onChange={e => setQuestion(e.target.value)}
        onKeyDown={e => e.key === "Enter" && ask()}
      />
      
      <button
        className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700"
        onClick={ask}
        disabled={loading}
      >
        {loading ? "Думаю..." : "Спросить"}
      </button>

      {answer && (
        <div className="mt-6 p-4 bg-gray-100 rounded text-black">
          {answer}
        </div>
      )}
    </main>
  )
}