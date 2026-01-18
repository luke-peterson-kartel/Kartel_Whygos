import { StatusDot } from '../primitives/StatusDot'
import { StatusType } from '@/lib/utils/status'

interface TeamMemberCardProps {
  name: string
  title: string
  goalsCount: number
  totalGoals: number
  status: StatusType
}

export function TeamMemberCard({ name, title, goalsCount, totalGoals, status }: TeamMemberCardProps) {
  return (
    <div className="flex items-center justify-between p-3 border border-gray-200 rounded bg-white hover:bg-gray-50 transition-colors">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-sm font-semibold text-gray-600">
          {name.split(' ').map(n => n[0]).join('')}
        </div>
        <div>
          <p className="text-sm font-medium text-gray-900">{name}</p>
          <p className="text-xs text-gray-500">{title}</p>
        </div>
      </div>
      <div className="flex items-center space-x-3">
        <div className="text-right">
          <p className="text-xs text-gray-600">{goalsCount}/{totalGoals} goals</p>
        </div>
        <StatusDot status={status} size="md" />
      </div>
    </div>
  )
}
