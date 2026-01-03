'use client'

import { useState } from 'react'
import { Send } from 'lucide-react'

export default function HomePage() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<string[]>([])

  const handleSend = () => {
    if (!input.trim()) return
    setMessages(prev => [...prev, input])
    setInput('')
  }

  return (
    <main className="flex justify-center items-center bg-gradient-to-b from-neutral-950 to-neutral-900 h-[calc(100vh-64px)] px-6">
      
      {/* Chat Container */}
      <div className="w-full max-w-3xl h-[75vh] rounded-2xl bg-neutral-900/80 backdrop-blur border border-neutral-800 shadow-2xl flex flex-col">

        {/* Header */}
        <div className="px-6 py-4 border-b border-neutral-800">
          <h1 className="text-lg font-semibold text-white">
            Chat
          </h1>
          <p className="text-sm text-neutral-400">
            Think. Reflect. Build clarity.
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 px-6 py-4 space-y-3 overflow-hidden">
          {messages.length === 0 && (
            <div className="text-neutral-500 text-sm mt-10">
              Start a conversation with <span className="text-white">WorkJournal</span>.
            </div>
          )}

          {messages.map((msg, idx) => (
            <div
              key={idx}
              className="self-end max-w-[80%] bg-indigo-600 text-white px-4 py-2 rounded-xl text-sm shadow"
            >
              {msg}
            </div>
          ))}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-neutral-800">
          <div className="flex items-center gap-3 bg-neutral-800 rounded-xl px-4 py-3">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Type your message..."
              className="flex-1 bg-transparent text-sm text-white placeholder-neutral-400 outline-none"
            />
            <button
              onClick={handleSend}
              className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 transition"
            >
              <Send size={16} className="text-white" />
            </button>
          </div>
        </div>

      </div>
    </main>
  )
}
