'use client'

import { useOnboarding } from '@/lib/context/OnboardingContext'
import { Check } from 'lucide-react'

const steps = [
  { number: 1, name: 'Profile', path: '/onboarding/profile' },
  { number: 2, name: 'Company Goals', path: '/onboarding/company' },
  { number: 3, name: 'Department Goals', path: '/onboarding/department' },
  { number: 4, name: 'Your Goals', path: '/onboarding/goals' },
  { number: 5, name: 'Complete', path: '/onboarding/complete' },
]

export function WizardNavigation() {
  const { currentStep } = useOnboarding()

  return (
    <nav aria-label="Progress">
      <ol className="flex items-center justify-between w-full max-w-3xl mx-auto">
        {steps.map((step, idx) => (
          <li key={step.number} className="relative flex-1">
            {/* Connector line */}
            {idx !== steps.length - 1 && (
              <div
                className={`absolute top-4 left-1/2 w-full h-0.5 ${
                  currentStep > step.number ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              />
            )}

            {/* Step indicator */}
            <div className="relative flex flex-col items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                  currentStep > step.number
                    ? 'bg-blue-600 text-white'
                    : currentStep === step.number
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {currentStep > step.number ? (
                  <Check className="w-5 h-5" />
                ) : (
                  step.number
                )}
              </div>
              <span className="mt-2 text-xs font-medium text-gray-600">
                {step.name}
              </span>
            </div>
          </li>
        ))}
      </ol>
    </nav>
  )
}
