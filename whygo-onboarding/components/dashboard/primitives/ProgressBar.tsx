interface ProgressBarProps {
  percentage: number | null
  showLabel?: boolean
  height?: 'sm' | 'md' | 'lg'
}

const heightClasses = {
  sm: 'h-1',
  md: 'h-2',
  lg: 'h-3'
}

export function ProgressBar({ percentage, showLabel = true, height = 'md' }: ProgressBarProps) {
  const safePercentage = percentage ? Math.min(Math.max(percentage, 0), 100) : 0

  const barColor =
    percentage === null ? 'bg-gray-300' :
    safePercentage >= 100 ? 'bg-green-500' :
    safePercentage >= 80 ? 'bg-yellow-500' :
    'bg-red-500'

  return (
    <div className="w-full">
      <div className={`w-full bg-gray-200 rounded-full overflow-hidden ${heightClasses[height]}`}>
        <div
          className={`${barColor} ${heightClasses[height]} transition-all duration-300`}
          style={{ width: `${safePercentage}%` }}
        />
      </div>
      {showLabel && percentage !== null && (
        <span className="text-xs text-gray-600 mt-1">{Math.round(safePercentage)}%</span>
      )}
    </div>
  )
}
