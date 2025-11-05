/**
 * Component to display commit history
 * WHY? Shows past generated commits for reference
 */
import { useState, useEffect } from 'react'
import axios from 'axios'

interface CommitHistory {
  id: number
  message: string
  commit_type: string
  files: string[]
  created_at: string
  used: boolean
}

export default function HistoryPanel() {
  const [history, setHistory] = useState<CommitHistory[]>([])
  const [loading, setLoading] = useState(true)

  // Fetch history when component mounts
  // WHY useEffect? Runs once when component loads
  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const response = await axios.get('http://localhost:8000/history?limit=5')
      setHistory(response.data.history)
    } catch (err) {
      console.error('Failed to fetch history:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <p className="text-gray-500 text-center">Loading history...</p>
      </div>
    )
  }

  if (history.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold mb-3 text-gray-800">
          📜 Recent History
        </h3>
        <p className="text-gray-500 text-sm">No history yet. Generate your first commit!</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-3 text-gray-800">
        📜 Recent History
      </h3>

      <div className="space-y-3">
        {history.map((item) => (
          <div
            key={item.id}
            className="p-3 bg-gray-50 rounded-lg border border-gray-200 hover:shadow-md transition"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-gray-600 uppercase">
                {item.commit_type}
              </span>
              <span className="text-xs text-gray-400">
                {new Date(item.created_at).toLocaleDateString()}
              </span>
            </div>
            <p className="text-sm text-gray-700 line-clamp-2">
              {item.message.split('\n')[0]}
            </p>
            <div className="mt-2 text-xs text-gray-500">
              {item.files.length} file(s) • {item.used ? '✓ Used' : 'Not used'}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
