'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/lib/context/OnboardingContext'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export default function CompanyGoalsPage() {
  const router = useRouter()
  const { data, setCurrentStep } = useOnboarding()

  useEffect(() => {
    setCurrentStep(2)
  }, [])

  if (!data) {
    router.push('/onboarding/profile')
    return null
  }

  const handleContinue = () => {
    router.push('/onboarding/department')
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Company Goals for 2026</h2>
        <p className="mt-2 text-gray-600">
          These are Kartel's 4 strategic priorities. Your department and individual goals will ladder up to these.
        </p>
      </div>

      <div className="space-y-4">
        {data.company_goals.map((goal, idx) => (
          <Card key={goal.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <CardTitle className="text-xl">
                  Company Goal #{idx + 1}
                </CardTitle>
                <Badge variant="outline">{goal.outcomes.length} Outcomes</Badge>
              </div>
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
                          <span>Q1: {outcome.target_q1 || 'TBD'}</span>
                          <span>Q2: {outcome.target_q2 || 'TBD'}</span>
                          <span>Q3: {outcome.target_q3 || 'TBD'}</span>
                          <span>Q4: {outcome.target_q4 || 'TBD'}</span>
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

      <div className="flex justify-between pt-6">
        <Button variant="outline" onClick={() => router.back()}>
          Back
        </Button>
        <Button onClick={handleContinue}>
          Continue to Department Goals
        </Button>
      </div>
    </div>
  )
}
