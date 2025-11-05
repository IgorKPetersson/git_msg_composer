/**
 * Component to display list of changed files
 * WHY? Shows user what files will be included in commit
 */
interface Props {
  files: string[]
  insertions: number
  deletions: number
}

export default function FilesList({ files, insertions, deletions }: Props) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-3 text-gray-800">
        📁 Files Changed ({files.length})
      </h3>

      {/* Statistics */}
      <div className="flex gap-4 mb-4 text-sm">
        <span className="text-green-600 font-medium">
          +{insertions} insertions
        </span>
        <span className="text-red-600 font-medium">
          -{deletions} deletions
        </span>
      </div>

      {/* Files List */}
      <div className="space-y-2">
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center gap-2 p-2 bg-gray-50 rounded border border-gray-200 hover:bg-gray-100 transition"
          >
            <span className="text-gray-400">📄</span>
            <code className="text-sm text-gray-700 flex-1">{file}</code>
          </div>
        ))}
      </div>
    </div>
  )
}
