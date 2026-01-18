import { IndividualGoal } from '@/lib/types/api'
import { ConnectionBadge } from '../primitives/ConnectionBadge'

interface GoalConnectionsProps {
  goal: IndividualGoal
}

export function GoalConnections({ goal }: GoalConnectionsProps) {
  if (!goal.parent_goal_ids || goal.parent_goal_ids.length === 0) {
    return null
  }

  return (
    <div className="space-y-1">
      <span className="text-xs text-gray-500">Connected to:</span>
      <div className="flex flex-wrap gap-1">
        {goal.parent_goal_ids.map((parentId) => {
          const isDeptGoal = parentId.startsWith('dg_')
          const isCompanyGoal = parentId.startsWith('cg_')

          const label = isDeptGoal
            ? `Dept Goal #${parentId.replace('dg_', '').split('_')[0]}`
            : isCompanyGoal
            ? `Company Goal #${parentId.replace('cg_', '')}`
            : parentId

          return (
            <ConnectionBadge
              key={parentId}
              label={label}
              type={isCompanyGoal ? 'company' : 'department'}
            />
          )
        })}
      </div>
    </div>
  )
}
