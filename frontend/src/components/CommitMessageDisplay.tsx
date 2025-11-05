/**
 * Component to display generated commit message
 * WHY separate component? Keeps code organized and reusable
 */
interface Props {
  commitMessage: {
    message: string
    type: string
  }
  onCopy: () => void
  onRegenerate: () => void
}

export default function CommitMessageDisplay({ commitMessage, onCopy, onRegenerate }: Props) {
  // Get color based on commit type
  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      feat: 'text-green-600 bg-green-50 border-green-200',
      fix: 'text-red-600 bg-red-50 border-red-200',
      docs: 'text-blue-600 bg-blue-50 border-blue-200',
      refactor: 'text-purple-600 bg-purple-50 border-purple-200',
      test: 'text-yellow-600 bg-yellow-50 border-yellow-200',
      chore: 'text-gray-600 bg-gray-50 border-gray-200',
      style: 'text-pink-600 bg-pink-50 border-pink-200',
      perf: 'text-orange-600 bg-orange-50 border-orange-200',
    }
    return colors[type] || colors.chore
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          ✅ Generated Commit Message
        </h2>
        <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getTypeColor(commitMessage.type)}`}>
          {commitMessage.type}
        </span>
      </div>

      {/* Commit Message Display */}
      <div className="bg-gray-50 rounded-lg p-4 mb-4 border border-gray-200">
        <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800">
          {commitMessage.message}
        </pre>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={onCopy}
          className="flex-1 bg-git-green text-white py-2 px-4 rounded-lg hover:bg-green-600 transition font-medium"
        >
          📋 Copy to Clipboard
        </button>
        <button
          onClick={onRegenerate}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition"
        >
          🔄 Regenerate
        </button>
      </div>

      {/* Usage Hint */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-sm text-blue-800">
          💡 <strong>Tip:</strong> Copy this message and use it with:
          <code className="ml-2 text-xs">git commit -m "..."</code>
        </p>
      </div>
    </div>
  )
}
