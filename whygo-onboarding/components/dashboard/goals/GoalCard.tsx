import { IndividualGoal } from '@/lib/types/api'
import { DashboardCard } from '../layouts/DashboardCard'
import { GoalHeader } from './GoalHeader'
import { GoalProgress } from './GoalProgress'
import { GoalConnections } from './GoalConnections'
import { GoalActions } from './GoalActions'
import { getGoalStatus } from '@/lib/utils/status'

interface GoalCardProps {
  goal: IndividualGoal
  currentQuarter?: 'q1' | 'q2' | 'q3' | 'q4'
  onEdit?: () => void
  onViewDetails?: () => void
}

export function GoalCard({ goal, currentQuarter = 'q1', onEdit, onViewDetails }: GoalCardProps) {
  const status = getGoalStatus(goal.outcomes, currentQuarter)

  return (
    <DashboardCard>
      <GoalHeader goal={goal} status={status.status} />
      <GoalProgress goal={goal} currentQuarter={currentQuarter} />
      <GoalConnections goal={goal} />
      <GoalActions goal={goal} onEdit={onEdit} onViewDetails={onViewDetails} />
    </DashboardCard>
  )
}
