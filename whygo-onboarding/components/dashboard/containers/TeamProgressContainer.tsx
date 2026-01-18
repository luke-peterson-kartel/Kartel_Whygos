'use client'

import { DashboardCard } from '../layouts/DashboardCard'
import { TeamMemberList } from '../team/TeamMemberList'
import { Loader2 } from 'lucide-react'

// Mock data for now - will be replaced with real API call
export function TeamProgressContainer() {
  const isLoading = false

  if (isLoading) {
    return (
      <DashboardCard title="Team Progress">
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
        </div>
      </DashboardCard>
    )
  }

  // Mock team members
  const teamMembers = [
    { id: '1', name: 'Wayan Palmieri', title: 'VP Production', goalsCount: 3, totalGoals: 3, status: 'on_track' as const },
    { id: '2', name: 'Fill Isgro', title: 'VP Generative', goalsCount: 2, totalGoals: 3, status: 'slightly_behind' as const },
  ]

  return (
    <DashboardCard title="Team Progress">
      <TeamMemberList members={teamMembers} emptyMessage="No direct reports" />
    </DashboardCard>
  )
}
