import { IndividualGoal } from '@/lib/types/api'
import { Button } from '@/components/ui/button'
import { Check, X } from 'lucide-react'

interface ApprovalCardProps {
  goal: IndividualGoal
  personName: string
  onApprove?: () => void
  onReject?: () => void
  onViewDetails?: () => void
}

export function ApprovalCard({ goal, personName, onApprove, onReject, onViewDetails }: ApprovalCardProps) {
  return (
    <div className="border border-gray-200 rounded p-3 bg-white space-y-2">
      <div>
        <p className="text-xs text-gray-500 mb-1">{personName}</p>
        <p className="text-sm font-medium text-gray-900 line-clamp-2">{goal.goal}</p>
      </div>

      <div className="flex items-center space-x-2">
        <Button variant="ghost" size="sm" onClick={onViewDetails} className="text-xs flex-1">
          Details
        </Button>
        {onApprove && (
          <Button variant="default" size="sm" onClick={onApprove} className="text-xs">
            <Check className="w-3 h-3 mr-1" />
            Approve
          </Button>
        )}
        {onReject && (
          <Button variant="outline" size="sm" onClick={onReject} className="text-xs">
            <X className="w-3 h-3" />
          </Button>
        )}
      </div>
    </div>
  )
}
