'use client'

import { useMyGoals } from '@/lib/api/queries'
import { GoalList } from '../goals/GoalList'
import { Loader2 } from 'lucide-react'
import { DashboardCard } from '../layouts/DashboardCard'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-react'

interface MyGoalsContainerProps {
  onCreateGoal?: () => void
}

export function MyGoalsContainer({ onCreateGoal }: MyGoalsContainerProps) {
  const { data: goals, isLoading, error } = useMyGoals()

  if (isLoading) {
    return (
      <DashboardCard title="Your Goals">
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
        </div>
      </DashboardCard>
    )
  }

  if (error) {
    return (
      <DashboardCard title="Your Goals">
        <div className="text-center py-8 text-red-600 text-sm">
          Failed to load goals
        </div>
      </DashboardCard>
    )
  }

  const action = onCreateGoal && goals && goals.length < 3 ? (
    <Button variant="ghost" size="sm" onClick={onCreateGoal} className="text-xs">
      <Plus className="w-3 h-3 mr-1" />
      Add Goal
    </Button>
  ) : undefined

  return (
    <DashboardCard title="Your Goals" action={action}>
      <GoalList goals={goals || []} />
    </DashboardCard>
  )
}
