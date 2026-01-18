'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { getMyGoals } from '@/lib/api/goals'
import { IndividualGoal } from '@/lib/types/api'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { LogOut, Loader2 } from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()
  const [goals, setGoals] = useState<IndividualGoal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [personName, setPersonName] = useState('')

  useEffect(() => {
    // Check auth and load data
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token')
      if (!token) {
        router.push('/')
        return
      }
      setPersonName(localStorage.getItem('person_name') || 'User')
    }
    loadGoals()
  }, [])

  const loadGoals = async () => {
    try {
      const data = await getMyGoals()
      setGoals(data)
    } catch (error) {
      console.error('Failed to load goals:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('person_id')
      localStorage.removeItem('person_name')
      localStorage.removeItem('person_level')
    }
    router.push('/')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900">Welcome, {personName}!</h2>
          <p className="mt-2 text-gray-600">Your 2026 WhyGOs</p>
        </div>

        {goals.length === 0 ? (
          <Card>
            <CardContent className="pt-6 text-center">
              <p className="text-gray-600">No goals yet. Create your first goal in onboarding.</p>
              <Button onClick={() => router.push('/onboarding/goals')} className="mt-4">
                Create Goal
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {goals.map((goal) => (
              <Card key={goal.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <CardTitle>{goal.goal}</CardTitle>
                    <Badge
                      variant={goal.status === 'approved' ? 'default' : 'secondary'}
                    >
                      {goal.status}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="text-sm font-semibold text-gray-500 uppercase mb-1">Why</h4>
                    <p className="text-gray-700">{goal.why}</p>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">
                      Outcomes ({goal.outcomes.length})
                    </h4>
                    <ul className="space-y-2">
                      {goal.outcomes.map((outcome) => (
                        <li key={outcome.id} className="border-l-2 border-blue-600 pl-3">
                          <p className="font-medium">{outcome.description}</p>
                          <p className="text-sm text-gray-600">
                            Target: {outcome.target_annual} ({outcome.metric_type})
                          </p>
                        </li>
                      ))}
                    </ul>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
