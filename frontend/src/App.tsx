/**
 * Main App Component
 * WHY this structure? Clean, organized, easy to understand
 */
import { useState } from 'react'
import axios from 'axios'
import CommitMessageDisplay from './components/CommitMessageDisplay'
import LoadingSpinner from './components/LoadingSpinner'
import FilesList from './components/FilesList'
import HistoryPanel from './components/HistoryPanel'

// Type definitions - WHY? TypeScript helps catch errors
interface CommitMessage {
  message: string
  type: string
  files_changed: string[]
  insertions: number
  deletions: number
}

function App() {
  // State management - tracks app data
  const [commitMessage, setCommitMessage] = useState<CommitMessage | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showHistory, setShowHistory] = useState(false)

  /**
   * Analyze staged changes and generate commit message
   * WHY async? API calls take time, don't block UI
   */
  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)

    try {
      // Call backend API
      const response = await axios.post<CommitMessage>('http://localhost:8000/analyze', {
        repo_path: null  // Uses current directory
      })

      setCommitMessage(response.data)
    } catch (err: any) {
      // Handle errors gracefully
      if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Failed to analyze changes. Make sure backend is running and you have staged changes.')
      }
    } finally {
      setLoading(false)
    }
  }

  /**
   * Copy commit message to clipboard
   * WHY? Makes it easy to paste into git commit
   */
  const handleCopy = () => {
    if (commitMessage) {
      navigator.clipboard.writeText(commitMessage.message)
      alert('Copied to clipboard!')
    }
  }

  /**
   * Regenerate with different style
   */
  const handleRegenerate = async () => {
    await handleAnalyze()  // For now, just regenerate same way
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🚀 Git Commit Composer
              </h1>
              <p className="text-gray-600 mt-1">
                AI-powered commit messages using Google Gemini
              </p>
            </div>
            <button
              onClick={() => setShowHistory(!showHistory)}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
            >
              {showHistory ? 'Hide' : 'Show'} History
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Main Action */}
          <div className="lg:col-span-2 space-y-6">
            {/* Action Card */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4 text-gray-800">
                Analyze Staged Changes
              </h2>
              <p className="text-gray-600 mb-4">
                Make sure you have staged your changes with <code>git add</code> first.
              </p>

              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="w-full bg-git-blue text-white py-3 px-6 rounded-lg font-semibold
                         hover:bg-blue-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed
                         flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <LoadingSpinner /> Analyzing...
                  </>
                ) : (
                  '✨ Generate Commit Message'
                )}
              </button>

              {/* Error Display */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-red-700">⚠️ {error}</p>
                </div>
              )}
            </div>

            {/* Commit Message Display */}
            {commitMessage && (
              <CommitMessageDisplay
                commitMessage={commitMessage}
                onCopy={handleCopy}
                onRegenerate={handleRegenerate}
              />
            )}

            {/* Files Changed */}
            {commitMessage && commitMessage.files_changed.length > 0 && (
              <FilesList
                files={commitMessage.files_changed}
                insertions={commitMessage.insertions}
                deletions={commitMessage.deletions}
              />
            )}
          </div>

          {/* Right Column - Info & History */}
          <div className="space-y-6">
            {/* Quick Guide */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-3 text-gray-800">
                📖 Quick Guide
              </h3>
              <ol className="space-y-2 text-sm text-gray-600">
                <li>1. Make changes to your code</li>
                <li>2. Stage changes: <code>git add .</code></li>
                <li>3. Click "Generate Commit Message"</li>
                <li>4. Copy and use in: <code>git commit -m "..."</code></li>
              </ol>
            </div>

            {/* Commit Types Info */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold mb-3 text-gray-800">
                🏷️ Commit Types
              </h3>
              <div className="space-y-2 text-sm">
                <div><span className="font-semibold text-green-600">feat:</span> New feature</div>
                <div><span className="font-semibold text-red-600">fix:</span> Bug fix</div>
                <div><span className="font-semibold text-blue-600">docs:</span> Documentation</div>
                <div><span className="font-semibold text-purple-600">refactor:</span> Code refactoring</div>
                <div><span className="font-semibold text-yellow-600">test:</span> Testing</div>
                <div><span className="font-semibold text-gray-600">chore:</span> Maintenance</div>
              </div>
            </div>

            {/* History Panel */}
            {showHistory && <HistoryPanel />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 pb-6 text-center text-gray-600 text-sm">
        <p>Powered by Google Gemini Flash 🤖</p>
        <p className="mt-1">Built with React, TypeScript, FastAPI & Python</p>
      </footer>
    </div>
  )
}

export default App
