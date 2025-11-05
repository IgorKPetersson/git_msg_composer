/**
 * Simple loading spinner component
 * WHY? Shows user something is happening during API calls
 */
export default function LoadingSpinner() {
  return (
    <div className="inline-block animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
  )
}
