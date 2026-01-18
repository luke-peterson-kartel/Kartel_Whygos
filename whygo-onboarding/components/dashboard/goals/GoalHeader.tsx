import { IndividualGoal } from '@/lib/types/api'
import { StatusDot } from '../primitives/StatusDot'
import { Badge } from '@/components/ui/badge'
import { StatusType } from '@/lib/utils/status'

interface GoalHeaderProps {
  goal: IndividualGoal
  status: StatusType
}

export function GoalHeader({ goal, status }: GoalHeaderProps) {
  const statusBadgeVariant =
    goal.status === 'approved' ? 'default' :
    goal.status === 'pending_approval' ? 'secondary' :
    'outline'

  return (
    <div className="flex items-start justify-between">
      <div className="flex items-start space-x-2 flex-1">
        <StatusDot status={status} size="md" />
        <h4 className="text-sm font-semibold text-gray-900 line-clamp-2">{goal.goal}</h4>
      </div>
      <Badge variant={statusBadgeVariant} className="text-xs capitalize">
        {goal.status.replace('_', ' ')}
      </Badge>
    </div>
  )
}
