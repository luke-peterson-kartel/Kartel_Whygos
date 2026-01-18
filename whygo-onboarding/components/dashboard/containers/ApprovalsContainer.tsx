'use client'

import { usePendingApprovals } from '@/lib/api/queries'
import { ApprovalList } from '../approvals/ApprovalList'
import { Loader2 } from 'lucide-react'
import { DashboardCard } from '../layouts/DashboardCard'

export function ApprovalsContainer() {
  const { data: approvals, isLoading, error } = usePendingApprovals()

  if (isLoading) {
    return (
      <DashboardCard title="Pending Approvals">
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
        </div>
      </DashboardCard>
    )
  }

  if (error) {
    return (
      <DashboardCard title="Pending Approvals">
        <div className="text-center py-8 text-red-600 text-sm">
          Failed to load approvals
        </div>
      </DashboardCard>
    )
  }

  // Map goals to include person name (mock for now)
  const approvalsWithNames = (approvals || []).map(goal => ({
    goal,
    personName: 'Team Member' // Will be replaced with real name lookup
  }))

  return (
    <DashboardCard title="Pending Approvals">
      <ApprovalList approvals={approvalsWithNames} />
    </DashboardCard>
  )
}
