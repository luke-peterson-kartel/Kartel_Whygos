import { IndividualGoal } from '@/lib/types/api'
import { GoalCard } from './GoalCard'

interface GoalListProps {
  goals: IndividualGoal[]
  currentQuarter?: 'q1' | 'q2' | 'q3' | 'q4'
  onEdit?: (goal: IndividualGoal) => void
  onViewDetails?: (goal: IndividualGoal) => void
  emptyMessage?: string
}

export function GoalList({
  goals,
  currentQuarter = 'q1',
  onEdit,
  onViewDetails,
  emptyMessage = 'No goals yet. Create your first goal!'
}: GoalListProps) {
  if (goals.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 text-sm">
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {goals.map((goal) => (
        <GoalCard
          key={goal.id}
          goal={goal}
          currentQuarter={currentQuarter}
          onEdit={() => onEdit?.(goal)}
          onViewDetails={() => onViewDetails?.(goal)}
        />
      ))}
    </div>
  )
}
