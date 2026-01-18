import { IndividualGoal } from '@/lib/types/api'
import { ProgressBar } from '../primitives/ProgressBar'
import { QuarterBadge } from '../primitives/QuarterBadge'
import { getGoalStatus } from '@/lib/utils/status'

interface GoalProgressProps {
  goal: IndividualGoal
  currentQuarter?: 'q1' | 'q2' | 'q3' | 'q4'
}

export function GoalProgress({ goal, currentQuarter = 'q1' }: GoalProgressProps) {
  const status = getGoalStatus(goal.outcomes, currentQuarter)

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-600">Progress</span>
        <span className="text-xs font-medium text-gray-900">
          {status.percentage ? `${Math.round(status.percentage)}%` : 'Not started'}
        </span>
      </div>
      <ProgressBar percentage={status.percentage} showLabel={false} height="sm" />

      <div className="flex items-center space-x-2">
        <QuarterBadge quarter="Q1" status={getGoalStatus(goal.outcomes, 'q1').status} isCurrent={currentQuarter === 'q1'} />
        <QuarterBadge quarter="Q2" status={getGoalStatus(goal.outcomes, 'q2').status} isCurrent={currentQuarter === 'q2'} />
        <QuarterBadge quarter="Q3" status={getGoalStatus(goal.outcomes, 'q3').status} isCurrent={currentQuarter === 'q3'} />
        <QuarterBadge quarter="Q4" status={getGoalStatus(goal.outcomes, 'q4').status} isCurrent={currentQuarter === 'q4'} />
      </div>
    </div>
  )
}
