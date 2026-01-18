'use client'

import { Person } from '@/lib/types/api'
import { DashboardProvider } from '@/lib/context/DashboardContext'
import { SplitViewLayout } from '@/components/dashboard/layouts/SplitViewLayout'
import { MyGoalsContainer } from '@/components/dashboard/containers/MyGoalsContainer'
import { LeadershipContainer } from '@/components/dashboard/containers/LeadershipContainer'
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
      <SplitViewLayout
        leftPanel={<MyGoalsContainer onCreateGoal={handleCreateGoal} />}
        rightPanel={<LeadershipContainer />}
      />
    </DashboardProvider>
  )
}
