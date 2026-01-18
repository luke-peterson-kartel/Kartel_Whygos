'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useOnboarding } from '@/lib/context/OnboardingContext'
import { getOnboardingContext, startOnboarding } from '@/lib/api/onboarding'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Loader2 } from 'lucide-react'
import { OnboardingContext } from '@/lib/types/api'

export default function ProfilePage() {
  const router = useRouter()
  const { setData, setCurrentStep } = useOnboarding()
  const [isLoading, setIsLoading] = useState(true)
  const [context, setContext] = useState<OnboardingContext | null>(null)

  useEffect(() => {
    setCurrentStep(1)
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const data = await getOnboardingContext()
      setContext(data)
      setData(data)

      // Try to mark onboarding as started (non-blocking)
      if (data.person.onboarding_status === 'not_started') {
        try {
          await startOnboarding()
        } catch (error) {
          // Ignore errors - this is just a status update
          console.warn('Could not update onboarding status:', error)
        }
      }
    } catch (error) {
      console.error('Failed to load onboarding context:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleContinue = () => {
    router.push('/onboarding/company')
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    )
  }

  if (!context) {
    return (
      <Card>
        <CardContent className="pt-6">
          <p className="text-red-600">Failed to load profile data</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Welcome!</h2>
        <p className="mt-2 text-gray-600">
          Let's confirm your profile before we get started
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Your Profile</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-500">Name</label>
            <p className="text-lg font-semibold">{context.person.name}</p>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-500">Title</label>
            <p className="text-lg">{context.person.title}</p>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-500">Department</label>
            <p className="text-lg">{context.department.name}</p>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-500">Role</label>
            <Badge variant="secondary" className="text-sm capitalize">
              {context.person.level.replace('_', ' ')}
            </Badge>
          </div>

          {context.manager && (
            <div>
              <label className="text-sm font-medium text-gray-500">Reports to</label>
              <p className="text-lg">{context.manager.name}</p>
            </div>
          )}
        </CardContent>
        <CardFooter>
          <Button onClick={handleContinue} className="w-full">
            Continue to Company Goals
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
