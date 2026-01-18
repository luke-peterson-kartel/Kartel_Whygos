'use client'

import { TeamProgressContainer } from './TeamProgressContainer'
import { ApprovalsContainer } from './ApprovalsContainer'
import { useDashboard } from '@/lib/context/DashboardContext'

export function LeadershipContainer() {
  const { canViewTeam, canApproveGoals } = useDashboard()

  if (!canViewTeam && !canApproveGoals) {
    return (
      <>
        <div className="mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Team & Approvals</h2>
          <p className="text-sm text-gray-600 mt-1">
            Leadership features
          </p>
        </div>
        <div className="text-center py-12 text-gray-500 text-sm bg-white rounded-lg border border-gray-200 p-8">
          <p>Leadership features available for managers and executives</p>
        </div>
      </>
    )
  }

  return (
    <>
      <div className="mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Team & Approvals</h2>
        <p className="text-sm text-gray-600 mt-1">
          Monitor your team's progress
        </p>
      </div>
      <div className="space-y-4">
        {canViewTeam && <TeamProgressContainer />}
        {canApproveGoals && <ApprovalsContainer />}
      </div>
    </>
  )
}
