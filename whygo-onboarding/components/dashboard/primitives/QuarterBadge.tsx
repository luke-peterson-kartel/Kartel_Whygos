import { StatusType } from '@/lib/utils/status'
import { Check, X, Clock } from 'lucide-react'

interface QuarterBadgeProps {
  quarter: 'Q1' | 'Q2' | 'Q3' | 'Q4'
  status: StatusType | null
  isCurrent?: boolean
}

const statusConfig = {
  on_track: { icon: Check, color: 'text-green-600 bg-green-50 border-green-200' },
  slightly_behind: { icon: Clock, color: 'text-yellow-600 bg-yellow-50 border-yellow-200' },
  off_track: { icon: X, color: 'text-red-600 bg-red-50 border-red-200' },
  not_started: { icon: Clock, color: 'text-gray-400 bg-gray-50 border-gray-200' }
}

export function QuarterBadge({ quarter, status, isCurrent = false }: QuarterBadgeProps) {
  const config = status ? statusConfig[status] : statusConfig.not_started
  const Icon = config.icon

  return (
    <div
      className={`flex items-center space-x-1 px-2 py-1 rounded border text-xs font-medium ${config.color} ${
        isCurrent ? 'ring-2 ring-blue-400' : ''
      }`}
    >
      <Icon className="w-3 h-3" />
      <span>{quarter}</span>
    </div>
  )
}
