'use client'

import { TeamProgressContainer } from './TeamProgressContainer'
import { ApprovalsContainer } from './ApprovalsContainer'
import { useDashboard } from '@/lib/context/DashboardContext'

export function LeadershipContainer() {
  const { canViewTeam, canApproveGoals } = useDashboard()

  if (!canViewTeam && !canApproveGoals) {
    return (
      <div className="text-center py-12 text-gray-500 text-sm">
        <p>Leadership features available for managers and executives</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {canViewTeam && <TeamProgressContainer />}
      {canApproveGoals && <ApprovalsContainer />}
    </div>
  )
}
