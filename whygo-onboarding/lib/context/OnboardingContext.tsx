'use client'

import { createContext, useContext, useState, ReactNode } from 'react'
import { OnboardingContext as OnboardingData } from '../types/api'

interface OnboardingContextType {
  data: OnboardingData | null
  setData: (data: OnboardingData) => void
  currentStep: number
  setCurrentStep: (step: number) => void
  totalSteps: number
}

const OnboardingContext = createContext<OnboardingContextType | undefined>(undefined)

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<OnboardingData | null>(null)
  const [currentStep, setCurrentStep] = useState(1)
  const totalSteps = 5

  return (
    <OnboardingContext.Provider
      value={{ data, setData, currentStep, setCurrentStep, totalSteps }}
    >
      {children}
    </OnboardingContext.Provider>
  )
}

export function useOnboarding() {
  const context = useContext(OnboardingContext)
  if (context === undefined) {
    throw new Error('useOnboarding must be used within an OnboardingProvider')
  }
  return context
}
