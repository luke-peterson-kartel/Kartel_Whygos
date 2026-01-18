import { IndividualGoal } from '@/lib/types/api'
import { Button } from '@/components/ui/button'
import { Edit, MoreVertical } from 'lucide-react'

interface GoalActionsProps {
  goal: IndividualGoal
  onEdit?: () => void
  onViewDetails?: () => void
}

export function GoalActions({ goal, onEdit, onViewDetails }: GoalActionsProps) {
  return (
    <div className="flex items-center space-x-2 pt-2 border-t border-gray-100">
      <Button variant="ghost" size="sm" onClick={onViewDetails} className="text-xs">
        View Details
      </Button>
      {goal.status !== 'approved' && onEdit && (
        <Button variant="ghost" size="sm" onClick={onEdit} className="text-xs">
          <Edit className="w-3 h-3 mr-1" />
          Edit
        </Button>
      )}
      <Button variant="ghost" size="sm" className="text-xs ml-auto">
        <MoreVertical className="w-3 h-3" />
      </Button>
    </div>
  )
}
