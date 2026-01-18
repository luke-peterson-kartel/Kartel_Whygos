'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/lib/context/OnboardingContext'
import { completeOnboarding } from '@/lib/api/onboarding'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { CheckCircle2 } from 'lucide-react'

export default function CompletePage() {
  const router = useRouter()
  const { data, setCurrentStep } = useOnboarding()

  useEffect(() => {
    setCurrentStep(5)
    if (data) {
      markComplete()
    }
  }, [data])

  const markComplete = async () => {
    try {
      await completeOnboarding()
    } catch (error) {
      // Non-blocking - just log the error
      console.warn('Could not update onboarding status:', error)
    }
  }

  const handleDashboard = () => {
    router.push('/dashboard')
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center">
        <CheckCircle2 className="w-16 h-16 text-green-600 mx-auto mb-4" />
        <h2 className="text-3xl font-bold text-gray-900">You're All Set!</h2>
        <p className="mt-2 text-gray-600">
          Your goal has been submitted for approval
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>What Happens Next?</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-semibold">
              1
            </div>
            <div>
              <h4 className="font-semibold">Manager Review</h4>
              <p className="text-sm text-gray-600">
                {data?.manager ? `${data.manager.name} will` : 'Your manager will'} review your goal for alignment and feasibility
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-semibold">
              2
            </div>
            <div>
              <h4 className="font-semibold">Approval</h4>
              <p className="text-sm text-gray-600">
                Once approved, your goal becomes active
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-semibold">
              3
            </div>
            <div>
              <h4 className="font-semibold">Track Progress</h4>
              <p className="text-sm text-gray-600">
                Update your progress quarterly in the dashboard
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Button onClick={handleDashboard} className="w-full">
        Go to Dashboard
      </Button>
    </div>
  )
}
