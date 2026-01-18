'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/lib/context/OnboardingContext'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ArrowUp } from 'lucide-react'

export default function DepartmentGoalsPage() {
  const router = useRouter()
  const { data, setCurrentStep } = useOnboarding()

  useEffect(() => {
    setCurrentStep(3)
  }, [])

  if (!data) {
    router.push('/onboarding/profile')
    return null
  }

  const handleContinue = () => {
    router.push('/onboarding/goals')
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">
          {data.department.name} Department Goals
        </h2>
        <p className="mt-2 text-gray-600">
          These are your department's priorities. Your individual goals should connect to at least one of these.
        </p>
      </div>

      {data.department_goals.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-gray-600 text-center">
              Your department hasn't set goals yet. You can still create individual goals and connect them later.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {data.department_goals.map((goal, idx) => (
            <Card key={goal.id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-xl">
                    Department Goal #{idx + 1}
                  </CardTitle>
                  <Badge variant="outline">{goal.outcomes.length} Outcomes</Badge>
                </div>
                {/* Show ladder-up connection */}
                {goal.parent_goal_ids.length > 0 && (
                  <div className="flex items-center space-x-2 text-sm text-gray-600 mt-2">
                    <ArrowUp className="w-4 h-4" />
                    <span>Ladders to Company Goal #{goal.parent_goal_ids[0].replace('cg_', '')}</span>
                  </div>
                )}
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold text-gray-500 uppercase mb-1">Why</h4>
                  <p className="text-gray-700">{goal.why}</p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-500 uppercase mb-1">Goal</h4>
                  <p className="text-lg font-medium">{goal.goal}</p>
                </div>

                <div>
                  <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Outcomes</h4>
                  <ul className="space-y-2">
                    {goal.outcomes.map((outcome) => (
                      <li key={outcome.id} className="flex items-start space-x-2">
                        <span className="text-blue-600 mt-1">•</span>
                        <div className="flex-1">
                          <p className="font-medium">{outcome.description}</p>
                          <div className="flex items-center space-x-4 mt-1 text-sm text-gray-600">
                            <span>Annual: {outcome.target_annual || 'TBD'}</span>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={() => router.back()}>
          Back
        </Button>
        <Button onClick={handleContinue}>
          Continue to Your Goals
        </Button>
      </div>
    </div>
  )
}
