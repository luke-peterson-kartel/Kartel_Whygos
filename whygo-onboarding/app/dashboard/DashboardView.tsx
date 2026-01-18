'use client'

import { Person } from '@/lib/types/api'
import { DashboardProvider } from '@/lib/context/DashboardContext'
import { SplitViewLayout } from '@/components/dashboard/layouts/SplitViewLayout'
import { MyGoalsContainer } from '@/components/dashboard/containers/MyGoalsContainer'
import { LeadershipContainer } from '@/components/dashboard/containers/LeadershipContainer'
import { GoalsContextSidebar } from '@/components/dashboard/sidebar/GoalsContextSidebar'
import { useRouter } from 'next/navigation'

interface DashboardViewProps {
  user: Person
}

export default function DashboardView({ user }: DashboardViewProps) {
  const router = useRouter()

  const handleCreateGoal = () => {
    router.push('/onboarding/goals')
  }

  return (
    <DashboardProvider user={user}>
      <div className="flex h-full">
        <GoalsContextSidebar />
        <div className="flex-1 overflow-auto">
          <SplitViewLayout
            leftPanel={<MyGoalsContainer onCreateGoal={handleCreateGoal} />}
            rightPanel={<LeadershipContainer />}
          />
        </div>
      </div>
    </DashboardProvider>
  )
}
