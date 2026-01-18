import { IndividualGoal } from '@/lib/types/api'
import { ApprovalCard } from './ApprovalCard'

interface ApprovalListProps {
  approvals: Array<{ goal: IndividualGoal; personName: string }>
  onApprove?: (goal: IndividualGoal) => void
  onReject?: (goal: IndividualGoal) => void
  onViewDetails?: (goal: IndividualGoal) => void
  emptyMessage?: string
}

export function ApprovalList({
  approvals,
  onApprove,
  onReject,
  onViewDetails,
  emptyMessage = 'No pending approvals'
}: ApprovalListProps) {
  if (approvals.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 text-sm">
        {emptyMessage}
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {approvals.map(({ goal, personName }) => (
        <ApprovalCard
          key={goal.id}
          goal={goal}
          personName={personName}
          onApprove={() => onApprove?.(goal)}
          onReject={() => onReject?.(goal)}
          onViewDetails={() => onViewDetails?.(goal)}
        />
      ))}
    </div>
  )
}
