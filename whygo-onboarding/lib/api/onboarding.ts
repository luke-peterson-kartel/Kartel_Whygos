import { api } from './client'
import { OnboardingContext } from '../types/api'

export async function getOnboardingContext(): Promise<OnboardingContext> {
  return api.get<OnboardingContext>('/api/onboarding/context')
}

export async function startOnboarding(): Promise<void> {
  await api.post('/api/onboarding/start')
}

export async function completeOnboarding(): Promise<void> {
  await api.post('/api/onboarding/complete')
}
