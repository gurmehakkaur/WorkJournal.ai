'use client'

import { useState } from 'react'
import { Send } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function HomePage() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = input.trim()
    setInput('')

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage }])
    setLoading(true)

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages.map(msg => ({
            role: msg.role,
            content: msg.content
          })).concat({ role: 'user', content: userMessage })
        }),
      })

      const data = await response.json()

      // Add assistant response to chat
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }])
    } finally {
      setLoading(false)
    }
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
        <div className="flex-1 px-6 py-4 space-y-3 overflow-y-auto">
          {messages.length === 0 && (
            <div className="text-neutral-500 text-sm mt-10">
              Let us talk and add a new entry to your <span className="text-white">WorkJournal</span>.
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[80%] px-4 py-2 rounded-xl text-sm shadow ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-neutral-800 text-neutral-100'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-neutral-800 text-neutral-100 px-4 py-2 rounded-xl text-sm">
                <span className="inline-block animate-pulse">Thinking...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-neutral-800">
          <div className="flex items-center gap-3 bg-neutral-800 rounded-xl px-4 py-3">
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !loading && handleSend()}
              placeholder="Type your message..."
              disabled={loading}
              className="flex-1 bg-transparent text-sm text-white placeholder-neutral-400 outline-none disabled:opacity-50"
            />
            <button
              onClick={handleSend}
              disabled={loading}
              className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send size={16} className="text-white" />
            </button>
          </div>
        </div>

      </div>
    </main>
  )
}
