import { StatusType } from '@/lib/utils/status'

interface StatusDotProps {
  status: StatusType
  size?: 'sm' | 'md' | 'lg'
}

const sizeClasses = {
  sm: 'w-2 h-2',
  md: 'w-3 h-3',
  lg: 'w-4 h-4'
}

const colorClasses = {
  on_track: 'bg-green-500',
  slightly_behind: 'bg-yellow-500',
  off_track: 'bg-red-500',
  not_started: 'bg-gray-300'
}

export function StatusDot({ status, size = 'md' }: StatusDotProps) {
  return (
    <div
      className={`rounded-full ${sizeClasses[size]} ${colorClasses[status]}`}
      aria-label={status.replace('_', ' ')}
    />
  )
}
